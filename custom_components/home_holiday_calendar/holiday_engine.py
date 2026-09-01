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


def _thanksgiving_date(year: int) -> date:
    """Return the fourth Thursday in November for the given year."""
    day = date(year, 11, 1)
    first_thursday = day + timedelta(days=(3 - day.weekday()) % 7)
    return first_thursday + timedelta(weeks=3)


def gregorian_holiday(day: date) -> HolidayInfo:
    """Return the actual fixed/rule-based Gregorian holiday for the civil date."""

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

    if day == _thanksgiving_date(day.year):
        return _info("thanksgiving", "gregorian_rule")

    return NONE


def gregorian_observance_for_evening(day: date) -> HolidayInfo:
    """Return the Gregorian holiday observance associated with this evening.

    This deliberately differs from :func:`gregorian_holiday` for holidays whose
    home-automation observance spans more than the literal holiday date.

    Current observance policy:
    - Thanksgiving: Wednesday through Sunday of Thanksgiving week.
    - Independence Day: actual date only when Monday-Thursday; Friday-Sunday
      weekend when July 4 falls Friday or Saturday; Saturday-Sunday when July 4
      falls Sunday.
    - All other supported Gregorian holidays: actual civil date only.
    """

    # Thanksgiving observance: Wednesday through Sunday around the fourth
    # Thursday in November.
    thanksgiving = _thanksgiving_date(day.year)
    if thanksgiving - timedelta(days=1) <= day <= thanksgiving + timedelta(days=3):
        return _info("thanksgiving", "observance_rule")

    # Independence Day observance window.
    july_4 = date(day.year, 7, 4)
    weekday = july_4.weekday()  # Monday=0 ... Sunday=6

    if weekday <= 3:  # Monday-Thursday: July 4 only.
        july_start = july_end = july_4
    elif weekday == 4:  # Friday: Friday-Sunday.
        july_start = july_4
        july_end = july_4 + timedelta(days=2)
    elif weekday == 5:  # Saturday: Friday-Sunday.
        july_start = july_4 - timedelta(days=1)
        july_end = july_4 + timedelta(days=1)
    else:  # Sunday: Saturday-Sunday.
        july_start = july_4 - timedelta(days=1)
        july_end = july_4

    if july_start <= day <= july_end:
        return _info("july_4", "observance_rule")

    # Remaining Gregorian holidays follow their actual civil dates.
    return gregorian_holiday(day)


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
    """Resolve the actual civil-date holiday with Gregorian priority."""
    greg = gregorian_holiday(day)
    if greg.key != "none":
        return greg
    return jewish_holiday_for_civil_day(day, israel=israel)


def resolve_tonight(day: date, *, israel: bool = False) -> HolidayInfo:
    """Resolve the automation-friendly holiday observance for tonight.

    Gregorian observance rules have priority. This both supports extended
    Thanksgiving/Independence Day lighting windows and preserves the requested
    Christmas-over-Hanukkah behavior on December 24-25.
    """
    greg = gregorian_observance_for_evening(day)
    if greg.key != "none":
        return greg
    return jewish_holiday_tonight(day, israel=israel)


def next_holiday(day: date, *, israel: bool = False, max_days: int = 550) -> tuple[date, HolidayInfo]:
    """Return the next future evening with a normalized holiday observance."""
    for offset in range(1, max_days + 1):
        candidate = day + timedelta(days=offset)
        holiday = resolve_tonight(candidate, israel=israel)
        if holiday.key != "none":
            return candidate, holiday
    return day, NONE
