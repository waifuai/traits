"""
Personality data models module for the Personality Analysis System.

This module defines the core data structures used to represent personality traits
and statistics throughout the system. It uses Python dataclasses for clean,
immutable data representation.

Classes:
    Personality: Represents a personality profile with friendliness and dominance scores.
    PersonStats: Stores personality statistics and metadata for a person.
"""

from dataclasses import dataclass

@dataclass
class Personality:
    """Represents a personality profile with friendliness and dominance scores.
    
    Attributes:
        friendliness (float): Score from -10 (hostile) to 10 (friendly)
        dominance (float): Score from -10 (submissive) to 10 (dominant)
    """
    friendliness: float
    dominance: float

@dataclass
class PersonStats:
    """Stores personality statistics for a person."""
    name: str
    personality: Personality
    n_friendliness: int = 0
    n_dominance: int = 0