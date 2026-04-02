import os
import logging

logger = logging.getLogger(__name__)

class OpenAIClient:
    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY", "")
        self.client = None
        if api_key:
            try:
                from openai import AsyncOpenAI
                self.client = AsyncOpenAI(api_key=api_key)
                logger.info("OpenAI client initialized.")
            except Exception:
                self.client = None

    async def generate_text(self, system_prompt: str, user_prompt: str) -> str:
        if not self.client:
            return ""
        try:
            resp = await self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.8,
                max_tokens=800,
            )
            return resp.choices[0].message.content or ""
        except Exception as e:
            logger.error(f"OpenAI fallback failed: {e}")
            return ""

    async def transcribe_audio(self, audio_path: str) -> str:
        if not self.client:
            return ""
        try:
            with open(audio_path, "rb") as f:
                transcript = await self.client.audio.transcriptions.create(
                    model="whisper-1", file=f
                )
            return transcript.text
        except Exception as e:
            logger.error(f"OpenAI transcription failed: {e}")
            return ""
