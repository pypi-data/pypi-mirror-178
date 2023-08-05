from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, List


@dataclass
class FileLocation:
    @staticmethod
    def create_internal(file_name: str, static_content: bool = False):
        return InternalLocation(InternalLocationData(fileName=file_name, staticContent=static_content))

    @staticmethod
    def create_external(file_url: str, username: Optional[str] = None, password: Optional[str] = None):
        return ExternalLocation(ExternalLocationData(fileUrl=file_url, username=username, password=password))


@dataclass
class InternalLocationData:
    fileName: str
    staticContent: bool = False


@dataclass
class ExternalLocationData:
    fileUrl: str
    username: Optional[str] = None
    password: Optional[str] = None


@dataclass
class InternalLocation(FileLocation):
    InternalLocation: InternalLocationData


@dataclass
class ExternalLocation(FileLocation):
    ExternalLocation: ExternalLocationData


class ResourceCategory(str, Enum):
    FIRMWARE = "FIRMWARE"
    SOFTWARE = "SOFTWARE"
    UNKNOWN = "UNKNOWN"
    IMAGE = "IMAGE"


class ResourceExpirationTime(str, Enum):
    ONE_DAY = "ONE_DAY"
    ONE_WEEK = "ONE_WEEK"
    ONE_MONTH = "ONE_MONTH"
    FOREVER = "FOREVER"


class DownloadProtocol(str, Enum):
    HTTP = "HTTP"
    HTTPS = "HTTPS"
    COAP = "COAP"
    COAPS = "COAPS"
    COAP_TCP = "COAP_TCP"
    COAP_TLS = "COAP_TLS"


@dataclass
class DownloadOptions:
    protocol: DownloadProtocol


@dataclass
class ResourceDownloadData:
    address: str


@dataclass
class Resource:
    name: str
    domain: str
    location: FileLocation
    category: ResourceCategory
    expirationTime: ResourceExpirationTime
    visibleForSubtenants: bool = False
    description: Optional[str] = None
    id: Optional[str] = None
    device: Optional[str] = None
    properties: Dict[str, str] = field(default_factory=dict)
    directGroups: List[str] = field(default_factory=list)


@dataclass
class FileData:
    pass


@dataclass
class Base64FileData(FileData):
    data: str
