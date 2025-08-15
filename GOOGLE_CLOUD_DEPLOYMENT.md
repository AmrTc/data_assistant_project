# 🚀 Google Cloud Deployment Guide

## 📋 Voraussetzungen

### 1. **Google Cloud Account & Projekt**
```bash
# Google Cloud CLI installieren
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# Anmelden
gcloud auth login

# Projekt setzen
gcloud config set project YOUR_PROJECT_ID
```

### 2. **Benötigte APIs aktivieren**
```bash
# Cloud Build API
gcloud services enable cloudbuild.googleapis.com

# Cloud Run API
gcloud services enable run.googleapis.com

# Container Registry API
gcloud services enable containerregistry.googleapis.com
```

### 3. **Berechtigungen**
```bash
# Cloud Build Service Account Berechtigungen
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:YOUR_PROJECT_NUMBER@cloudbuild.gserviceaccount.com" \
    --role="roles/run.admin"

gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:YOUR_PROJECT_NUMBER@cloudbuild.gserviceaccount.com" \
    --role="roles/iam.serviceAccountUser"
```

## 🐳 Lokaler Docker Test

### 1. **Image bauen**
```bash
docker build -t data-assistant .
```

### 2. **Lokal testen**
```bash
# Mit Docker
docker run -p 8080:8080 data-assistant

# Mit Docker Compose
docker-compose up --build
```

### 3. **Testen**
```bash
curl http://localhost:8080
# Oder im Browser: http://localhost:8080
```

## ☁️ Google Cloud Deployment

### 1. **Automatisches Deployment (empfohlen)**
```bash
# Code zu GitHub pushen
git push origin main

# Cloud Build Trigger erstellen (in Google Cloud Console)
# Oder manuell auslösen:
gcloud builds submit --config cloudbuild.yaml .
```

### 2. **Manuelles Deployment**
```bash
# Image bauen und pushen
docker build -t gcr.io/YOUR_PROJECT_ID/data-assistant .
docker push gcr.io/YOUR_PROJECT_ID/data-assistant

# Zu Cloud Run deployen
gcloud run deploy data-assistant \
    --image gcr.io/YOUR_PROJECT_ID/data-assistant \
    --platform managed \
    --region europe-west1 \
    --allow-unauthenticated \
    --port 8080 \
    --memory 2Gi \
    --cpu 1 \
    --max-instances 10
```

## 🔧 Konfiguration

### 1. **Umgebungsvariablen**
```bash
# In Google Cloud Console oder über gcloud
gcloud run services update data-assistant \
    --set-env-vars ANTHROPIC_API_KEY=your_key_here
```

### 2. **Secrets verwalten**
```bash
# Secret Manager (empfohlen)
echo -n "your-api-key" | gcloud secrets create anthropic-api-key --data-file=-

# In Cloud Run verwenden
gcloud run services update data-assistant \
    --set-env-vars ANTHROPIC_API_KEY=projects/YOUR_PROJECT_ID/secrets/anthropic-api-key/versions/latest
```

## 📊 Monitoring & Logs

### 1. **Logs anzeigen**
```bash
gcloud logging read "resource.type=cloud_run_revision" --limit=50
```

### 2. **Metriken überwachen**
- Google Cloud Console → Cloud Run → Metriken
- Request Count, Latency, Error Rate

## 🔒 Sicherheit

### 1. **HTTPS (automatisch)**
- Cloud Run bietet automatisch HTTPS
- Custom Domain möglich

### 2. **IAM & Berechtigungen**
```bash
# Nur bestimmte User erlauben
gcloud run services remove-iam-policy-binding data-assistant \
    --member="allUsers" \
    --role="roles/run.invoker"

# Bestimmte User hinzufügen
gcloud run services add-iam-policy-binding data-assistant \
    --member="user:user@example.com" \
    --role="roles/run.invoker"
```

## 🚨 Troubleshooting

### 1. **Build-Fehler**
```bash
# Logs anzeigen
gcloud builds log BUILD_ID

# Lokal testen
docker build -t test-image .
```

### 2. **Runtime-Fehler**
```bash
# Service-Logs
gcloud run services logs read data-assistant

# Container-Logs
gcloud logging read "resource.type=cloud_run_revision"
```

### 3. **Performance-Probleme**
- Memory/CPU Limits erhöhen
- Max Instances anpassen
- Cold Start optimieren

## 💰 Kostenoptimierung

### 1. **Ressourcen optimieren**
```bash
# Minimal-Konfiguration
gcloud run deploy data-assistant \
    --memory 512Mi \
    --cpu 0.5 \
    --max-instances 5
```

### 2. **Auto-scaling**
- Min Instances: 0 (Cold Start)
- Max Instances: 10 (Kostenkontrolle)

## 🔄 CI/CD Pipeline

### 1. **GitHub Actions (optional)**
```yaml
# .github/workflows/deploy.yml
name: Deploy to Google Cloud
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: google-github-actions/setup-gcloud@v0
      - run: gcloud builds submit --config cloudbuild.yaml .
```

## ✅ Deployment-Checkliste

- [ ] Google Cloud Projekt erstellt
- [ ] APIs aktiviert
- [ ] Berechtigungen gesetzt
- [ ] Docker Image lokal getestet
- [ ] Code zu GitHub gepusht
- [ ] Cloud Build ausgelöst
- [ ] Service läuft auf Cloud Run
- [ ] HTTPS funktioniert
- [ ] Umgebungsvariablen gesetzt
- [ ] Monitoring konfiguriert

## 🌐 Zugriff

Nach erfolgreichem Deployment:
```
https://data-assistant-XXXXX-ew.a.run.app
```

## 📞 Support

- Google Cloud Documentation
- Cloud Run Troubleshooting Guide
- Stack Overflow: google-cloud-run
