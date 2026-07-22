from __future__ import annotations

from .approvals import ApprovalManager
from .audit import AuditLog
from .permissions import PermissionManager
from .policy import Policy


class GovernanceManager:

    def __init__(self):

        self.permissions = PermissionManager()

        self.approvals = ApprovalManager()

        self.audit = AuditLog()

        self.policies = {}

    def add_policy(
        self,
        policy: Policy,
    ):

        self.policies[
            policy.name
        ] = policy

    def policy(
        self,
        name: str,
    ):

        return self.policies.get(
            name
        )

    def allowed(
        self,
        role: str,
        action: str,
    ) -> bool:

        if not self.permissions.can(
            role,
            action,
        ):

            return False

        for policy in self.policies.values():

            if not policy.allows(
                action
            ):

                return False

        return True
