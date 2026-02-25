# ⚡ PILOTE — Automatisation du Contrôle de Gestion

Application Streamlit production-ready pour l'automatisation complète du pilotage de la performance financière.

---

## 🚀 Installation & Lancement

```bash
# 1. Installer les dépendances
pip install -r requirements_pilote.txt

# 2. Lancer l'application
streamlit run pilote_cg.py

# 3. Ouvrir dans le navigateur
# http://localhost:8501
```

---

## 📦 Modules de l'Application

| Module | Description |
|--------|-------------|
| ⚡ Dashboard Exécutif | KPIs temps réel · Alertes · Graphiques synthèse |
| 📊 Budget vs Réel | Analyse écarts automatisée · Waterfall · Drill-down |
| 🔮 Forecasting ML | Prévisions CA à 6-12 mois · Intervalles de confiance |
| 🚨 Détection Anomalies | Z-score · Règles métier · Heatmap de risque |
| 💰 Rentabilité | P&L par produit · Matrice BCG · Analyse clients |
| 🏦 Trésorerie | Prévision 90j · Alertes tension · Flux hebdomadaires |
| 📥 Import & Auto | Pipeline ETL · Mapping colonnes · Code Python |
| 📄 Rapports Auto | Génération Excel multi-onglets · Commentaires IA |

---

## 📐 Architecture Technique

```
pilote_cg.py
├── Configuration (design system, couleurs, CSS)
├── Génération données (cache Streamlit)
├── Sidebar (navigation + filtres globaux)
└── Pages (8 modules)
    ├── Dashboard Exécutif
    ├── Budget vs Réel
    ├── Forecasting ML
    ├── Détection Anomalies
    ├── Rentabilité
    ├── Trésorerie
    ├── Import & Automatisation
    └── Rapports Automatiques
```

---

## 🔧 Personnalisation

### Connecter vos vraies données

Remplacez les fonctions `generate_*` par vos connexions réelles :

```python
# Exemple : Connexion SQL Server
import pyodbc
import pandas as pd

def load_from_sql():
    conn = pyodbc.connect("DRIVER={SQL Server};SERVER=votre-serveur;DATABASE=finance;")
    df = pd.read_sql("""
        SELECT date, ca_reel, ca_budget, ebitda
        FROM reporting.mensuel
        WHERE date >= DATEADD(month, -24, GETDATE())
    """, conn)
    return df
```

### Activer les alertes email

Dans `pilote_cg.py`, configurez le fichier `.env` :

```
SMTP_SERVER=smtp.votre-serveur.com
SMTP_PORT=587
SMTP_USER=pilote@votre-entreprise.com
SMTP_PASSWORD=votre_mot_de_passe
ALERT_RECIPIENTS=cfo@entreprise.com,equipe-finance@entreprise.com
```

### Déployer sur le cloud

```bash
# Streamlit Cloud (gratuit)
# 1. Pusher le code sur GitHub
# 2. Connecter à share.streamlit.io

# Azure / AWS / GCP
# Utiliser Docker :
docker build -t pilote-cg .
docker run -p 8501:8501 pilote-cg
```

---

## 📋 Données Requises

Pour utiliser vos propres données, préparez un fichier avec ces colonnes :

| Colonne | Type | Description |
|---------|------|-------------|
| `date` | Date | Mois de la donnée |
| `ca_reel` | Nombre | CA réalisé |
| `ca_budget` | Nombre | CA budgété |
| `charges_fixes` | Nombre | Charges fixes du mois |
| `charges_variables` | Nombre | Charges variables |
| `charges_personnel` | Nombre | Masse salariale |
| `ebitda_reel` | Nombre | EBITDA réalisé |

Téléchargez le template Excel directement dans l'application (module Import).

---

## 🛠️ Dépendances

- `streamlit` — Framework application web
- `plotly` — Visualisations interactives
- `pandas` — Manipulation de données
- `numpy` — Calculs numériques
- `scikit-learn` — Machine learning (forecasting)
- `openpyxl` — Lecture/écriture Excel
- `xlsxwriter` — Génération Excel avancée

---

*PILOTE v1.0 · Formation Contrôle de Gestion & Data Science*
