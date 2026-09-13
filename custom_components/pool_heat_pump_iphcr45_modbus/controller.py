import asyncio
import logging
from collections.abc import Awaitable, Callable
from datetime import timedelta

from homeassistant.core import CALLBACK_TYPE, HomeAssistant
from homeassistant.helpers.event import async_track_time_interval

from .modbus_handler import ModbusHandler

_LOGGER = logging.getLogger(__name__)
_PROBE_INTERVAL = 5  # une tentative de reconnexion toutes les N cycles de poll ignorés
_MODBUS_FAIL_THRESHOLD = 3

PollListener = Callable[[], Awaitable[bool]]


class PacController:
    def __init__(
        self,
        hass: HomeAssistant,
        update_callback: Callable[[object], None | Awaitable[None]],
        scan_interval: int,
        handler: ModbusHandler,
    ) -> None:
        self._hass = hass
        self._update_callback = update_callback
        self._scan_interval = scan_interval
        self._remove_listener: CALLBACK_TYPE | None = None
        self._handler = handler
        self.modbus_ok = False
        self._modbus_fail_count = 0
        self._modbus_fail_threshold = _MODBUS_FAIL_THRESHOLD
        self._probe_counter = 0
        self._poll_listeners: list[PollListener] = []

    @property
    def scan_interval(self) -> int:
        return self._scan_interval

    @property
    def handler(self) -> ModbusHandler:
        return self._handler

    @property
    def poll_listeners(self) -> list[PollListener]:
        """Copie de la liste des callbacks de poll (accès public sécurisé)."""
        return list(self._poll_listeners)

    def add_poll_listener(self, callback: PollListener) -> None:
        """Enregistre un callback appelé après chaque cycle de poll réussi
        (piloté par le même timer que les capteurs, cf. update_sensors)."""
        self._poll_listeners.append(callback)

    def remove_poll_listener(self, callback: PollListener) -> None:
        self._poll_listeners = [cb for cb in self._poll_listeners if cb is not callback]

    async def start(self) -> None:
        # Établit l'état de liaison dès le démarrage pour que les entités ne
        # restent pas `unavailable` jusqu'au premier cycle de poll.
        self.modbus_ok = bool(
            await self._hass.async_add_executor_job(self._handler.connect)
        )
        self._start_polling()

    async def stop(self) -> None:
        if self._remove_listener:
            self._remove_listener()
            self._remove_listener = None
        await self._hass.async_add_executor_job(self._handler.close)

    def _start_polling(self) -> None:
        if self._remove_listener:
            self._remove_listener()
        self._remove_listener = async_track_time_interval(
            self._hass, self._dispatch_update, timedelta(seconds=self._scan_interval)
        )

    async def _dispatch_update(self, now) -> None:
        """Indirection nécessaire : au moment où start() enregistre le timer
        (avant que les plateformes soient chargées), self._update_callback est
        encore le no-op passé par __init__.py. sensor.py le remplace ensuite par
        update_sensors ; passer l'attribut directement à async_track_time_interval
        figerait la référence d'origine. On relit donc l'attribut à chaque
        déclenchement."""
        result = self._update_callback(now)
        if asyncio.iscoroutine(result):
            await result

    async def update_interval(self, new_interval: int) -> None:
        self._scan_interval = new_interval
        self._modbus_fail_count = 0
        self._probe_counter = 0
        self._start_polling()

    def notify_modbus_success(self) -> None:
        self._modbus_fail_count = 0
        self._probe_counter = 0
        self.modbus_ok = True

    def notify_modbus_failure(self) -> None:
        self._modbus_fail_count += 1
        if self._modbus_fail_count >= self._modbus_fail_threshold:
            self.modbus_ok = False

    def should_skip_poll(self) -> bool:
        """True si le poll doit être sauté car la PAC est déconnectée.

        Autorise quand même une tentative de reconnexion toutes les
        _PROBE_INTERVAL cycles, sinon la connexion ne se rétablirait jamais.
        """
        if self._modbus_fail_count < self._modbus_fail_threshold:
            return False
        self._probe_counter += 1
        if self._probe_counter >= _PROBE_INTERVAL:
            self._probe_counter = 0
            _LOGGER.debug("Modbus disconnected — attempting reconnection")
            return False
        _LOGGER.debug(
            "Modbus disconnected — poll skipped (%d/%d before next attempt)",
            self._probe_counter,
            _PROBE_INTERVAL,
        )
        return True
