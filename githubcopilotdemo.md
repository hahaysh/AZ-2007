# GitHub Copilot 시작하기 - 실습 가이드

이 문서는 GitHub Copilot을 처음 사용하기 위한 **준비 과정**을 단계별로 정리한 가이드입니다.  
아래 순서를 따라하면, 바로 Visual Studio Code에서 Copilot 기능을 활용할 수 있습니다.  

---

## 1. 필수 도구 설치

1. **Git 설치**
   - [Git 공식 다운로드](https://git-scm.com/downloads) 페이지에서 운영체제에 맞는 설치 파일을 다운로드하고 설치하세요.
   - 설치 완료 후, 터미널(또는 PowerShell)에서 아래 명령어로 설치 여부를 확인합니다.
     ```bash
     git --version
     ```

2. **Python 설치**
   - [Python 공식 다운로드](https://www.python.org/downloads/) 페이지에서 최신 버전을 설치하세요.
   - 설치 시 `Add Python to PATH` 옵션을 반드시 체크하세요.
   - 설치 확인:
     ```bash
     python --version
     ```

3. **Visual Studio Code 설치**
   - [VS Code 공식 다운로드](https://code.visualstudio.com/) 페이지에서 설치하세요.

---

## 2. GitHub Copilot 확장 설치

1. VS Code 실행 후, 좌측 **Extensions(확장 프로그램)** 메뉴로 이동합니다.
2. 아래 확장을 검색하여 설치합니다.
   - **GitHub Copilot**
   - **GitHub Copilot Chat**
3. 설치 후 **GitHub 계정으로 로그인**합니다.

---

## 3. GitHub Copilot 구독 준비

Copilot을 사용하려면 **활성화된 구독**이 필요합니다. 방법은 두 가지입니다:

- **개인 계정 구독**
  - [GitHub Copilot Pro](https://github.com/features/copilot) (월간/연간 결제)
  - 또는 30일 무료 체험판 사용 가능
- **조직 계정 구독**
  - 조직에서 Copilot 라이선스를 할당받아 사용 가능

---

## 4. Copilot 설정하기

Copilot은 **GitHub.com**과 **Visual Studio Code**에서 각각 설정할 수 있습니다.

1. **Visual Studio Code에서**
   - 상단 메뉴 → 오른쪽 화살표 아이콘 클릭 → **코드 완성 구성** 메뉴 선택
   - 언어별로 Copilot 사용 여부를 켜거나 끌 수 있습니다.

2. **GitHub.com에서**
   - 계정 → **Settings → Copilot** 메뉴 이동
   - 구독 관리 및 조직/개인 설정 변경 가능

---

## 5. 준비 완료

이제 모든 준비가 끝났습니다! 🎉  
이제 VS Code에서 파일을 열고 코드를 작성하면, Copilot이 자동으로 제안해주는 코드를 경험할 수 있습니다.  

> 팁: `Ctrl + Enter` (Windows/Linux) 또는 `Cmd + Enter` (Mac)를 누르면 Copilot이 코드 제안을 보여줍니다.
