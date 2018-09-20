import datetime
import csv


class TimeKeeper:

    def __init__(self, filename):
        self.filename = filename

    def timer_start(self):
        start_timestamp = datetime.datetime.now()
        return start_timestamp

    def timer_stop(self):
        stop_timestamp = datetime.datetime.now()
        return stop_timestamp

    def duration(self, start, stop):
        duration = stop - start
        return duration

    def dump_timestamp(self, description, value):
        with open(self.filename, mode='a') as Timestamp_file:
            timer_writer = csv.writer(Timestamp_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            timer_writer.writerow(['Task', description, 'Duration', value])
