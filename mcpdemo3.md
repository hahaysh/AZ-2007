### **MCP Server 실습가이드: VS Code + Confluence + Python**

#### **🎯 실습 목표**
- MCP 개념과 아키텍처 이해
- Python으로 간단한 MCP 서버 구현
- VS Code Copilot과 MCP 서버 연동 실습

#### **📋 사전 준비사항**
```bash
# 필수 설치 항목
- Python 3.8+
- VS Code (최신 버전)
- Node.js 18+
- GitHub Copilot 구독
```

#### **🛠️ 실습 단계**

**1단계: 환경 설정**
```bash
mkdir mcp-confluence-demo
cd mcp-confluence-demo
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install mcp flask requests python-dotenv
```

**2단계: 간단한 MCP 서버 구현**
```python
# simple_mcp_server.py
import json
import sys
from mcp import Server
from mcp.types import Tool, TextContent

class SimpleMCPServer:
    def __init__(self):
        self.server = Server("simple-confluence")
        self.setup_tools()
    
    def setup_tools(self):
        @self.server.list_tools()
        async def list_tools():
            return [
                Tool(
                    name="search_confluence", 
                    description="Confluence 페이지 검색",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"}
                        }
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict):
            if name == "search_confluence":
                return [TextContent(
                    type="text",
                    text=f"검색 결과: '{arguments['query']}'에 대한 페이지를 찾았습니다!"
                )]

if __name__ == "__main__":
    server = SimpleMCPServer()
    server.server.run()
```

**3단계: VS Code 설정**
```json
// .vscode/mcp.json
{
  "servers": {
    "simple-confluence": {
      "command": "python",
      "args": ["simple_mcp_server.py"],
      "env": {
        "CONFLUENCE_URL": "https://your-confluence.com",
        "CONFLUENCE_TOKEN": "your-token"
      }
    }
  }
}
```

**4단계: 실습 시나리오**
1. VS Code에서 Copilot Chat 열기 (`Ctrl+Shift+I`)
2. Agent 모드로 전환
3. Tools 버튼에서 MCP 도구 활성화
4. "Confluence에서 'API 문서' 검색해줘" 요청
5. MCP 서버 자동 호출 과정 관찰

#### **🔍 문제 해결 가이드**
- **MCP 서버가 시작되지 않는 경우**: Python 경로와 패키지 설치 확인
- **VS Code에서 도구가 보이지 않는 경우**: mcp.json 파일 위치와 문법 확인
- **권한 오류**: MCP 서버 신뢰 설정 확인
