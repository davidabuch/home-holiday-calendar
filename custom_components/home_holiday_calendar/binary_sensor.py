"""Binary sensor platform for Home Holiday Calendar."""

from __future__ import annotations

from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .entity import HomeHolidayCalendarEntity


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    """Set up Home Holiday Calendar binary sensors."""
    async_add_entities([HolidayTonightActiveSensor(entry.runtime_data, entry.entry_id)])


class HolidayTonightActiveSensor(HomeHolidayCalendarEntity, BinarySensorEntity):
    """Whether tonight has a normalized holiday."""

    _attr_name = "Home Holiday Calendar Holiday Tonight"
    _attr_icon = "mdi:calendar-star"

    def __init__(self, coordinator, entry_id: str) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry_id}_holiday_tonight"

    @property
    def is_on(self) -> bool:
        return self.coordinator.data["tonight"].key != "none"

    @property
    def extra_state_attributes(self) -> dict:
        holiday = self.coordinator.data["tonight"]
        return {
            "holiday": holiday.key,
            "display_name": holiday.display_name,
            "source": holiday.source,
        }
