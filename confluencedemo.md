* 서버 2개: `server_confluence_stdio.py`, `server_confluence_http.py`
* 클라이언트 2개: `client_confluence_stdio.py`, `client_confluence_http.py`
---

# 0) 선행 준비

## 패키지 설치

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install fastmcp requests python-dotenv
```

## 환경변수(.env 또는 셸)

프로젝트 루트에 `.env` 생성(또는 셸에서 export):

```dotenv
CONFLUENCE_SITE=your-domain.atlassian.net
CONFLUENCE_EMAIL=you@example.com
CONFLUENCE_API_TOKEN=your-api-token
```

---

# 1) 서버(표준입출력 STDIO) — `server_confluence_stdio.py`

```python
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
```

---

# 2) 서버(HTTP) — `server_confluence_http.py`

```python
# server_confluence_http.py
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

mcp = FastMCP("ConfluenceMCP-HTTP")

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
    # HTTP 엔드포인트: http://127.0.0.1:8010/mcp/
    mcp.run(transport="http", host="127.0.0.1", port=8010)
```

---

# 3) 클라이언트(STDIO 전용) — `client_confluence_stdio.py`

```python
# client_confluence_stdio.py
# client_confluence_stdio.py
import asyncio, argparse, json
from fastmcp import Client
from dotenv import load_dotenv

def pretty(result):
    blocks = getattr(result, "content", [])
    texts = [b.text for b in (blocks or []) if hasattr(b, "text") and b.text]
    return "\n".join(texts) if texts else json.dumps(result, default=str, ensure_ascii=False)

async def main():
    p = argparse.ArgumentParser()
    p.add_argument("--server", default="./server_confluence_stdio.py")
    p.add_argument("--env", default="./.env")
    args = p.parse_args()

    load_dotenv(args.env)  # 없으면 무시

    async with Client(args.server) as client:  # 경로 전달 → STDIO 자동
        await client.ping()
        # 예: 스페이스 5개
        res = await client.call_tool("list_spaces", {"limit": 5})
        print("[list_spaces]\n", pretty(res))
        # 예: CQL 샘플
        res = await client.call_tool("search_cql", {"cql": "type=page", "limit": 3})
        print("\n[search_cql]\n", pretty(res))

    # 예시 코드 추가 (demo 부분 안에)
    # 특정 페이지 ID로 본문 가져오기
    page_id = "123456789"  # 실제 Confluence 페이지 ID로 교체
    res = await client.call_tool("get_page", {"page_id": page_id})
    print("\n[get_page]")
    print(pretty(res))

    # 해당 페이지의 자식 페이지들 가져오기
    res = await client.call_tool("get_children", {"page_id": page_id, "limit": 5})
    print("\n[get_children]")
    print(pretty(res))


if __name__ == "__main__":
    asyncio.run(main())

```

---

# 4) 클라이언트(HTTP 전용) — `client_confluence_http.py`

```python
# client_confluence_http.py
import asyncio, argparse, json
from fastmcp import Client
from dotenv import load_dotenv

def pretty(result):
    blocks = getattr(result, "content", [])
    texts = [b.text for b in (blocks or []) if hasattr(b, "text") and b.text]
    return "\n".join(texts) if texts else json.dumps(result, default=str, ensure_ascii=False)

async def main():
    p = argparse.ArgumentParser()
    p.add_argument("--url", default="http://127.0.0.1:8010/mcp/")
    p.add_argument("--env", default="./.env")
    args = p.parse_args()

    load_dotenv(args.env)  # 서버가 읽어야 하므로, 서버 실행 전에 .env 설정이 되어 있어야 함

    async with Client(args.url) as client:  # URL 전달 → HTTP 자동
        await client.ping()
        res = await client.call_tool("list_spaces", {"limit": 5})
        print("[list_spaces]\n", pretty(res))
        res = await client.call_tool("search_cql", {"cql": "type=page", "limit": 3})
        print("\n[search_cql]\n", pretty(res))
        
    # 예시 코드 추가 (demo 부분 안에)
    # 특정 페이지 ID로 본문 가져오기
    page_id = "123456789"  # 실제 Confluence 페이지 ID로 교체
    res = await client.call_tool("get_page", {"page_id": page_id})
    print("\n[get_page]")
    print(pretty(res))

    # 해당 페이지의 자식 페이지들 가져오기
    res = await client.call_tool("get_children", {"page_id": page_id, "limit": 5})
    print("\n[get_children]")
    print(pretty(res))

if __name__ == "__main__":
    asyncio.run(main())
```

---

# 5) 실행 단계 (Step-by-step)

## A) STDIO 세트

```bash
# 1) .env 준비(또는 셸 export)
# 2) 서버/클라이언트 파일 저장
python client_confluence_stdio.py --server ./server_confluence_stdio.py --env ./.env
```

* 클라이언트가 서버 프로세스를 **STDIO로 직접 스폰**해서 붙습니다.

## B) HTTP 세트

```bash
# 1) .env 준비(또는 셸 export)
# 2) HTTP 서버 기동
python server_confluence_http.py
# 3) HTTP 클라이언트 호출
python client_confluence_http.py --url http://127.0.0.1:8010/mcp/ --env ./.env
```

* 여러 클라이언트가 동시에 붙을 수 있고, 원격 접속 테스트에 적합합니다.
