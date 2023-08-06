import json
from dataclasses import dataclass
from datetime import datetime, date, timedelta
from pathlib import Path
from typing import Any, Dict, Protocol

from lifetime import Period


@dataclass()
class Token:
    created_on: datetime = datetime.now()
    expires_on: datetime = datetime.now()

    @property
    def elapsed(self) -> timedelta:
        return datetime.now() - self.created_on

    @property
    def is_valid(self) -> bool:
        return self.expires_on > datetime.now()

    @property
    def is_expired(self) -> bool:
        return not self.is_valid


class TokenHandler(Protocol):
    def read(self) -> Token:
        ...

    def write(self, token: Token) -> None:
        ...


class Tick:
    def __init__(self, handler: TokenHandler):
        self._handler = handler
        self.token = handler.read()

    def commit(self, period: Period) -> None:
        self.token = Token(expires_on=period.expires_on())
        self._handler.write(self.token)

    def __bool__(self):
        return self.token.is_valid


class JsonTokenHandler:
    def __init__(self, file_name: str | Path):
        self.file_name = Path(file_name)

    def read(self) -> Token:
        if not self.file_name.is_file():
            return Token()

        with self.file_name.open() as f:
            j = json.load(f, cls=_JsonDateTimeDecoder)
            return Token(j["created_on"], j["expires_on"])

    def write(self, token: Token) -> None:
        self.file_name.parent.mkdir(parents=True, exist_ok=True)
        with self.file_name.open("w") as f:
            json.dump({"created_on": token.created_on, "expires_on": token.expires_on}, f, cls=_JsonDateTimeEncoder)


class _JsonDateTimeEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o, (date, datetime)):
            return o.isoformat()


class _JsonDateTimeDecoder(json.JSONDecoder):
    def __init__(self):
        super().__init__(object_hook=self.parse_datetime_or_default)

    @staticmethod
    def parse_datetime_or_default(d: Dict):
        r = dict()
        for k in d.keys():
            r[k] = d[k]
            if isinstance(d[k], str):
                try:
                    r[k] = datetime.fromisoformat(d[k])  # try parse date-time
                except ValueError:
                    pass  # default value is already set
        return r
