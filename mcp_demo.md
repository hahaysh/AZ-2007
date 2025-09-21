# 전체 소스

## server.py (HelloMCP 전용)

```python
# server.py
from fastmcp import FastMCP
import os

# 서버 이름/인사말을 환경변수로 커스터마이즈 가능(없으면 기본값 사용)
SERVER_NAME = os.getenv("HELLOMCP_SERVER_NAME", "HelloMCP")
GREETING_MESSAGE = os.getenv("GREETING_MESSAGE", "안녕하세요")

mcp = FastMCP(SERVER_NAME)

# === Tools ===
@mcp.tool
def greet(name: str) -> str:
    """이름을 받아 인사말을 반환합니다."""
    return f"{GREETING_MESSAGE}, {name}님!"

@mcp.tool
def add(a: int, b: int) -> int:
    """두 숫자를 더합니다."""
    return a + b

# === Resource ===
@mcp.resource("resource://hello/message")
def hello_message() -> str:
    """간단한 리소스 메시지."""
    return "이건 HelloMCP 리소스 예제입니다."

# === Prompt ===
@mcp.prompt("summarize")
def summarize_prompt(text: str) -> str:
    """주어진 글을 한 문단으로 요약하도록 지시하는 프롬프트를 생성합니다."""
    return f"아래 글을 한국어로 한 문단으로 정확하게 요약하세요:\n\n{text}"

if __name__ == "__main__":
    # 기본 전송: STDIO (클라이언트가 프로세스를 스폰해서 붙음)
    mcp.run()
    # HTTP로 띄우고 싶다면 위 한 줄 대신 아래 예시:
    # mcp.run(transport="http", host="127.0.0.1", port=8000)
```

---

## client.py (HelloMCP 전용, STDIO/HTTP 모두 지원)

```python
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
    async with Client(target, env_file=args.env) as client:
        await demo_calls(client)
        if not args.quick:
            print("\n(종료하려면 Ctrl+C) 대화형 모드는 생략했습니다.")


if __name__ == "__main__":
    asyncio.run(main())
```

---

# 실행 순서 (Step by Step)

아래는 **두 가지 방식**(① STDIO, ② HTTP) 중 **원하는 한 가지 방식만** 선택해서 따라 하시면 됩니다.

---

## A. STDIO 방식 (가장 간단: 클라이언트가 서버 프로세스를 직접 실행)

### 1) 가상환경 & 라이브러리 설치

```bash
python -m venv .venv
# Windows: .venv/Scripts/activate
# macOS/Linux:
source .venv/bin/activate

pip install fastmcp python-dotenv
```

### 2) 파일 준비

* 위의 **server.py**, **client.py** 내용을 각각 파일로 저장

### 3) (선택) .env 생성 — HelloMCP용

```dotenv
# .env  (없어도 실행 가능)
HELLOMCP_SERVER_NAME=HelloMCP
GREETING_MESSAGE="안녕하세요! 이것은 HelloMCP 서버의 기본 인사말입니다."
```

### 4) 클라이언트로 서버 스폰 & 호출

```bash
# .env 없이도 가능
python client.py --server ./server.py --quick

# .env를 서버 프로세스에 주입하고 싶다면
python client.py --server ./server.py --env ./.env --quick
```

> `--quick`을 빼면 데모 호출 후 안내 문구만 출력하고 종료 대기 상태가 됩니다.

---

## B. HTTP 방식 (여러 클라이언트 접속/원격 테스트용)

### 1) 가상환경 & 라이브러리 설치

```bash
python -m venv .venv
source .venv/bin/activate
pip install fastmcp python-dotenv
```

### 2) 파일 준비

* 위의 **server.py**, **client.py** 저장

### 3) (선택) .env 생성

```dotenv
HELLOMCP_SERVER_NAME=HelloMCP
GREETING_MESSAGE=안녕하세요! 이것은 HelloMCP 서버의 기본 인사말입니다.
```

### 4) 서버를 HTTP로 실행 (택1)

**방법 4-1: server.py 수정 없이 CLI로 실행**

```bash
# 기본 엔드포인트는 /mcp/
fastmcp run server.py --transport http --port 8000
```

**방법 4-2: server.py에서 run을 HTTP로 지정하고 직접 실행**

```python
# server.py 하단을 이렇게 바꿔도 됩니다.
# if __name__ == "__main__":
#     mcp.run(transport="http", host="127.0.0.1", port=8000)
```

```bash
python server.py
```

### 5) 클라이언트로 HTTP 서버 호출

```bash
python client.py --url http://127.0.0.1:8000/mcp/ --quick
```

> 인증이 필요한 구성이라면 `Client(..., headers={"Authorization": "Bearer <TOKEN>"})` 형태로 확장하시면 됩니다(이 예제는 인증 없이 동작).

---

# 문제 발생 시 체크리스트

* **패키지/버전**: `pip show fastmcp` / `python -V` 확인 (권장: Python 3.10+)
* **경로**: `server.py`, `client.py` 파일 경로 오타/권한
* **.env**: 없어도 실행 가능. 다만 환경변수로 커스터마이즈 하려면 `--env ./.env`로 서버에 주입(STDIO일 때)
* **HTTP 404**: 엔드포인트는 `http://HOST:PORT/mcp/` 형태인지 확인
* **서버 로그 확인**: 에러가 의심되면 `python server.py` 단독 실행으로 콘솔 로그 먼저 체크

