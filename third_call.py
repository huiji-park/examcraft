import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.environ["LLM_GATEWAY_API_KEY"],
    base_url="https://api.llmgateway.io/v1",
)


def ask_llm(question: list[dict[str, str]]) -> str:
    response = client.chat.completions.create(
        model="gpt-5-nano", #gpt-5.6-luna로 추후 변경
        reasoning_effort="minimal", #추론설정
        messages=messages,
    )

    # LLMGateway의 확장 usage 필드까지 dict로 꺼냄
    usage = response.usage.model_dump() if response.usage is not None else {}

    prompt_tokens = usage.get("prompt_tokens", 0)
    completion_tokens = usage.get("completion_tokens", 0)
    total_tokens = usage.get("total_tokens", 0)

    completion_details = usage.get("completion_tokens_details") or {}
    reasoning_tokens = completion_details.get("reasoning_tokens", 0)

    cost = usage.get("cost")
    cost_details = usage.get("cost_details") or {}

    input_cost = cost_details.get("input_cost")
    output_cost = cost_details.get("output_cost")
    cached_input_cost = cost_details.get("cached_input_cost")

    print("\n==========사용량============")
    print(f"입력 토큰 : {prompt_tokens}")
    print(f"출력 토큰 :  {completion_tokens}")
    print(f"추론 토큰 : {reasoning_tokens}")
    print(f"총 토큰 : {total_tokens}")

    if cost is not None:
        print(f"총 비용 : ${cost:.8f}")
    else:
        print("총 비용 : 정보 없음")

    if input_cost is not None:
        print(f"입력 비용 : ${input_cost:.8f}")

    if output_cost is not None:
        print(f"출력 비용 : ${output_cost:.8f}")

    if cached_input_cost is not None:
        print(f"캐시 입력 비용 : ${cached_input_cost:.8f}")

    print("========================\n")

    return response.choices[0].message.content or ""

if __name__ == "__main__":
    messages = [
        {
            "role": "system",
            "content": "너는 한국어로 명확하게 설명하는 학습 보조자야."
        }
    ]
    print("ExamCraft CLI — 종료: exit / 새 대화: reset")

    while True:
        question = input("\n질문: ").strip()

        if question.lower() == "exit":
            print("\n프로그램을 종료합니다.")
            break

        if question.lower() == "reset":
            messages = messages[:1]
            print("\n새 대화를 시작합니다.")
            continue

        if not question:
            print("질문을 입력하세요.")
            continue

        messages.append({
            "role": "user",
            "content": question
        })

        answer = ask_llm(messages)
        print(answer)

        messages.append({
            "role": "assistant",
            "content": answer
        })