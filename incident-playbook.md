
# Incident Playbook

## Sev-1 (Customer impacting)
1) Declare incident and open bridge (Slack/Zoom). Assign roles (Incident Commander, Comms, Scribe).
2) Check Grafana: Error rate and p95 latency panels.
3) `kubectl -n enterprise-mig get pods` and `kubectl logs` to find failing pods.
4) Rollback: `kubectl -n enterprise-mig rollout undo deployment/enterprise-app`.
5) Mitigate blast radius (scale replicas, disable feature flag).

## Root Cause Analysis (RCA) Template
- Summary:
- Impact window:
- User impact:
- Timeline:
- Root cause:
- Fix:
- Prevention/follow-ups:
