from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, model_validator


class YushoWinner(BaseModel):
    """Model for a yusho winner."""
    type: str = Field(..., description="Division name")
    rikishi_id: int = Field(..., alias="rikishiId", description="Rikishi's ID")
    shikona_en: str = Field(..., alias="shikonaEn", description="Rikishi's English shikona")
    shikona_jp: str = Field(..., alias="shikonaJp", description="Rikishi's Japanese shikona")


class SpecialPrize(BaseModel):
    """Model for a special prize winner."""
    type: str = Field(..., description="Prize type")
    rikishi_id: int = Field(..., alias="rikishiId", description="Rikishi's ID")
    shikona_en: str = Field(..., alias="shikonaEn", description="Rikishi's English shikona")
    shikona_jp: str = Field(..., alias="shikonaJp", description="Rikishi's Japanese shikona")


class Match(BaseModel):
    """Model for a single torikumi match."""
    id: str = Field(..., description="Match ID in format YYYYMM-day-matchNo-eastId-westId")
    basho_id: str = Field(..., alias="bashoId", description="Basho ID in YYYYMM format")
    division: str = Field(..., description="Division name")
    day: int = Field(..., description="Day of the tournament (1-15)")
    match_no: int = Field(..., alias="matchNo", description="Match number for the day")
    east_id: int = Field(..., alias="eastId", description="East rikishi's ID")
    east_shikona: str = Field(..., alias="eastShikona", description="East rikishi's shikona")
    east_rank: str = Field(..., alias="eastRank", description="East rikishi's rank")
    west_id: int = Field(..., alias="westId", description="West rikishi's ID")
    west_shikona: str = Field(..., alias="westShikona", description="West rikishi's shikona")
    west_rank: str = Field(..., alias="westRank", description="West rikishi's rank")
    kimarite: str = Field(..., description="Winning technique used")
    winner_id: int = Field(..., alias="winnerId", description="Winner's ID")
    winner_en: str = Field(..., alias="winnerEn", description="Winner's English name")
    winner_jp: str = Field(..., alias="winnerJp", description="Winner's Japanese name")


class Torikumi(BaseModel):
    """Model for the torikumi endpoint response."""
    date: str = Field(..., description="Basho date in YYYYMM format")
    location: str = Field(..., description="Tournament location")
    start_date: datetime = Field(..., alias="startDate", description="Tournament start date")
    end_date: datetime = Field(..., alias="endDate", description="Tournament end date")
    yusho: List[YushoWinner] = Field(..., description="List of yusho winners")
    special_prizes: List[SpecialPrize] = Field(..., alias="specialPrizes", description="List of special prize winners")
    
    @model_validator(mode='before')
    @classmethod
    def extract_matches(cls, data: dict) -> dict:
        """Extract matches from the root level into a matches field."""
        if isinstance(data, dict):
            matches = []
            for key in list(data.keys()):
                if isinstance(data[key], dict) and 'id' in data[key]:
                    matches.append(data.pop(key))
            data['matches'] = matches
        return data
    
    matches: List[Match] = Field(..., alias="torikumi", description="List of matches for the specified day") 