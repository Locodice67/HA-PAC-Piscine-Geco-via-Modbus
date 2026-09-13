import logging
import threading

from pymodbus.client import ModbusTcpClient

_LOGGER = logging.getLogger(__name__)

COIL = "coil"
DISCRETE_INPUT = "discrete_input"
INPUT = "input"
HOLDING = "holding"


class ModbusHandler:
    """Connexion Modbus TCP persistante vers la passerelle de la PAC.

    Le client de pymodbus est synchrone : chaque méthode est bloquante et doit
    être appelée depuis un thread executor (hass.async_add_executor_job), jamais
    directement depuis la boucle d'événements. La connexion est gardée ouverte
    entre les appels et un verrou sérialise l'accès, car toutes les plateformes
    partagent la même instance.
    """

    def __init__(self, host="192.168.1.100", port=502, unit_id=1, timeout=3):
        self.host = host
        self.port = port
        self.unit_id = unit_id
        self._client = ModbusTcpClient(host=self.host, port=self.port, timeout=timeout)
        self._lock = threading.Lock()

    def connect(self):
        """Ouvre la connexion persistante. Peut être appelé plusieurs fois."""
        with self._lock:
            self._ensure_connected()

    def close(self):
        with self._lock:
            self._client.close()

    def _ensure_connected(self):
        if not self._client.connected:
            self._client.connect()

    def read(self, address, input_type=HOLDING, count=1):
        """Lit `count` valeurs et renvoie la première, ou None en cas d'échec."""
        with self._lock:
            try:
                self._ensure_connected()
                if input_type == COIL:
                    result = self._client.read_coils(
                        address=address, count=count, device_id=self.unit_id
                    )
                elif input_type == DISCRETE_INPUT:
                    result = self._client.read_discrete_inputs(
                        address=address, count=count, device_id=self.unit_id
                    )
                elif input_type == INPUT:
                    result = self._client.read_input_registers(
                        address=address, count=count, device_id=self.unit_id
                    )
                else:
                    result = self._client.read_holding_registers(
                        address=address, count=count, device_id=self.unit_id
                    )

                if result.isError():
                    _LOGGER.debug(
                        "Erreur de lecture Modbus à %s (%s) : %s",
                        address,
                        input_type,
                        result,
                    )
                    return None

                if input_type in (COIL, DISCRETE_INPUT):
                    return 1 if result.bits[0] else 0
                return result.registers[0]
            except Exception as err:
                _LOGGER.debug(
                    "Exception de lecture Modbus à %s (%s) : %s", address, input_type, err
                )
                return None

    def write(self, address, value, input_type=HOLDING):
        with self._lock:
            try:
                self._ensure_connected()
                if input_type == COIL:
                    result = self._client.write_coil(
                        address=address, value=bool(value), device_id=self.unit_id
                    )
                else:
                    result = self._client.write_register(
                        address=address, value=int(value), device_id=self.unit_id
                    )
                return not result.isError()
            except Exception as err:
                _LOGGER.debug(
                    "Exception d'écriture Modbus à %s (%s) : %s", address, input_type, err
                )
                return False

    def read_verified(self, address, expected_value, input_type=HOLDING, tolerance=0):
        """Relit un registre après une écriture pour confirmer qu'elle est appliquée.

        Opération verrouillée séparée (pas imbriquée) : à appeler après write(),
        avec un court délai si l'appareil a besoin de temps pour traiter.
        """
        result = self.read(address, input_type=input_type)
        if result is None:
            return False
        return abs(result - expected_value) <= tolerance
