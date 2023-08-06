from dataclasses import asdict
from typing import List, Optional

from coiote.utils import ApiEndpoint, StringResult, api_call, sanitize_request_param
from coiote.v3.model.groups import GroupUpdateRequest, Group


class Groups(ApiEndpoint):
    def __init__(
            self, *args, **kwargs
    ):
        super().__init__(*args, **kwargs, api_url="groups")

    @api_call()
    def get_all(self, search_criteria: Optional[str] = None) -> List[str]:
        return self.session.get(self.get_url(), params={"searchCriteria": search_criteria})

    @api_call(StringResult)
    def add_group(self, group: Group) -> StringResult:
        return self.session.post(self.get_url(), json=asdict(group))

    @api_call(Group)
    def get_one(self, group_id: str) -> Group:
        group_id = sanitize_request_param(group_id)
        return self.session.get(self.get_url(f"/{group_id}"))

    @api_call()
    def update_one(self, group_id: str, update: GroupUpdateRequest) -> None:
        group_id = sanitize_request_param(group_id)
        return self.session.put(self.get_url(f"/{group_id}"), json=asdict(update))

    @api_call()
    def delete_one(self, group_id: str) -> None:
        group_id = sanitize_request_param(group_id)
        return self.session.delete(self.get_url(f"/{group_id}"))
