# echobot-repo

Minimal scaffold for Echobot Slack bot.

Structure:
- services/echobot/
  - Dockerfile
  - main.py
  - requirements.txt

cloudbuild.yaml builds the image from services/echobot and deploys to Cloud Run (echobot service) in us-central1 using service account echo-deployer@echobot-486304.iam.gserviceaccount.com and Secret Manager secrets:
- slack-bot-token
- slack-signing-secret

Defaults:
- Artifact Registry repo: us-central1-docker.pkg.dev/echobot-486304/echobot-repo/echobot
- Cloud Run service: echobot

Instructions to push to GitHub are below.
