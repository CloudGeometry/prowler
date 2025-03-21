from prowler.lib.check.models import Check, Check_Report_GCP
from prowler.providers.gcp.services.logging.logging_client import logging_client


class logging_sink_created(Check):
    def execute(self) -> Check_Report_GCP:
        findings = []
        projects_with_sink = set()
        for sink in logging_client.sinks:
            report = Check_Report_GCP(
                metadata=self.metadata(),
                resource=sink,
                location=logging_client.region,
            )
            projects_with_sink.add(sink.project_id)
            report.status = "FAIL"
            report.status_extended = f"Sink {sink.name} is enabled but not exporting copies of all the log entries in project {sink.project_id}."
            if sink.filter == "all":
                report.status = "PASS"
                report.status_extended = f"Sink {sink.name} is enabled exporting copies of all the log entries in project {sink.project_id}."
            findings.append(report)

        for project in logging_client.project_ids:
            if project not in projects_with_sink:
                report = Check_Report_GCP(
                    metadata=self.metadata(),
                    resource=logging_client.projects[project],
                    project_id=project,
                    location=logging_client.region,
                )
                report.status = "FAIL"
                report.status_extended = f"There are no logging sinks to export copies of all the log entries in project {project}."
                findings.append(report)

        return findings
