from datetime import datetime, timezone
from typing import Any, Optional, Union
from fastapi import HTTPException, status
from pydantic import BaseModel, computed_field, model_validator
from core.helpers.utils import parse_query_str


class BaseRequest(BaseModel):
    auth_id: Optional[int] = None
    group_id: Optional[int] = None
    group_name: Optional[str] = None
    current_date: datetime = datetime.now(timezone.utc).replace(tzinfo=None)
    fields: Optional[Any] = None

    @model_validator(mode="before")
    def set_current_date(cls, values):
        if "current_date" not in values:
            values["current_date"] = datetime.now(timezone.utc).replace(tzinfo=None)
        return values

    @computed_field
    def is_superuser(self) -> bool:
        return True if self.group_name == "Supper Admin" else False


def authorization_handler(request_init_data: Union[str, None] = None) -> BaseRequest:
    try:
        request = BaseRequest()

        if request_init_data is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
            )

        current_user = parse_query_str(request_init_data)

        request = BaseRequest(
            auth_id=int(current_user.get("id", 0)),
            group_id=int(current_user.get("group_id", 0)),
            group_name=current_user.get("group_name", None),
        )

        return request

    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
