from datetime import datetime, time, timedelta
from typing import Protocol

from dateutil.relativedelta import relativedelta


class Period(Protocol):
    def expires_on(self) -> datetime:
        ...


class Duration:
    def __init__(self, delta: timedelta, starts_on: datetime = datetime.now()):
        self.delta = delta
        self.starts_on = starts_on

    def expires_on(self) -> datetime:
        return self.starts_on + self.delta


class EndOfDay:
    def __init__(self, starts_on: datetime = datetime.now(), offset: int = 0):
        self.starts_on = starts_on
        self.offset = offset

    def expires_on(self) -> datetime:
        return datetime.combine(self.starts_on, time.min) + relativedelta(days=1) - relativedelta(seconds=1) + relativedelta(days=self.offset)


class EndOfWeek:
    def __init__(self, starts_on: datetime = datetime.now(), offset: int = 0):
        self.starts_on = starts_on
        self.offset = offset

    def expires_on(self) -> datetime:
        return datetime.combine(self.starts_on, time.min) + relativedelta(days=7 - self.starts_on.weekday()) - relativedelta(seconds=1) + relativedelta(weeks=self.offset)


class EndOfMonth:
    def __init__(self, starts_on: datetime = datetime.now(), offset: int = 0):
        self.starts_on = starts_on
        self.offset = offset

    def expires_on(self) -> datetime:
        return datetime.combine(self.starts_on, time.min).replace(day=1) + relativedelta(months=1) - relativedelta(seconds=1) + relativedelta(months=self.offset)
