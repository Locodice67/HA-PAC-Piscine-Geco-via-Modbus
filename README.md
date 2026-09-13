# Swimming-Pool-Heat-Pump-IPHCR45-Modbus

**🌍 Langue / Language : [🇫🇷 Français](#français) · [🇬🇧 English](#english)**

![IPHCR45](custom_components/swimming_pool_heat_pump_iphcr45_modbus/brand/logo.png)

---

## Français

Intégration Home Assistant pour piloter une **PAC (pompe à chaleur) de piscine** en **Modbus TCP**, via une passerelle RS485 → Ethernet. **Aucun cloud, aucune connexion Internet** : tout reste local.

La référence **IPHCR45** correspond à une pompe à chaleur de piscine **Full Inverter** haute performance de la marque **Fairland**, souvent distribuée sous différentes marques ou gammes : **Geco / AES / Madimack / BWT / Rapid / Confort**.

Objectif initial : **piloter la pompe à chaleur sans être obligé de passer par le cloud Tuya**.

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
| Mode de travail | Smart / Silence | holding 1 |
| Défauts | Défaut général, défaut E3 | discrete 16 / 51 |
| Diagnostic | État de la communication Modbus | — |

Chaque fonction est exposée comme entité dans Home Assistant (voir le tableau des entités plus bas).

### Matériel nécessaire

- Une **passerelle RS485 → Ethernet** (testé : Waveshare RS485 TO ETH / POE).
- Le connecteur **RS485** de la carte de contrôle de la PAC (port prévu pour le module Wi-Fi optionnel).
- Un câble entre la PAC et la passerelle. Un **câble RJ45** convient.

Le port RS485 est le connecteur de la carte de contrôle (broches `B`, `A`, `G`, `+12V`).

### Montage pas à pas

**1. Ouvrir le coffret électrique**

Couper l'alimentation puis **attendre 5 minutes** avant d'ouvrir (voir l'étiquette « CAUTION » sur le capot).

Déposer les vis du dessus et de l'alimentation, puis enlever les caches. Dévisser ensuite les vis du couvercle « CAUTION » et du capot voisin (**7 à 8 vis**).

![Ouverture du coffret](images/open_the_box.jpg)

**2. Repérer le connecteur RS485**

C'est le petit connecteur **4 broches `B`, `A`, `G`, `+12V`** de la carte. C'est le port normalement prévu pour le module Wi-Fi optionnel.

![Repérage du connecteur](images/localise_the_connecteur.jpg)

**3. Câbler le connecteur**

Relier **`B` → `B`**, **`A` → `A`** et **`G` → `GND`**. La passerelle est alimentée en **PoE** : le **`+12V` n'est pas nécessaire**. Un **câble RJ45** convient.

![Câblage du connecteur](images/wire_the_connector.jpg)

### 🛒 Où acheter

| Article | Lien |
|---|---|
| **Kit de connecteurs JST-XH** (2/3/4/5/6 broches, pas 2,54 mm) — pour réaliser le connecteur | [Amazon.fr — YIXISI, 460 pièces](https://www.amazon.fr/dp/B082ZLYRRN) |
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
| **Device IP** | IP de la passerelle elle-même |
| **Esclave Modbus** | `1` |

> - **Device IP** : l'adresse IP de la passerelle elle-même ; à adapter à la plage d'adresses (**IP Range**) de ton réseau.
> - **Destination IP** : on peut y mettre la même adresse que **Device IP**, ou l'adresse de **Home Assistant**. Dans notre cas, ce réglage semble sans effet.
> - **Enable Multi-Host** : à activer **en premier** ; c'est ce réglage qui fait apparaître l'option **Time Out**.

![Configuration de la passerelle Waveshare](images/config_waveshare.png)

### Installation de l'intégration

**Via HACS (dépôt personnalisé)**

1. HACS → Intégrations → ⋯ → *Dépôts personnalisés*
2. Ajouter `Locodice67/Swimming-Pool-Heat-Pump-IPHCR45-Modbus`, catégorie *Intégration*
3. Installer, puis redémarrer Home Assistant

**Manuelle**

Copier le dossier `custom_components/swimming_pool_heat_pump_iphcr45_modbus/` dans `/config/custom_components/`, puis redémarrer Home Assistant.

### Mise à niveau depuis `pac_piscine_geco`

Le domaine de l'intégration a changé (`pac_piscine_geco` → `swimming_pool_heat_pump_iphcr45_modbus`). Home Assistant identifie une intégration par le nom de son dossier : **une entrée de configuration existante ne se chargera plus** après la mise à jour. La migration se fait une seule fois :

1. Paramètres → Appareils et services → **PAC Piscine** → ⋯ → **Supprimer**.
2. **Redémarrer Home Assistant**.
3. Ré-ajouter l'intégration (*Swimming-Pool-Heat-Pump-IPHCR45-Modbus*) avec les mêmes paramètres de connexion.

Les `entity_id` sont recréés à l'identique (le nom de l'appareil, « PAC Piscine », est inchangé), donc les automatisations et les dashboards continuent de fonctionner.

### Configuration

Paramètres → Appareils et services → **Ajouter une intégration** → *Swimming-Pool-Heat-Pump-IPHCR45-Modbus*.

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

### Limitations

- **Mode de travail (registre 1)** : sur l'unité testée (**GEPAC08**), l'**écriture** du registre 1 est **refusée** par la carte (testé avec `0`, `2` et `3`), alors que l'écriture d'autres registres `holding` fonctionne (la consigne, registre 3, passe). Le mode reste donc **lisible** mais **non pilotable** via Modbus sur ce firmware (réglage au clavier de la PAC). À vérifier selon les modèles.
- Les adresses proviennent de la **fiche Modbus officielle des cartes MWH216 / MWH298**. Les cartes **Geco / AES / Madimack / BWT / Rapid / Confort / Fairland** se ressemblent, mais le modèle exact peut différer : vérifie les valeurs (températures eau/air) contre les mesures réelles.

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

Home Assistant integration to control a **swimming pool heat pump** over **Modbus TCP**, through an RS485 → Ethernet gateway. **No cloud, no Internet connection required**: everything runs locally.

The **IPHCR45** reference is a high-performance **Full Inverter** swimming pool heat pump from **Fairland**, often distributed under different brands or ranges: **Geco / AES / Madimack / BWT / Rapid / Confort**.

Original goal: **control the heat pump without going through the Tuya cloud**.

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
| Working mode | Smart / Silence | holding 1 |
| Faults | General fault, E3 fault | discrete 16 / 51 |
| Diagnostic | Modbus communication status | — |

Every feature is exposed as an entity in Home Assistant (see the entity table below).

### Hardware

- An **RS485 → Ethernet gateway** (tested: Waveshare RS485 TO ETH / POE).
- The **RS485** connector on the heat pump control board (the port intended for the optional Wi-Fi module).
- A cable between the heat pump and the gateway. A **RJ45 cable** is suitable.

The RS485 port is the connector on the control board (pins `B`, `A`, `G`, `+12V`).

### Step-by-step assembly

**1. Open the electrical box**

Switch off the power, then **wait 5 minutes** before opening (see the “CAUTION” label on the cover).

Remove the screws on the top and on the power supply, then take off the covers. Then unscrew the screws of the “CAUTION” cover and of the adjacent hood (**7 to 8 screws**).

![Opening the box](images/open_the_box.jpg)

**2. Locate the RS485 connector**

It is the small **4-pin `B`, `A`, `G`, `+12V`** connector on the board. This is the port normally intended for the optional Wi-Fi module.

![Locating the connector](images/localise_the_connecteur.jpg)

**3. Wire the connector**

Connect **`B` → `B`**, **`A` → `A`** and **`G` → `GND`**. The gateway is powered over **PoE**, so **`+12V` is not needed**. A **RJ45 cable** is suitable.

![Wiring the connector](images/wire_the_connector.jpg)

### 🛒 Where to buy

| Item | Link |
|---|---|
| **JST-XH connector kit** (2/3/4/5/6 pins, 2.54 mm) — to build the connector | [Amazon.fr — YIXISI, 460 pcs](https://www.amazon.fr/dp/B082ZLYRRN) |
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
| **Device IP** | The gateway's own IP address |
| **Modbus slave** | `1` |

> - **Device IP**: the gateway's own IP address; keep it consistent with your network's IP range.
> - **Destination IP**: can be set to the same address as **Device IP**, or to **Home Assistant**'s address. In our case this setting appears to have no effect.
> - **Enable Multi-Host**: enable this **first**; it then exposes the **Time Out** setting.

![Waveshare gateway configuration](images/config_waveshare.png)

### Integration installation

**Via HACS (custom repository)**

1. HACS → Integrations → ⋯ → *Custom repositories*
2. Add `Locodice67/Swimming-Pool-Heat-Pump-IPHCR45-Modbus`, category *Integration*
3. Install, then restart Home Assistant

**Manual**

Copy the `custom_components/swimming_pool_heat_pump_iphcr45_modbus/` folder into `/config/custom_components/`, then restart Home Assistant.

### Upgrade from `pac_piscine_geco`

The integration domain changed (`pac_piscine_geco` → `swimming_pool_heat_pump_iphcr45_modbus`). Home Assistant identifies an integration by its folder name, so **an existing configuration entry will no longer load** after the update. Migration is a one-time operation:

1. Settings → Devices & services → **PAC Piscine** → ⋯ → **Delete**.
2. **Restart Home Assistant**.
3. Re-add the integration (*Swimming-Pool-Heat-Pump-IPHCR45-Modbus*) with the same connection settings.

Entity IDs are recreated identically (the device name, “PAC Piscine”, is unchanged), so automations and dashboards keep working.

### Configuration

Settings → Devices & services → **Add integration** → *Swimming-Pool-Heat-Pump-IPHCR45-Modbus*.

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

### Limitations

- **Working mode (register 1)**: on the tested unit (**GEPAC08**) the **write** to register 1 is **rejected** by the board (tested with `0`, `2` and `3`), while other `holding` writes work (the setpoint, register 3, goes through). The mode is therefore **readable** but **not controllable** over Modbus on this firmware (it is set on the heat pump keypad). Model dependent.
- The addresses come from the **official Modbus documentation for the MWH216 / MWH298 boards**. **Geco / AES / Madimack / BWT / Rapid / Confort / Fairland** boards look alike, but the exact model may differ: verify the values (water/air temperatures) against actual measurements.

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

[⬆️ Haut / Top](#swimming-pool-heat-pump-iphcr45-modbus)
