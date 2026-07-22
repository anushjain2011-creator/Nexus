"""
SecurityAgent — "Is the project secure?"

Responsible for protecting project assets, enforcing access
control, monitoring security risks, safeguarding sensitive
information, and ensuring security best practices are followed
throughout the project lifecycle.
"""

from __future__ import annotations

from typing import Optional

from nexus.core.base_agent import BaseAgent, AgentResponse
from nexus.core.event_bus import EventBus
from nexus.core.registry import register_agent
from nexus.core.world_model import WorldModel


@register_agent
class SecurityAgent(BaseAgent):
    name = "security_agent"
    description = (
        "You monitor project security, manage access controls, identify "
        "security risks, protect sensitive information, and recommend "
        "security improvements."
    )

    def __init__(
        self,
        world: WorldModel,
        bus: Optional[EventBus] = None,
        **kwargs,
    ):
        super().__init__(world, bus, **kwargs)

    def review_access_controls(self) -> AgentResponse:
        """
        Review project permissions.
        """

        return self.run(
            "Review the current project permissions and access controls. "
            "Identify excessive privileges, missing permissions, inactive "
            "accounts, and recommend improvements following the principle "
            "of least privilege."
        )

    def security_audit(self) -> AgentResponse:
        """
        Perform a security assessment.
        """

        return self.run(
            "Perform a security audit of the current project. Review "
            "authentication, authorization, secrets management, data "
            "protection, infrastructure, integrations, and overall "
            "security posture."
        )

    def identify_vulnerabilities(self) -> AgentResponse:
        """
        Identify security vulnerabilities.
        """

        return self.run(
            "Analyze the project for security vulnerabilities including "
            "misconfigurations, exposed credentials, insecure workflows, "
            "dependency risks, and potential attack vectors."
        )

    def review_sensitive_data(self) -> AgentResponse:
        """
        Review handling of sensitive information.
        """

        return self.run(
            "Review how sensitive project information is stored, shared, "
            "and accessed. Identify risks involving confidential data, "
            "personal information, credentials, and intellectual property."
        )

    def recommend_security_improvements(self) -> AgentResponse:
        """
        Recommend security enhancements.
        """

        return self.run(
            "Recommend improvements that strengthen authentication, "
            "authorization, encryption, auditing, monitoring, backups, "
            "incident response, and overall project security."
        )

    def incident_response(self) -> AgentResponse:
        """
        Recommend actions following a security incident.
        """

        return self.run(
            "Review the current security incident. Recommend immediate "
            "containment, investigation, recovery, communication, and "
            "long-term preventive actions."
        )

    def handle_event(
        self,
        description: str,
    ) -> AgentResponse:
        """
        Respond to security-related events.
        """

        return self.run(
            f"A security event occurred: '{description}'. "
            "Determine how this affects project security, access control, "
            "data protection, infrastructure, and compliance. Recommend "
            "the appropriate response and mitigation."
        )
