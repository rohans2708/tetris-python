"""Utility helpers for loading and saving persistent player upgrades."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict

# Basiswerte für die freischaltbaren Upgrades
DEFAULT_UNLOCKED: Dict[str, float] = {
    "rotation_buffer": 0,
    "ghost_piece": 0,
    "smoother_gravity": 0,
    "score_multiplier": 1,
    "hard_drop": 0,
    "bomb_block": 0,
    "bomb_unlocked": 0,
    "preview_plus": 0,
    "hold_unlocked": 0,
}

DEFAULT_META: Dict[str, int] = {"meta_currency": 0}

# Speicherort der JSON-Datei (Projekt-Root)
UPGRADES_FILE = Path(__file__).resolve().parent.parent / "upgrades.json"


def _ensure_storage() -> Dict[str, Any]:
    """Sorgt dafür, dass die JSON-Datei existiert und liefert deren Inhalt."""
    if not UPGRADES_FILE.exists():
        payload: Dict[str, Any] = {"players": {}}
        UPGRADES_FILE.write_text(json.dumps(payload, indent=2))
        return payload

    try:
        return json.loads(UPGRADES_FILE.read_text())
    except json.JSONDecodeError:
        payload = {"players": {}}
        UPGRADES_FILE.write_text(json.dumps(payload, indent=2))
        return payload


def _coerce_int(value: Any, default: float) -> float:
    try:
        return float(value)
    except Exception:
        return default


def load_upgrades(name: str) -> Dict[str, Any]:
    """Lädt die Upgrade-Daten für einen Spieler oder liefert Standardwerte."""
    storage = _ensure_storage()
    players = storage.setdefault("players", {})
    player_entry = players.get(name, {})

    unlocked_raw = player_entry.get("unlocked", {})
    unlocked: Dict[str, float] = {
        key: _coerce_int(unlocked_raw.get(key, default), default)
        for key, default in DEFAULT_UNLOCKED.items()
    }

    meta_raw = player_entry.get("meta", {})
    meta_currency = _coerce_int(
        meta_raw.get("meta_currency", DEFAULT_META["meta_currency"]),
        DEFAULT_META["meta_currency"],
    )

    result: Dict[str, Any] = {
        "unlocked": unlocked,
        "meta": {"meta_currency": meta_currency},
    }

    # Für Abwärtskompatibilität: direkte Schlüssel spiegeln
    for key, value in unlocked.items():
        result[key] = value
    result["meta_currency"] = meta_currency

    return result


def save_upgrades(name: str, data: Dict[str, Any]) -> None:
    """Speichert die Upgrade-Daten des Spielers in der JSON-Datei."""
    storage = _ensure_storage()
    players = storage.setdefault("players", {})

    unlocked_target = DEFAULT_UNLOCKED.copy()
    unlocked_source = data.get("unlocked", {})
    for key in unlocked_target.keys():
        if key in data:
            unlocked_target[key] = (_coerce_int(data[key], unlocked_target[key]))
        elif key in unlocked_source:
            unlocked_target[key] = _coerce_int(unlocked_source[key], unlocked_target[key])

    meta_currency = _coerce_int(
        data.get(
            "meta_currency",
            data.get("meta", {}).get("meta_currency", DEFAULT_META["meta_currency"]),
        ),
        DEFAULT_META["meta_currency"],
    )

    players[name] = {
        "unlocked": unlocked_target,
        "meta": {"meta_currency": meta_currency},
    }

    data.setdefault("unlocked", {}).update(unlocked_target)
    data.update(unlocked_target)
    data.setdefault("meta", {})["meta_currency"] = meta_currency
    data["meta_currency"] = meta_currency

    UPGRADES_FILE.write_text(json.dumps(storage, indent=2, sort_keys=True))
