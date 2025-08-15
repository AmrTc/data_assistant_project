# Streamlit Cloud Deployment Guide

## 🚨 **KRITISCHE EINSTELLUNG - Main file path**

### **Main file path MUSS exakt so sein**:
```
app.py
```

### **NICHT erlaubt**:
- ❌ `new_data_assistant_project/app.py`
- ❌ `new_data_assistant_project/frontend/app.py`
- ❌ `frontend/app.py`
- ❌ `src/app.py`

### **NUR erlaubt**:
- ✅ `app.py` (im Repository-Root)

## 🚀 Wichtige Einstellungen in Streamlit Cloud

### 1. **Main file path**
```
app.py
```
**WICHTIG**: NICHT `new_data_assistant_project/frontend/app.py` oder ähnliches!

### 2. **Python version**
```
3.9 oder höher
```

### 3. **Requirements file**
```
requirements.txt
```

### 4. **Working directory**
```
/ (Root des Repositories)
```

## 📁 Projektstruktur für Streamlit Cloud

```
data_assistant_project/           ← Repository Root (Streamlit Cloud läuft hier)
├── app.py                        ← **Haupt-Entry Point**
├── streamlit_app.py              ← Alternative Entry Point (falls nötig)
├── requirements.txt              ← Python Dependencies
├── packages.txt                  ← System Dependencies
├── setup.sh                     ← Setup Script
├── .streamlit/config.toml       ← Streamlit Konfiguration
├── README.md                     ← Projekt-Dokumentation
│
└── new_data_assistant_project/   ← App-Verzeichnis
    ├── frontend/
    │   └── app.py               ← Haupt-App-Logik
    ├── src/
    │   ├── utils/
    │   │   ├── path_utils.py    ← Pfad-Verwaltung
    │   │   ├── auth_manager.py  ← Authentifizierung
    │   │   └── chat_manager.py  ← Chat-Verwaltung
    │   ├── database/
    │   │   ├── models.py        ← Datenbank-Modelle
    │   │   └── schema.py        ← Datenbank-Schema
    │   └── agents/
    │       ├── clt_cft_agent.py ← CLT-CFT Agent
    │       └── ReAct_agent.py   ← ReAct Agent
    └── data/                     ← Daten-Verzeichnis
```

## 🔧 Streamlit Cloud Konfiguration

### Schritt 1: Repository verbinden
1. Gehen Sie zu [share.streamlit.io](https://share.streamlit.io)
2. Verbinden Sie Ihr GitHub Repository
3. Wählen Sie den `main` Branch

### Schritt 2: App-Einstellungen
```
App name: data-assistant-project
Main file path: app.py          ← **WICHTIG: Nur app.py**
Python version: 3.9
Requirements file: requirements.txt
```

### Schritt 3: Secrets konfigurieren
In den Streamlit Cloud Settings:
```toml
ANTHROPIC_API_KEY = "your-api-key-here"
```

## 🐛 Häufige Probleme und Lösungen

### Problem 1: "No such file or directory: new_data_assistant_project/app.py"
**Symptom**: 
```
FileNotFoundError: [Errno 2] No such file or directory: '/mount/src/data_assistant_project/new_data_assistant_project/app.py'
```

**Lösung**: 
- **Main file path MUSS auf `app.py` gesetzt sein**
- NICHT auf `new_data_assistant_project/app.py`
- Überprüfen Sie die Einstellungen in Streamlit Cloud

### Problem 2: Import-Fehler
**Symptom**: 
```
ModuleNotFoundError: No module named 'new_data_assistant_project.src.utils.auth_manager'
```

**Lösung**: 
- Alle Imports verwenden jetzt konsistente, vollständige Pfade
- Path-Utilities wurden korrigiert

### Problem 3: Verzeichnis-Fehler
**Symptom**: 
```
❌ Missing directory: new_data_assistant_project/src
```

**Lösung**: 
- Path-Utilities wurden korrigiert
- Verzeichnisse werden relativ zum App-Verzeichnis gesucht

## ✅ Deployment-Checkliste

- [ ] Repository ist mit Streamlit Cloud verbunden
- [ ] **Main file path ist auf `app.py` gesetzt** ← **KRITISCH**
- [ ] Python version ist 3.9 oder höher
- [ ] Requirements file ist `requirements.txt`
- [ ] ANTHROPIC_API_KEY ist in Secrets konfiguriert
- [ ] Alle Imports verwenden konsistente Pfade
- [ ] Path-Utilities sind korrigiert
- [ ] Lokaler Test funktioniert: `streamlit run app.py`

## 🧪 Lokaler Test

```bash
# Vom Repository-Root aus testen (wie Streamlit Cloud)
cd data_assistant_project
streamlit run app.py
```

## 📊 Monitoring

Nach dem Deployment:
1. Überprüfen Sie die Logs in Streamlit Cloud
2. **Stellen Sie sicher, dass der Main file path korrekt ist**
3. Testen Sie die Login/Registrierung
4. Überprüfen Sie alle Hauptfunktionen
5. Testen Sie die Datenbank-Verbindung

## 🆘 Support

Bei Problemen:
1. **Überprüfen Sie den Main file path in Streamlit Cloud**
2. Überprüfen Sie die Logs in Streamlit Cloud
3. Stellen Sie sicher, dass alle Einstellungen korrekt sind
4. Testen Sie lokal mit `streamlit run app.py`
5. Überprüfen Sie die Import-Pfade

## 🚨 **WICHTIGSTE REGEL:**

**Der Main file path in Streamlit Cloud MUSS exakt `app.py` sein, nicht mehr und nicht weniger!**

Das Projekt ist jetzt vollständig für Streamlit Cloud vorbereitet! 🎉
