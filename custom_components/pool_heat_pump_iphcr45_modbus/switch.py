import asyncio
import logging

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN, WRITE_VERIFY_DELAY
from .controller import PacController
from .entity import PacDeviceMixin
from .modbus_handler import ModbusHandler

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    config_entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    controller: PacController = entry_data["controller"]
    handler = controller.handler

    async_add_entities(
        [
            PacSwitch(
                hass,
                handler,
                controller,
                config_entry.entry_id,
                entry_data["model_config"]["switch"],
            )
        ]
    )


class PacSwitch(PacDeviceMixin, SwitchEntity):
    _attr_should_poll = False

    def __init__(
        self,
        hass: HomeAssistant,
        handler: ModbusHandler,
        controller: PacController,
        entry_id: str,
        config: dict,
    ) -> None:
        self._hass = hass
        self._handler = handler
        self._controller = controller
        self._entry_id = entry_id
        self._config = config

        self._attr_has_entity_name = True
        self._attr_translation_key = config["translation_key"]
        self._attr_unique_id = f"{entry_id}_{config['unique_id']}"
        self._attr_icon = "mdi:power"
        self._attr_is_on = False

    @property
    def extra_state_attributes(self):
        return {"modbus_address": self._config["address"]}

    async def async_added_to_hass(self) -> None:
        await self._async_poll_refresh()
        self._controller.add_poll_listener(self._async_poll_refresh)

    async def async_will_remove_from_hass(self) -> None:
        self._controller.remove_poll_listener(self._async_poll_refresh)

    async def _async_poll_refresh(self) -> bool:
        raw = await self._hass.async_add_executor_job(
            self._handler.read, self._config["address"], self._config["input_type"]
        )
        if raw is None:
            return False
        self._attr_is_on = raw == self._config["on_value"]
        self.async_write_ha_state()
        return True

    async def async_turn_on(self, **kwargs) -> None:
        await self._write(self._config["on_value"], True)

    async def async_turn_off(self, **kwargs) -> None:
        await self._write(self._config["off_value"], False)

    async def _write(self, value: int, expected_on: bool) -> None:
        ok = await self._hass.async_add_executor_job(
            self._handler.write,
            self._config["address"],
            value,
            self._config["input_type"],
        )
        if not ok:
            _LOGGER.warning("Failed to write heat pump on/off state (%s)", value)
            return

        await asyncio.sleep(WRITE_VERIFY_DELAY)
        verified = await self._hass.async_add_executor_job(
            self._handler.read_verified,
            self._config["address"],
            value,
            self._config["input_type"],
            0,
        )
        if not verified:
            _LOGGER.warning("Heat pump command not confirmed by the device (%s)", value)
            return

        self._attr_is_on = expected_on
        self.async_write_ha_state()
