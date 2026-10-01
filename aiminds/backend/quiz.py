"""LLM-based MCQ generation, grounded ONLY in retrieved chunks (this is the 'G' in RAG)."""
import json, os
import anthropic

client = anthropic.Anthropic()            # reads ANTHROPIC_API_KEY from the environment
MODEL = os.getenv("LLM_MODEL", "claude-sonnet-5-5")

def make_mcqs(context: str, n: int = 5) -> list[dict]:
    prompt = f"""Using ONLY the material below, write {n} multiple-choice questions for statistical officers.
Return ONLY a JSON list. Each item: {{"q": str, "options": [4 strings], "answer": index 0-3, "explanation": str}}.

Material:
{context}"""
    msg = client.messages.create(model=MODEL, max_tokens=2000, messages=[{"role": "user", "content": prompt}])
    text = msg.content[0].text
    items = json.loads(text[text.index("["): text.rindex("]") + 1])
    # validate: model output is untrusted, so check the shape before using it
    return [m for m in items if len(m.get("options", [])) == 4 and m.get("answer") in range(4)]
