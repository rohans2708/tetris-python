"""
Dieses Modul kümmert sich um das Laden und Speichern der dauerhaften Upgrade-Daten.

Die Daten werden in einer JSON-Datei namens `upgrades.json` im Projekt-Root
gespeichert. Fehlt die Datei, werden sinnvolle Standardwerte zurückgegeben.
"""

import pandas as pd
import os
from typing import Dict, Any

# Standard-Schema, falls keine Datei vorhanden ist
DEFAULT_DATA: Dict[str, Any] = {
    "rotation_buffer": 0,
    "ghost_piece": 0,
    "smoother_gravity": 0,
    "score_multiplier": 1,
    "hard_drop": 0,
    "meta_currency": 0,
    "bomb_block": 0,
}

# Pfad zu upgrades.json im Projekt-Root
UPGRADES_FILE = "/Users/robin/CodeProjects/tetris-python-master/upgrades.csv"


def load_upgrades(name) -> Dict[str, Any]:
    """Lädt Upgrade-Daten aus der JSON-Datei (oder liefert Defaults)."""
    data = DEFAULT_DATA.copy()
    csv = pd.read_csv(UPGRADES_FILE)
    # find the row with the name
    row = csv[csv['Name'] == name]
    # get the upgrades column
    if row.empty:
        return data
    upgrades = row['Upgrades']
    if upgrades.empty:
        return data
    upgrades = upgrades.values[0]
    for upgrade in upgrades.split(','):
        key, value = upgrade.split(':')
        try:
            data[key] = int(value)
        except Exception:
            pass
    return data


def save_upgrades(name, data: Dict[str, Any]) -> None:
    csv = pd.read_csv(UPGRADES_FILE)
    # Create the upgrade string
    upgrade_string = ','.join([f"{key}:{value}" for key, value in data.items()])

    # Check if the name already exists
    if name in csv['Name'].values:
        # Update the existing row
        csv.loc[csv['Name'] == name, 'Upgrades'] = upgrade_string
    else:
        # Add a new row
        new_row = pd.DataFrame({'Name': [name], 'Upgrades': [upgrade_string]})
        csv = pd.concat([csv, new_row], ignore_index=True)

    # Save the updated DataFrame back to the file
    csv.to_csv(UPGRADES_FILE, index=False)



