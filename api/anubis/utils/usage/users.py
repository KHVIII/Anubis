from datetime import datetime
from typing import List, Set, Tuple

from sqlalchemy.sql import distinct

from anubis.models import db, Submission, TheiaSession
from anubis.utils.cache import cache
from anubis.utils.data import is_debug


def _get_active_ids(Model, day_start: datetime, day_end: datetime) -> List[str]:
    active_owner_ids: List[str] = db.session.query(
        distinct(Model.owner_id)
    ).filter(
        Model.created >= day_start,
        Model.created <= day_end,
    ).all()
    return active_owner_ids


def _get_day_start_end(day: datetime = None) -> Tuple[datetime, datetime]:
    if day is None:
        day = datetime.now()
    day_start = day.replace(hour=0, second=0, microsecond=0)
    day_end = day.replace(hour=23, second=59, microsecond=0)
    return day_start, day_end


@cache.memoize(timeout=60, source_check=True, unless=is_debug)
def get_active_theia_users(day: datetime = None) -> Set[str]:
    day_start, day_end = _get_day_start_end(day)
    active_owner_ids = _get_active_ids(TheiaSession, day_start, day_end)
    return set(active_owner_ids)


@cache.memoize(timeout=60, source_check=True, unless=is_debug)
def get_active_submission_users(day: datetime = None) -> Set[str]:
    day_start, day_end = _get_day_start_end(day)
    active_owner_ids = _get_active_ids(Submission, day_start, day_end)
    return set(active_owner_ids)