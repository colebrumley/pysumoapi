"""Models for the banzuke endpoint."""

from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field

from pysumoapi.models.match import Match


class RikishiBanzuke(BaseModel):
    """Model for a rikishi's banzuke entry."""

    model_config = ConfigDict(populate_by_name=True)

    id: str = Field(..., description="Rikishi ID")
    shikona_en: str = Field(
        ..., alias="shikonaEn", description="Rikishi's English shikona"
    )
    shikona_jp: str = Field(
        ..., alias="shikonaJp", description="Rikishi's Japanese shikona"
    )
    rank: str = Field(..., description="Rikishi's rank")
    heya: str = Field(..., description="Rikishi's heya")
    height: Optional[int] = Field(None, description="Rikishi's height in cm")
    weight: Optional[int] = Field(None, description="Rikishi's weight in kg")
    birth_date: Optional[str] = Field(
        None, alias="birthDate", description="Rikishi's birth date"
    )
    debut: Optional[str] = Field(None, description="Rikishi's debut date")
    matches: List[Match] = Field(
        default_factory=list, description="List of matches for this rikishi"
    )


class Banzuke(BaseModel):
    """Model for the banzuke response."""

    model_config = ConfigDict(populate_by_name=True)

    basho_id: str = Field(..., alias="bashoId", description="Basho ID in YYYYMM format")
    division: str = Field(..., description="Division name")
    rikishi: List[RikishiBanzuke] = Field(
        ..., description="List of rikishi in the division"
    )
