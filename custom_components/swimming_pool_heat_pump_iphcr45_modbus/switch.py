import asyncio
import logging

from homeassistant.components.switch import SwitchEntity

from .const import DOMAIN
from .entity import PacDeviceMixin

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    entry_data = hass.data[DOMAIN][config_entry.entry_id]
    controller = entry_data["controller"]
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

    def __init__(self, hass, handler, controller, entry_id, config):
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

    async def async_added_to_hass(self):
        await self._async_poll_refresh()
        self._controller.add_poll_listener(self._async_poll_refresh)

    async def async_will_remove_from_hass(self):
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

    async def async_turn_on(self, **kwargs):
        await self._write(self._config["on_value"], True)

    async def async_turn_off(self, **kwargs):
        await self._write(self._config["off_value"], False)

    async def _write(self, value, expected_on):
        ok = await self._hass.async_add_executor_job(
            self._handler.write,
            self._config["address"],
            value,
            self._config["input_type"],
        )
        if not ok:
            _LOGGER.warning("Échec d'écriture de la marche/arrêt de la PAC (%s)", value)
            return

        await asyncio.sleep(0.5)
        verified = await self._hass.async_add_executor_job(
            self._handler.read_verified,
            self._config["address"],
            value,
            self._config["input_type"],
            0,
        )
        if not verified:
            _LOGGER.warning("Commande de la PAC non confirmée par l'appareil (%s)", value)
            return

        self._attr_is_on = expected_on
        self.async_write_ha_state()
