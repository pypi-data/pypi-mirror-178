import dataclasses
from typing import Optional
from datetime import datetime
from uuid import UUID


@dataclasses.dataclass
class UserCreated:
    status: str
    message: str
    token: str


@dataclasses.dataclass
class User:
    message: str
    token: str


@dataclasses.dataclass
class CountryData:
    _id: UUID
    name_en: str
    name_fa: str
    flag: str
    fifa_code: str
    iso2: str
    groups: str
    id: str


@dataclasses.dataclass
class Match:
    id: int
    type: str
    group: str
    home_team: CountryData
    away_team: CountryData
    home_score: int
    away_score: int
    home_scorers: Optional[int]
    away_scorers: Optional[int]
    persian_date: str
    local_date: datetime
    stadium_id: str
    time_elapsed: str
    finished: str
    matchday: int


@dataclasses.dataclass
class Matchs:
    data: list[Match]


@dataclasses.dataclass
class Team:
    id: str
    matches_played: int
    win: int
    draw: int
    lose: int
    goals_for: int
    goals_against: int
    goal_difference: int
    points: int
    country: CountryData


@dataclasses.dataclass
class Teams:
    data: list[CountryData]


@dataclasses.dataclass
class Standing:
    teams: list[Team]


@dataclasses.dataclass
class Group:
    group: str
    standing: Standing


@dataclasses.dataclass
class Groups:
    data: list[Group]
