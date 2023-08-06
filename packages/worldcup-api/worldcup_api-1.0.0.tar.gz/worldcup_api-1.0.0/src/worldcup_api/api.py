from aiohttp import ClientSession
from datetime import datetime as dt
from .exceptions import *
from .types import *


class WorldCupApi:
    def __init__(self):
        self.url = "http://api.cup2022.ir/api/v1"
        self._session = ClientSession
        self._headers = {
            "Content-Type": "application/json",
        }
        self._token = ""

    async def register(
        self,
        *,
        name: str,
        email: str,
        password: str,
    ):
        data = {
            "name": name,
            "email": email,
            "password": password,
            "passwordConfirm": password,
        }
        async with self._session(headers=self._headers) as session:
            async with session.post(f"{self.url}/user", json=data) as response:
                if response.status == 400:
                    raise AlreadyRegistered(f"{email} is already registered")
                if response.status == 200:
                    data = await response.json()
                    status = data["status"]
                    message = data["message"]
                    token = data["data"]["token"]
                    self._token = token
                    return UserCreated(status=status, message=message, token=token)

    async def login(
        self,
        *,
        email: str,
        password: str,
    ):
        data = {
            "email": email,
            "password": password,
        }
        async with self._session(headers=self._headers) as session:
            async with session.post(f"{self.url}/user/login", json=data) as response:
                if response.status == 400:
                    raise NotRegistered(f"{email} is not registered")
                if response.status == 200:
                    data = await response.json()
                    status = data["status"]
                    token = data["token"]
                    self._token = token
                    self._headers["Authorization"] = f"Bearer {token}"
                    return User(message=status, token=token)

    async def get_teams(self):
        if not self._token:
            raise NotLoggedIn()
        async with self._session(
            headers=self._headers
        ) as s, s.get(f"{self.url}/team") as response:
            if response.status == 200:
                datas = await response.json()
                x = []
                for data in datas["data"]:
                    x.append(
                        CountryData(
                            _id=data["_id"],
                            name_en=data["name_en"],
                            name_fa=data["name_fa"],
                            flag=data["flag"],
                            fifa_code=data["fifa_code"],
                            iso2=data["iso2"],
                            groups=data["groups"],
                            id=data["id"],
                        )
                    )
                return Teams(data=x)

    async def get_team(self, *, team_id: str):
        if not self._token:
            raise NotLoggedIn()
        async with self._session(
            headers=self._headers
        ) as s, s.get(f"{self.url}/team/{team_id}") as response:
            if response.status == 200:
                data = await response.json()
                return CountryData(
                    _id=data["_id"],
                    name_en=data["name_en"],
                    name_fa=data["name_fa"],
                    flag=data["flag"],
                    fifa_code=data["fifa_code"],
                    iso2=data["iso2"],
                    groups=data["groups"],
                    id=data["id"],
                )

    async def get_matchs(self):
        if not self._token:
            raise NotLoggedIn()
        async with self._session(
            headers=self._headers
        ) as s, s.get(f"{self.url}/match") as response:
            if response.status == 200:
                datas = await response.json()
                x = []
                for data in datas["data"]:
                    home_team = await self.get_team(team_id=data["home_team_id"])
                    away_team = await self.get_team(team_id=data["away_team_id"])
                    match = Match(
                        id=data["id"],
                        type=data["type"],
                        group=data["group"],
                        home_team=home_team,
                        away_team=away_team,
                        home_score=data["home_score"],
                        away_score=data["away_score"],
                        home_scorers=data["home_scorers"],
                        away_scorers=data["away_scorers"],
                        persian_date=data["persian_date"],
                        local_date=dt.strptime(data["local_date"], "%Y-%m-%d %I:%M %p"),
                        stadium_id=data["stadium_id"],
                        time_elapsed=data["time_elapsed"],
                        finished=data["finished"],
                        matchday=data["matchday"],
                    )
                    x.append(match)
                return Matchs(data=x)
            return None

    async def get_match(self, *, match_id: str):
        if not self._token:
            raise NotLoggedIn()
        async with self._session(
            headers=self._headers
        ) as s, s.get(f"{self.url}/bymatch/{match_id}") as response:
            if response.status == 200:
                data = await response.json()
                home_team = await self.get_team(team_id=data["home_team_id"])
                away_team = await self.get_team(team_id=data["away_team_id"])
                return Match(
                    id=data["id"],
                    type=data["type"],
                    group=data["group"],
                    home_team=home_team,
                    away_team=away_team,
                    home_score=data["home_score"],
                    away_score=data["away_score"],
                    home_scorers=data["home_scorers"],
                    away_scorers=data["away_scorers"],
                    persian_date=data["persian_date"],
                    local_date=dt.strptime(data["local_date"], "%Y-%m-%d %I:%M %p"),
                    stadium_id=data["stadium_id"],
                    time_elapsed=data["time_elapsed"],
                    finished=data["finished"],
                    matchday=data["matchday"],
                )
            return None

    async def get_standings(self):
        if not self._token:
            raise NotLoggedIn()
        async with self._session(
            headers=self._headers
        ) as s, s.get(f"{self.url}/standings") as response:
            if response.status == 200:
                datas = await response.json()
                x = []
                y = []
                for data in datas["data"]:
                    for team in data["teams"]:
                        country = await self.get_team(team_id=team["team_id"])
                        tim = Team(
                            id=team["team_id"],
                            matches_played=team["mp"],
                            win=team["w"],
                            lose=team["l"],
                            points=team["pts"],
                            goals_for=team["gf"],
                            goals_against=team["ga"],
                            goal_difference=team["gd"],
                            draw=team["d"],
                            country=country,
                        )
                        if tim not in x:
                            x.append(tim)
                    standing = Standing(
                        teams=x
                    )
                    grup = Group(
                        group=data["group"],
                        standing=standing
                    )
                    y.append(grup)
                return Groups(data=y)
            return None
