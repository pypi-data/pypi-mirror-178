from dataclasses import asdict
from typing import Optional, List

from coiote.utils import ApiEndpoint, api_call, sanitize_request_param
from coiote.v3.model.users import UserCreateRequest, User, UserPatchRequest


class Users(ApiEndpoint):
    def __init__(
            self, *args, **kwargs
    ):
        super().__init__(*args, **kwargs, api_url="users")

    @api_call()
    def get_all(self, search_criteria: Optional[str] = None) -> List[str]:
        return self.session.get(self.get_url(), params={"searchCriteria": search_criteria})

    @api_call()
    def create_one(self, user: UserCreateRequest):
        return self.session.post(self.get_url(), json=asdict(user))

    @api_call()
    def find_many(self, username: Optional[str] = None, email: Optional[str] = None, domain: Optional[str] = None,
                  active_only: bool = False) -> List[str]:
        params = {
            "username": username,
            "email": email,
            "domain": domain,
            "isActiveOnly": active_only
        }
        return self.session.get(self.get_url("/search/usernames"), params=params)

    @api_call(User)
    def get_one(self, username: str) -> User:
        username = sanitize_request_param(username)
        return self.session.get(self.get_url(f"/{username}"))

    @api_call()
    def delete_one(self, username: str):
        username = sanitize_request_param(username)
        return self.session.delete(self.get_url(f"/{username}"))

    @api_call()
    def update_one(self, username: str, user: UserPatchRequest):
        username = sanitize_request_param(username)
        return self.session.patch(self.get_url(f"/{username}"), json=asdict(user))
