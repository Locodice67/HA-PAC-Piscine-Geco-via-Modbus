# Plan de travail — PAC Piscine IPHCR45

Feuille de route de l'intégration `pool_heat_pump_iphcr45_modbus`.
Dernière mise à jour : 2026-09-11.

---

## État actuel

### Terminé ✅
- Intégration custom `pool_heat_pump_iphcr45_modbus` : `climate`, `switch`, `number`, 2 `select`, 5 `sensor`, 3 `binary_sensor`.
- Renommage **Greco → Geco** (domaine, dossier, textes, dépôt GitHub).
- Images de marque : `brand/icon.png`, `icon@2x.png`, `logo.png`, `logo@2x.png`.
- Modèle corrigé en **`GEPAC08 (Modbus)`** ; courant compresseur borné à **10 A**.
- README **bilingue FR/EN** (switch de langue cliquable).
- Section **« Matériel de référence »** (plaque signalétique GEPAC08).

### Vérifié
- ✅ Lecture Modbus (températures, PFC, courant, %, états, défauts).
- ✅ Écriture Modbus sur la **consigne** (`holding 3`).
- ❌ Écriture du **mode de travail** (`holding 1`) **refusée** par la carte — testé avec `0`, `2` et `3`.

---

## Travaux restants

### 1. Mode de travail 🔴 *(priorité)*
- [ ] Tester l'écriture du `holding 1` **PAC éteinte** (hypothèse : réglage verrouillé en marche).
- [ ] Sinon : **scanner** les registres `holding` pour localiser le bon registre.
- [ ] Sinon : **retirer** le `select` « Mode de travail » et le `fan_mode` du thermostat (contrôles inertes).
- [ ] Option `turbo` (`=3`) ajoutée **en local seulement** : à pousser ou à reverter.

### 2. Capteurs à ajouter — registres d'entrée `3x` (lecture) 🟠
- [ ] `1` — vitesse cible compresseur (Hz)
- [ ] `3` — température entrée d'eau *(type 1)*
- [ ] `6` — échappement gaz *(type 2)*
- [ ] `7` — évaporateur / serpentin extérieur *(type 1)*
- [ ] `8` — retour gaz *(type 1)*
- [ ] `9` — échangeur titane / serpentin intérieur *(type 1)*
- [ ] `10` — fréquence compresseur (Hz)
- [ ] `12` — plaque de refroidissement *(type 2)*
- [ ] `13` — ouverture vanne EEV
- [ ] `14` — vitesse ventilateur DC (RPM)

### 3. Défauts & protections — entrées TOR `1x` 🟠
- [ ] `1` — dégivrage en cours
- [ ] `2–6` — DIN1 → DIN5
- [ ] `7–15` — OUT1 → OUT9
- [ ] `17` — demande de marche compresseur
- [ ] `48–59, 61` — erreurs E0–Eb, Ed → **capteur « code défaut » décodé**
- [ ] `64–74` — protections P0–PA → capteur décodé
- [ ] `80–91` — défauts F0–Fb → capteur décodé

### 4. Réglages — `4x` (lecture/écriture) 🟡
- [ ] `2` — plage de température mode Auto (84–140, pas 2)
- [ ] `4` — plage de température mode Froid (84–120, pas 2)
- [ ] `5` — mode pompe P0 (0–2)
- [ ] `6` — temps de marche pompe P1 (10–120 min, pas 5)
- [ ] `7` — temps compresseur avant dégivrage (30–90 min)
- [ ] `8` — température d'entrée dégivrage P3 (26–60)
- [ ] `9` — durée max dégivrage P4 (1–12 min)
- [ ] `10` — température de sortie dégivrage P5 (76–120)
- [ ] `17, 18` — surchauffe vanne EEV (40–100)
- [ ] `25` — mémoire après coupure (0–1)

### 5. Bobine — `0x` 🟡
- [ ] `1` — dégivrage forcé (écriture FC05)

### 6. Correctifs 🟠
- [ ] **Consigne selon le mode** : `4x2` en Auto / `4x3` en Chaud / `4x4` en Froid (aujourd'hui toujours `4x3`).
- [ ] **Températures type 2** (`3x6`, `3x12`) : `scale 0.5`, **`offset 0`** (et non `offset -30`).
- [ ] **Valeurs du mode de travail** : aligner sur la fiche (`0` Smart / `1` Silence / `3` Turbo) selon le résultat du test.

### 7. Documentation & ergonomie de configuration 🟠
- [x] **README — guide de montage** : photos **open_the_box / localise_the_connecteur / wire_the_connector** intégrées dans `images/` ✅ *fait — `15f0f54`*
- [x] **README — liens d'achat** : kit **JST-XH** (Amazon) + passerelle Waveshare ✅ *fait — `8e73149`*
  - N° de série **flouté** sur la photo du connecteur (*`9120856`*)
- [x] **Config flow — Marque → Modèle** : étape « Marque » (**Geco**) puis **liste des modèles** (GEPAC08), pour ne créer que les registres du modèle choisi ✅ *fait — commit `7cba3bd`*

---

## Points ouverts / à trancher
- [x] **Local = dépôt** : l'option `turbo` du sélecteur est désormais dans le dépôt (plus de divergence).
- [ ] **Ordre des langues** du README (FR d'abord — actuellement).
- [ ] **Enrichir le README** : section « Dépannage », sommaire cliquable, photos dans `images/`.
- [ ] **Rappel protocole** (fiche officielle) : écriture `4x` en **FC06**, `0x` en **FC05** ; **max 3 registres consécutifs** en `3x`/`4x` (48 pour les bits) ; **60 ms** mini entre deux requêtes ; esclave `1`.

---

## Électrolyseur (Pool Technologie) — PR en amont
- [ ] **PR #5** — concentration pH + taille du bassin réglable → **fixer la plage du volume** (l'appareil a accepté `23 m³` : plage dynamique validée ?).
- [ ] **PR #6** — diagnostics cellule + alarmes (issue #4) → en revue.
