from __future__ import annotations
import base64
import json
import os
import uuid
from datetime import datetime


class _Encoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return {"__bytes__": base64.b64encode(obj).decode()}
        return super().default(obj)


def _decode(obj):
    if "__bytes__" in obj:
        return base64.b64decode(obj["__bytes__"])
    return obj

SESSIONS_DIR = os.path.join(os.path.dirname(__file__), "sessions")


def _ensure_dir():
    os.makedirs(SESSIONS_DIR, exist_ok=True)


def list_sessions() -> list[dict]:
    _ensure_dir()
    sessions = []
    for fname in os.listdir(SESSIONS_DIR):
        if fname.endswith(".json"):
            path = os.path.join(SESSIONS_DIR, fname)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f, object_hook=_decode)
                    sessions.append(data)
            except (json.JSONDecodeError, KeyError):
                os.remove(path)
    return sorted(sessions, key=lambda x: x["created_at"], reverse=True)


def load_session(session_id: str) -> dict | None:
    path = os.path.join(SESSIONS_DIR, f"{session_id}.json")
    if not os.path.exists(path):
        return None
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f, object_hook=_decode)


def save_session(session_id: str, name: str, messages: list):
    _ensure_dir()
    path = os.path.join(SESSIONS_DIR, f"{session_id}.json")
    existing = load_session(session_id)
    created_at = existing["created_at"] if existing else datetime.now().isoformat()
    with open(path, "w", encoding="utf-8") as f:
        json.dump({
            "id": session_id,
            "name": name,
            "messages": messages,
            "created_at": created_at,
            "updated_at": datetime.now().isoformat(),
        }, f, ensure_ascii=False, indent=2, cls=_Encoder)


def create_session() -> str:
    session_id = str(uuid.uuid4())[:8]
    save_session(session_id, "새 대화", [])
    return session_id


def delete_session(session_id: str):
    path = os.path.join(SESSIONS_DIR, f"{session_id}.json")
    if os.path.exists(path):
        os.remove(path)


def auto_name(messages: list) -> str:
    for msg in messages:
        if msg["role"] == "user" and msg.get("content"):
            name = msg["content"].strip().replace("\n", " ")
            return name[:25] + "..." if len(name) > 25 else name
    return "새 대화"
