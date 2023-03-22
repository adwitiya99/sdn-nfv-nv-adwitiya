from mongoengine import EmbeddedDocument, Document, StringField, IntField, EmbeddedDocumentField, ObjectIdField
from enum import Enum


# PackageBundle is a subdocument of NetworkLog. So it will have no sperate collection in the database.
class PackageBundle(EmbeddedDocument):
    id = StringField()
    name = StringField()
    version = StringField()

    @staticmethod
    def from_json(data: dict):
        return PackageBundle(
            id=data.get("id", ""),
            name=data.get("name", ""),
            version=data.get("version", "")
        )


# NetworkLog is a document. So it will have a sperate collection in the database [Collection name: network_log]
class NetworkLog(Document):
    _id = ObjectIdField()
    timestamp = IntField()
    level = StringField()
    thread_name = StringField()
    class_name = StringField()
    message = StringField()
    bundle = EmbeddedDocumentField(PackageBundle)
    network_name = StringField()
    element_name = StringField()
    config_type = StringField()
    uploaded_on = IntField()
    meta = {
        'collection': 'network_log'
    }

    @staticmethod
    def from_json(data: dict):
        return NetworkLog(
            timestamp=data.get("timestamp", ""),
            level=data.get("level", ""),
            thread_name=data.get("thread_name", ""),
            class_name=data.get("class_name", ""),
            message=data.get("message", ""),
            bundle=PackageBundle.from_json(data.get("bundle", {})) if "bundle" in data else None,
            network_name=data.get("network_name", ""),
            element_name=data.get("element_name", ""),
            config_type=data.get("config_type", ""),
            uploaded_on=data.get("uploaded_on", 0)
        )


# ApplicationLog is a document. So it will have a sperate collection in the database [Collection name: application_log]
class ApplicationLog(Document):
    _id = ObjectIdField()
    timestamp = IntField()
    level = StringField()
    message = StringField()
    source = StringField()
    meta = {'collection': 'appication_log'}

    @staticmethod
    def from_json(data: dict):
        return ApplicationLog(
            timestamp=data.get("timestamp", ""),
            level=data.get("level", ""),
            message=data.get("message", ""),
            source=data.get("source", "")
        )


# Some enums
class LogType(Enum):
    NETWORK = "NETWORK"
    APPLICATION = "APPLICATION"


class ParserType(Enum):
    KARAF = "KARAF"
    ATOMIX = "ATOMIX"
    PING = "PING"
    DEVICES = "DEVICES"
    NONE = "NONE"


class LogLevel(Enum):
    INFO = "INFO"
    DEBUG = "DEBUG"
    WARN = "WARN"
    ERROR = "ERROR"
    TRACE = "TRACE"


# if __name__ == "__main__":
#     from mongoengine import connect
#     connect(host="mongodb://localhost:27017", db="cdcju")
#     # cell = NetworkLog._get_collection()
#     # cell.database.command("text", cell.message, search="192.168.0.194".encode())
#     # records = NetworkLog.objects.search_text("192.168.0.194")
#     # for record in records:
#     #     print(str(record._id)+" > "+record.message)
#     records = NetworkLog.objects(message__contains="192.168.0.194", config_type="ping.log", network_name="NT48", element_name="H123", uploaded_on__gte=1674290185000).count()
#     # for record in records:
#     #     print(str(record._id)+" > "+record.message)
#
#
#     print("HI")