from logmanager.models import NetworkLog, ApplicationLog, LogLevel, LogType, ParserType
from logmanager.logparser import KarafLogParser, AtomixLogParser, PingLogParser, DeviceLogParser
import time

'''
-----------------------
If No Parser selected , it assumes the given data is formatted as per the required log type and inserts it as it is
If Parser selected, it parses the data based on specification and inserts it
-----------------------
insertLog(logs, log_type=LogType.APPLICATION, parser_type=ParserType.NONE) function accepts logs 
in both dict and list format. If dict is provided, it converts it to list and then inserts it.
-----------------------
'''


class LogManager:
    @staticmethod
    def insertLog(logs, log_type=LogType.APPLICATION, parser_type=ParserType.NONE, network_name=None, element_name=None,
                  config_type=None):
        # Check data type
        if type(logs) not in [dict, list]:
            print("Invalid data type provided to LogManagement. Expected dict or list.")
            return False

        # If dict, convert to list
        if type(logs) is dict:
            logs = [logs]

        try:
            # If parser selected , parse the data
            if parser_type == ParserType.KARAF:
                karaf_parser = KarafLogParser(logs)
                karaf_parser.parse()
                print("Parsed logs using Karaf parser")
                logs = karaf_parser.getParsedData()
            elif parser_type == ParserType.ATOMIX:
                atomix_parser = AtomixLogParser(logs)
                atomix_parser.parse()
                print("Parsed logs using Atomix parser")
                logs = atomix_parser.getParsedData()
            elif parser_type == ParserType.PING:
                ping_parser = PingLogParser(logs)
                ping_parser.parse()
                print("Parsed logs using Ping parser")
                logs = ping_parser.getParsedData()
            elif parser_type == ParserType.DEVICES:
                devices_log_parser = DeviceLogParser(logs)
                devices_log_parser.parse()
                print("Parsed logs using Devices Log parser")
                logs = devices_log_parser.getParsedData()
            elif parser_type == ParserType.NONE:
                # Pre-process data if necessary , as they are not processed by any parser or additional function
                # CHECK 1: Insert current timestamp if not present
                logs = [log if "timestamp" in log else {**log, "timestamp": int(time.time() * 1000)} for log in logs]
                # CHECK 2: If level is not present, insert it as INFO
                logs = [log if "level" in log else {**log, "level": LogLevel.INFO} for log in logs]
                # CHECK 3: Convert level from enum to string, if applicable
                logs = [log if "level" not in log or type(log["level"]) is not LogLevel else {**log, "level": log[
                    "level"].value} for log in logs]
        except Exception as e:
            print("Error occured while parsing logs")
            print(e)
            return False

        try:
            # Insert data
            if log_type == LogType.NETWORK:
                print("Convert logs to NetworkLog objects")
                # Insert network name and element name
                if network_name is not None:
                    logs = [{**log, "network_name": network_name} for log in logs]
                if element_name is not None:
                    logs = [{**log, "element_name": element_name} for log in logs]
                if config_type is not None:
                    logs = [{**log, "config_type": config_type} for log in logs]
                logs_object = [NetworkLog.from_json(log) for log in logs]
                print("Inserting logs into NetworkLog collection")
                NetworkLog.objects.insert(logs_object)
                print("Inserted logs into NetworkLog collection")
                return True
            elif log_type == LogType.APPLICATION:
                print("Convert logs to ApplicationLog objects")
                logs_object = [ApplicationLog.from_json(log) for log in logs]
                print("Inserting logs into ApplicationLog collection")
                ApplicationLog.objects.insert(logs_object)
                print("Inserted logs into ApplicationLog collection")
                return True
        except Exception as e:
            print("Error occured while inserting logs")
            print(e)
            return False

        return False

    # An specified logger dedicated to application logs
    @staticmethod
    def get_data(query={}):
        return ApplicationLog.objects()



class ApplicationLogger:
    source = ""

    @staticmethod
    def setSource(source):
        ApplicationLogger.source = source

    @staticmethod
    def insertLog(logs):
        LogManager.insertLog(logs, log_type=LogType.APPLICATION, parser_type=ParserType.NONE)

    @staticmethod
    def info(message):
        ApplicationLogger.insertLog({
            "source": ApplicationLogger.source,
            "level": LogLevel.INFO,
            "message": message
        })

    @staticmethod
    def debug(message):
        ApplicationLogger.insertLog({
            "source": ApplicationLogger.source,
            "level": LogLevel.DEBUG,
            "message": message
        })

    @staticmethod
    def warn(message):
        ApplicationLogger.insertLog({
            "source": ApplicationLogger.source,
            "level": LogLevel.WARN,
            "message": message
        })

    @staticmethod
    def error(message):
        ApplicationLogger.insertLog({
            "source": ApplicationLogger.source,
            "level": LogLevel.ERROR,
            "message": message
        })

    @staticmethod
    def trace(message):
        ApplicationLogger.insertLog({
            "source": ApplicationLogger.source,
            "level": LogLevel.TRACE,
            "message": message
        })

    @staticmethod
    def get_data(query={}):
        logs = LogManager.get_data(query)
        return logs
