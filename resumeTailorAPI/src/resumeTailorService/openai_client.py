import os
from typing import Optional

from openai import AsyncOpenAI


class OpenAIClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
    ) -> None:
        resolved_api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not resolved_api_key:
            raise ValueError("OPENAI_API_KEY is not set")

        self._client = AsyncOpenAI(api_key=resolved_api_key)
        self._model = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")

        temperature_raw = os.getenv("OPENAI_TEMPERATURE", "0.2")
        try:
            self._temperature = float(temperature_raw)
        except ValueError as exc:
            raise ValueError(f"Invalid OPENAI_TEMPERATURE: {temperature_raw}") from exc

        max_tokens_raw = os.getenv("OPENAI_MAX_TOKENS")
        self._max_tokens: Optional[int]
        if max_tokens_raw is None or max_tokens_raw.strip() == "":
            self._max_tokens = None
        else:
            try:
                self._max_tokens = int(max_tokens_raw)
            except ValueError as exc:
                raise ValueError(f"Invalid OPENAI_MAX_TOKENS: {max_tokens_raw}") from exc

    async def tailor_resume(self, prompt: str) -> str:
        if not prompt or not prompt.strip():
            raise ValueError("Prompt is empty")

        try:
            resp = await self._client.chat.completions.create(
                model=self._model,
                messages=[{"role": "user", "content": prompt}],
                temperature=self._temperature,
                max_tokens=self._max_tokens,
            )
        except Exception as exc:
            raise RuntimeError(f"OpenAI request failed: {exc}") from exc

        content = resp.choices[0].message.content if resp.choices else None
        return (content or "").strip()
