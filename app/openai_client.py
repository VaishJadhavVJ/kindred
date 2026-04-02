import os
import json
from typing import Optional
from openai import AsyncOpenAI

class OpenAIClient:
    """Fallback client for OpenAI API to use when RocketRide is offline."""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if self.api_key:
            self.client = AsyncOpenAI(api_key=self.api_key)
        else:
            self.client = None

    async def generate_text(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        """Fallback LLM generation using gpt-4o."""
        if not self.client:
            print("[OpenAI Fallback] No OPENAI_API_KEY set.")
            return None
            
        try:
            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={ "type": "json_object" } if "JSON" in system_prompt else None
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"[OpenAI Fallback] Generation error: {e}")
            return None

    async def transcribe_audio(self, audio_path: str) -> Optional[str]:
        """Fallback Whisper transcription."""
        if not self.client:
            print("[OpenAI Fallback] No OPENAI_API_KEY set.")
            return None
            
        try:
            with open(audio_path, "rb") as audio_file:
                transcript = await self.client.audio.transcriptions.create(
                    model="whisper-1", 
                    file=audio_file
                )
            return transcript.text
        except Exception as e:
            print(f"[OpenAI Fallback] Transcription error: {e}")
            return None
