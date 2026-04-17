import httpx

from app.core.config import settings
from app.core.exception import BusinessException


class LLMService:
    def chat(self, messages: list[dict[str, str]]) -> str:
        if not settings.LLM_API_KEY:
            raise BusinessException(
                code=50041,
                message="LLM_API_KEY is not configured",
                status_code=500,
            )

        if not settings.LLM_BASE_URL:
            raise BusinessException(
                code=50042,
                message="LLM_BASE_URL is not configured",
                status_code=500,
            )

        if not settings.LLM_MODEL_NAME:
            raise BusinessException(
                code=50043,
                message="LLM_MODEL_NAME is not configured",
                status_code=500,
            )

        url = settings.LLM_BASE_URL.rstrip("/") + "/chat/completions"
        headers = {
            "Authorization": f"Bearer {settings.LLM_API_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": settings.LLM_MODEL_NAME,
            "messages": messages,
            "temperature": 0.7,
        }

        try:
            with httpx.Client(timeout=60.0) as client:
                response = client.post(url, headers=headers, json=payload)
                response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            detail = exc.response.text[:300]
            raise BusinessException(
                code=50241,
                message=f"llm request failed: {detail}",
                status_code=502,
            )
        except httpx.HTTPError as exc:
            raise BusinessException(
                code=50242,
                message=f"llm request error: {exc}",
                status_code=502,
            )

        data = response.json()

        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError):
            raise BusinessException(
                code=50243,
                message="invalid llm response format",
                status_code=502,
            )

        cleaned_content = str(content).strip()
        if not cleaned_content:
            raise BusinessException(
                code=50244,
                message="llm returned empty content",
                status_code=502,
            )

        return cleaned_content


llm_service = LLMService()