# Blockers and Unproven Claims

## Missing locally (required for execution)

| Tool | Why needed | Blocker | Workaround |
|------|-----------|---------|-----------|
| `python 3.11+` | AlphaEvolve client, examples, evaluators | Required | Install from python.org or Windows Store |
| `uv` | Fast Python dependency management | Recommended | `pip install uv` once Python exists |
| `terraform` | Cluster Toolkit IaC, Cloud Deployment | Required for HPC | Use Cloud Shell on cloud.google.com |

## Unproven (not tested in this snapshot)

### Google Cloud authentication and access
- **Not tested:** `gcloud auth application-default login`
- **Not tested:** Gemini Enterprise licence presence
- **Not tested:** AlphaEvolve provisioned App/Engine ID
- **Not tested:** `discoveryengine.googleapis.com` API access
- **Not tested:** `businessaicode.googleapis.com` (Antigravity) API access

### Cloud service connectivity
- **Not tested:** Cloud Run deployment or invocation
- **Not tested:** Cloud Build trigger and build execution
- **Not tested:** Artifact Registry access or image push
- **Not tested:** Cloud Storage bucket creation or write
- **Not tested:** Secret Manager API for credentials

### Advanced AI/ML services
- **Not tested:** Vertex AI Agent Engine runtime
- **Not tested:** Agent Development Kit (ADK) instantiation
- **Not tested:** Gemini 2.0 Flash or model access
- **Not tested:** Agent tool binding and execution
- **Not tested:** AlphaEvolve remote evaluation on Cloud Run

### Infrastructure-as-code
- **Not tested:** Cluster Toolkit `gcluster` binary (Windows unsupported natively)
- **Not tested:** GKE cluster provisioning
- **Not tested:** Slurm cluster creation
- **Not tested:** Terraform state management
- **Not tested:** Application Design Center template deployment

## CEO approval gates (required before execution)

These actions require **explicit owner approval** before we proceed:

1. **Enable billing or APIs** — charges may apply
   - discoveryengine.googleapis.com
   - businessaicode.googleapis.com
   - aiplatform.googleapis.com
   - cloudbuild.googleapis.com
   - run.googleapis.com
   - artifactregistry.googleapis.com

2. **Create external service accounts** — grants persistent cloud access
   - Service account creation
   - IAM role assignment
   - Service account impersonation

3. **Deploy to production** — affects real users/customers
   - Production Cloud Run services
   - Public load balancers
   - Customer-facing endpoints

4. **Modify DNS or SSL** — breaks existing services
   - Domain records
   - Certificate provisioning
   - Traffic routing

5. **Install native code or scripts** — security risk
   - npm packages with install scripts
   - Python dependencies with C extensions
   - Terraform providers with third-party binaries

6. **Create commitments or purchases** — financial impact
   - Reserved capacity
   - Long-term contracts
   - Third-party service subscriptions

7. **Expose or export credentials** — security breach risk
   - Save tokens to files
   - Print secrets in logs
   - Share credentials across users/agents

## How to unblock each capability

| Capability | Required | Time | Owner decision |
|---|---|---|---|
| AlphaEvolve local proof | Python 3.11+, uv | 15 min | Install Python |
| Cloud Run staging proof | gcloud creds, project, API | 30 min | Approve API enable, project selection |
| Gemini Enterprise proof | Active licence, App ID | 60 min | Verify licence, approve authentication |
| Cluster Toolkit on Windows | WSL2 or Cloud Shell | N/A | Use alternative execution environment |
| Agent Engine deployment | ADK SDK, Vertex AI API | 45 min | Approve API enable, ADK install |

## Safety checkpoint before proceeding

Before any action that costs money, changes infrastructure, or grants credentials:

1. Check `a11-executive-blast-radius` skill for money, reach, identity, reversal, evidence.
2. Create a decision fossil in `.agents/DECISIONS.md` with the trade-offs.
3. Prepare a rollback target and the exact reversal command.
4. Request owner approval if GREEN/AMBER/RED classified.
