from .controller import PacController
from .const import (
    DOMAIN,
    SCAN_INTERVAL,
    CONF_SCAN_INTERVAL,
    CONF_BRAND,
    CONF_MODEL,
)
from .modbus_handler import ModbusHandler
from .models import DEFAULT_BRAND, DEFAULT_MODEL, resolve_model

PLATFORMS = ["sensor", "binary_sensor", "switch", "number", "select", "climate"]


async def async_setup_entry(hass, entry):
    hass.data.setdefault(DOMAIN, {})

    data = dict(entry.data)

    # Modèle choisi à la configuration (repli sur le défaut pour les entrées
    # créées avant l'ajout de la sélection marque/modèle).
    model_config = resolve_model(
        data.get(CONF_BRAND, DEFAULT_BRAND),
        data.get(CONF_MODEL, DEFAULT_MODEL),
    )

    handler = ModbusHandler(data["host"], data["port"], data["unit_id"])

    scan_interval = entry.options.get(
        CONF_SCAN_INTERVAL, data.get(CONF_SCAN_INTERVAL, SCAN_INTERVAL)
    )
    controller = PacController(hass, lambda now: None, scan_interval, handler)

    hass.data[DOMAIN][entry.entry_id] = {
        **data,
        "model_config": model_config,
        "controller": controller,
        "scan_interval": scan_interval,
    }

    await controller.start()
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    entry.async_on_unload(entry.add_update_listener(_async_update_listener))
    return True


async def _async_update_listener(hass, entry):
    """Recharge l'intégration quand les options changent."""
    await hass.config_entries.async_reload(entry.entry_id)


async def async_unload_entry(hass, entry):
    unloaded = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unloaded:
        controller = hass.data[DOMAIN][entry.entry_id]["controller"]
        await controller.stop()
        hass.data[DOMAIN].pop(entry.entry_id)
    return unloaded
