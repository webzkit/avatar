from typing import Any, Dict, Optional
from pydantic import BaseModel


class UserRelationship(BaseModel):
    name: str
    email: str
    group: Optional[Dict[str, Any]] = None
