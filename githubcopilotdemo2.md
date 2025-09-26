# GitHub Copilot 실습 가이드

이 문서는 GitHub Copilot을 처음 사용해보기 위한 실습용 가이드입니다.  
Python 콘솔 앱을 예시로 Copilot의 주요 기능(자동완성, 주석 기반 코드 생성, 채팅)을 체험합니다.

---

## 1. 샘플 앱 다운로드

먼저 데모용 샘플 앱을 다운로드합니다.

[샘플 앱 다운로드 링크](https://raw.githubusercontent.com/MicrosoftLearning/APL-2007-Accelerate-app-development-by-using-GitHub-Copilot/master/LearnModuleExercises/Downloads/SampleApps.zip)

압축을 해제한 뒤, 원하는 폴더에 저장하세요.

---

## 2. 실습 환경 준비

1. 작업 폴더 생성 후 VS Code에서 엽니다.
2. Python 가상환경을 만들고 활성화합니다.

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

3. `main.py` 파일을 생성하고 아래 코드를 작성합니다.

```python
def main():
    print("Hello, Console App!")

if __name__ == "__main__":
    main()
```

4. 실행 확인:

```powershell
python main.py
```

---

## 3. Copilot 자동완성 실습

1. `main.py` 파일에서 새 함수 정의를 작성해봅니다.
   (아래처럼 입력하고 잠시 기다리면 코드 제안이 출력 됩니다. 뒤에 샘플들도 마찬가지...)

```python
def add(
```

👉 Copilot이 함수 내용을 자동 제안합니다.  
`Tab` 키로 제안을 적용할 수 있습니다.

1. 복잡한 함수 이름을 입력해도 자동완성 제안이 생성됩니다.

```python
def addPrimeNumbersInNumericList(
```

---

## 4. 주석 기반 코드 생성 실습

주석을 작성하면 Copilot이 코드를 제안합니다.

```python
# Create function generate a list of 100 random integers from 1 to 100
```

```python
# Create function sums only the prime numbers between 1 and 100
```

```python
# Write a program that generates an n x n magic square
```

👉 `Tab` 키를 눌러 제안된 코드를 적용하세요.

---

## 5. Copilot Chat 실습

Copilot Chat을 통해 AI와 대화하며 코드 작업을 진행할 수 있습니다.

### 열기 방법

* 상단메뉴 사이드바 Copilot 아이콘 클릭
* 단축키 `Ctrl + Alt + I`
* 편집기 인라인 채팅: `Ctrl + I`

### 채팅열기창에서 모드 선택
함수 하나를 처음부터 끝까지 선택을 하고,,,

- Ask 모드

코드 설명이나 오류 원인을 묻습니다.

```text
선택된 코드에서 is_prime은 무슨 역할을 하나요?
```

- Edit 모드

코드 수정/리팩토링을 요청합니다.

```text
이 함수에 오류 처리를 추가해줘
```

- Agent 모드

여러 단계가 포함된 작업을 요청합니다.(시간 많이 소요)

```text
Write a Python program that creates a list of 100 random integers between 1 and 1000, 
then sort the list, remove duplicates, and print the average of the remaining numbers.
```

---

## 6. 추가 기능 실습

### 인라인 채팅 & 스마트 액션

* 코드 선택 후 `/explain`, `/fix`, `/refactor` 같은 명령을 사용합니다.
* 예시:

```text
/explain #selection
/refactor #selection
```

### Chat Participants

* 대화 범위를 지정할 수 있습니다.

```text
@workspace /explain 모든함수
@terminal 방금 출력된 오류 해결 방법 알려줘
```

### Chat Variables

* 동적 변수 활용 (#selection, #terminal 등)

```text
#selection 코드가 코드 스타일 가이드를 따르고 있는지 확인해주세요.
```

---

## 7. 미니 프로젝트: To-Do 리스트 앱 만들기

Copilot Agent 모드로 간단한 웹 앱을 생성해봅니다.

```text

주제: 간단한 "할 일 목록(To-Do List)" 웹 애플리케이션

1: 프로젝트 시작
python와 Flask를 사용하여 간단한 웹 서버를 만들고, 기본적인 To-Do 리스트 앱의 API 엔드포인트를 정의해주세요.


2: 데이터 저장 기능 추가
To-Do 항목을 추가하고 삭제할 수 있도록 간단한 데이터 저장 기능을 구현해주세요. 로컬 메모리 또는 파일을 활용해 주세요.

3: 프론트엔드 추가
HTML, CSS, JavaScript를 사용하여 간단한 웹 인터페이스를 만들어 주세요. 사용자가 To-Do 항목을 추가하고 삭제할 수 있어야 합니다.

4: 상태 저장 및 개선
할 일 목록이 새로고침해도 유지될 수 있도록, 데이터를 로컬 스토리지 또는 데이터베이스에 저장하는 기능을 추가해주세요.

5: 스타일 및 사용자 경험 개선
Bootstrap 또는 Tailwind CSS를 활용하여 앱의 디자인을 개선하고, 간단한 애니메이션을 추가해 주세요.
```

👉 이후에 프롬프트로 요구사항을 추가하면서 발전시켜 보세요.

```text
디자인을 초등학생에게 맞게 귀엽게 구성해줘.
제목은 "우리 지혜가 할일"로 해줘.
한국어/영어/일본어 다국어 지원 추가해줘.
```

---

## 마무리

이 실습을 통해 Copilot의 주요 기능인:

* **자동완성 제안**
* **주석 기반 코드 생성**
* **Copilot Chat (Ask, Edit, Agent 모드)**

을 직접 체험할 수 있습니다.
