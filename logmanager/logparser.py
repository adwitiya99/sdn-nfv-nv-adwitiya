import re
from datetime import datetime


class KarafLogParser:
    def __init__(self, lines):
        # Input lines .. Expected list of lines
        self.lines = lines
        # Temporary variables
        self.log_line = ""
        self.additional_logs = []
        # Parsed logs
        self.parsed_data = []

    def parse(self):
        for line in self.lines:
            # Check whether it's an log forma of karaf
            if re.match("^(.+)\s*\|\s*(.+)\s*\|\s*(.+)\s*(\|\s*(.+))*$", line):
                # Push log data
                self.push_log(line)
            # If it's not an log format of karaf, add to additional ogs
            else:
                self.additional_logs.append(line)

                # An blank call to push last data
        self.push_log("")

    def push_log(self, new_log_line):
        # If already there is some log_line , push log_line and additional_logs
        if self.log_line != "":
            splitted_lines = self.log_line.split("|")
            splitted_lines = [x.strip() for x in splitted_lines]
            # As per format, it should have exactly 6 parts
            if len(splitted_lines) == 6:
                data = {}
                # Convert timestamp to timestamp
                data["timestamp"] = self.convert_to_timestamp(splitted_lines[0])
                data["level"] = splitted_lines[1]
                data["thread_name"] = splitted_lines[2]
                data["class_name"] = splitted_lines[3]

                # parse bundle details
                bundle = splitted_lines[4].split(" - ")
                data["bundle"] = {}
                data["bundle"]["id"] = bundle[0]
                data["bundle"]["name"] = bundle[1]
                data["bundle"]["version"] = bundle[2]

                data["message"] = splitted_lines[5] + "\n" + "".join(self.additional_logs)
                data["uploaded_on"] = int(datetime.now().timestamp() * 1000)
                self.parsed_data.append(data)

        # delete additiona_logs and set new log_line
        self.additional_logs = []
        self.log_line = new_log_line

    # Helper function to comvert sppecified datetime to milliseconds epoch
    def convert_to_timestamp(self, time_str):
        format_str = "%Y-%m-%dT%H:%M:%S,%f"
        # Use the strptime() method to parse the input string and create a datetime object
        dt_obj = datetime.strptime(time_str, format_str)
        # Use the timestamp() method to convert the datetime object to a timestamp
        timestamp = int(dt_obj.timestamp() * 1000)
        return timestamp

    # Get parsed data
    def getParsedData(self):
        return self.parsed_data


class AtomixLogParser:
    def __init__(self, lines):
        # Input lines .. Expected list of lines
        self.lines = lines
        # Temporary variables
        self.log_line = ""
        self.additional_logs = []
        # Parsed logs
        self.parsed_data = []

    def parse(self):
        for line in self.lines:
            # Check whether it's an log forma of karaf
            if re.match("^[\d\:\.]+\s+\[[\w\s-]+\]\s+\w+\s+[\w\.]+ - .*$", line):
                # Push log data
                self.push_log(line)
            # If it's not an log format of karaf, add to additional ogs
            else:
                self.additional_logs.append(line)

                # An blank call to push last data
        self.push_log("")

    def push_log(self, new_log_line):
        # If already there is some log_line , push log_line and additional_logs
        if self.log_line != "":
            splitted_parts = self.log_line.split(" ", 3)
            splitted_parts = [x.strip() for x in splitted_parts]
            # As per format, it should have exactly 4 parts
            if len(splitted_parts) == 4:
                data = {}
                data["timestamp"] = self.convert_to_milliseconds(splitted_parts[0])
                data["level"] = splitted_parts[2]
                data["thread_name"] = splitted_parts[1][1:-1]
                # Split again to seperate class and message
                split_tmp = splitted_parts[3].split(" - ")
                data["class_name"] = split_tmp[0]
                data["message"] = split_tmp[1] + "\n" + "".join(self.additional_logs)
                data["uploaded_on"] = int(datetime.now().timestamp() * 1000)

                self.parsed_data.append(data)

        # delete additiona_logs and set new log_line
        self.additional_logs = []
        self.log_line = new_log_line

    # Helper function to comvert sppecified axios log time format to milliseconds
    def convert_to_milliseconds(self, timestamp):
        dt_object = datetime.strptime(timestamp, '%H:%M:%S.%f')
        time_object = dt_object.time()
        milliseconds = (
                                   time_object.hour * 3600 + time_object.minute * 60 + time_object.second) * 1000 + time_object.microsecond / 1000
        return int(milliseconds)

    # Get parsed data
    def getParsedData(self):
        return self.parsed_data


class PingLogParser:
    def __init__(self, lines):
        # Input lines .. Expected list of lines
        self.lines = lines
        # Parsed logs
        self.parsed_data = []

    def parse(self):
        for line in self.lines:
            self.push_log(line)

    def push_log(self, new_log_line):
        if new_log_line.strip() == "":
            return
        splitted_parts = new_log_line.split(" ", 1)
        splitted_parts = [x.strip() for x in splitted_parts]

        data = {
            "timestamp": self.convert_to_milliseconds(splitted_parts[0]),
            "level": "INFO",
            "class_name": "ping",
            "message": splitted_parts[1],
            "uploaded_on": int(datetime.now().timestamp() * 1000)
        }

        if data["timestamp"] == 0:
            return
        self.parsed_data.append(data)

    # Helper function to comvert sppecified axios log time format to milliseconds
    def convert_to_milliseconds(self, timestamp):
        try:
            dt_object = datetime.strptime(timestamp, '%H:%M:%S.%f')
            time_object = dt_object.time()
            milliseconds = (
                                   time_object.hour * 3600 + time_object.minute * 60 + time_object.second) * 1000 + time_object.microsecond / 1000
            return int(milliseconds)
        except Exception as e:
            print(e)
            return 0

    # Get parsed data
    def getParsedData(self):
        return self.parsed_data


class DeviceLogParser:
    def __init__(self, lines):
        # Input lines .. Expected list of lines
        self.lines = lines
        # Parsed logs
        self.parsed_data = []

    def parse(self):
        for line in self.lines:
            self.push_log(line)

    def push_log(self, new_log_line):
        if new_log_line.strip() == "":
            return

        data = {
            "timestamp": int(datetime.now().timestamp() * 1000),
            "level": "INFO",
            "class_name": "devices.log",
            "message": new_log_line,
            "uploaded_on": int(datetime.now().timestamp() * 1000)
        }

        self.parsed_data.append(data)

    # Get parsed data
    def getParsedData(self):
        return self.parsed_data
