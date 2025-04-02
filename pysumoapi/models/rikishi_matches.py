"""Models for rikishi matches."""
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class Match(BaseModel):
    """Model representing a single match."""
    basho_id: str = Field(alias="bashoId")
    division: Optional[str] = None
    day: int
    match_no: Optional[int] = Field(None, alias="matchNo")
    east_id: int = Field(alias="eastId")
    east_shikona: str = Field(alias="eastShikona")
    east_rank: str = Field(alias="eastRank")
    west_id: int = Field(alias="westId")
    west_shikona: str = Field(alias="westShikona")
    west_rank: str = Field(alias="westRank")
    kimarite: Optional[str] = None
    winner_id: int = Field(alias="winnerId")
    winner_en: str = Field(alias="winnerEn")
    winner_jp: str = Field(alias="winnerJp")


class RikishiMatchesResponse(BaseModel):
    """Model representing a response containing rikishi matches."""
    limit: int
    skip: int
    total: int
    records: List[Match]
    opponent_wins: Optional[int] = Field(None, alias="opponentWins")
    rikishi_wins: Optional[int] = Field(None, alias="rikishiWins")


class RikishiOpponentMatchesResponse(BaseModel):
    """Model representing a response containing matches between two rikishi."""
    matches: List[Match]
    kimarite_losses: Dict[str, int] = Field(alias="kimariteLosses")
    kimarite_wins: Dict[str, int] = Field(alias="kimariteWins")
    opponent_wins: int = Field(alias="opponentWins")
    rikishi_wins: int = Field(alias="rikishiWins")
    total: int 