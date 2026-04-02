"""
RocketRide AI client — the ONLY AI layer for Project Kindred.

RocketRide runs LLM nodes (OpenAI, Anthropic, Google, etc.) and Whisper
inside visual pipelines. We build .pipe files in the VS Code extension
and call them from Python.

Engine: localhost:5565 (via Docker or VS Code extension).
"""

import json
import base64
from typing import Optional

import httpx


class RocketRideClient:
    """
    Calls the RocketRide engine's REST API to run pipelines.

    Flow:
    1. POST /use  {filepath: "pipeline.pipe"} → get token
    2. POST /send {token, data, contentType}  → get result
    3. POST /terminate {token}                → cleanup
    """

    def __init__(self, uri: str = "http://localhost:5565"):
        self.uri = uri.rstrip("/")
        self.connected = False
        self._http = httpx.AsyncClient(timeout=60.0)

    async def try_connect(self):
        """Ping the RocketRide engine to see if it's running."""
        try:
            resp = await self._http.get(f"{self.uri}/health", timeout=5.0)
            if resp.status_code == 200:
                self.connected = True
                print(f"[RocketRide] Engine connected at {self.uri}")
            else:
                print(f"[RocketRide] Engine returned {resp.status_code}")
        except Exception as e:
            print(f"[RocketRide] Engine not available at {self.uri}: {e}")
            self.connected = False

    async def run_pipeline(
        self,
        pipeline_path: str,
        input_data: str,
        content_type: str = "text/plain",
    ) -> Optional[str]:
        """Load a .pipe file, push data through it, return the output."""
        if not self.connected:
            return None

        try:
            # 1. Load pipeline
            use_resp = await self._http.post(
                f"{self.uri}/use",
                json={"filepath": pipeline_path},
            )
            use_resp.raise_for_status()
            token = use_resp.json().get("token")
            if not token:
                return None

            # 2. Send data through pipeline
            send_resp = await self._http.post(
                f"{self.uri}/send",
                json={"token": token, "data": input_data, "contentType": content_type},
            )
            send_resp.raise_for_status()
            result = send_resp.json()

            # 3. Cleanup
            try:
                await self._http.post(f"{self.uri}/terminate", json={"token": token})
            except Exception:
                pass

            if isinstance(result, dict):
                return result.get("output", result.get("data", json.dumps(result)))
            return str(result)

        except Exception as e:
            print(f"[RocketRide] Pipeline error: {e}")
            return None

    async def transcribe_audio(self, audio_path: str) -> Optional[str]:
        """Send audio through the Whisper pipeline."""
        with open(audio_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        return await self.run_pipeline(
            "./pipelines/kindred_whisper.pipe", b64, "audio/webm"
        )

    async def generate_text(self, system_prompt: str, user_prompt: str) -> Optional[str]:
        """Send prompts through the LLM pipeline."""
        payload = json.dumps({"system": system_prompt, "user": user_prompt})
        return await self.run_pipeline(
            "./pipelines/kindred_llm.pipe", payload, "application/json"
        )

    async def disconnect(self):
        await self._http.aclose()
