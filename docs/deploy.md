# Deploying to Google Cloud Run

The GitHub Actions workflow (`.github/workflows/ci.yml`) tests every pull request and, on each
push to `main`, builds the Docker image, pushes it to Artifact Registry and deploys it to Cloud Run.

It needs a one-time setup in Google Cloud. Nothing secret is stored in GitHub: the workflow signs
in with Workload Identity Federation, and Cloud Run reads the Anthropic API key from Secret Manager.

## 1. Set names

Run these in a shell with the [gcloud CLI](https://cloud.google.com/sdk/docs/install) signed in
(`gcloud auth login`). Replace the values in the first block.

```bash
PROJECT_ID=my-project-id
REGION=europe-west1
REPO=vsa
SERVICE=veloria-support-assistant
GITHUB_REPO=your-github-user/technical-support-assistant

PROJECT_NUMBER=$(gcloud projects describe "$PROJECT_ID" --format='value(projectNumber)')
DEPLOYER=github-deployer@$PROJECT_ID.iam.gserviceaccount.com
RUNTIME=vsa-runtime@$PROJECT_ID.iam.gserviceaccount.com
gcloud config set project "$PROJECT_ID"
```

## 2. Enable APIs and create the image repository

```bash
gcloud services enable run.googleapis.com artifactregistry.googleapis.com \
  secretmanager.googleapis.com iamcredentials.googleapis.com sts.googleapis.com

gcloud artifacts repositories create "$REPO" --repository-format=docker --location="$REGION"
```

## 3. Store the Anthropic API key

```bash
printf '%s' "PASTE-YOUR-KEY" | gcloud secrets create anthropic-api-key --data-file=-
```

## 4. Create the service accounts

`vsa-runtime` is what the app runs as; it can only read the API key.
`github-deployer` is what GitHub Actions uses; it can push images and deploy.

```bash
gcloud iam service-accounts create vsa-runtime
gcloud iam service-accounts create github-deployer

gcloud secrets add-iam-policy-binding anthropic-api-key \
  --member="serviceAccount:$RUNTIME" --role=roles/secretmanager.secretAccessor

for ROLE in roles/run.admin roles/artifactregistry.writer; do
  gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$DEPLOYER" --role="$ROLE"
done
gcloud iam service-accounts add-iam-policy-binding "$RUNTIME" \
  --member="serviceAccount:$DEPLOYER" --role=roles/iam.serviceAccountUser
```

## 5. Let GitHub Actions sign in (Workload Identity Federation)

Only workflows from your repository can use the deployer account.

```bash
gcloud iam workload-identity-pools create github --location=global

gcloud iam workload-identity-pools providers create-oidc github-provider \
  --location=global --workload-identity-pool=github \
  --issuer-uri=https://token.actions.githubusercontent.com \
  --attribute-mapping=google.subject=assertion.sub,attribute.repository=assertion.repository \
  --attribute-condition="assertion.repository == '$GITHUB_REPO'"

gcloud iam service-accounts add-iam-policy-binding "$DEPLOYER" \
  --role=roles/iam.workloadIdentityUser \
  --member="principalSet://iam.googleapis.com/projects/$PROJECT_NUMBER/locations/global/workloadIdentityPools/github/attribute.repository/$GITHUB_REPO"

echo "GCP_WIF_PROVIDER=projects/$PROJECT_NUMBER/locations/global/workloadIdentityPools/github/providers/github-provider"
```

## 6. Add the GitHub repository variables

In GitHub: Settings > Secrets and variables > Actions > Variables > New repository variable.

| Variable | Value |
|---|---|
| `GCP_PROJECT_ID` | your project ID |
| `GCP_REGION` | e.g. `europe-west1` |
| `AR_REPOSITORY` | `vsa` |
| `GCP_WIF_PROVIDER` | printed by the last command above |
| `GCP_DEPLOY_SA` | `github-deployer@PROJECT_ID.iam.gserviceaccount.com` |
| `GCP_RUNTIME_SA` | `vsa-runtime@PROJECT_ID.iam.gserviceaccount.com` |
| `CLOUD_RUN_PUBLIC` | `true` for a public demo, otherwise leave unset |

With `CLOUD_RUN_PUBLIC=true` anyone with the URL can ask questions, and every question costs
API credits. `--max-instances=3` in the workflow limits how far that can go; consider a spend
limit in the Anthropic Console as well.

The `deploy` job uses a GitHub environment called `production`. GitHub creates it on the first
run; add required reviewers to it (Settings > Environments) if you want to approve each deploy.

## 7. Deploy

Push to `main`, or run the workflow by hand from the Actions tab with the `main` branch selected
(on any other branch the deploy job is skipped). The deploy job prints the
service URL. If the service is private, open it through an authenticated proxy:

```bash
gcloud run services proxy "$SERVICE" --region="$REGION" --port=8080
```
