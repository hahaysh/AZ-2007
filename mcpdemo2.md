# 🚀 MCP 입문자를 위한 30분 실습 가이드

**"MCP의 핵심을 빠르게 이해하고 체험하기"**

---

## ⏰ 실습 개요

**목표**: MCP가 무엇인지, 어떻게 동작하는지 30분 안에 체험하기  
**대상**: MCP를 처음 접하는 개발자  
**완료 시간**: 30분  
**준비물**: VS Code, Python 3.8+

---

## 🛠 사전 준비 (5분)

### 1. 필수 소프트웨어 확인
```bash
# 버전 확인
code --version    # VS Code 1.102+ 필요
python --version  # Python 3.8+ 필요
```

### 2. 작업 폴더 생성
```bash
mkdir mcp-30min-lab
cd mcp-30min-lab
```

---

## Part 1: 첫 번째 MCP 서버 만들기 (10분)

### Step 1: 간단한 Python MCP 서버 생성

`simple_mcp.py` 파일 생성:

```python
#!/usr/bin/env python3
import json
import sys

def handle_request(request):
    """MCP 요청 처리"""
    method = request.get("method")
    
    if method == "tools/list":
        # 사용 가능한 도구 목록 반환
        return {
            "tools": [
                {
                    "name": "hello",
                    "description": "인사말을 생성합니다",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"}
                        }
                    }
                }
            ]
        }
    
    elif method == "tools/call":
        # 도구 실행
        tool_name = request.get("params", {}).get("name")
        arguments = request.get("params", {}).get("arguments", {})
        
        if tool_name == "hello":
            name = arguments.get("name", "익명")
            message = f"안녕하세요, {name}님! 🐍 Python MCP 서버에서 인사드립니다!"
            return {
                "content": [{"type": "text", "text": message}]
            }
    
    return {"error": "Unknown method"}

# 메인 루프
if __name__ == "__main__":
    print("🐍 Simple Python MCP 서버가 시작되었습니다!", file=sys.stderr)
    
    for line in sys.stdin:
        try:
            request = json.loads(line.strip())
            response = handle_request(request)
            print(json.dumps(response))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.stdout.flush()
```

### Step 2: VS Code에서 MCP 서버 설정

`.vscode/mcp.json` 파일 생성:

```json
{
  "servers": {
    "simple-python": {
      "command": "python",
      "args": ["simple_mcp.py"]
    }
  }
}
```

### Step 3: 첫 번째 테스트

1. VS Code에서 `Ctrl+Shift+P` → **"MCP: Restart Servers"**
2. **"Trust"** 클릭 (신뢰 확인)
3. `Ctrl+Alt+I` → 채팅 창 열기
4. 드롭다운에서 **"Agent"** 모드 선택
5. **"Tools"** 버튼 클릭 → `hello` 도구 확인

**테스트 명령**:
```
"김개발"이라는 이름으로 인사해줘
```

**✅ 체크포인트**: AI가 `hello` 도구를 사용해서 인사말을 생성했나요?

---

## Part 2: Confluence 연동하기 (10분)

### Step 1: Confluence 설정

`.env` 파일 생성:
```bash
# 본인의 Confluence 정보로 변경
CONFLUENCE_URL=https://your-domain.atlassian.net
CONFLUENCE_EMAIL=your-email@company.com
CONFLUENCE_TOKEN=your-api-token
```

### Step 2: Confluence MCP 서버 생성

`confluence_mcp.py` 파일 생성:

```python
#!/usr/bin/env python3
import json
import sys
import os
import requests
import base64
from dotenv import load_dotenv

load_dotenv()

class ConfluenceClient:
    def __init__(self):
        self.base_url = os.getenv('CONFLUENCE_URL')
        self.email = os.getenv('CONFLUENCE_EMAIL')
        self.token = os.getenv('CONFLUENCE_TOKEN')
        
        if not all([self.base_url, self.email, self.token]):
            print("⚠️ .env 파일에 Confluence 설정을 확인하세요", file=sys.stderr)
            return
        
        # 인증 헤더 생성
        auth_string = f"{self.email}:{self.token}"
        auth_bytes = base64.b64encode(auth_string.encode()).decode()
        
        self.headers = {
            'Authorization': f'Basic {auth_bytes}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
    
    def search_pages(self, query):
        """페이지 검색"""
        try:
            url = f"{self.base_url}/wiki/rest/api/content/search"
            params = {'cql': f'text ~ "{query}"', 'limit': 5}
            
            response = requests.get(url, headers=self.headers, params=params)
            if response.status_code == 200:
                results = response.json().get('results', [])
                return [{'title': r.get('title'), 'id': r.get('id')} for r in results]
            else:
                return f"검색 실패: {response.status_code}"
        except Exception as e:
            return f"오류: {str(e)}"

confluence = ConfluenceClient()

def handle_request(request):
    method = request.get("method")
    
    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "confluence_search",
                    "description": "Confluence에서 페이지를 검색합니다",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "query": {"type": "string"}
                        }
                    }
                }
            ]
        }
    
    elif method == "tools/call":
        tool_name = request.get("params", {}).get("name")
        arguments = request.get("params", {}).get("arguments", {})
        
        if tool_name == "confluence_search":
            query = arguments.get("query", "")
            results = confluence.search_pages(query)
            return {
                "content": [{"type": "text", "text": f"🔍 '{query}' 검색 결과:\n{json.dumps(results, ensure_ascii=False, indent=2)}"}]
            }
    
    return {"error": "Unknown method"}

if __name__ == "__main__":
    print("🏢 Confluence MCP 서버가 시작되었습니다!", file=sys.stderr)
    
    for line in sys.stdin:
        try:
            request = json.loads(line.strip())
            response = handle_request(request)
            print(json.dumps(response))
            sys.stdout.flush()
        except Exception as e:
            print(json.dumps({"error": str(e)}))
            sys.stdout.flush()
```

### Step 3: 필요한 패키지 설치

```bash
pip install requests python-dotenv
```

### Step 4: VS Code 설정 업데이트

`.vscode/mcp.json` 업데이트:

```json
{
  "servers": {
    "simple-python": {
      "command": "python",
      "args": ["simple_mcp.py"]
    },
    "confluence": {
      "command": "python",
      "args": ["confluence_mcp.py"]
    }
  }
}
```

### Step 5: Confluence 테스트

1. `Ctrl+Shift+P` → **"MCP: Restart Servers"**
2. Agent 모드에서 **"Tools"** → `confluence_search` 도구 확인

**테스트 명령**:
```
Confluence에서 "API" 관련 페이지를 찾아줘
```

**✅ 체크포인트**: Confluence에서 실제 페이지를 검색해서 결과를 보여주나요?

---

## Part 3: 통합 시나리오 체험 (5분)

### 실제 업무 시나리오 테스트

다음 명령을 차례로 실행해보세요:

**시나리오 1: 인사 + 검색**
```
"홍길동"으로 인사하고, Confluence에서 "프로젝트" 관련 문서도 찾아줘
```

**시나리오 2: 복합 작업**
```
먼저 "팀장님"께 인사드리고, 회의록이나 보고서 관련 Confluence 페이지를 검색해줘
```

**✅ 최종 체크포인트**: AI가 여러 MCP 도구를 조합해서 작업을 수행하나요?

---

## 🎯 학습 완료! 

### 🎉 축하합니다! 30분 만에 다음을 경험했습니다:

✅ **MCP 서버 직접 구현** - Python으로 간단한 MCP 서버 만들기  
✅ **VS Code 연동** - MCP 서버를 VS Code에 등록하고 사용  
✅ **외부 시스템 연결** - Confluence API와 MCP를 통한 데이터 조회  
✅ **AI 도구 체험** - Agent가 MCP 도구들을 자동으로 조합해서 작업 수행  

### 🔑 핵심 개념 정리

**MCP = AI와 외부 시스템을 연결하는 표준 다리**

1. **MCP 서버**: 외부 시스템(Confluence, GitHub 등)과 연결된 도구들을 제공
2. **MCP 클라이언트**: VS Code가 AI 대신 MCP 서버에 요청을 보냄  
3. **도구 조합**: AI가 여러 MCP 도구를 자동으로 선택하고 조합해서 복잡한 작업 수행

### 🚀 다음 단계

**더 배우고 싶다면:**
- GitHub MCP 서버 연동해보기
- 파일 시스템 MCP 서버 추가하기  
- 나만의 커스텀 MCP 도구 만들기

**실무에 적용하려면:**
- 회사 내부 API를 MCP 서버로 만들기
- 자주 하는 반복 작업을 MCP 도구로 자동화
- 팀 워크플로우에 MCP 통합하기

---

## 🔧 문제해결

### 자주 발생하는 문제들

**1. MCP 서버가 시작되지 않음**
- Python 경로 확인: `which python`
- 권한 확인: `python simple_mcp.py` 직접 실행

**2. Confluence 연결 안됨**  
- `.env` 파일 내용 확인
- API 토큰 권한 확인

**3. 도구가 호출되지 않음**
- Agent 모드인지 확인
- Tools에서 도구가 선택되어 있는지 확인
