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
