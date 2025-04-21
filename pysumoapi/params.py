from enum import Enum
from pydantic import BaseModel, Field

class Pagination(BaseModel):
    limit: int | None = Field(default=None, gt=0, le=1000)
    skip: int | None = Field(default=None, ge=0)

class SortOrder(str, Enum):
    asc = "asc"
    desc = "desc" 