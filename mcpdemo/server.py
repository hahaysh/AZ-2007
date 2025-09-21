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
