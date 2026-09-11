import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.environ["LLM_GATEWAY_API_KEY"],
    base_url="https://api.llmgateway.io/v1",
)


def ask_llm(question: str) -> str:
    response = client.chat.completions.create(
        model="gpt-5-nano", #gpt-5.6-luna로 추후 변경
        reasoning_effort="minimal", #추론설정
        messages=[
            {
                "role": "user",
                "content": question,
            }
        ],
    )

    # LLMGateway의 확장 usage 필드까지 dict로 꺼냄
    data = response.model_dump()
    usage = data.get("usage") or {}

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
    answer = ask_llm("""
      고등학교 물리학 수준의 객관식 문제 10개를 만들어 줘.

      조건:
      - 주제: 뉴턴 운동 법칙
      - 각 문제는 5지선다형
      - 정답은 하나만 존재해야 함
      - 각 문제마다 정답 번호를 표시
      - 각 문제마다 2~3문장의 해설 작성
      - 문제끼리 최대한 중복되지 않게 작성
    """) #여러줄 문자열
    print(answer)