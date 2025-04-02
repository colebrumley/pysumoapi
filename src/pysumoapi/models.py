"""
Pydantic models for Sumo API responses.
"""
from datetime import datetime
from typing import List, Optional, Dict

from pydantic import BaseModel, Field


class DivisionStats(BaseModel):
    """Model representing statistics for a specific division."""
    Jonidan: int
    Jonokuchi: int
    Juryo: int
    Makushita: int
    Makuuchi: int
    Sandanme: int


class Sansho(BaseModel):
    """Model representing special prizes won by a rikishi."""
    Gino_sho: int = Field(alias="Gino-sho")
    Kanto_sho: int = Field(alias="Kanto-sho")
    Shukun_sho: int = Field(alias="Shukun-sho")


class RikishiStats(BaseModel):
    """Model representing a rikishi's overall performance statistics."""
    absence_by_division: DivisionStats = Field(alias="absenceByDivision")
    basho: int
    basho_by_division: DivisionStats = Field(alias="bashoByDivision")
    loss_by_division: DivisionStats = Field(alias="lossByDivision")
    sansho: Sansho
    total_absences: int = Field(alias="totalAbsences")
    total_by_division: DivisionStats = Field(alias="totalByDivision")
    total_losses: int = Field(alias="totalLosses")
    total_matches: int = Field(alias="totalMatches")
    total_wins: int = Field(alias="totalWins")
    wins_by_division: DivisionStats = Field(alias="winsByDivision")
    yusho: int
    yusho_by_division: DivisionStats = Field(alias="yushoByDivision")


class RankHistory(BaseModel):
    """Model representing a rikishi's rank at a particular tournament."""
    id: str
    basho_id: str = Field(alias="bashoId")
    rikishi_id: int = Field(alias="rikishiId")
    rank_value: int = Field(alias="rankValue")
    rank: str


class ShikonaHistory(BaseModel):
    """Model representing a rikishi's shikona (ring name) at a particular tournament."""
    id: str
    basho_id: str = Field(alias="bashoId")
    rikishi_id: int = Field(alias="rikishiId")
    shikona_en: str = Field(alias="shikonaEn")
    shikona_jp: str = Field(alias="shikonaJp")


class MeasurementHistory(BaseModel):
    """Model representing a rikishi's measurements at a particular tournament."""
    id: str
    basho_id: str = Field(alias="bashoId")
    rikishi_id: int = Field(alias="rikishiId")
    height: int
    weight: int


class Rikishi(BaseModel):
    """Model representing a sumo wrestler."""
    id: int
    sumodb_id: Optional[int] = Field(None, alias="sumodbId")
    nsk_id: Optional[int] = Field(None, alias="nskId")
    shikona_en: str = Field(alias="shikonaEn")
    shikona_jp: str = Field(alias="shikonaJp")
    current_rank: str = Field(alias="currentRank")
    heya: str
    birth_date: datetime = Field(alias="birthDate")
    shusshin: Optional[str] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    debut: Optional[str] = None
    rank_history: Optional[List[RankHistory]] = Field(None, alias="rankHistory")
    shikona_history: Optional[List[ShikonaHistory]] = Field(None, alias="shikonaHistory")
    measurement_history: Optional[List[MeasurementHistory]] = Field(None, alias="measurementHistory")
    updated_at: datetime = Field(alias="updatedAt")


class RikishiList(BaseModel):
    """Model representing a paginated list of rikishi."""
    limit: int
    skip: int
    total: int
    records: List[Rikishi]


class Basho(BaseModel):
    """Model representing a sumo tournament."""
    id: str
    name: str
    start_date: datetime = Field(alias="startDate")
    end_date: datetime = Field(alias="endDate")
    location: str
    division: str


class Kimarite(BaseModel):
    """Model representing a winning technique in sumo."""
    id: str
    name: str
    description: str
    category: str 