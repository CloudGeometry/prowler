from prowler.lib.check.models import Check, Check_Report_Kubernetes
from prowler.lib.utils.utils import is_owned_by_root
from prowler.providers.kubernetes.services.core.core_client import core_client


class kubelet_conf_file_ownership(Check):
    def execute(self) -> Check_Report_Kubernetes:
        findings = []
        for node in core_client.nodes.values():
            report = Check_Report_Kubernetes(metadata=self.metadata(), resource=node)
            # It can only be checked if Prowler is being executed inside a worker node or if the file is the default one
            if node.inside:
                if is_owned_by_root("/etc/kubernetes/kubelet.conf") is None:
                    report.status = "MANUAL"
                    report.status_extended = f"kubelet.conf file not found in Node {node.name}, please verify kubelet.conf file ownership manually."
                else:
                    report.status = "PASS"
                    report.status_extended = f"kubelet.conf file ownership is set to root:root in Node {node.name}."
                    if not is_owned_by_root("/etc/kubernetes/kubelet.conf"):
                        report.status = "FAIL"
                        report.status_extended = f"kubelet.conf file ownership is not set to root:root in Node {node.name}."
            else:
                report.status = "MANUAL"
                report.status_extended = f"Prowler is not being executed inside Node {node.name}, please verify kubelet.conf file ownership manually."
            findings.append(report)
        return findings
