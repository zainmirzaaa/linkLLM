import os
import openai

OPENAI_API_KEY = os.getenv()
openai.api_key = OPENAI_API_KEY

async def query_openai(prompt: str) -> str:
    if not OPENAI_API_KEY:
        return "[LLM disabled: missing OPENAI_API_KEY]"
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        return resp.choices[0].message["content"]
    except Exception as e:
        return f"[LLM error: {e}]"
    

async def rephrase_query(q: str) -> str:
    prompt = (
        "Rephrase the following Stack Overflow search query to be concise and specific:\n"
        f"Query: {q}\nRephrased:"
    )
    answer = await query_openai(prompt)
    return answer.strip()


def _truncate(text: str, max_tokens: int = 800) -> str:
    # naive truncation; good enough for a small commit
    return text[: max_tokens * 4]  # ~4 chars per token rough

async def safe_query(prompt: str) -> str:
    return await query_openai(_truncate(prompt))


