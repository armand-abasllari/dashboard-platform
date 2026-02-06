import os
from typing import Any, Dict, List

import requests

from sqlalchemy.orm import Session

from ..db import SessionLocal
from .base import write_snapshot


STEAM_API_BASE = "https://api.steampowered.com"


def _get_json(url: str, params: Dict[str, Any]) -> Dict[str, Any]:
    r = requests.get(url, params=params, timeout=20)
    r.raise_for_status()
    return r.json()


def fetch_profile(api_key: str, steam_id64: str) -> Dict[str, Any]:
    url = f"{STEAM_API_BASE}/ISteamUser/GetPlayerSummaries/v2/"
    data = _get_json(url, {"key": api_key, "steamids": steam_id64})
    players = data.get("response", {}).get("players", [])
    return players[0] if players else {}


def fetch_owned_games(api_key: str, steam_id64: str) -> Dict[str, Any]:
    url = f"{STEAM_API_BASE}/IPlayerService/GetOwnedGames/v1/"
    return _get_json(
        url,
        {
            "key": api_key,
            "steamid": steam_id64,
            "include_appinfo": True,          # game names/icons
            "include_played_free_games": True,
        },
    )


def build_summary(profile: Dict[str, Any], owned: Dict[str, Any]) -> Dict[str, Any]:
    games: List[Dict[str, Any]] = owned.get("response", {}).get("games", []) or []
    total_minutes = sum(int(g.get("playtime_forever", 0)) for g in games)

    return {
        "steam_id64": profile.get("steamid"),
        "persona_name": profile.get("personaname"),
        "profile_url": profile.get("profileurl"),
        "avatar": profile.get("avatarfull") or profile.get("avatarmedium") or profile.get("avatar"),
        "game_count": owned.get("response", {}).get("game_count", len(games)),
        "total_playtime_minutes": total_minutes,
        "total_playtime_hours": round(total_minutes / 60, 1),
    }


def build_top_games(owned: Dict[str, Any], limit: int = 10) -> List[Dict[str, Any]]:
    games: List[Dict[str, Any]] = owned.get("response", {}).get("games", []) or []
    games_sorted = sorted(games, key=lambda g: int(g.get("playtime_forever", 0)), reverse=True)[:limit]

    out: List[Dict[str, Any]] = []
    for g in games_sorted:
        minutes = int(g.get("playtime_forever", 0))
        out.append(
            {
                "appid": g.get("appid"),
                "name": g.get("name"),
                "playtime_minutes": minutes,
                "playtime_hours": round(minutes / 60, 1),
                "img_icon_url": g.get("img_icon_url"),
                "img_logo_url": g.get("img_logo_url"),
            }
        )
    return out


def collect_and_store(db: Session, api_key: str, steam_id64: str) -> None:
    profile = fetch_profile(api_key, steam_id64)
    owned = fetch_owned_games(api_key, steam_id64)

    summary_payload = build_summary(profile, owned)
    top_games_payload = {"limit": 10, "items": build_top_games(owned, limit=10)}

    write_snapshot(db, service="steam", metric="summary", payload=summary_payload)
    write_snapshot(db, service="steam", metric="top_games", payload=top_games_payload)


def main() -> None:
    api_key = os.getenv("STEAM_API_KEY")
    steam_id64 = os.getenv("STEAM_ID64")

    if not api_key or not steam_id64:
        raise RuntimeError("Missing STEAM_API_KEY or STEAM_ID64 in environment")

    db = SessionLocal()
    try:
        collect_and_store(db, api_key, steam_id64)
        print("OK: stored steam/summary and steam/top_games snapshots")
    finally:
        db.close()


if __name__ == "__main__":
    main()
