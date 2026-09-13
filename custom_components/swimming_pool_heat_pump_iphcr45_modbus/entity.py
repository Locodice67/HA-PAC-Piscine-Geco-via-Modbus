from .const import DOMAIN
from .models import DEVICE_NAME


class PacDeviceMixin:
    """device_info commun à toutes les entités de la PAC (un seul appareil).

    Le fabricant et le modèle proviennent du modèle sélectionné à la
    configuration (voir models.BRANDS).
    """

    _entry_id: str

    @property
    def device_info(self):
        model = self.hass.data[DOMAIN][self._entry_id].get("model_config", {})
        return {
            "identifiers": {(DOMAIN, self._entry_id)},
            "name": DEVICE_NAME,
            "manufacturer": model.get("manufacturer"),
            "model": model.get("model"),
        }
