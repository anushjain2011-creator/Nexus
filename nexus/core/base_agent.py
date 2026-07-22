
"""
BaseAgent — the shared contract every Nexus agent implements.

Design goals:
  - Every agent gets read access to the WorldModel's summary automatically,
    so agents share situational awareness without extra plumbing.
  - Agents can publish events (e.g. 'risk.detected') so other agents can
    react — this is what creates cascading behavior across the system.
  - Calling the LLM is centralized here so agent subclasses stay thin:
    they mostly define a system prompt, a set of tools, and how to apply
    the model's output back onto the WorldModel.

LLM backend: uses the OpenAI-compatible chat.completions API, so it works
with OpenAI itself, Featherless.ai, or any other OpenAI-compatible host —
configured entirely through env vars (see .env.example):
    OPENAI_API_KEY
    OPENAI_BASE_URL   (omit for real OpenAI, set for Featherless etc.)
    OPENAI_MODEL      (defaults to gpt-4o-mini if unset)
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from typing import Any, Optional

from nexus.core.world_model import WorldModel
from nexus.core.event_bus import EventBus
from pathlib import Path

from nexus.skills import SkillManager
from nexus.memory.manager import memory_manager
from nexus.tools import tool_manager

DEFAULT_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")


@dataclass
class AgentResponse:
    """Normalized result returned by every agent run, regardless of what
    the agent internally did."""
    agent_name: str
    summary: str
    raw_text: str = ""
    tool_calls: list[dict[str, Any]] = field(default_factory=list)
    data: dict[str, Any] = field(default_factory=dict)


def _to_openai_tool(tool: dict[str, Any]) -> dict[str, Any]:
    """Convert our Anthropic-style tool schema
    ({name, description, input_schema}) into OpenAI's function-calling
    format ({type: 'function', function: {name, description, parameters}}).
    Keeping our own tools() definitions in the simpler shape means agent
    subclasses don't need to know which backend is in use."""
    return {
        "type": "function",
        "function": {
            "name": tool["name"],
            "description": tool.get("description", ""),
            "parameters": tool.get("input_schema", {"type": "object", "properties": {}}),
        },
    }


class BaseAgent:
    """Subclass this for each specialized agent (Research, Planning,
    Finance, Risk, ...). Subclasses typically override:
      - name / description
      - system_prompt()
      - tools() if the agent exposes tool-use functions
      - handle_tool_call() if it defines tools
      - run() only if the default single-turn flow isn't enough
    """

    name: str = "base_agent"
    description: str = "Generic Nexus agent."

   def __init__(
    self,
    runtime,
    model: Optional[str] = None,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> None:
self.runtime = runtime

self.world = runtime.world
self.bus = runtime.bus
self.memory = runtime.memory
self.skills = runtime.skills
self.tool_manager = runtime.tools
self.agent_registry = runtime.registry

self.model = model or DEFAULT_MODEL

        from openai import OpenAI  # imported lazily so core/world_model
                                    # usage doesn't require the SDK installed

        self.client = OpenAI(
            api_key=api_key or os.environ.get("OPENAI_API_KEY"),
            base_url=base_url or os.environ.get("OPENAI_BASE_URL"),
        )
self.skills = SkillManager(
            llm=self,
        )

        self.skills.load(
            Path(__file__).parent.parent
            / "skills"
            / "definitions"
        )

        self.memory = memory_manager

        self.tool_manager = tool_manager

        self.agent_registry = None
    # ---- override in subclasses -------------------------------------------------

    def system_prompt(self) -> str:
        """The agent's role and how it should behave. Subclasses should
        override this; base version is intentionally generic."""
        return (
            f"You are the {self.name} inside Nexus, an execution operating "
            f"system that turns human goals into coordinated action. "
            f"{self.description}\n\n"
            f"Current project state:\n{self.world.summary_for_prompt()}"
        )

    def tools(self) -> list[dict[str, Any]]:
        """Tool definitions this agent can call, in Anthropic-style shape
        ({name, description, input_schema}). Translated to whatever the
        active backend needs at call time. Empty by default."""
        return []

    def handle_tool_call(self, tool_name: str, tool_input: dict[str, Any]) -> Any:
        """Execute a tool call the model requested. Subclasses with tools()
        must override this to actually mutate the WorldModel."""
        raise NotImplementedError(
            f"{self.name} declared tools but did not implement handle_tool_call"
        )

    # ---- shared execution flow -------------------------------------------------
def generate(
        self,
        prompt: str,
    ) -> str:

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": self.system_prompt(),
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            max_tokens=1500,
        )

        return response.choices[0].message.content or ""
    def run(self, instruction: str, max_tool_turns: int = 5) -> AgentResponse:
        """Send `instruction` to the model with this agent's system prompt
        and tools, looping through any tool calls until the model produces
        a final text answer."""
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": self.system_prompt()},
            {"role": "user", "content": instruction},
        ]
        tool_calls_made: list[dict[str, Any]] = []
        openai_tools = [_to_openai_tool(t) for t in self.tools()]

        for _ in range(max_tool_turns):
            response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=1500,
                messages=messages,
                tools=openai_tools or None,
            )

            choice = response.choices[0].message
            requested_calls = choice.tool_calls or []

            if not requested_calls:
                final_text = choice.content or ""
                return AgentResponse(
                    agent_name=self.name,
                    summary=final_text,
                    raw_text=final_text,
                    tool_calls=tool_calls_made,
                )

            messages.append({
                "role": "assistant",
                "content": choice.content,
                "tool_calls": [
                    {
                        "id": call.id,
                        "type": "function",
                        "function": {
                            "name": call.function.name,
                            "arguments": call.function.arguments,
                        },
                    }
                    for call in requested_calls
                ],
            })

            for call in requested_calls:
                try:
                    tool_input = json.loads(call.function.arguments or "{}")
                except json.JSONDecodeError:
                    tool_input = {}

                result = self.handle_tool_call(call.function.name, tool_input)
                tool_calls_made.append({
                    "tool": call.function.name,
                    "input": tool_input,
                    "result": result,
                })
                if self.bus:
                    self.bus.publish(f"{self.name}.tool_used",
                                      tool=call.function.name, input=tool_input)

                messages.append({
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": json.dumps(result, default=str),
                })

        return AgentResponse(
            agent_name=self.name,
            summary="Max tool turns reached without a final answer.",
            tool_calls=tool_calls_made,
        )
    def run_skill(
        self,
        name: str,
        **kwargs,
    ):

        return self.skills.execute(
            name,
            **kwargs,
        )


    def use_tool(
        self,
        name: str,
        **kwargs,
    ):

        return self.tool_manager.execute(
            name,
            **kwargs,
        )


    def remember(
        self,
        text: str,
        metadata: dict | None = None,
    ):

        return self.memory.store(
            text=text,
            metadata=metadata or {},
        )


    def recall(
        self,
        query: str,
        limit: int = 5,
    ):

        return self.memory.search(
            query=query,
            limit=limit,
        )


    def set_agent_registry(
        self,
        registry,
    ):

        self.agent_registry = registry


    def ask_agent(
        self,
        agent_name: str,
        instruction: str,
    ):

        if self.agent_registry is None:

            raise RuntimeError(
                "No Agent Registry configured."
            )

        agent = self.agent_registry.get(
            agent_name,
        )

        if agent is None:

            raise ValueError(
                f"Unknown agent '{agent_name}'."
            )

        return agent.run(
            instruction,
        )


    def publish_event(
        self,
        event: str,
        **payload,
    ):

        if self.bus:

            self.bus.publish(
                event,
                **payload,
            )


    def capabilities(
        self,
    ):

        return {
            "agent": self.name,
            "skills": len(
                self.skills.all()
            ),
            "tools": len(
                self.tool_manager.all()
            ),
            "memory": True,
            "collaboration": self.agent_registry is not None,
        }
