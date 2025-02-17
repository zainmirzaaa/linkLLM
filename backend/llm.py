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
