# server_confluence_stdio.py
from fastmcp import FastMCP
import os, requests

SITE  = os.getenv("CONFLUENCE_SITE", "").strip()
EMAIL = os.getenv("CONFLUENCE_EMAIL", "").strip()
TOKEN = os.getenv("CONFLUENCE_API_TOKEN", "").strip()

BASE_V2 = f"https://{SITE}/wiki/api/v2"   if SITE else None
BASE_V1 = f"https://{SITE}/wiki/rest/api" if SITE else None
AUTH    = (EMAIL, TOKEN)
HEADERS = {"Accept": "application/json"}
TIMEOUT = 60

def _check():
    if not (SITE and EMAIL and TOKEN):
        raise RuntimeError("환경변수 CONFLUENCE_SITE / CONFLUENCE_EMAIL / CONFLUENCE_API_TOKEN 필요")

def _get(url, params=None):
    _check()
    r = requests.get(url, params=params, headers=HEADERS, auth=AUTH, timeout=TIMEOUT)
    r.raise_for_status()
    return r.json()

mcp = FastMCP("ConfluenceMCP-STDIO")

@mcp.tool
def list_spaces(limit: int = 25):
    data = _get(f"{BASE_V2}/spaces", {"limit": max(1, min(limit, 100))})
    return [{"id": s["id"], "key": s["key"], "name": s["name"]} for s in data.get("results", [])]

@mcp.tool
def get_page(page_id: str, body_format: str = "storage"):
    return _get(f"{BASE_V2}/pages/{page_id}", {"body-format": body_format})

@mcp.tool
def search_cql(cql: str, limit: int = 10):
    data = _get(f"{BASE_V1}/content/search", {"cql": cql, "limit": max(1, min(limit, 50))})
    out = []
    for it in data.get("results", []):
        cid   = it.get("id") or it.get("content", {}).get("id")
        title = it.get("title") or it.get("content", {}).get("title")
        out.append({"id": cid, "title": title})
    return out

@mcp.tool
def get_children(page_id: str, limit: int = 25):
    data = _get(f"{BASE_V2}/pages/{page_id}/children", {"limit": max(1, min(limit, 100))})
    return [{"id": p["id"], "title": p["title"]} for p in data.get("results", [])]

if __name__ == "__main__":
    mcp.run()  # STDIO
