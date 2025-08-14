# 🚀 Enterprise Cloud Migration & Security Hardening

[![CI/CD](https://github.com/<YOUR_GITHUB_USERNAME>/enterprise-cloud-migration-security/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/<YOUR_GITHUB_USERNAME>/enterprise-cloud-migration-security/actions/workflows/ci-cd.yml)
![Kubernetes](https://img.shields.io/badge/Kubernetes-EKS%20%7C%20AKS-326ce5)
![Terraform](https://img.shields.io/badge/Terraform-IaC-623CE4)
![Observability](https://img.shields.io/badge/Observability-Prometheus%20%7C%20Grafana-orange)
![License](https://img.shields.io/badge/License-MIT-yellow)

A portfolio-ready demonstration of migrating an on-prem workload to **AWS (EKS)** and **Azure (AKS)** with **Infrastructure as Code**, **Kubernetes**, **observability**, and **security hardening**.

> **Resume match**: “Migrated 10+ enterprise applications from on-prem to AWS and Azure, deploying Kubernetes (EKS/AKS) clusters with automated failover, implementing IaC using Terraform, and integrating Prometheus, Grafana, and Prisma for observability/security; led incident management and root cause analysis, reducing MTTR by 50% and improving service reliability by 30%.”

---

## 🔎 What this shows
- **Workload:** Python **FastAPI** service exposing `/healthz`, `/metrics` (Prometheus), and `/predict` (dummy analytics).
- **Kubernetes:** Deployment, Service, **HPA**, Ingress; separate overlays for **AWS** and **Azure**.
- **Observability:** Prometheus scrape config + Grafana dashboard JSON (rate, error rate, p95 latency).
- **Security Hardening:** TLS-ready ingress, RBAC skeleton, least-privileged idea, image scanning hook in CI.
- **IaC:** Terraform skeletons for **AWS EKS** and **Azure AKS**.
- **CI/CD:** GitHub Actions pipeline (build → scan placeholder → push → `kubectl apply`).

---

## 🗂️ Repository structure
```
enterprise-cloud-migration-security/
├─ workloads/app/                  # FastAPI service (migrated workload)
├─ k8s/
│  ├─ base/                        # Namespace, Deployment, Service, HPA, Ingress
│  ├─ overlays/
│  │  ├─ aws/                      # Image/registry patch for AWS
│  │  └─ azure/                    # Image/registry patch for Azure
│  └─ monitoring/                  # Prometheus config, Grafana dashboard
├─ infra/
│  ├─ aws-eks/                     # Terraform (EKS skeleton)
│  └─ azure-aks/                   # Terraform (AKS skeleton)
├─ .github/workflows/ci-cd.yml     # CI/CD pipeline
└─ docs/incident-playbook.md       # Incident response guide + RCA template
```

---

## 🧪 Run locally (Docker)
```bash
# From repo root
docker build -t enterprise-app:local ./workloads/app
docker run -p 8000:8000 enterprise-app:local

# Test
curl -s http://localhost:8000/healthz
curl -s http://localhost:8000/predict -H 'Content-Type: application/json' -d '{"symbol":"AMZN","window":5}'
curl -s http://localhost:8000/metrics
```

---

## ☸️ Deploy to Kubernetes (demo flow)
> Assumes you have a cluster context set (kind/minikube/EKS/AKS).

```bash
kubectl apply -f k8s/base/namespace.yaml
kubectl apply -f k8s/base/deployment.yaml
kubectl apply -f k8s/base/service.yaml
kubectl apply -f k8s/base/hpa.yaml
kubectl apply -f k8s/monitoring/prometheus.yaml

# (Optional) Ingress if you have an NGINX ingress controller
kubectl apply -f k8s/base/ingress.yaml

# Port-forward to test
kubectl -n enterprise-mig port-forward svc/enterprise-app 8000:80
# http://localhost:8000/docs, /healthz, /metrics
```

**AWS overlay (image registry patch example)**  
Edit `k8s/overlays/aws/deployment-patch.yaml` and set your ECR/registry image.

**Azure overlay**  
Edit `k8s/overlays/azure/deployment-patch.yaml` and set your ACR/registry image.

---

## 🔧 CI/CD (GitHub Actions)
Pipeline: **build → test (placeholder) → image push → deploy**

Set these **GitHub Secrets** in your repo:
- `REGISTRY` – e.g., `ghcr.io/<YOUR_GITHUB_USERNAME>` or your ECR/ACR URI  
- `REGISTRY_USER` – registry username (or `GHCR` token user)  
- `REGISTRY_PASSWORD` – registry password / PAT / token  
- `KUBE_CONFIG` – base64-encoded kubeconfig for your cluster

> On pushes to `main`, the workflow builds and pushes the image, updates the K8s manifest image tag, and applies manifests to the cluster.

---

## 📈 SRE: SLIs/SLOs & Error Budget
- **Availability SLI**: `2xx+3xx responses / total requests`  
  - **SLO**: **99.9%** monthly  
- **Latency SLI**: p95 of `/predict`  
  - **SLO**: **p95 < 200 ms**  
- **Error budget**: **0.1%** monthly — gate releases if breached

**Grafana panels included (JSON)**:
- Request Rate, Error Rate (non-2xx), p95 Latency

---

## 🛡️ Security Hardening (examples)
- **Ingress/TLS** ready; add your certificate manager or terminate at ALB/AGIC.
- **RBAC** skeleton + namespace scoping (principle of least privilege).
- **NetworkPolicies** (add rules to restrict east-west traffic).
- **Image scanning**: hook Trivy/Grype stage into CI before push.

---

## 🧰 Terraform (EKS & AKS skeletons)
- `infra/aws-eks`: provider + EKS module example (uncomment & set vars: `region`, `profile`, `cluster_name`, `subnet_ids`, `vpc_id`).
- `infra/azure-aks`: provider + AKS cluster example (uncomment & set vars: `cluster_name`, `location`, `resource_group`).

> Add remote state (S3/DynamoDB for AWS, Azure Storage for AKS) for team use.

---

## 🚨 Incident Playbook
See **`docs/incident-playbook.md`** for:
- Triage steps (metrics, logs, dashboards)
- Rollback (`kubectl rollout undo`)
- RCA template + continuous improvement checklist

---

## 🗺️ Roadmap
- Add canary/blue-green strategy (Argo Rollouts)
- Add service mesh (Linkerd/Istio) for mTLS + traffic policy
- Integrate Trivy image scan + policy gate in CI
- Expand Grafana dashboard & alerts (PrometheusRule)

---

## 📄 License
MIT — free to use for learning and portfolio purposes.

---

### ✅ Setup checklist
- [ ] Replace badge username: `<YOUR_GITHUB_USERNAME>`
- [ ] Set registry in `k8s/base/deployment.yaml` (and overlays)
- [ ] Add required **GitHub Secrets** (`REGISTRY`, `REGISTRY_USER`, `REGISTRY_PASSWORD`, `KUBE_CONFIG`)
- [ ] (Optional) Fill Terraform variables and create clusters (EKS/AKS)
