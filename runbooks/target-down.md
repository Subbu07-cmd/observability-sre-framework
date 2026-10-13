# Runbook: TargetDown

1. Check whether it's the host or the exporter: `ssh <host> systemctl status node_exporter`
2. If the host is unreachable, check the EC2 status checks. The `ec2-status-check-*` alarm auto-recovers failed hardware.
3. If only the exporter is down, `sudo systemctl restart node_exporter`, then re-run `ansible-playbook node_exporter.yml -l <host>`.
4. If a Kubernetes target is down, `kubectl get pods -A -o wide | grep <instance>` and check events.
5. Resolve once `up == 1` has held for 5 minutes.
