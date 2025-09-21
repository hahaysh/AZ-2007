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

if __name__ == "__main__":
    asyncio.run(main())
