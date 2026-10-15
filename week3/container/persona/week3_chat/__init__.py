"""A single-turn, tool-free Jupyter AI persona for the Goal zero checkpoint."""

import json
import os
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlsplit

import httpx
from jupyter_ai_persona_manager import BasePersona, PersonaDefaults
from openai import APIConnectionError, APIStatusError, APITimeoutError, AsyncOpenAI

SYSTEM_PROMPT = (
    "Explain the supplied Python in at most three sentences for a beginner. "
    "You have no notebook tools. Do not claim to have read, edited, or run a notebook."
)
LOCKED = "Provider access is disabled. Use the static companion, or explicitly approve the live launch."


@dataclass
class Answer:
    text: str
    trace: dict | None = None


def model_settings():
    """Accept the selected local Ollama endpoint; never read provider credentials."""
    base = os.environ.get("DEMO_API_BASE", "http://host.docker.internal:11434/v1/")
    url = urlsplit(base)
    if (url.scheme != "http" or url.hostname not in {"host.docker.internal", "127.0.0.1"}
            or url.port != 11434 or url.path != "/v1/"
            or url.username or url.password or url.query or url.fragment):
        raise ValueError("Use the reviewed local Ollama endpoint.")
    model = os.environ.get("DEMO_MODEL", "gpt-oss:20b")
    if model != "gpt-oss:20b":
        raise ValueError("A different model requires a new compatibility review.")
    return base, model


async def ask_model(text):
    # No health/model-discovery call is made when access is disabled.
    if os.environ.get("DEMO_PROVIDER_APPROVED") != "yes":
        return Answer(LOCKED)
    base, model = model_settings()
    # The SDK requires a nonempty key. This constant is NOT a provider secret.
    # Ignore inherited proxy variables, disable retries, and do not log bodies.
    async with AsyncOpenAI(
        base_url=base, api_key="teaching-no-secret", max_retries=0, timeout=60,
        http_client=httpx.AsyncClient(trust_env=False, timeout=60),
    ) as client:
        result = await client.chat.completions.create(
            model=model, stream=False,
            messages=[{"role": "system", "content": SYSTEM_PROMPT},
                      {"role": "user", "content": text}],
        )
    reply = result.choices[0].message
    trace = {
        "request": {"method": "POST", "path": "/v1/chat/completions",
                    "model": model, "stream": False,
                    "messages": [{"role": "system", "content": "<redacted>"},
                                 {"role": "user", "content": "<redacted>"}]},
        "response": {"choices": [{"message": {
            "role": "assistant", "content": "<redacted>" if reply.content else None,
            "tool_calls_returned": bool(reply.tool_calls),
        }}]},
        "note": "Content omitted by construction; no tools were supplied or dispatched.",
    }
    if reply.tool_calls or not reply.content:
        return Answer("No text-only answer was returned. No action was performed.", trace)
    return Answer(reply.content, trace)


class ModelChatPersona(BasePersona):
    @property
    def defaults(self):
        return PersonaDefaults(
            name="Model chat (no tools)",
            description="One message to the instructor's local model service; no tool loop.",
            avatar_path=str(Path(__file__).with_name("avatar.svg")),
            system_prompt=SYSTEM_PROMPT,
            slash_commands=set(),
        )

    async def process_message(self, message):
        # Deliberately no history, attachments, tool discovery or tool dispatch.
        try:
            answer = await ask_model(message.body)
            self.send_message(answer.text)
            if answer.trace:
                self.send_message("API exchange summary (content redacted):\n```json\n" + json.dumps(answer.trace, indent=2) + "\n```")
        except APITimeoutError:
            self.send_message("Model request failed: timed out waiting for local Ollama. Check that the model is available and retry when ready.")
        except APIConnectionError:
            self.send_message("Model request failed: could not connect to local Ollama. Run bash week3/demo.sh reachability from the repository root.")
        except APIStatusError as exc:
            # Report only the numeric status, never the body or exception text.
            self.send_message(f"Model request failed: local Ollama returned HTTP {exc.status_code}. Check the model name and local service. Details were not recorded.")
        except Exception:
            # Provider error bodies and tracebacks may contain private content.
            self.send_message("Model request failed. Check local reachability and the validation guide; details were not recorded.")

    async def handle_uncaught_exception(self, exc):
        self.send_message("Chat failed. Details were not recorded. Restart the demonstration.")
