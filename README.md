# PAC Piscine Geco

**🌍 Langue / Language : [🇫🇷 Français](#français) · [🇬🇧 English](#english)**

![Geco](custom_components/pac_piscine_geco/brand/logo.png)

---

## Français

Intégration Home Assistant pour piloter une **PAC (pompe à chaleur) de piscine Geco** — testée sur **GEPAC08 (compresseur INVERTER)** — en **Modbus TCP**, via une passerelle RS485 → Ethernet. **Aucun cloud, aucune connexion Internet** : tout reste local.

Objectif initial : **débloquer le mode « Super Silence »** (production limitée, appareil plus silencieux et plus sobre).

### Fonctionnalités

| Fonction | Détail | Registre |
|---|---|---|
| Marche / Arrêt | Allume ou éteint la PAC | coil 0 |
| Thermostat | Consigne, mode (Auto/Chaud/Froid) | holding 3 / holding 0 |
| Température courante | Entrée d'eau | input 3 |
| Température eau (sortie) | Sortie d'eau | input 4 |
| Température air | Ambiante | input 5 |
| Compresseur | Pourcentage de charge | input 0 |
| Intensité compresseur | Courant absorbé | input 11 |
| Tension PFC | Tension interne | input 2 |
| Mode de travail | Smart / Silence / Super Silence / Turbo | holding 1 |
| Défauts | Défaut général, défaut E3 | discrete 16 / 51 |
| Diagnostic | État de la communication Modbus | — |

Chaque fonction est exposée comme entité dans Home Assistant (voir le tableau des entités plus bas).

### Matériel nécessaire

- Une **passerelle RS485 → Ethernet** (testé : Waveshare RS485 TO ETH / POE).
- Le connecteur **RS485** de la carte de contrôle de la PAC (port prévu pour le module Wi-Fi optionnel).
- Un câble entre la PAC et la passerelle (UTP conseillé : **3 fils** — `B`, `A`, `G`).

Le port RS485 est le connecteur **`CN12`** de la carte de contrôle (broches `B`, `A`, `G`, `+12V`).

### Montage pas à pas

**1. Ouvrir le coffret électrique**

Couper l'alimentation puis **attendre 5 minutes** avant d'ouvrir (voir l'étiquette « CAUTION » sur le capot).

![Ouverture du coffret](images/open_the_box.jpg)

**2. Repérer le connecteur RS485**

C'est le petit connecteur **4 broches `A` `B` `G` `12v`** de la carte (série `MWH298-V3`) —  C'est le port normalement prévu pour le module Wi-Fi optionnel.

![Repérage du connecteur CN12](images/localise_the_connecteur.jpg)

**3. Câbler le connecteur**

Relier **`B` → `B`**, **`A` → `A`** et **`G` → `GND`**. Le **`+12V` n'est pas nécessaire** : la passerelle est alimentée en **PoE** (ou par sa propre alimentation).

![Câblage du connecteur](images/wire_the_connector.jpg)

### 🛒 Où acheter

| Article | Lien |
|---|---|
| **Kit de connecteurs JST-XH** (2/3/4/5/6 broches, pas 2,54 mm) — pour réaliser le connecteur `CN12` | [Amazon.fr — YIXISI, 460 pièces](https://www.amazon.fr/dp/B082ZLYRRN) |
| **Passerelle RS485 → Ethernet, 1 canal** | [Amazon.fr — Waveshare](https://www.amazon.fr/dp/B0BRNBTFVC) |
| **Passerelle RS485 → Ethernet, 2 canaux** (une seule passerelle pour deux équipements) | [Amazon.fr — Waveshare](https://www.amazon.fr/dp/B0CB8LXQFH) |

> La version **1 canal** suffit pour la PAC. La version **2 canaux** permet de raccorder deux équipements RS485 avec une seule passerelle (ex. PAC + électrolyseur). Voir aussi la [doc Waveshare](https://www.waveshare.com/wiki/RS485_TO_ETH_(B)).

### Configuration de la passerelle

Dans l'interface web de la passerelle (Waveshare RS485 TO ETH / POE) :

| Réglage | Valeur |
|---|---|
| **Work Mode** | `TCP Server` |
| **Protocol** | `Modbus TCP to RTU` |
| **Device Port** | `4196` (défaut Waveshare ; ici `4197`) |
| **Baud Rate / Databits / Parity / Stopbits** | `9600` / `8` / `None` / `1` |
| **IP mode** | `Static` |
| **Esclave Modbus** | `1` |

![Configuration de la passerelle Waveshare](images/config_waveshare.png)

### Installation de l'intégration

**Via HACS (dépôt personnalisé)**

1. HACS → Intégrations → ⋯ → *Dépôts personnalisés*
2. Ajouter `Locodice67/HA-Swimming-Pool-Heat-Pump-Geco-Modbus`, catégorie *Intégration*
3. Installer, puis redémarrer Home Assistant

**Manuelle**

Copier le dossier `custom_components/pac_piscine_geco/` dans `/config/custom_components/`, puis redémarrer Home Assistant.

### Configuration

Paramètres → Appareils et services → **Ajouter une intégration** → *PAC Piscine Geco*.

| Champ | Valeur usuelle |
|---|---|
| Adresse IP | IP de la passerelle RS485 → Ethernet |
| Port TCP | `4196` (défaut Waveshare ; modifiable — ex. `4197`) |
| Adresse Modbus (esclave) | `1` |
| Intervalle de rafraîchissement | `30` s |

L'intervalle est modifiable ensuite via le bouton *Configurer* de l'intégration.

### Entités créées

| Plateforme | Entité | Registre |
|---|---|---|
| `climate` | Thermostat | input 3 / holding 3 / holding 0 / holding 1 |
| `switch` | Marche/Arrêt | coil 0 |
| `number` | Consigne température | holding 3 |
| `select` | Mode (Auto/Chaud/Froid) | holding 0 |
| `select` | Mode de travail | holding 1 |
| `sensor` | Température eau | input 4 |
| `sensor` | Température air | input 5 |
| `sensor` | Intensité compresseur | input 11 |
| `sensor` | Tension PFC | input 2 |
| `sensor` | Compresseur | input 0 |
| `binary_sensor` | Status | coil 0 |
| `binary_sensor` | Défaut général | discrete input 16 |
| `binary_sensor` | Défaut E3 | discrete input 51 |
| `binary_sensor` | État communication Modbus | diagnostic |

> `number` et les deux `select` écrivent **les mêmes registres** que le `climate` : ce sont des vues alternatives. Le `climate` suffit pour piloter la PAC.

### Dashboard

Un simple thermostat + un bouton marche/arrêt + les capteurs suffisent. Exemple d'organisation :

- **Thermostat** (climate) — consigne et mode
- **Marche/Arrêt** (switch)
- **Mesures** — températures eau/air, compresseur, intensité, tension PFC
- **État** — défauts, communication Modbus

### Automatisation d'exemple : « Super Silence »

Séquence type : allumer la PAC, laisser quelques secondes, régler la consigne, puis passer en mode **Super Silence**.

```yaml
# Exemple (à adapter) : PAC ON -> 30 °C -> Super Silence
actions:
  - action: switch.turn_on
    target:
      entity_id: switch.pac_piscine_marche_arret
  - delay:
      seconds: 5
  - action: climate.set_temperature
    target:
      entity_id: climate.pac_piscine_thermostat
    data:
      temperature: 30
  - action: select.select_option
    target:
      entity_id: select.pac_piscine_mode_de_travail
    data:
      option: super_silence
```

### Limitations

- **Mode de travail (registre 1)** : sur l'unité testée (**GEPAC08**), l'**écriture** du registre 1 est **refusée** par la carte (testé avec `0`, `2` et `3`), alors que l'écriture d'autres registres `holding` fonctionne (la consigne, registre 3, passe). Le mode reste donc **lisible** mais **non pilotable** via Modbus sur ce firmware (réglage au clavier de la PAC). À vérifier selon les modèles.
- Les adresses proviennent de la **fiche Modbus officielle des cartes MWH216 / MWH298**. Les cartes Geco / AES / Madimack se ressemblent, mais le modèle exact peut différer : vérifie les valeurs (températures eau/air) contre les mesures réelles.

### Matériel de référence

Valeurs relevées sur la plaque signalétique de l'unité de développement.

**GECO — Swimming Pool Heat Pump — modèle `GEPAC08`** (compresseur **INVERTER**)

| Donnée | Valeur | Conditions |
|---|---|---|
| Puissance chauffage | 8,4 kW | air 26 °C / eau 26 °C / 80 % HR |
| COP | 14,1 ~ 7,0 | idem |
| COP à 50 % | 10,3 | idem |
| Puissance chauffage | 6,1 kW | air 15 °C / eau 26 °C / 70 % HR |
| COP | 7,0 ~ 4,8 | idem |
| COP à 50 % | 6,3 | idem |
| Puissance froid | 4,0 kW | air 35 °C / eau 28 °C / 80 % HR |
| Alimentation | 230 V / 1 Ph / 50 Hz | — |
| Pression sonore à 1 m | 38,8 ~ 48,2 dB(A) | — |
| Pression sonore à 50 % | 41,4 dB(A) | — |
| Puissance absorbée | 0,17 ~ 1,2 kW | air 15 °C |
| Courant absorbé | 0,74 ~ 5,2 A | air 15 °C |
| Courant max | 8,5 A | — |
| Débit d'eau conseillé | 2 ~ 4 m³/h | — |
| Fluide frigorigène | R32 — 650 g | GWP 675 · éq. CO₂ 0,439 t |
| Indice de protection | IPX4 | — |
| Poids | 45 kg | — |

### Liens utiles

- [Documentation Modbus de Home Assistant](https://www.home-assistant.io/integrations/modbus/)
- [Waveshare RS485 TO ETH (B)](https://www.waveshare.com/wiki/RS485_TO_ETH_(B))

---

## English

Home Assistant integration to control a **Geco swimming pool heat pump** — tested on a **GEPAC08 (INVERTER compressor)** — over **Modbus TCP**, through an RS485 → Ethernet gateway. **No cloud, no Internet connection required**: everything runs locally.

Original goal: **unlock the “Super Silence” mode** (limited output, quieter and more efficient unit).

### Features

| Feature | Description | Register |
|---|---|---|
| Power on/off | Turn the heat pump on or off | coil 0 |
| Thermostat | Setpoint and mode (Auto/Heat/Cool) | holding 3 / holding 0 |
| Current temperature | Water inlet | input 3 |
| Water outlet temperature | Water outlet | input 4 |
| Ambient temperature | Air | input 5 |
| Compressor | Load percentage | input 0 |
| Compressor current | Current draw | input 11 |
| PFC voltage | Internal voltage | input 2 |
| Working mode | Smart / Silence / Super Silence / Turbo | holding 1 |
| Faults | General fault, E3 fault | discrete 16 / 51 |
| Diagnostic | Modbus communication status | — |

Every feature is exposed as an entity in Home Assistant (see the entity table below).

### Hardware

- An **RS485 → Ethernet gateway** (tested: Waveshare RS485 TO ETH / POE).
- The **RS485** connector on the heat pump control board (the port intended for the optional Wi-Fi module).
- A cable between the heat pump and the gateway (UTP recommended: **3 wires** — `B`, `A`, `G`).

The RS485 port is the **`CN12`** connector on the control board (pins `B`, `A`, `G`, `+12V`).

### Step-by-step assembly

**1. Open the electrical box**

Switch off the power, then **wait 5 minutes** before opening (see the “CAUTION” label on the cover).

![Opening the box](images/open_the_box.jpg)

**2. Locate the RS485 connector**

It is the small **4-pin `CN12`** connector on the board (MWH298-V3 series) — pins `B`, `A`, `G`, `+12V`. This is the port normally intended for the optional Wi-Fi module.

![Locating the CN12 connector](images/localise_the_connecteur.jpg)

**3. Wire the connector**

Connect **`B` → `B`**, **`A` → `A`** and **`G` → `GND`**. **`+12V` is not needed**: the gateway is powered over **PoE** (or by its own supply).

![Wiring the connector](images/wire_the_connector.jpg)

### 🛒 Where to buy

| Item | Link |
|---|---|
| **JST-XH connector kit** (2/3/4/5/6 pins, 2.54 mm) — to build the `CN12` connector | [Amazon.fr — YIXISI, 460 pcs](https://www.amazon.fr/dp/B082ZLYRRN) |
| **RS485 → Ethernet gateway, 1 channel** | [Amazon.fr — Waveshare](https://www.amazon.fr/dp/B0BRNBTFVC) |
| **RS485 → Ethernet gateway, 2 channels** (a single gateway for two devices) | [Amazon.fr — Waveshare](https://www.amazon.fr/dp/B0CB8LXQFH) |

> The **1-channel** version is enough for the heat pump. The **2-channel** version lets you connect two RS485 devices with a single gateway (e.g. heat pump + electrolyser). See also the [Waveshare docs](https://www.waveshare.com/wiki/RS485_TO_ETH_(B)).

### Gateway configuration

In the gateway web UI (Waveshare RS485 TO ETH / POE):

| Setting | Value |
|---|---|
| **Work Mode** | `TCP Server` |
| **Protocol** | `Modbus TCP to RTU` |
| **Device Port** | `4196` (Waveshare default; here `4197`) |
| **Baud Rate / Databits / Parity / Stopbits** | `9600` / `8` / `None` / `1` |
| **IP mode** | `Static` |
| **Modbus slave** | `1` |

![Waveshare gateway configuration](images/config_waveshare.png)

### Integration installation

**Via HACS (custom repository)**

1. HACS → Integrations → ⋯ → *Custom repositories*
2. Add `Locodice67/HA-Swimming-Pool-Heat-Pump-Geco-Modbus`, category *Integration*
3. Install, then restart Home Assistant

**Manual**

Copy the `custom_components/pac_piscine_geco/` folder into `/config/custom_components/`, then restart Home Assistant.

### Configuration

Settings → Devices & services → **Add integration** → *PAC Piscine Geco*.

| Field | Usual value |
|---|---|
| IP address | RS485 → Ethernet gateway IP |
| TCP port | `4196` (Waveshare default; configurable — e.g. `4197`) |
| Modbus unit (slave) id | `1` |
| Refresh interval | `30` s |

The interval can be changed afterwards through the integration's *Configure* button.

### Created entities

| Platform | Entity | Register |
|---|---|---|
| `climate` | Thermostat | input 3 / holding 3 / holding 0 / holding 1 |
| `switch` | On/Off | coil 0 |
| `number` | Temperature setpoint | holding 3 |
| `select` | Mode (Auto/Heat/Cool) | holding 0 |
| `select` | Working mode | holding 1 |
| `sensor` | Water temperature | input 4 |
| `sensor` | Air temperature | input 5 |
| `sensor` | Compressor current | input 11 |
| `sensor` | PFC voltage | input 2 |
| `sensor` | Compressor | input 0 |
| `binary_sensor` | Status | coil 0 |
| `binary_sensor` | General fault | discrete input 16 |
| `binary_sensor` | E3 fault | discrete input 51 |
| `binary_sensor` | Modbus communication status | diagnostic |

> `number` and both `select` entities write **the same registers** as the `climate`: they are alternative views. The `climate` alone is enough to control the heat pump.

### Dashboard

A thermostat plus an on/off button and the sensors are enough. Suggested layout:

- **Thermostat** (climate) — setpoint and mode
- **On/Off** (switch)
- **Measurements** — water/air temperatures, compressor, current, PFC voltage
- **Status** — faults, Modbus communication

### Example automation: “Super Silence”

Typical sequence: turn the heat pump on, wait a few seconds, set the setpoint, then switch to **Super Silence**.

```yaml
# Example (adapt as needed): heat pump ON -> 30 °C -> Super Silence
actions:
  - action: switch.turn_on
    target:
      entity_id: switch.pac_piscine_marche_arret
  - delay:
      seconds: 5
  - action: climate.set_temperature
    target:
      entity_id: climate.pac_piscine_thermostat
    data:
      temperature: 30
  - action: select.select_option
    target:
      entity_id: select.pac_piscine_mode_de_travail
    data:
      option: super_silence
```

### Limitations

- **Working mode (register 1)**: on the tested unit (**GEPAC08**) the **write** to register 1 is **rejected** by the board (tested with `0`, `2` and `3`), while other `holding` writes work (the setpoint, register 3, goes through). The mode is therefore **readable** but **not controllable** over Modbus on this firmware (it is set on the heat pump keypad). Model dependent.
- The addresses come from the **official Modbus documentation for the MWH216 / MWH298 boards**. Geco / AES / Madimack boards look alike, but the exact model may differ: verify the values (water/air temperatures) against actual measurements.

### Reference hardware

Values read from the nameplate of the development unit.

**GECO — Swimming Pool Heat Pump — model `GEPAC08`** (**INVERTER** compressor)

| Data | Value | Conditions |
|---|---|---|
| Heating capacity | 8.4 kW | air 26 °C / water 26 °C / 80 % RH |
| COP | 14.1 ~ 7.0 | idem |
| COP at 50 % | 10.3 | idem |
| Heating capacity | 6.1 kW | air 15 °C / water 26 °C / 70 % RH |
| COP | 7.0 ~ 4.8 | idem |
| COP at 50 % | 6.3 | idem |
| Cooling capacity | 4.0 kW | air 35 °C / water 28 °C / 80 % RH |
| Power supply | 230 V / 1 Ph / 50 Hz | — |
| Sound pressure at 1 m | 38.8 ~ 48.2 dB(A) | — |
| Sound pressure at 50 % | 41.4 dB(A) | — |
| Rated input power | 0.17 ~ 1.2 kW | air 15 °C |
| Rated input current | 0.74 ~ 5.2 A | air 15 °C |
| Max input current | 8.5 A | — |
| Advised water flux | 2 ~ 4 m³/h | — |
| Refrigerant | R32 — 650 g | GWP 675 · CO₂e 0.439 t |
| Protection level | IPX4 | — |
| Weight | 45 kg | — |

### Useful links

- [Home Assistant Modbus documentation](https://www.home-assistant.io/integrations/modbus/)
- [Waveshare RS485 TO ETH (B)](https://www.waveshare.com/wiki/RS485_TO_ETH_(B))

---

[⬆️ Haut / Top](#pac-piscine-geco)
