# client.py
import argparse
import asyncio
import json
from typing import Any

from fastmcp import Client


def _text_content(blocks: Any) -> str:
    """FastMCP content 블록에서 텍스트만 뽑아보기 위한 헬퍼."""
    try:
        texts = []
        for b in (blocks or []):
            if hasattr(b, "text") and b.text is not None:
                texts.append(str(b.text))
        return "\n".join(texts) if texts else json.dumps(blocks, default=str, ensure_ascii=False)
    except Exception:
        return str(blocks)


async def demo_calls(client: Client) -> None:
    # 연결 확인
    await client.ping()

    # 인트로스펙션
    tools = await client.list_tools()
    resources = await client.list_resources()
    prompts = await client.list_prompts()

    print("\n[Tools]")
    for t in tools:
        print(f" - {t.name}: {t.description}")

    print("\n[Resources]")
    for r in resources:
        print(f" - {r.uri}")

    print("\n[Prompts]")
    for p in prompts:
        print(f" - {p.name}")

    tool_names = {t.name for t in tools}

    # greet 테스트
    if "greet" in tool_names:
        res = await client.call_tool("greet", {"name": "FastMCP 사용자"})
        print("\n[greet]")
        print(_text_content(getattr(res, "content", [])))

    # add 테스트
    if "add" in tool_names:
        res = await client.call_tool("add", {"a": 7, "b": 5})
        print("\n[add]")
        print(_text_content(getattr(res, "content", [])))

    # 리소스 읽기
    try:
        content = await client.read_resource("resource://hello/message")
        print("\n[resource://hello/message]")
        print(_text_content(content))
    except Exception as e:
        print(f"\n[resource skipped] {e}")

    # 프롬프트 렌더링
    try:
        prompt = await client.get_prompt("summarize", {
            "text": "FastMCP는 MCP 서버/클라이언트를 쉽게 만들도록 돕는 파이써닉 프레임워크입니다."
        })
        print("\n[prompt summarize → messages]")
        for m in prompt.messages:
            # m.content는 블록 리스트. 텍스트 블록을 찾아 출력
            text = None
            for b in m.content:
                if hasattr(b, "text") and b.text is not None:
                    text = b.text
                    break
            print(f" - {m.role}: {text}")
    except Exception as e:
        print(f"\n[prompt skipped] {e}")


async def main():
    parser = argparse.ArgumentParser(description="HelloMCP Client")
    parser.add_argument("--server", default="./server.py", help="STDIO로 실행할 서버 스크립트 경로(.py)")
    parser.add_argument("--url", help="HTTP 서버 MCP 엔드포인트 (예: http://127.0.0.1:8000/mcp/)")
    parser.add_argument("--env", help="서버 프로세스에 전달할 .env 파일 경로(선택)", default=None)
    parser.add_argument("--quick", action="store_true", help="데모 호출만 하고 종료")
    args = parser.parse_args()

    # 경로(.py) 또는 URL을 넘기면 fastmcp.Client가 자동으로 전송 방식을 추론합니다.
    target = args.url if args.url else args.server

    # env_file은 STDIO일 때 서버 프로세스에 환경변수를 주입합니다(없으면 무시).
    #async with Client(target, env_file=args.env) as client:
    async with Client(target) as client:
        await demo_calls(client)
        if not args.quick:
            print("\n(종료하려면 Ctrl+C) 대화형 모드는 생략했습니다.")


if __name__ == "__main__":
    asyncio.run(main())
