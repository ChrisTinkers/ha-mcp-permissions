"""Read-only connectivity check; prints no token, item text or secrets."""
import asyncio
import os
import httpx

TARGET = "todo.ha_weiterentwicklung"
API = "http://supervisor/core/api"


async def main():
    token = os.environ.get("SUPERVISOR_TOKEN", "")
    if not token:
        print("HA diagnostic: FAILED - Supervisor token unavailable", flush=True)
        return

    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            response = await client.get(
                f"{API}/states/{TARGET}",
                headers={"Authorization": f"Bearer {token}"},
            )
        if response.status_code != 200:
            print(f"HA diagnostic: FAILED - entity lookup HTTP {response.status_code}", flush=True)
            return
        data = response.json()
        if data.get("entity_id") != TARGET:
            print("HA diagnostic: FAILED - unexpected entity", flush=True)
            return
        print("HA diagnostic: OK - allowed to-do entity is readable", flush=True)
        async with httpx.AsyncClient(timeout=8.0) as client:
            items_response = await client.post(
                f"{API}/services/todo/get_items?return_response",
                json={"entity_id": TARGET},
                headers={"Authorization": f"Bearer {token}"},
            )
        if items_response.status_code != 200:
            print(f"MCP read diagnostic: FAILED - get_items HTTP {items_response.status_code}", flush=True)
            return
        data = items_response.json()
        if not isinstance(data, dict):
            print("MCP read diagnostic: FAILED - unexpected response shape", flush=True)
            return
        print("MCP read diagnostic: OK - to-do items can be queried without changes", flush=True)
    except Exception as error:
        print(f"HA diagnostic: FAILED - {type(error).__name__}", flush=True)


if __name__ == "__main__":
    asyncio.run(main())
