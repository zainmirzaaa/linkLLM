import json, datetime

def log_json(event: str, **fields):
    payload = {"ts": datetime.datetime.utcnow().isoformat() + "Z",
               "event": event, **fields}
    print(json.dumps(payload, ensure_ascii=False))
