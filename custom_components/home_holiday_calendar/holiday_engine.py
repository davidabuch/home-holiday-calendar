"""Pure holiday calculation engine for Home Holiday Calendar."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Final

from pyluach.dates import GregorianDate


@dataclass(frozen=True, slots=True)
class HolidayInfo:
    """Normalized holiday information."""

    key: str
    display_name: str
    source: str
    raw_name: str | None = None


NONE: Final = HolidayInfo("none", "None", "none", None)

DISPLAY_NAMES: Final[dict[str, str]] = {
    "new_year": "New Year",
    "valentines_day": "Valentine's Day",
    "st_patricks_day": "St. Patrick's Day",
    "july_4": "Independence Day",
    "halloween": "Halloween",
    "thanksgiving": "Thanksgiving",
    "christmas": "Christmas",
    "hanukkah": "Hanukkah",
    "purim": "Purim",
    "passover": "Passover",
    "shavuot": "Shavuot",
    "rosh_hashanah": "Rosh Hashanah",
    "yom_kippur": "Yom Kippur",
    "sukkot": "Sukkot",
    "shemini_atzeret": "Shemini Atzeret",
    "simchat_torah": "Simchat Torah",
    "lag_baomer": "Lag BaOmer",
    "tu_bishvat": "Tu BiShvat",
    "tu_bav": "Tu BAv",
    "purim_katan": "Purim Katan",
    "shushan_purim": "Shushan Purim",
    "passover_sheni": "Pesach Sheni",
}


def _info(key: str, source: str, raw_name: str | None = None) -> HolidayInfo:
    return HolidayInfo(key, DISPLAY_NAMES[key], source, raw_name)


def gregorian_holiday(day: date) -> HolidayInfo:
    """Return fixed/rule-based Gregorian holiday for the civil date."""

    md = (day.month, day.day)
    fixed = {
        (1, 1): "new_year",
        (2, 14): "valentines_day",
        (3, 17): "st_patricks_day",
        (7, 4): "july_4",
        (10, 31): "halloween",
        (12, 24): "christmas",
        (12, 25): "christmas",
        (12, 31): "new_year",
    }
    if md in fixed:
        return _info(fixed[md], "fixed_gregorian")

    if day.month == 11 and day.weekday() == 3:
        occurrence = ((day.day - 1) // 7) + 1
        if occurrence == 4:
            return _info("thanksgiving", "gregorian_rule")

    return NONE


def _normalize_jewish_festival(raw: str | None) -> HolidayInfo:
    if not raw:
        return NONE
    name = raw.lower().strip()
    if "chanuka" in name or "chanukah" in name or "hanukkah" in name:
        return _info("hanukkah", "hebrew_calendar", raw)
    if "purim katan" in name:
        return _info("purim_katan", "hebrew_calendar", raw)
    if "shushan purim" in name:
        return _info("shushan_purim", "hebrew_calendar", raw)
    if "purim" in name:
        return _info("purim", "hebrew_calendar", raw)
    if "pesach sheni" in name:
        return _info("passover_sheni", "hebrew_calendar", raw)
    if "pesach" in name:
        return _info("passover", "hebrew_calendar", raw)
    if "shavu" in name:
        return _info("shavuot", "hebrew_calendar", raw)
    if "rosh hashana" in name or "rosh hashanah" in name:
        return _info("rosh_hashanah", "hebrew_calendar", raw)
    if "yom kippur" in name:
        return _info("yom_kippur", "hebrew_calendar", raw)
    if "simchas torah" in name or "simchat torah" in name:
        return _info("simchat_torah", "hebrew_calendar", raw)
    if "shmini atzeres" in name or "shemini atzeret" in name:
        return _info("shemini_atzeret", "hebrew_calendar", raw)
    if "succos" in name or "sukkot" in name:
        return _info("sukkot", "hebrew_calendar", raw)
    if "lag baomer" in name or "lag b'omer" in name:
        return _info("lag_baomer", "hebrew_calendar", raw)
    if "tu bishvat" in name or "tu b'shvat" in name:
        return _info("tu_bishvat", "hebrew_calendar", raw)
    if "tu b'av" in name or "tu bav" in name:
        return _info("tu_bav", "hebrew_calendar", raw)
    return NONE


def jewish_holiday_for_civil_day(day: date, *, israel: bool = False) -> HolidayInfo:
    """Return the Jewish festival associated with the civil day at midnight."""
    hebrew = GregorianDate(day.year, day.month, day.day).to_heb()
    raw = hebrew.festival(israel=israel, include_working_days=True)
    return _normalize_jewish_festival(raw)


def jewish_holiday_tonight(day: date, *, israel: bool = False) -> HolidayInfo:
    """Return the Jewish festival that begins/continues after sunset tonight."""
    return jewish_holiday_for_civil_day(day + timedelta(days=1), israel=israel)


def resolve_today(day: date, *, israel: bool = False) -> HolidayInfo:
    """Resolve the civil-date holiday with Gregorian priority."""
    greg = gregorian_holiday(day)
    if greg.key != "none":
        return greg
    return jewish_holiday_for_civil_day(day, israel=israel)


def resolve_tonight(day: date, *, israel: bool = False) -> HolidayInfo:
    """Resolve the holiday associated with tonight, Gregorian first."""
    greg = gregorian_holiday(day)
    if greg.key != "none":
        return greg
    return jewish_holiday_tonight(day, israel=israel)


def next_holiday(day: date, *, israel: bool = False, max_days: int = 550) -> tuple[date, HolidayInfo]:
    """Return the next future evening with a normalized holiday."""
    for offset in range(1, max_days + 1):
        candidate = day + timedelta(days=offset)
        holiday = resolve_tonight(candidate, israel=israel)
        if holiday.key != "none":
            return candidate, holiday
    return day, NONE
