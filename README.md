# ExamCraft — AI Assessment Copilot

강의자료 기반 평가문항 생성 서비스를 만드는 12주 학습 프로젝트입니다.

## 현재 구현
- Day 1: LLM Gateway를 통한 첫 LLM 호출
- Day 2: CLI 반복 입력, 빈 입력 처리, 종료 명령
- 토큰 사용량과 비용 출력
- Day 3: 대화 기록 유지, reset으로 초기화.

## 실행 환경
- Python 3.14.7
- LLM Gateway
- 모델: gpt-5-nano

## 실행 방법
- 가상환경 생성 및 requirements.txt 패키지 설치
- LLM_GATEWAY_API_KEY 설정
- 실행 명령: 직접 작성

## 현재 구조
사용자 → CLI → ask_llm() → LLM Gateway → 답변 출력

실행 중 사용자 질문과 AI 답변을 메모리에 저장하고 다음 요청에 함께 전달합니다. reset을 입력하면 system 메시지만 남기고 대화를 초기화합니다. 프로그램 종료 시 기록은 사라집니다.

## 해결한 문제
응답 전체를 변환할 때 metadata 타입 불일치 경고가 발생했다.
사용량 객체만 변환하도록 수정해 해결했다.

## 다음 작업
프롬프트 개선과 API 실패 처리