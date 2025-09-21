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

if __name__ == "__main__":
    asyncio.run(main())
