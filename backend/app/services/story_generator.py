import json
import re

from app.services.llm.base import BaseLLMProvider

SYSTEM_PROMPT = """You are an expert business analyst and agile coach. Your task is to analyze a requirements document and generate well-structured user stories following the standard format.

For each user story produce:
- title: a concise summary (max 10 words)
- description: the full story in format "As a [role], I want [goal], so that [benefit]"
- acceptance_criteria: a JSON array of strings, one testable criterion per item (e.g. ["Given valid credentials, the user is logged in.", "An error message is shown for invalid input."])
- priority: one of "critical", "high", "medium", "low"
- story_points: estimated effort (Fibonacci: 1, 2, 3, 5, 8, 13)

Return ONLY valid JSON — an array of story objects with those exact keys. No markdown fences, no extra commentary."""


USER_PROMPT_TEMPLATE = """Analyze the following requirements document and generate user stories:

---
{document_content}
---

Generate comprehensive user stories that cover all the requirements. Return a JSON array."""


def _normalise_acceptance_criteria(value: object) -> str | None:
    """
    Normalise the acceptance_criteria field from whatever the LLM returns
    into a newline-separated string of bullet items.

    Handles:
      - list  → join items, one per line
      - str   → split on common delimiters (newline, "1.", "- ") then join
      - other → None
    """
    if not value:
        return None

    if isinstance(value, list):
        items = [str(item).strip().lstrip("-•*").strip() for item in value if str(item).strip()]
        return "\n".join(items)

    if isinstance(value, str):
        text = value.strip()
        # Split on newlines first
        lines = [l.strip() for l in re.split(r"\n+", text) if l.strip()]
        # Strip leading numbering ("1.", "2.") or bullet chars
        cleaned = [re.sub(r"^[\d]+[.)]\s*|^[-•*]\s*", "", l) for l in lines]
        return "\n".join(c for c in cleaned if c)

    return None


async def generate_stories(document_content: str, provider: BaseLLMProvider) -> list[dict]:
    """Call the LLM and return a list of story dicts."""
    user_prompt = USER_PROMPT_TEMPLATE.format(document_content=document_content[:12000])
    raw = await provider.complete(SYSTEM_PROMPT, user_prompt)

    # Strip possible markdown fences in case the model includes them
    raw = re.sub(r"```(?:json)?", "", raw).strip().rstrip("`").strip()

    try:
        stories = json.loads(raw)
    except json.JSONDecodeError:
        # Attempt to extract the first JSON array from the response
        match = re.search(r"\[.*\]", raw, re.DOTALL)
        if not match:
            raise ValueError(f"LLM did not return valid JSON. Response: {raw[:500]}")
        stories = json.loads(match.group())

    if not isinstance(stories, list):
        raise ValueError("Expected a JSON array of stories")

    # Normalise acceptance_criteria regardless of what format the LLM chose
    for story in stories:
        story["acceptance_criteria"] = _normalise_acceptance_criteria(
            story.get("acceptance_criteria")
        )

    return stories
