from typing import List, Literal, Optional
from pydantic import BaseModel, Field


class Match(BaseModel):
    """Model for a single match in a rikishi's record."""
    result: Literal["win", "loss", "absent", "fusen loss", "fusen win"] = Field(..., description="Result of the match")
    opponent_shikona_en: str = Field(..., alias="opponentShikonaEn", description="Opponent's English shikona")
    opponent_shikona_jp: str = Field(..., alias="opponentShikonaJp", description="Opponent's Japanese shikona")
    opponent_id: int = Field(..., alias="opponentID", description="Opponent's ID")
    kimarite: str = Field(..., description="Winning technique used")


class RikishiBanzuke(BaseModel):
    """Model for a rikishi's banzuke entry."""
    side: Literal["East", "West"] = Field(..., description="Side of the banzuke")
    rikishi_id: int = Field(..., alias="rikishiID", description="Rikishi's ID")
    shikona_en: str = Field(..., alias="shikonaEn", description="Rikishi's English shikona")
    rank_value: int = Field(..., alias="rankValue", description="Numeric rank value")
    rank: str = Field(..., description="Full rank description")
    record: Optional[List[Match]] = Field(None, description="List of matches in the basho")
    wins: int = Field(..., description="Number of wins")
    losses: int = Field(..., description="Number of losses")
    absences: int = Field(..., description="Number of absences")


class Banzuke(BaseModel):
    """Model for the banzuke endpoint response."""
    basho_id: str = Field(..., alias="bashoId", description="Basho ID in YYYYMM format")
    division: Literal["Makuuchi", "Juryo", "Makushita", "Sandanme", "Jonidan", "Jonokuchi"] = Field(..., description="Division name")
    east: List[RikishiBanzuke] = Field(..., description="List of rikishi on the East side")
    west: List[RikishiBanzuke] = Field(..., description="List of rikishi on the West side") 