from prowler.lib.check.models import Check, Check_Report_Azure
from prowler.providers.azure.services.entra.entra_client import entra_client


class entra_security_defaults_enabled(Check):
    def execute(self) -> Check_Report_Azure:
        findings = []

        for (
            tenant,
            security_default,
        ) in entra_client.security_default.items():
            report = Check_Report_Azure(
                metadata=self.metadata(), resource=security_default
            )
            report.subscription = f"Tenant: {tenant}"
            report.status = "FAIL"
            report.status_extended = "Entra security defaults is disabled."

            if getattr(security_default, "is_enabled", False):
                report.status = "PASS"
                report.status_extended = "Entra security defaults is enabled."

            findings.append(report)

        return findings
