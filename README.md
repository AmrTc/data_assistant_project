# Data Assistant Project

## 🚀 Streamlit Cloud Deployment

### Wichtige Hinweise für Streamlit Cloud:

1. **Main file path**: `app.py` (im Root-Verzeichnis)
2. **Python version**: 3.9+
3. **Requirements file**: `requirements.txt`

### Projektstruktur:
```
data_assistant_project/           ← Repository Root (Streamlit Cloud läuft hier)
├── app.py                        ← **Haupt-Entry Point für Streamlit Cloud**
├── requirements.txt              ← Python Dependencies
├── packages.txt                  ← System Dependencies
├── setup.sh                     ← Setup Script
├── .streamlit/config.toml       ← Streamlit Konfiguration
│
└── new_data_assistant_project/   ← App-Verzeichnis
    ├── frontend/
    │   └── app.py               ← Haupt-App-Logik
    ├── src/
    │   ├── utils/
    │   ├── database/
    │   └── agents/
    └── data/
```

### Lokaler Test:
```bash
# Vom Repository-Root aus testen (wie Streamlit Cloud)
cd data_assistant_project
streamlit run app.py
```

### Streamlit Cloud Settings:
- **Main file path**: `app.py`
- **Python version**: 3.9+
- **Requirements file**: `requirements.txt`

### Secrets in Streamlit Cloud:
```toml
ANTHROPIC_API_KEY = "your-api-key-here"
```

## 🎯 Features

- Intelligent Data Assistant mit CLT-CFT Agent
- Benutzer-Authentifizierung und Rollenverwaltung
- SQL Query Execution mit ReAct Agent
- Kognitive Last-Theorie basierte Erklärungen
- Assessment-System für Benutzer-Profiling

## 🔧 Troubleshooting

### Problem: "No such file or directory: app.py"
**Lösung**: Stellen Sie sicher, dass der Main file path in Streamlit Cloud auf `app.py` gesetzt ist

### Problem: Import-Fehler
**Lösung**: Alle Imports verwenden jetzt konsistente, vollständige Pfade

### Problem: Verzeichnis-Fehler
**Lösung**: Path-Utilities wurden korrigiert und funktionieren in Streamlit Cloud

Das Projekt ist jetzt bereit für Streamlit Cloud! 🎉
