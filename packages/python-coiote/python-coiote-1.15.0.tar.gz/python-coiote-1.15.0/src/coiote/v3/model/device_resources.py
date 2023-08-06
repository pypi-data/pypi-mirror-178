from dataclasses import dataclass
from enum import Enum
from typing import List, Union


class InstanceType(str, Enum):
    Single = "Single"
    Multiple = "Multiple"


class Lwm2mResourceType(str, Enum):
    String = "String"
    Integer = "Integer"
    UnsignedInteger = "UnsignedInteger"
    Float = "Float"
    Boolean = "Boolean"
    Opaque = "Opaque"
    Time = "Time"
    Objlnk = "Objlnk"
    Corelnk = "Corelnk"
    NoneType = "None"


class Lwm2mResourceOperationType(str, Enum):
    Read = "Read"
    Write = "Write"
    Execute = "Execute"


@dataclass
class Lwm2mResourceDefinition:
    id: int
    name: str
    operations: List[Lwm2mResourceOperationType]
    instanceType: InstanceType
    mandatory: bool
    type: Lwm2mResourceType
    range: str
    units: str
    description: str


@dataclass
class SingleInstanceResourceData:
    value: str


@dataclass
class MultiInstanceResourceData:
    values: List[str]


@dataclass
class SingleInstanceResourceValue:
    Single: SingleInstanceResourceData

    def get_value(self) -> str:
        return self.Single.value


@dataclass
class MultipleInstanceResourceValue:
    Multiple: MultiInstanceResourceData

    def get_value(self) -> List[str]:
        return self.Multiple.values


@dataclass
class Lwm2mResourceData:
    path: str
    value: Union[SingleInstanceResourceValue, MultipleInstanceResourceValue]
    resourceId: int
    operations: List[Lwm2mResourceOperationType]
    mandatory: bool
    type: Lwm2mResourceType
    range: str
    units: str
    description: str


@dataclass
class Lwm2mObjectDefinition:
    id: int
    name: str
    objectVersion: str
    instanceType: InstanceType
    mandatory: bool
    resourceDefinitions: List[Lwm2mResourceDefinition]
