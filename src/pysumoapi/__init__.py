"""
PySumoAPI - A modern Python client for the Sumo API
"""

__version__ = "0.1.0"

from .client import SumoAPI
from .models import Rikishi, Basho, Kimarite

__all__ = ["SumoAPI", "Rikishi", "Basho", "Kimarite"] 