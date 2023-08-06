from kafka import KafkaConsumer
from kafka.consumer.subscription_state import ConsumerRebalanceListener
from kafka.structs import TopicPartition
import traceback
from collections import namedtuple
import time
from MessageArchiveKafka import MessageArchiveKafkaRecord, MessageArchiveKafkaReader, MessageArchiveKafkaWriter
import os
import sys
import signal
import psutil
from setproctitle import setproctitle, getproctitle

PartitionInfo = namedtuple("PartitionInfo",
    ["header", "writer", "offset"])

class KafkaPythonConsumer(ConsumerRebalanceListener):

  def __init__(self, consumer_id, config, logger):
    self.consumer_id=consumer_id
    self.config = config
    self.logger = logger
    self.partitions = {}
    self.consumer = None

    self.check_for_rotation_secs = 60
    self.last_rotation_check = 0
    self.shutting_down = False
    self.message_processing = False

  def exit_gracefully(self, signum, frame):

    if self.message_processing == False:
      self.logger.info("Fast shutdown available ... exiting")
      self.logger.info("Print stack trace. Don't panic!")
      self.logger.info("-----------------------------------------------")
      for chunk in traceback.format_stack(frame):
        for line in chunk.split("\n"):
          self.logger.info(line)
      self.logger.info("-----------------------------------------------")
      for part in self.partitions:
        self.partitions[part].writer.close()
      self.consumer.commit()
      sys.exit(0)

    self.logger.info("Graceful shutdown of consumer "+str(self.consumer_id)+" started....")
    self.shutting_down = True

  def run(self):

    nice_level = self.config.get("consumer", "consumer_nice_level")
    p = psutil.Process(os.getpid())
    p.nice(int(nice_level))

    bootstrap_server = self.config.get('consumer', 'kafka_bootstrap')
    consumer_group = self.config.get('consumer', 'kafka_consumer_group')

    setproctitle("[consumer"+self.consumer_id+"] "+getproctitle())

    while self.shutting_down == False:
      try:
        offset_reset = self.config.get('consumer', 'kafka_auto_offset_reset')
        self.consumer = KafkaConsumer(bootstrap_servers=bootstrap_server, consumer_timeout_ms=60000, group_id=consumer_group, auto_offset_reset=offset_reset)
        topic_whitelist = self.config.get('consumer', 'topic_whitelist')
        self.logger.info("Topic list is "+topic_whitelist)

        self.consumer.subscribe(topic_whitelist.split(","), None, self)

        self.logger.info("Consumer "+self.consumer_id+" starting.... "+str(self.consumer.assignment()))

        signal.signal(signal.SIGINT, self.exit_gracefully)
        signal.signal(signal.SIGTERM, self.exit_gracefully)

        last_offset_warning_time=0

        while self.shutting_down == False:
          for message in self.consumer:
            self.message_processing = True
            self.logger.debug(message)
            key = message.topic+':'+str(message.partition)
            part_info = self.partitions[key]
            expected_offset = part_info.writer.get_latest_offset()
            if expected_offset != None:
              expected_offset=expected_offset+1
              if (message.offset < expected_offset):
                currenttime = time.mktime(time.gmtime())
                if (currenttime>last_offset_warning_time+10):
                  self.logger.warn("Message offset is lower than the file. Skipping message... topic: "+message.topic+", partition: "+str(message.partition)+", offset: "+str(message.offset)+"(latest in file: "+str(expected_offset-1)+")")
                  self.logger.warn("Surpressing further offset warnings for the next 10 seconds")
                last_offset_warning_time=currenttime
                continue
              if (message.offset > expected_offset):
                self.logger.error("We have missing messages! topic: "+message.topic+", partition: "+str(message.partition)+", offset: "+str(message.offset)+" (latest in file: "+str(expected_offset-1)+")")
            part_info.writer.write_message(message.offset, message.key, message.value)
            part_info = part_info._replace(offset=message.offset)
            self.partitions[key]=part_info
            self.check_for_rotation()
            if self.shutting_down == True:
              break
            self.message_processing = False
          self.check_for_rotation()

        for part in self.partitions:
          self.partitions[part].writer.close()

        self.logger.info("Graceful shutdown of consumer "+str(self.consumer_id)+" successful")
      except Exception as e:
        self.logger.error("Unexpected error with kafka consumer: "+str(e))
        self.logger.error(traceback.format_exc())
        self.logger.error("Sleeping for 30 seconds before trying again")
        if self.consumer != None:
          self.consumer.commit()
          self.consumer.close()

        for part in self.partitions:
          self.partitions[part].writer.close()

        time.sleep(30)
    # save all our offsets
    self.consumer.commit()

  def check_for_rotation(self):
     current_time = time.mktime(time.gmtime())
     if current_time<(self.last_rotation_check+self.check_for_rotation_secs):
       return
     for k in self.partitions:
       if current_time>(int(self.partitions[k].header.get_starttime())+int(self.config.get("consumer", "max_age_seconds"))):
         self.rotate_partition(k) 

  def rotate_partition(self,partition):
     if int(self.partitions[partition].offset) == int(self.partitions[partition].header.get_start_offset()):
       self.logger.debug("Skiping rotate for partition "+partition+". No new writes")
       return
     self.logger.info("I need to rotate "+partition)
     self.partitions[partition].writer.close()

     start_offset = self.partitions[partition].header.get_start_offset()
     end_offset = self.partitions[partition].offset
     topic = self.partitions[partition].header.get_topic()
     part_number = self.partitions[partition].header.get_partition()

     dest_dir = os.path.join(self.config.get("main", "working_directory"),"tocompress",topic, str(part_number))

     date = time.strftime("%y%m%d")

     dest_filename = os.path.join(dest_dir, topic+"-"+str(part_number)+"_"+str(start_offset)+"-"+str(end_offset)+"_"+date+".mak")

     self.mkdirp(dest_dir)

     os.rename(self.partitions[partition].writer.get_filename(), dest_filename)

     self.create_new_data_file(self.partitions[partition].writer.get_filename(), TopicPartition(topic=topic, partition=part_number))


  def get_part_list_string(self, items):
     comma = ""
     return_str = ""
     for x in items:
        return_str = return_str+comma+x.topic+":"+str(x.partition)
        comma = ", "
     return return_str

  def on_partitions_revoked(self, revoked):
     try:
       self.logger.info("Consumer "+str(self.consumer_id)+" got revoked: "+self.get_part_list_string(revoked))

       for topic_partition in revoked:
         key = topic_partition.topic+":"+str(topic_partition.partition)
         if key in self.partitions.keys():
           self.partitions[key].writer.close()
           del self.partitions[key]

     except Exception as e:
       self.logger.error("Unexpected error: "+str(e))
       self.logger.error(traceback.format_exc())
       raise

  def mkdirp(self, directory):
    if not os.path.isdir(directory):
      os.makedirs(directory)

  def create_new_data_file(self, fullname, topic_partition):
    position = self.consumer.position(topic_partition)
    header = MessageArchiveKafkaRecord()
    header.set_topic(topic_partition.topic)
    header.set_partition(topic_partition.partition)
    header.set_start_offset(position)
    last_offset=position
    header.set_starttime(time.mktime(time.gmtime()))
    bmw = MessageArchiveKafkaWriter(fullname)
    bmw.write_header(header)

    part_info=PartitionInfo(header=header, writer=bmw, offset=last_offset)
    key = topic_partition.topic+":"+str(topic_partition.partition)
    self.partitions[key] =  part_info


  def on_partitions_assigned(self, assigned):
     try:
       self.logger.info("Consumer "+str(self.consumer_id)+" got assigned: "+self.get_part_list_string(assigned))

       for topic_partition in assigned:

         working_dir=self.config.get("main", "working_directory")

         filedir = os.path.join(self.config.get("main", "working_directory"),"inprogress",topic_partition.topic, str(topic_partition.partition))
         fullname = os.path.join(filedir, "data.mak")

         key = topic_partition.topic+":"+str(topic_partition.partition)
         if key in self.partitions.keys():
           self.logger.debug("Already managing topic:  "+topic_partition.topic+", parition: "+str(topic_partition.partition)+" ... do nothing")
           next

         if os.path.exists(fullname):
           self.logger.debug("Resuming from existing file for topic: "+topic_partition.topic+", parition: "+str(topic_partition.partition))
           bmr = MessageArchiveKafkaReader(fullname)
           header = bmr.get_header()
           last_offset=bmr.get_last_offset()
           bmr.close()
           bmw = MessageArchiveKafkaWriter(fullname)

           part_info=PartitionInfo(header=header, writer=bmw, offset=last_offset)
           self.partitions[key] =  part_info

         else:
           self.logger.debug("Creating new file for topic: "+topic_partition.topic+", parition: "+str(topic_partition.partition))

           self.mkdirp(filedir)
           self.create_new_data_file(fullname, topic_partition)

     except Exception as e:
       self.logger.error("Unexpected error: "+str(e))
       self.logger.error(traceback.format_exc())
       raise




