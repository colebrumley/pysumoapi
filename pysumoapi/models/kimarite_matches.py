"""Models for kimarite matches."""

from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict, Field
from zoneinfo import ZoneInfo


class KimariteMatch(BaseModel):
    """Model for a single kimarite match."""

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={datetime: lambda dt: dt.astimezone(ZoneInfo("UTC")).isoformat()},
    )

    kimarite: str = Field(..., description="The kimarite used in the match")
    basho_id: str = Field(..., alias="bashoId", description="The ID of the basho")
    day: int = Field(..., description="The day of the basho", ge=1, le=15)
    match_no: int = Field(..., alias="matchNo", description="The match number", gt=0)
    east_id: str = Field(..., alias="eastId", description="The ID of the east rikishi")
    east_shikona: str = Field(
        ..., alias="eastShikona", description="The shikona of the east rikishi"
    )
    east_rank: str = Field(
        ..., alias="eastRank", description="The rank of the east rikishi"
    )
    west_id: str = Field(..., alias="westId", description="The ID of the west rikishi")
    west_shikona: str = Field(
        ..., alias="westShikona", description="The shikona of the west rikishi"
    )
    west_rank: str = Field(
        ..., alias="westRank", description="The rank of the west rikishi"
    )
    winner_id: str = Field(
        ..., alias="winnerId", description="The ID of the winning rikishi"
    )
    winner_en: str = Field(
        ..., alias="winnerEn", description="The English name of the winning rikishi"
    )
    winner_jp: str = Field(
        ..., alias="winnerJp", description="The Japanese name of the winning rikishi"
    )
    created_at: datetime = Field(
        ..., alias="createdAt", description="When the record was created"
    )
    updated_at: datetime = Field(
        ..., alias="updatedAt", description="When the record was last updated"
    )


class KimariteMatchesResponse(BaseModel):
    """Model for the kimarite matches response."""

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={datetime: lambda dt: dt.astimezone(ZoneInfo("UTC")).isoformat()},
    )

    limit: int = Field(
        ..., description="The maximum number of records returned", ge=1, le=1000
    )
    skip: int = Field(..., description="The number of records skipped", ge=0)
    total: int = Field(..., description="The total number of records", ge=0)
    records: List[KimariteMatch] = Field(
        ..., description="The list of kimarite matches"
    )
