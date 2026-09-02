"""Coordinator for Home Holiday Calendar."""

from __future__ import annotations

from datetime import timedelta
import logging

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util

from .const import DOMAIN
from .holiday_engine import jewish_holiday_tonight, next_holiday, resolve_today, resolve_tonight

_LOGGER = logging.getLogger(__name__)


class HomeHolidayCalendarCoordinator(DataUpdateCoordinator[dict]):
    """Calculate holiday state from the local Home Assistant date."""

    def __init__(self, hass: HomeAssistant, *, israel: bool) -> None:
        super().__init__(hass, logger=_LOGGER, name=DOMAIN, update_interval=timedelta(minutes=30))
        self.israel = israel

    async def _async_update_data(self) -> dict:
        today = dt_util.now().date()
        current = resolve_today(today, israel=self.israel)
        tonight = resolve_tonight(today, israel=self.israel)
        previous_evening = resolve_tonight(
            today - timedelta(days=1),
            israel=self.israel,
        )
        jewish_tonight = jewish_holiday_tonight(today, israel=self.israel)
        next_date, upcoming = next_holiday(today, israel=self.israel)
        return {
            "civil_date": today.isoformat(),
            "today": current,
            "tonight": tonight,
            "previous_evening": previous_evening,
            "jewish_tonight": jewish_tonight,
            "next_date": next_date.isoformat(),
            "next": upcoming,
        }
