from dataclasses import asdict
from typing import List, Optional

from coiote.utils import ApiEndpoint, StringResult, api_call, sanitize_request_param
from coiote.v3.model.assigned_device_properties import AssignedDeviceProperty, AssignedDevicePropertyUpsertRequest, \
    AssignedDevicePropertyUpdateRequest


class AssignedDeviceProperties(ApiEndpoint):
    def __init__(
            self, *args, **kwargs
    ):
        super().__init__(*args, **kwargs, api_url="assignedDeviceProperties")

    @api_call()
    def get_all(self, search_criteria: Optional[str] = None) -> List[str]:
        return self.session.get(self.get_url(), params={"searchCriteria": search_criteria})

    @api_call(StringResult)
    def upsert_property(self, property_id: str, property: AssignedDevicePropertyUpsertRequest) -> StringResult:
        property_id = sanitize_request_param(property_id)
        return self.session.put(self.get_url(f"/{property_id}"), json=asdict(property))

    @api_call(AssignedDeviceProperty)
    def get_one(self, property_id: str) -> AssignedDeviceProperty:
        property_id = sanitize_request_param(property_id)
        return self.session.get(self.get_url(f"/{property_id}"))

    @api_call()
    def delete_one(self, property_id: str) -> None:
        property_id = sanitize_request_param(property_id)
        return self.session.delete(self.get_url(f"/{property_id}"))

    @api_call(AssignedDeviceProperty)
    def update_one(self, property_id: str, update: AssignedDevicePropertyUpdateRequest) -> None:
        property_id = sanitize_request_param(property_id)
        return self.session.patch(self.get_url(f"/{property_id}"), json=asdict(update))
