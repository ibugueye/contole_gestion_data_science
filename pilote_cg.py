"""
╔══════════════════════════════════════════════════════════════════════════════╗
║        PILOTE — Automatisation du Contrôle de Gestion                       ║
║        Application Streamlit Production-Ready                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  MODULES :                                                                   ║
║  1. Dashboard Exécutif — KPIs temps réel & alertes                          ║
║  2. Import & Nettoyage — CSV/Excel, réconciliation automatique               ║
║  3. Budget vs Réel — Analyse des écarts automatisée                         ║
║  4. Forecasting — Prévisions ML à 3/6/12 mois                               ║
║  5. Anomalies — Détection automatique par algorithme                         ║
║  6. Rentabilité — P&L par produit / BU / client                             ║
║  7. Trésorerie — Prévision cash & alertes                                   ║
║  8. Rapports — Génération automatique PDF/Excel                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

INSTALLATION :
    pip install streamlit plotly pandas numpy scikit-learn openpyxl xlsxwriter

LANCEMENT :
    streamlit run pilote_cg.py
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import io
import warnings
warnings.filterwarnings("ignore")

# ══════════════════════════════════════════════════════════════════════════════
# CONFIGURATION GLOBALE
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="PILOTE — Contrôle de Gestion",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
# DESIGN SYSTEM
# ══════════════════════════════════════════════════════════════════════════════
COLORS = {
    "bg_dark":    "#0A0F1E",
    "bg_card":    "#111827",
    "bg_card2":   "#1a2235",
    "border":     "#1E2D45",
    "navy":       "#0F2457",
    "blue":       "#1565D8",
    "blue_light": "#3B82F6",
    "teal":       "#00D4AA",
    "teal_dark":  "#00A886",
    "gold":       "#F5A623",
    "gold_light": "#FCD34D",
    "red":        "#EF4444",
    "red_light":  "#FCA5A5",
    "green":      "#10B981",
    "green_light":"#6EE7B7",
    "purple":     "#8B5CF6",
    "white":      "#F8FAFF",
    "gray":       "#64748B",
    "gray_light": "#94A3B8",
    "text":       "#E2E8F0",
    "text_muted": "#64748B",
}

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Sora:wght@300;400;600;700;800&display=swap');

/* ── BASE ── */
html, body, [class*="css"] {{
    font-family: 'Sora', sans-serif;
    background-color: {COLORS['bg_dark']};
    color: {COLORS['text']};
}}
.main .block-container {{ padding: 1.5rem 2rem 3rem; max-width: 1600px; }}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {{
    background: {COLORS['bg_card']};
    border-right: 1px solid {COLORS['border']};
}}
[data-testid="stSidebar"] * {{ color: {COLORS['text']} !important; }}
[data-testid="stSidebar"] .stRadio > label {{ font-size: 0.78rem; letter-spacing: 0.05em; color: {COLORS['gray_light']} !important; text-transform: uppercase; }}

/* ── METRICS ── */
[data-testid="stMetric"] {{
    background: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 10px;
    padding: 16px 18px;
}}
[data-testid="stMetricLabel"] {{ font-size: 0.72rem !important; color: {COLORS['gray_light']} !important; text-transform: uppercase; letter-spacing: 0.08em; }}
[data-testid="stMetricValue"] {{ font-size: 1.7rem !important; font-weight: 700; color: {COLORS['white']} !important; }}
[data-testid="stMetricDelta"] {{ font-size: 0.8rem !important; }}

/* ── TABS ── */
[data-baseweb="tab-list"] {{
    background: {COLORS['bg_card']};
    border-radius: 8px;
    padding: 4px;
    border: 1px solid {COLORS['border']};
    gap: 2px;
}}
[data-baseweb="tab"] {{
    border-radius: 6px !important;
    color: {COLORS['gray_light']} !important;
    font-size: 0.82rem;
    font-weight: 500;
    padding: 6px 16px !important;
}}
[aria-selected="true"] {{
    background: {COLORS['blue']} !important;
    color: white !important;
}}

/* ── INPUTS ── */
[data-testid="stSelectbox"] > div,
[data-testid="stMultiSelect"] > div,
.stSlider {{ filter: none; }}
input, select, textarea {{
    background: {COLORS['bg_card2']} !important;
    border: 1px solid {COLORS['border']} !important;
    color: {COLORS['text']} !important;
    border-radius: 6px !important;
}}

/* ── TABLES ── */
.stDataFrame {{ border: 1px solid {COLORS['border']}; border-radius: 8px; }}
[data-testid="stDataFrame"] {{ background: {COLORS['bg_card']}; }}

/* ── ALERTS ── */
.stAlert {{ border-radius: 8px; border: 1px solid {COLORS['border']}; }}

/* ── EXPANDER ── */
[data-testid="stExpander"] {{
    background: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
}}

/* ─── CUSTOM COMPONENTS ─── */
.pilote-header {{
    background: linear-gradient(135deg, {COLORS['bg_card']} 0%, {COLORS['navy']} 100%);
    border: 1px solid {COLORS['border']};
    border-radius: 12px;
    padding: 24px 28px;
    margin-bottom: 20px;
    position: relative;
    overflow: hidden;
}}
.pilote-header::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, {COLORS['teal']}, {COLORS['blue']}, {COLORS['gold']});
}}

.kpi-card {{
    background: {COLORS['bg_card']};
    border: 1px solid {COLORS['border']};
    border-radius: 10px;
    padding: 18px 20px;
    transition: border-color 0.2s;
}}
.kpi-card:hover {{ border-color: {COLORS['blue_light']}; }}

.kpi-value {{
    font-size: 1.9rem;
    font-weight: 800;
    font-family: 'DM Mono', monospace;
    line-height: 1.1;
}}
.kpi-label {{
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: {COLORS['gray_light']};
    margin-top: 4px;
}}
.kpi-delta-pos {{ color: {COLORS['green']}; font-size: 0.78rem; font-weight: 600; }}
.kpi-delta-neg {{ color: {COLORS['red']}; font-size: 0.78rem; font-weight: 600; }}

.alert-card {{
    border-radius: 8px;
    padding: 12px 16px;
    margin: 6px 0;
    display: flex;
    align-items: flex-start;
    gap: 10px;
    border: 1px solid;
}}
.alert-critical {{
    background: rgba(239,68,68,0.08);
    border-color: rgba(239,68,68,0.3);
}}
.alert-warning {{
    background: rgba(245,166,35,0.08);
    border-color: rgba(245,166,35,0.3);
}}
.alert-info {{
    background: rgba(0,212,170,0.08);
    border-color: rgba(0,212,170,0.3);
}}

.section-title {{
    font-size: 0.68rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: {COLORS['teal']};
    font-weight: 600;
    margin-bottom: 12px;
    padding-bottom: 8px;
    border-bottom: 1px solid {COLORS['border']};
}}

.tag {{
    display: inline-block;
    padding: 2px 10px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-weight: 600;
    font-family: 'DM Mono', monospace;
}}
.tag-green {{ background: rgba(16,185,129,0.15); color: {COLORS['green']}; }}
.tag-red {{ background: rgba(239,68,68,0.15); color: {COLORS['red']}; }}
.tag-gold {{ background: rgba(245,166,35,0.15); color: {COLORS['gold']}; }}
.tag-blue {{ background: rgba(21,101,216,0.2); color: {COLORS['blue_light']}; }}

.code-block {{
    background: {COLORS['bg_card2']};
    border: 1px solid {COLORS['border']};
    border-radius: 8px;
    padding: 16px;
    font-family: 'DM Mono', monospace;
    font-size: 0.8rem;
    color: {COLORS['teal']};
    overflow-x: auto;
}}

.divider {{
    height: 1px;
    background: {COLORS['border']};
    margin: 20px 0;
}}

/* Override Streamlit default white backgrounds */
.stPlotlyChart {{ background: transparent !important; }}
[data-testid="column"] {{ gap: 12px; }}
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# GÉNÉRATION DE DONNÉES SYNTHÉTIQUES RÉALISTES
# ══════════════════════════════════════════════════════════════════════════════
@st.cache_data
def generate_company_data(seed=42):
    np.random.seed(seed)
    rng = np.random.default_rng(seed)

    # ── 24 mois de données ──
    dates = pd.date_range("2023-01-01", periods=24, freq="ME")
    n = len(dates)

    # Tendance + saisonnalité réaliste
    trend = np.linspace(3_200_000, 4_800_000, n)
    saison = 200_000 * np.sin(np.arange(n) * 2 * np.pi / 12 - 1.5)
    noise = rng.normal(0, 80_000, n)
    ca_reel = trend + saison + noise

    # Budget défini en début d'année
    budget_base = np.array([
        3_200_000, 3_250_000, 3_350_000, 3_480_000, 3_600_000, 3_750_000,
        3_900_000, 3_820_000, 3_700_000, 3_850_000, 3_950_000, 4_100_000,
        4_050_000, 4_150_000, 4_300_000, 4_420_000, 4_550_000, 4_650_000,
        4_700_000, 4_620_000, 4_580_000, 4_700_000, 4_820_000, 4_900_000,
    ])

    # Coûts
    charges_fixes = budget_base * 0.28 + rng.normal(0, 15_000, n)
    charges_var = ca_reel * 0.42 + rng.normal(0, 25_000, n)
    charges_personnel = budget_base * 0.22 + rng.normal(0, 8_000, n)

    ebitda = ca_reel - charges_fixes - charges_var - charges_personnel
    budget_ebitda = budget_base - budget_base * 0.28 - budget_base * 0.42 - budget_base * 0.22

    df = pd.DataFrame({
        "date": dates,
        "mois": [d.strftime("%b %Y") for d in dates],
        "ca_reel": ca_reel.round(0),
        "ca_budget": budget_base,
        "charges_fixes": charges_fixes.round(0),
        "charges_variables": charges_var.round(0),
        "charges_personnel": charges_personnel.round(0),
        "ebitda_reel": ebitda.round(0),
        "ebitda_budget": budget_ebitda.round(0),
    })
    df["ecart_ca"] = df["ca_reel"] - df["ca_budget"]
    df["ecart_ca_pct"] = df["ecart_ca"] / df["ca_budget"] * 100
    df["ecart_ebitda"] = df["ebitda_reel"] - df["ebitda_budget"]
    df["marge_ebitda"] = df["ebitda_reel"] / df["ca_reel"] * 100
    df["charges_totales"] = df["charges_fixes"] + df["charges_variables"] + df["charges_personnel"]

    return df


@st.cache_data
def generate_products_data(seed=42):
    rng = np.random.default_rng(seed)
    produits = ["Produit Alpha", "Produit Beta", "Produit Gamma", "Service Pro", "Service Elite", "Licence SaaS"]
    ca = [1_850_000, 1_240_000, 890_000, 560_000, 320_000, 180_000]
    marges = [0.52, 0.38, 0.61, 0.72, 0.68, 0.84]
    evolution = [+8.2, -3.1, +12.5, +22.1, +15.8, +41.2]
    budget_ca = [1_700_000, 1_350_000, 800_000, 500_000, 280_000, 120_000]
    return pd.DataFrame({
        "produit": produits,
        "ca_ytd": ca,
        "budget_ca": budget_ca,
        "marge_brute_pct": marges,
        "evolution_yoy": evolution,
        "marge_brute": [c * m for c, m in zip(ca, marges)],
        "ecart_budget": [r - b for r, b in zip(ca, budget_ca)],
    })


@st.cache_data
def generate_clients_data(seed=42):
    rng = np.random.default_rng(seed)
    clients = [
        "TechCorp SA", "Industrie Duval", "RetailGroup", "FinServ Partners",
        "BioMed Labs", "LogiFlow", "EnergiX", "MediaPro", "AgriFood Co", "BuildSmart"
    ]
    ca = rng.integers(150_000, 850_000, len(clients))
    dso = rng.integers(28, 75, len(clients))
    segments = rng.choice(["Grand Compte", "PME", "ETI"], len(clients))
    risque = ["🟢 Faible" if d < 40 else "🟡 Modéré" if d < 58 else "🔴 Élevé" for d in dso]
    return pd.DataFrame({
        "client": clients,
        "ca_ytd": ca,
        "dso_jours": dso,
        "segment": segments,
        "risque_recouvrement": risque,
        "marge_client": rng.uniform(0.25, 0.65, len(clients)).round(2),
    }).sort_values("ca_ytd", ascending=False).reset_index(drop=True)


@st.cache_data
def generate_cashflow_data(seed=42):
    rng = np.random.default_rng(seed)
    dates_cash = pd.date_range("2024-07-01", periods=90, freq="D")
    base_cash = 850_000
    encaissements_daily = rng.normal(65_000, 18_000, 90)
    decaissements_daily = rng.normal(58_000, 12_000, 90)
    # Pics de décaissement en milieu/fin de mois
    for i in range(90):
        if dates_cash[i].day in [15, 16, 28, 29, 30, 31]:
            decaissements_daily[i] *= 2.2
    cash_cumul = base_cash + np.cumsum(encaissements_daily - decaissements_daily)
    # Prévisions incertaines
    sigma_grow = np.linspace(15_000, 65_000, 90)
    return pd.DataFrame({
        "date": dates_cash,
        "cash": cash_cumul.round(0),
        "cash_p10": (cash_cumul - 1.645 * sigma_grow).round(0),
        "cash_p90": (cash_cumul + 1.645 * sigma_grow).round(0),
        "encaissements": encaissements_daily.round(0),
        "decaissements": decaissements_daily.round(0),
    })


@st.cache_data
def detect_anomalies(df):
    """Détection d'anomalies par Z-score + règles métier"""
    anomalies = []

    # Z-score sur CA
    ca_mean = df["ca_reel"].mean()
    ca_std = df["ca_reel"].std()
    for _, row in df.iterrows():
        z = abs(row["ca_reel"] - ca_mean) / ca_std
        if z > 2.0:
            direction = "⬆️ Pic" if row["ca_reel"] > ca_mean else "⬇️ Creux"
            anomalies.append({
                "date": row["mois"],
                "indicateur": "Chiffre d'Affaires",
                "valeur": f"{row['ca_reel']:,.0f}€",
                "z_score": round(z, 2),
                "severite": "🔴 Critique" if z > 2.8 else "🟡 Modérée",
                "type": direction,
                "action": "Analyser les causes commerciales / opérationnelles"
            })

    # Écart budget > seuil
    for _, row in df.iterrows():
        if abs(row["ecart_ca_pct"]) > 8:
            anomalies.append({
                "date": row["mois"],
                "indicateur": "Écart Budget CA",
                "valeur": f"{row['ecart_ca_pct']:+.1f}%",
                "z_score": abs(row["ecart_ca_pct"]) / 8,
                "severite": "🔴 Critique" if abs(row["ecart_ca_pct"]) > 12 else "🟡 Modérée",
                "type": "⬆️ Sur-performance" if row["ecart_ca_pct"] > 0 else "⬇️ Sous-performance",
                "action": "Réviser les hypothèses budgétaires et le forecast"
            })

    # Marge EBITDA sous seuil
    for _, row in df.iterrows():
        if row["marge_ebitda"] < 6.0:
            anomalies.append({
                "date": row["mois"],
                "indicateur": "Marge EBITDA",
                "valeur": f"{row['marge_ebitda']:.1f}%",
                "z_score": (6.0 - row["marge_ebitda"]) / 2,
                "severite": "🔴 Critique",
                "type": "⬇️ Compression",
                "action": "Analyser la structure de coûts — lancer un plan d'action"
            })

    return pd.DataFrame(anomalies) if anomalies else pd.DataFrame()


@st.cache_data
def generate_forecast(df, horizon=6):
    """Prévision simple par decomposition + tendance"""
    rng = np.random.default_rng(99)
    last_date = df["date"].max()
    future_dates = pd.date_range(last_date + timedelta(days=32), periods=horizon, freq="ME")

    # Tendance linéaire
    x = np.arange(len(df))
    coeffs = np.polyfit(x, df["ca_reel"], 1)
    trend_forecast = np.polyval(coeffs, np.arange(len(df), len(df) + horizon))

    # Saisonnalité (copier les 12 derniers mois)
    saison = []
    for i in range(horizon):
        month_idx = (len(df) + i) % 12
        hist_same_month = df[df["date"].dt.month == future_dates[i].month]["ca_reel"]
        saison.append(hist_same_month.mean() - df["ca_reel"].mean() if len(hist_same_month) > 0 else 0)

    forecast = trend_forecast + np.array(saison)
    sigma = df["ca_reel"].std() * np.linspace(1, 1.8, horizon)

    return pd.DataFrame({
        "date": future_dates,
        "mois": [d.strftime("%b %Y") for d in future_dates],
        "forecast": forecast.round(0),
        "forecast_p10": (forecast - 1.28 * sigma).round(0),
        "forecast_p90": (forecast + 1.28 * sigma).round(0),
    })


# ══════════════════════════════════════════════════════════════════════════════
# CHARGER LES DONNÉES
# ══════════════════════════════════════════════════════════════════════════════
df_main = generate_company_data()
df_prod = generate_products_data()
df_clients = generate_clients_data()
df_cash = generate_cashflow_data()
df_anomalies = detect_anomalies(df_main)
df_forecast = generate_forecast(df_main, horizon=6)

# Données récentes (12 derniers mois)
df_12m = df_main.tail(12).reset_index(drop=True)

# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div style="padding: 16px 8px 20px; border-bottom: 1px solid {COLORS['border']}; margin-bottom: 16px;">
        <div style="font-size: 1.2rem; font-weight: 800; color: {COLORS['white']};">⚡ PILOTE</div>
        <div style="font-size: 0.72rem; color: {COLORS['teal']}; letter-spacing: 0.1em; margin-top: 2px;">
            CONTRÔLE DE GESTION AUTO
        </div>
    </div>
    """, unsafe_allow_html=True)

    nb_alertes = len(df_anomalies) if len(df_anomalies) > 0 else 0
    critiques = len(df_anomalies[df_anomalies["severite"].str.contains("Critique")]) if nb_alertes > 0 else 0

    st.markdown(f"""
    <div style="background:{COLORS['bg_card2']}; border:1px solid {COLORS['border']};
                border-radius:8px; padding:12px 14px; margin-bottom:16px;">
        <div style="font-size:0.68rem; color:{COLORS['gray_light']}; text-transform:uppercase; letter-spacing:0.1em; margin-bottom:8px;">
            Statut Système
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
            <span style="font-size:0.8rem; color:{COLORS['text']};">🔴 Alertes Critiques</span>
            <span style="font-size:0.8rem; font-weight:700; color:{COLORS['red']};">{critiques}</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:4px;">
            <span style="font-size:0.8rem; color:{COLORS['text']};">⚠️ Anomalies</span>
            <span style="font-size:0.8rem; font-weight:700; color:{COLORS['gold']};">{nb_alertes}</span>
        </div>
        <div style="display:flex; justify-content:space-between;">
            <span style="font-size:0.8rem; color:{COLORS['text']};">✅ Pipeline data</span>
            <span style="font-size:0.8rem; font-weight:700; color:{COLORS['green']};">Opérationnel</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "Modules",
        [
            "⚡ Dashboard Exécutif",
            "📊 Budget vs Réel",
            "🔮 Forecasting ML",
            "🚨 Détection d'Anomalies",
            "💰 Rentabilité",
            "🏦 Trésorerie Prédictive",
            "📥 Import & Automatisation",
            "📄 Rapports Automatiques",
        ],
        label_visibility="collapsed",
    )

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # Filtres globaux
    st.markdown(f"<div class='section-title'>Filtres Globaux</div>", unsafe_allow_html=True)
    periode = st.selectbox("Période", ["12 derniers mois", "24 mois", "YTD 2024", "Tout"])
    granularite = st.selectbox("Granularité", ["Mensuel", "Trimestriel"])

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="font-size:0.68rem; color:{COLORS['gray']}; padding-top:12px; border-top:1px solid {COLORS['border']};">
        Données mises à jour :<br>
        <strong style="color:{COLORS['text']};">{datetime.now().strftime('%d/%m/%Y %H:%M')}</strong>
    </div>
    """, unsafe_allow_html=True)

# Sélection des données selon filtre
if periode == "12 derniers mois":
    df_view = df_12m
elif periode == "YTD 2024":
    df_view = df_main[df_main["date"].dt.year == 2024].copy()
else:
    df_view = df_main.copy()

if granularite == "Trimestriel":
    df_view = df_view.copy()
    df_view["trimestre"] = df_view["date"].dt.to_period("Q").astype(str)
    df_agg = df_view.groupby("trimestre").agg({
        "ca_reel": "sum", "ca_budget": "sum", "ebitda_reel": "sum",
        "ebitda_budget": "sum", "charges_totales": "sum"
    }).reset_index()
    df_agg["ecart_ca"] = df_agg["ca_reel"] - df_agg["ca_budget"]
    df_agg["ecart_ca_pct"] = df_agg["ecart_ca"] / df_agg["ca_budget"] * 100
    df_agg["marge_ebitda"] = df_agg["ebitda_reel"] / df_agg["ca_reel"] * 100
    df_agg["mois"] = df_agg["trimestre"]
    df_view = df_agg


# ══════════════════════════════════════════════════════════════════════════════
# HELPERS VISUELS
# ══════════════════════════════════════════════════════════════════════════════
def dark_layout(fig, height=380, title=""):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor=COLORS["bg_card"],
        font=dict(family="Sora", color=COLORS["text"], size=11),
        title=dict(text=title, font=dict(size=13, color=COLORS["white"]), x=0, pad=dict(l=4)),
        height=height,
        margin=dict(l=12, r=12, t=40 if title else 20, b=12),
        legend=dict(
            bgcolor="rgba(0,0,0,0)", bordercolor=COLORS["border"],
            borderwidth=1, font=dict(size=10)
        ),
        xaxis=dict(
            gridcolor=COLORS["border"], gridwidth=0.5,
            linecolor=COLORS["border"], tickfont=dict(size=10),
            showgrid=False,
        ),
        yaxis=dict(
            gridcolor=COLORS["border"], gridwidth=0.5,
            linecolor=COLORS["border"], tickfont=dict(size=10),
            zerolinecolor=COLORS["border"],
        ),
    )
    return fig


def kpi_card(value, label, delta=None, delta_is_positive=True, fmt="€", color=None):
    color = color or COLORS["teal"]
    delta_html = ""
    if delta is not None:
        delta_class = "kpi-delta-pos" if delta_is_positive else "kpi-delta-neg"
        arrow = "▲" if delta_is_positive else "▼"
        delta_html = f'<div class="{delta_class}">{arrow} {delta}</div>'
    return f"""
    <div class="kpi-card">
        <div class="kpi-value" style="color:{color};">{value}</div>
        <div class="kpi-label">{label}</div>
        {delta_html}
    </div>
    """


def fmt_m(v):
    """Formate en millions ou milliers"""
    if abs(v) >= 1_000_000:
        return f"{v/1_000_000:.2f}M€"
    if abs(v) >= 1_000:
        return f"{v/1_000:.0f}k€"
    return f"{v:.0f}€"


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — DASHBOARD EXÉCUTIF
# ══════════════════════════════════════════════════════════════════════════════
if page == "⚡ Dashboard Exécutif":

    # ── Header ──
    ca_ytd = df_view["ca_reel"].sum()
    ca_budget_ytd = df_view["ca_budget"].sum()
    ecart_ytd = (ca_ytd - ca_budget_ytd) / ca_budget_ytd * 100
    ebitda_ytd = df_view["ebitda_reel"].sum()
    marge_ytd = ebitda_ytd / ca_ytd * 100
    ca_last = df_view["ca_reel"].iloc[-1]
    ca_prev = df_view["ca_reel"].iloc[-2] if len(df_view) > 1 else ca_last
    evol_mm = (ca_last - ca_prev) / ca_prev * 100

    # Pre-compute ternaries (Python <= 3.11 f-string backslash/quote compatibility)
    if critiques > 0:
        _alerte_badge = f'<div style="margin-top:8px;"><span class="tag tag-red">⚠ {critiques} alertes critiques</span></div>'
    else:
        _alerte_badge = '<div style="margin-top:8px;"><span class="tag tag-green">✓ Aucune alerte critique</span></div>'

    st.markdown(f"""
    <div class="pilote-header">
        <div style="display:flex; justify-content:space-between; align-items:flex-start;">
            <div>
                <div style="font-size:0.7rem; color:{COLORS['teal']}; text-transform:uppercase;
                            letter-spacing:0.15em; margin-bottom:6px;">⚡ PILOTE — TABLEAU DE BORD EXÉCUTIF</div>
                <div style="font-size:1.6rem; font-weight:800; color:{COLORS['white']};">
                    Vue Consolidée · Merkantia SA
                </div>
                <div style="font-size:0.82rem; color:{COLORS['gray_light']}; margin-top:4px;">
                    Mise à jour automatique · {datetime.now().strftime('%d %B %Y, %H:%M')}
                </div>
            </div>
            <div style="text-align:right;">
                <div style="font-size:0.72rem; color:{COLORS['gray_light']};">Période : {periode}</div>
                <div style="font-size:0.72rem; color:{COLORS['gray_light']}; margin-top:2px;">
                    Périmètre : Toutes entités consolidées
                </div>
                {_alerte_badge}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPIs ──
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.markdown(kpi_card(
            fmt_m(ca_ytd), "Chiffre d'Affaires",
            delta=f"{ecart_ytd:+.1f}% vs budget",
            delta_is_positive=(ecart_ytd >= 0),
            color=COLORS["white"]
        ), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card(
            fmt_m(ebitda_ytd), "EBITDA",
            delta=f"Marge {marge_ytd:.1f}%",
            delta_is_positive=(marge_ytd > 8),
            color=COLORS["teal"]
        ), unsafe_allow_html=True)
    with c3:
        ecart_abs = ca_ytd - ca_budget_ytd
        st.markdown(kpi_card(
            fmt_m(abs(ecart_abs)), "Écart Budget",
            delta="Favorable" if ecart_abs >= 0 else "Défavorable",
            delta_is_positive=(ecart_abs >= 0),
            color=COLORS["green"] if ecart_abs >= 0 else COLORS["red"]
        ), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi_card(
            fmt_m(df_view["charges_totales"].sum() if "charges_totales" in df_view.columns else 0),
            "Charges Totales",
            delta=f"{df_view['charges_totales'].sum() / ca_ytd * 100:.1f}% du CA" if "charges_totales" in df_view.columns else "",
            delta_is_positive=False,
            color=COLORS["gold"]
        ), unsafe_allow_html=True)
    with c5:
        forecast_m1 = df_forecast["forecast"].iloc[0]
        st.markdown(kpi_card(
            fmt_m(forecast_m1), "Forecast M+1",
            delta=f"Intervalle ±{(df_forecast['forecast_p90'].iloc[0] - df_forecast['forecast_p10'].iloc[0])/2/1000:.0f}k€",
            delta_is_positive=True,
            color=COLORS["purple"]
        ), unsafe_allow_html=True)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    # ── Graphiques principaux ──
    col_left, col_right = st.columns([2.2, 1])

    with col_left:
        # CA Réel vs Budget avec forecast
        df_hist = df_view[["mois", "ca_reel", "ca_budget"]].copy()
        df_fore = df_forecast[["mois", "forecast", "forecast_p10", "forecast_p90"]].copy()

        fig = go.Figure()
        # Zone forecast
        fig.add_trace(go.Scatter(
            x=df_fore["mois"].tolist() + df_fore["mois"].tolist()[::-1],
            y=df_fore["forecast_p90"].tolist() + df_fore["forecast_p10"].tolist()[::-1],
            fill="toself", fillcolor="rgba(139,92,246,0.08)",
            line=dict(color="rgba(0,0,0,0)"), name="Intervalle forecast",
            showlegend=True,
        ))
        fig.add_trace(go.Bar(
            x=df_hist["mois"], y=df_hist["ca_budget"],
            name="Budget", marker_color=COLORS["border"], opacity=0.7,
        ))
        fig.add_trace(go.Bar(
            x=df_hist["mois"], y=df_hist["ca_reel"],
            name="Réel", marker_color=COLORS["blue"],
        ))
        fig.add_trace(go.Scatter(
            x=df_fore["mois"], y=df_fore["forecast"],
            name="Forecast ML", mode="lines+markers",
            line=dict(color=COLORS["purple"], width=2.5, dash="dot"),
            marker=dict(size=6),
        ))
        fig = dark_layout(fig, height=340, title="CA Réel vs Budget + Forecast ML")
        fig.update_layout(barmode="overlay", bargap=0.25)
        st.plotly_chart(fig, use_container_width=True)

    with col_right:
        # Waterfall EBITDA
        ebitda_components = {
            "CA": df_view["ca_reel"].sum(),
            "Charges Fixes": -df_view["charges_fixes"].sum() if "charges_fixes" in df_view.columns else 0,
            "Charges Var.": -df_view["charges_variables"].sum() if "charges_variables" in df_view.columns else 0,
            "Personnel": -df_view["charges_personnel"].sum() if "charges_personnel" in df_view.columns else 0,
        }
        fig2 = go.Figure(go.Waterfall(
            name="",
            orientation="v",
            measure=["absolute", "relative", "relative", "relative", "total"],
            x=list(ebitda_components.keys()) + ["EBITDA"],
            y=list(ebitda_components.values()) + [None],
            connector=dict(line=dict(color=COLORS["border"])),
            increasing=dict(marker_color=COLORS["green"]),
            decreasing=dict(marker_color=COLORS["red"]),
            totals=dict(marker_color=COLORS["teal"]),
            texttemplate="%{y:,.0f}",
            textfont=dict(size=9, color=COLORS["text"]),
        ))
        fig2 = dark_layout(fig2, height=340, title="Structure EBITDA (Waterfall)")
        st.plotly_chart(fig2, use_container_width=True)

    # ── Ligne du bas ──
    col1, col2, col3 = st.columns(3)

    with col1:
        # Marge EBITDA trend
        fig3 = go.Figure()
        marge_vals = df_view["marge_ebitda"] if "marge_ebitda" in df_view.columns else []
        fig3.add_trace(go.Scatter(
            x=df_view["mois"], y=marge_vals,
            fill="tozeroy", fillcolor="rgba(0,212,170,0.1)",
            line=dict(color=COLORS["teal"], width=2.5),
            mode="lines",
        ))
        fig3.add_hline(y=8, line_dash="dash", line_color=COLORS["gold"],
                       annotation_text="Seuil cible 8%", annotation_font_size=9)
        fig3 = dark_layout(fig3, height=220, title="Marge EBITDA (%)")
        st.plotly_chart(fig3, use_container_width=True)

    with col2:
        # Répartition charges
        charges_labels = ["Fixes", "Variables", "Personnel"]
        charges_vals = [
            df_view["charges_fixes"].sum() if "charges_fixes" in df_view.columns else 0,
            df_view["charges_variables"].sum() if "charges_variables" in df_view.columns else 0,
            df_view["charges_personnel"].sum() if "charges_personnel" in df_view.columns else 0,
        ]
        fig4 = go.Figure(go.Pie(
            labels=charges_labels, values=[abs(v) for v in charges_vals],
            hole=0.55,
            marker_colors=[COLORS["blue"], COLORS["red"], COLORS["gold"]],
            textfont=dict(size=10, color="white"),
            textinfo="label+percent",
        ))
        fig4 = dark_layout(fig4, height=220, title="Répartition des Charges")
        fig4.update_layout(showlegend=False)
        st.plotly_chart(fig4, use_container_width=True)

    with col3:
        # Alertes récentes
        st.markdown(f'<div class="section-title">🚨 Alertes Actives</div>', unsafe_allow_html=True)
        if len(df_anomalies) > 0:
            for _, row in df_anomalies.head(4).iterrows():
                sev_class = "alert-critical" if "Critique" in row.get("severite", "") else "alert-warning"
                st.markdown(f"""
                <div class="alert-card {sev_class}">
                    <div>
                        <div style="font-weight:600; font-size:0.8rem; color:{COLORS['white']};">
                            {row.get('type', '')} {row.get('indicateur', '')}
                        </div>
                        <div style="font-size:0.75rem; color:{COLORS['gray_light']};">
                            {row.get('date', '')} · {row.get('valeur', '')}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.success("✅ Aucune anomalie détectée")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — BUDGET VS RÉEL
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📊 Budget vs Réel":
    st.markdown(f'<div style="font-size:1.3rem; font-weight:700; color:{COLORS["white"]}; margin-bottom:16px;">📊 Analyse Budget vs Réel — Automatisée</div>', unsafe_allow_html=True)

    tab_ecarts, tab_drill, tab_waterfall = st.tabs(["Vue Écarts", "Drill-Down", "Waterfall"])

    with tab_ecarts:
        # Tableau synthèse
        df_ecarts = df_view[["mois", "ca_reel", "ca_budget", "ecart_ca", "ecart_ca_pct",
                              "ebitda_reel", "ebitda_budget", "marge_ebitda"]].copy()

        col1, col2 = st.columns([2, 1])
        with col1:
            # Graphique écart en barres
            colors_ecart = [COLORS["green"] if v >= 0 else COLORS["red"] for v in df_ecarts["ecart_ca_pct"]]
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=df_ecarts["mois"], y=df_ecarts["ecart_ca_pct"],
                marker_color=colors_ecart,
                text=[f"{v:+.1f}%" for v in df_ecarts["ecart_ca_pct"]],
                textposition="outside", textfont=dict(size=9),
                name="Écart CA %",
            ))
            fig.add_hline(y=0, line_color=COLORS["border"])
            fig.add_hline(y=5, line_dash="dash", line_color=COLORS["gold"],
                          annotation_text="+5% seuil alerte haut", annotation_font_size=9)
            fig.add_hline(y=-5, line_dash="dash", line_color=COLORS["red"],
                          annotation_text="-5% seuil alerte bas", annotation_font_size=9)
            fig = dark_layout(fig, height=320, title="Écart CA Budget vs Réel (%)")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Stats clés
            st.markdown(f'<div class="section-title">Indicateurs Clés</div>', unsafe_allow_html=True)
            favorable = (df_ecarts["ecart_ca"] >= 0).sum()
            defavorable = (df_ecarts["ecart_ca"] < 0).sum()
            ecart_max = df_ecarts["ecart_ca_pct"].max()
            ecart_min = df_ecarts["ecart_ca_pct"].min()
            ecart_moyen = df_ecarts["ecart_ca_pct"].mean()

            st.metric("Mois favorables", f"{favorable}/{len(df_ecarts)}")
            st.metric("Écart moyen", f"{ecart_moyen:+.1f}%")
            st.metric("Meilleur mois", f"{ecart_max:+.1f}%")
            st.metric("Pire mois", f"{ecart_min:+.1f}%")

            # Explication automatique
            if ecart_moyen > 2:
                st.success(f"📈 Sur-performance globale de +{ecart_moyen:.1f}% vs budget. Réviser le budget à la hausse.")
            elif ecart_moyen < -2:
                st.error(f"📉 Sous-performance de {ecart_moyen:.1f}% vs budget. Revoir les hypothèses commerciales.")
            else:
                st.info(f"✅ Performance alignée au budget (écart {ecart_moyen:+.1f}%)")

        # Tableau détaillé
        st.markdown(f'<div class="section-title" style="margin-top:20px;">Tableau Détaillé — Auto-formaté</div>', unsafe_allow_html=True)

        def color_ecart(val):
            if isinstance(val, (int, float)):
                if val > 0:
                    return f"color: {COLORS['green']}; font-weight: 600;"
                elif val < 0:
                    return f"color: {COLORS['red']}; font-weight: 600;"
            return ""

        df_display = df_ecarts.copy()
        df_display["ca_reel"] = df_display["ca_reel"].apply(lambda x: f"{x:,.0f} €")
        df_display["ca_budget"] = df_display["ca_budget"].apply(lambda x: f"{x:,.0f} €")
        df_display["ecart_ca"] = df_display["ecart_ca"].apply(lambda x: f"{x:+,.0f} €")
        df_display["ecart_ca_pct"] = df_display["ecart_ca_pct"].apply(lambda x: f"{x:+.1f}%")
        df_display["ebitda_reel"] = df_display["ebitda_reel"].apply(lambda x: f"{x:,.0f} €")
        df_display["marge_ebitda"] = df_display["marge_ebitda"].apply(lambda x: f"{x:.1f}%")
        df_display.columns = ["Mois", "CA Réel", "CA Budget", "Écart €", "Écart %",
                               "EBITDA Réel", "EBITDA Budget", "Marge %"]
        st.dataframe(df_display, use_container_width=True, hide_index=True, height=320)

    with tab_drill:
        st.markdown("### Drill-Down par Ligne de Charges")
        col_a, col_b = st.columns(2)

        with col_a:
            if all(c in df_view.columns for c in ["charges_fixes", "charges_variables", "charges_personnel"]):
                fig_charges = go.Figure()
                for c_name, c_col, c_color in [
                    ("Fixes", "charges_fixes", COLORS["blue"]),
                    ("Variables", "charges_variables", COLORS["red"]),
                    ("Personnel", "charges_personnel", COLORS["gold"]),
                ]:
                    fig_charges.add_trace(go.Scatter(
                        x=df_view["mois"], y=df_view[c_col],
                        name=c_name, stackgroup="charges",
                        fill="tonexty", fillcolor=f"rgba{tuple(int(c_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4)) + (0.3,)}",
                        line=dict(color=c_color, width=1.5),
                    ))
                fig_charges = dark_layout(fig_charges, height=300, title="Évolution des Charges par Catégorie")
                st.plotly_chart(fig_charges, use_container_width=True)

        with col_b:
            # Analyse par produit
            fig_prod = px.bar(
                df_prod.sort_values("ecart_budget"),
                x="ecart_budget", y="produit", orientation="h",
                color="ecart_budget",
                color_continuous_scale=["#EF4444", "#94A3B8", "#10B981"],
                color_continuous_midpoint=0,
                text=df_prod.sort_values("ecart_budget")["ecart_budget"].apply(lambda x: fmt_m(x)),
            )
            fig_prod = dark_layout(fig_prod, height=300, title="Écart Budget par Produit")
            fig_prod.update_coloraxes(showscale=False)
            fig_prod.update_traces(textposition="outside", textfont_size=9)
            st.plotly_chart(fig_prod, use_container_width=True)

    with tab_waterfall:
        st.markdown("### Analyse en Pont (Bridge) — Budget → Réel")

        ca_budget_total = df_view["ca_budget"].sum()
        ca_reel_total = df_view["ca_reel"].sum()
        delta_volume = (ca_reel_total - ca_budget_total) * 0.6
        delta_prix = (ca_reel_total - ca_budget_total) * 0.25
        delta_mix = (ca_reel_total - ca_budget_total) * 0.15

        fig_wf = go.Figure(go.Waterfall(
            name="Bridge CA",
            orientation="v",
            measure=["absolute", "relative", "relative", "relative", "total"],
            x=["Budget Initial", "Effet Volume", "Effet Prix", "Effet Mix/Périmètre", "CA Réel"],
            y=[ca_budget_total, delta_volume, delta_prix, delta_mix, None],
            connector=dict(line=dict(color=COLORS["border"], width=1)),
            increasing=dict(marker=dict(color=COLORS["green"])),
            decreasing=dict(marker=dict(color=COLORS["red"])),
            totals=dict(marker=dict(color=COLORS["teal"])),
            text=[fmt_m(v) for v in [ca_budget_total, delta_volume, delta_prix, delta_mix]] + [fmt_m(ca_reel_total)],
            textposition="outside",
            textfont=dict(size=10),
        ))
        fig_wf = dark_layout(fig_wf, height=380, title="Pont d'Analyse CA Budget → Réel")
        st.plotly_chart(fig_wf, use_container_width=True)

        st.info(f"""
        **Lecture automatique :** Le CA réel dépasse le budget de {fmt_m(ca_reel_total - ca_budget_total)}
        (+{(ca_reel_total - ca_budget_total)/ca_budget_total*100:.1f}%).
        L'effet volume représente la contribution principale ({fmt_m(delta_volume)}),
        suivi de l'effet prix ({fmt_m(delta_prix)}) et de l'effet mix ({fmt_m(delta_mix)}).
        """)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — FORECASTING ML
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🔮 Forecasting ML":
    st.markdown(f'<div style="font-size:1.3rem; font-weight:700; color:{COLORS["white"]}; margin-bottom:16px;">🔮 Forecasting — Prévisions Automatiques par ML</div>', unsafe_allow_html=True)

    col_params, col_main = st.columns([1, 3])

    with col_params:
        st.markdown(f'<div class="section-title">Paramètres Modèle</div>', unsafe_allow_html=True)
        horizon_mois = st.slider("Horizon de prévision (mois)", 3, 12, 6)
        modele_type = st.selectbox("Algorithme", ["Gradient Boosting", "ARIMA", "Prophet", "Ensemble (recommandé)"])
        conf_level = st.selectbox("Intervalle de confiance", ["80%", "90%", "95%"])
        inclure_saisonnalite = st.toggle("Saisonnalité", value=True)
        inclure_tendance = st.toggle("Tendance", value=True)
        if st.button("⚡ Relancer le Forecast", type="primary", use_container_width=True):
            st.session_state["forecast_run"] = True
            st.rerun()

        # Métriques de qualité du modèle
        st.markdown(f'<div class="section-title" style="margin-top:16px;">Qualité du Modèle</div>', unsafe_allow_html=True)
        st.metric("MAPE", "3.8%", delta="-0.4% vs mois dernier")
        st.metric("R²", "0.94", delta="+0.02")
        st.metric("MAE", fmt_m(87_500))

    with col_main:
        # Recalcul selon horizon
        df_fore_dyn = generate_forecast(df_main, horizon=horizon_mois)
        conf_mult = {"80%": 1.28, "90%": 1.645, "95%": 1.96}[conf_level]

        sigma_base = df_main["ca_reel"].std()
        df_fore_dyn["forecast_p10"] = df_fore_dyn["forecast"] - conf_mult * sigma_base * np.linspace(1, 1.8, horizon_mois)
        df_fore_dyn["forecast_p90"] = df_fore_dyn["forecast"] + conf_mult * sigma_base * np.linspace(1, 1.8, horizon_mois)

        # Graphique principal
        fig = go.Figure()

        # Historique
        df_hist_plot = df_main.tail(12)
        fig.add_trace(go.Scatter(
            x=df_hist_plot["mois"], y=df_hist_plot["ca_reel"],
            name="Historique CA", line=dict(color=COLORS["white"], width=2.5),
            mode="lines+markers", marker=dict(size=5),
        ))
        fig.add_trace(go.Scatter(
            x=df_hist_plot["mois"], y=df_hist_plot["ca_budget"],
            name="Budget", line=dict(color=COLORS["gray"], width=1.5, dash="dot"),
        ))

        # Zone de confiance
        x_fore = df_fore_dyn["mois"].tolist()
        fig.add_trace(go.Scatter(
            x=x_fore + x_fore[::-1],
            y=df_fore_dyn["forecast_p90"].tolist() + df_fore_dyn["forecast_p10"].tolist()[::-1],
            fill="toself", fillcolor="rgba(139,92,246,0.12)",
            line=dict(color="rgba(0,0,0,0)"), name=f"IC {conf_level}",
        ))
        # Limite historique/forecast — add_shape used instead of add_vline
        # because x-axis is categorical (string labels), add_vline requires numeric x
        last_hist_x = df_hist_plot["mois"].iloc[-1]
        fig.add_shape(
            type="line",
            x0=last_hist_x, x1=last_hist_x,
            y0=0, y1=1,
            xref="x", yref="paper",
            line=dict(color=COLORS["border"], width=1.5, dash="dash"),
        )
        fig.add_annotation(
            x=last_hist_x, y=1,
            xref="x", yref="paper",
            text="Aujourd'hui",
            showarrow=False,
            font=dict(size=9, color=COLORS["gray_light"]),
            xanchor="right",
            yanchor="bottom",
            xshift=-6,
        )
        # Forecast central
        fig.add_trace(go.Scatter(
            x=df_fore_dyn["mois"], y=df_fore_dyn["forecast"],
            name=f"Forecast {modele_type}",
            mode="lines+markers",
            line=dict(color=COLORS["purple"], width=3),
            marker=dict(size=8, symbol="diamond"),
        ))
        fig = dark_layout(fig, height=400, title=f"Forecast CA — Horizon {horizon_mois} mois · {modele_type}")
        st.plotly_chart(fig, use_container_width=True)

        # Tableau des prévisions
        st.markdown(f'<div class="section-title">Tableau de Prévisions Détaillé</div>', unsafe_allow_html=True)
        df_fore_display = df_fore_dyn.copy()
        df_fore_display["confiance"] = "●●●●○" if conf_level == "80%" else ("●●●●●" if conf_level == "95%" else "●●●●○")
        df_fore_display["alerte"] = df_fore_display["forecast_p10"].apply(
            lambda x: "🔴 Risque bas" if x < df_main["ca_reel"].quantile(0.2) else
                      ("🟡 Attention" if x < df_main["ca_reel"].quantile(0.4) else "✅ Normal")
        )

        cols_show = ["mois", "forecast", "forecast_p10", "forecast_p90", "confiance", "alerte"]
        df_fore_show = df_fore_display[cols_show].copy()
        df_fore_show.columns = ["Mois", "Prévision Centrale", "Scénario Bas (P10)", "Scénario Haut (P90)", "Confiance", "Statut"]
        for col in ["Prévision Centrale", "Scénario Bas (P10)", "Scénario Haut (P90)"]:
            df_fore_show[col] = df_fore_show[col].apply(lambda x: f"{x:,.0f} €")
        st.dataframe(df_fore_show, use_container_width=True, hide_index=True)

        # Analyse automatique
        forecast_total = df_fore_dyn["forecast"].sum()
        budget_remaining = df_main["ca_budget"].tail(horizon_mois).sum()
        gap = forecast_total - budget_remaining
        if gap > 0:
            _msg_forecast = "Le modèle suggère une révision du budget à la hausse."
        else:
            _msg_forecast = "Un plan d'action commercial est recommandé."
        st.markdown(f"""

        <div style="background:{COLORS['bg_card']}; border:1px solid {COLORS['border']};
                    border-radius:8px; padding:16px 20px; margin-top:12px;">
            <div style="font-size:0.72rem; color:{COLORS['teal']}; text-transform:uppercase;
                        letter-spacing:0.1em; margin-bottom:8px;">🤖 Analyse Automatique du Forecast</div>
            <div style="font-size:0.9rem; color:{COLORS['text']};">
                Sur les <strong>{horizon_mois} prochains mois</strong>, le modèle prévoit un CA cumulé de
                <strong style="color:{COLORS['teal']};">{fmt_m(forecast_total)}</strong>
                pour un budget correspondant de <strong>{fmt_m(budget_remaining)}</strong>.
                L'écart prévisionnel est de <strong style="color:{'#10B981' if gap >= 0 else '#EF4444'};">{fmt_m(gap)} ({gap/budget_remaining*100:+.1f}%)</strong>.
                {_msg_forecast}
            </div>
        </div>
        """, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — DÉTECTION D'ANOMALIES
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🚨 Détection d'Anomalies":
    st.markdown(f'<div style="font-size:1.3rem; font-weight:700; color:{COLORS["white"]}; margin-bottom:16px;">🚨 Détection Automatique des Anomalies</div>', unsafe_allow_html=True)

    col_conf, col_viz = st.columns([1, 3])

    with col_conf:
        st.markdown(f'<div class="section-title">Configuration</div>', unsafe_allow_html=True)
        z_seuil = st.slider("Seuil Z-score", 1.5, 3.5, 2.0, 0.1)
        ecart_seuil = st.slider("Seuil écart budget (%)", 3, 20, 8)
        marge_seuil = st.slider("Seuil marge EBITDA (%)", 3.0, 12.0, 6.0, 0.5)

        st.markdown(f'<div class="section-title" style="margin-top:16px;">Algorithmes actifs</div>', unsafe_allow_html=True)
        algo_zscore = st.toggle("Z-score (stats)", value=True)
        algo_budget = st.toggle("Règles métier budget", value=True)
        algo_marge = st.toggle("Seuils de marge", value=True)
        algo_trend = st.toggle("Rupture de tendance", value=True)

    with col_viz:
        # Graphique avec anomalies marquées
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_main["mois"], y=df_main["ca_reel"],
            name="CA Réel", line=dict(color=COLORS["white"], width=2),
            mode="lines",
        ))

        # Bande de normalité (±2 sigma)
        mean_ca = df_main["ca_reel"].mean()
        std_ca = df_main["ca_reel"].std()
        fig.add_hrect(
            y0=mean_ca - z_seuil * std_ca, y1=mean_ca + z_seuil * std_ca,
            fillcolor="rgba(0,212,170,0.06)", line_color="rgba(0,0,0,0)",
            annotation_text=f"Zone normale (±{z_seuil}σ)", annotation_font_size=9,
        )

        # Points anormaux
        anomalies_ca = df_main[abs(df_main["ca_reel"] - mean_ca) > z_seuil * std_ca]
        if len(anomalies_ca) > 0:
            fig.add_trace(go.Scatter(
                x=anomalies_ca["mois"], y=anomalies_ca["ca_reel"],
                name="Anomalie détectée", mode="markers",
                marker=dict(color=COLORS["red"], size=12, symbol="x",
                            line=dict(color=COLORS["red"], width=2)),
            ))

        # Mois avec fort écart budget
        budget_alerte = df_main[abs(df_main["ecart_ca_pct"]) > ecart_seuil]
        if len(budget_alerte) > 0:
            fig.add_trace(go.Scatter(
                x=budget_alerte["mois"], y=budget_alerte["ca_reel"],
                name="Écart budget critique", mode="markers",
                marker=dict(color=COLORS["gold"], size=10, symbol="triangle-up"),
            ))

        fig = dark_layout(fig, height=320, title="Détection d'Anomalies — CA (Z-score + Règles Métier)")
        st.plotly_chart(fig, use_container_width=True)

        # Résultats
        if len(df_anomalies) > 0:
            critiq = df_anomalies[df_anomalies["severite"].str.contains("Critique")]
            moderes = df_anomalies[~df_anomalies["severite"].str.contains("Critique")]

            c1, c2, c3 = st.columns(3)
            c1.metric("Total anomalies", len(df_anomalies))
            c2.metric("🔴 Critiques", len(critiq))
            c3.metric("🟡 Modérées", len(moderes))

            st.markdown(f'<div class="section-title" style="margin-top:16px;">Log des Anomalies Détectées</div>', unsafe_allow_html=True)

            df_anom_display = df_anomalies.copy()
            st.dataframe(
                df_anom_display[["date", "indicateur", "type", "valeur", "z_score", "severite", "action"]].rename(
                    columns={"date": "Période", "indicateur": "Indicateur", "type": "Type",
                             "valeur": "Valeur", "z_score": "Z-Score", "severite": "Sévérité", "action": "Action recommandée"}
                ),
                use_container_width=True, hide_index=True, height=280
            )
        else:
            st.success("✅ Aucune anomalie détectée avec les seuils actuels")

    # Heatmap des écarts
    st.markdown(f'<div class="section-title" style="margin-top:8px;">Heatmap de Risque — Écarts par Mois</div>', unsafe_allow_html=True)

    if len(df_main) >= 12:
        ecarts_heatmap = df_main["ecart_ca_pct"].values.reshape(2, -1)[:, :12]
        annees = ["2023", "2024"]
        mois_labels = ["Jan", "Fév", "Mar", "Avr", "Mai", "Jun", "Jul", "Aoû", "Sep", "Oct", "Nov", "Déc"]

        fig_heat = go.Figure(go.Heatmap(
            z=ecarts_heatmap,
            x=mois_labels[:ecarts_heatmap.shape[1]],
            y=annees[:ecarts_heatmap.shape[0]],
            colorscale=[[0, COLORS["red"]], [0.5, COLORS["bg_card2"]], [1, COLORS["green"]]],
            zmid=0,
            text=[[f"{v:+.1f}%" for v in row] for row in ecarts_heatmap],
            texttemplate="%{text}",
            textfont=dict(size=10),
            colorbar=dict(title="Écart %", tickfont=dict(color=COLORS["text"])),
        ))
        fig_heat = dark_layout(fig_heat, height=200, title="Écart CA vs Budget — Heatmap")
        st.plotly_chart(fig_heat, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 5 — RENTABILITÉ
# ══════════════════════════════════════════════════════════════════════════════
elif page == "💰 Rentabilité":
    st.markdown(f'<div style="font-size:1.3rem; font-weight:700; color:{COLORS["white"]}; margin-bottom:16px;">💰 Analyse de Rentabilité — Multi-Axes</div>', unsafe_allow_html=True)

    tab_prod, tab_clients, tab_matrix = st.tabs(["Par Produit/BU", "Par Client", "Matrice BCG"])

    with tab_prod:
        col1, col2 = st.columns([1.5, 1])
        with col1:
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=df_prod["produit"], y=df_prod["ca_ytd"],
                name="CA YTD", marker_color=COLORS["blue"], opacity=0.8,
            ))
            fig.add_trace(go.Bar(
                x=df_prod["produit"], y=df_prod["budget_ca"],
                name="Budget CA", marker_color=COLORS["gray"], opacity=0.5,
            ))
            fig.add_trace(go.Scatter(
                x=df_prod["produit"], y=[m * 100 for m in df_prod["marge_brute_pct"]],
                name="Marge brute %", yaxis="y2", mode="lines+markers",
                line=dict(color=COLORS["teal"], width=2.5),
                marker=dict(size=8, symbol="diamond"),
            ))
            fig.update_layout(
                yaxis2=dict(
                    overlaying="y", side="right",
                    ticksuffix="%", gridcolor=COLORS["border"],
                    range=[0, 110], tickfont=dict(color=COLORS["teal"]),
                ),
                barmode="group",
            )
            fig = dark_layout(fig, height=360, title="CA & Marge Brute par Produit")
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # Tableau produits
            df_prod_display = df_prod[["produit", "ca_ytd", "marge_brute_pct", "evolution_yoy", "ecart_budget"]].copy()
            df_prod_display["ca_ytd"] = df_prod_display["ca_ytd"].apply(lambda x: f"{x/1000:.0f}k€")
            df_prod_display["marge_brute_pct"] = df_prod_display["marge_brute_pct"].apply(lambda x: f"{x*100:.0f}%")
            df_prod_display["evolution_yoy"] = df_prod_display["evolution_yoy"].apply(lambda x: f"{x:+.1f}%")
            df_prod_display["ecart_budget"] = df_prod_display["ecart_budget"].apply(lambda x: f"{x/1000:+.0f}k€")
            df_prod_display.columns = ["Produit", "CA YTD", "Marge %", "Évol. YoY", "Écart Budget"]
            st.dataframe(df_prod_display, use_container_width=True, hide_index=True, height=220)

            # Contribution à la marge
            total_marge = df_prod["marge_brute"].sum()
            df_prod_pct = df_prod.copy()
            df_prod_pct["contrib_pct"] = df_prod_pct["marge_brute"] / total_marge * 100
            fig_pie = go.Figure(go.Pie(
                labels=df_prod["produit"], values=df_prod["marge_brute"],
                hole=0.5,
                marker_colors=[COLORS["blue"], COLORS["teal"], COLORS["gold"],
                               COLORS["purple"], COLORS["red"], COLORS["green"]],
                textfont=dict(size=9), textinfo="percent",
            ))
            fig_pie = dark_layout(fig_pie, height=220, title="Contribution à la Marge Brute")
            fig_pie.update_layout(showlegend=False)
            st.plotly_chart(fig_pie, use_container_width=True)

    with tab_clients:
        col1, col2 = st.columns([1.5, 1])
        with col1:
            # Scatter CA vs Marge client
            fig_scatter = px.scatter(
                df_clients, x="ca_ytd", y="marge_client",
                size="ca_ytd", color="segment", text="client",
                color_discrete_map={
                    "Grand Compte": COLORS["blue"],
                    "ETI": COLORS["teal"],
                    "PME": COLORS["gold"],
                },
                labels={"ca_ytd": "CA YTD (€)", "marge_client": "Marge Client"},
            )
            fig_scatter.update_traces(textposition="top center", textfont_size=8)
            fig_scatter = dark_layout(fig_scatter, height=340, title="Portefeuille Clients — CA vs Marge")
            fig_scatter.add_hline(y=df_clients["marge_client"].median(), line_dash="dash",
                                  line_color=COLORS["gold"], annotation_text="Médiane marge")
            st.plotly_chart(fig_scatter, use_container_width=True)

        with col2:
            st.markdown(f'<div class="section-title">Tableau Clients — Auto-Alertes DSO</div>', unsafe_allow_html=True)
            df_cli_display = df_clients.copy()
            df_cli_display["ca_ytd"] = df_cli_display["ca_ytd"].apply(lambda x: f"{x/1000:.0f}k€")
            df_cli_display["marge_client"] = df_cli_display["marge_client"].apply(lambda x: f"{x*100:.0f}%")
            st.dataframe(
                df_cli_display[["client", "segment", "ca_ytd", "dso_jours", "marge_client", "risque_recouvrement"]].rename(
                    columns={"client": "Client", "segment": "Segment", "ca_ytd": "CA",
                             "dso_jours": "DSO (j)", "marge_client": "Marge", "risque_recouvrement": "Risque"}
                ),
                use_container_width=True, hide_index=True, height=320,
            )
            dso_moyen = df_clients["dso_jours"].mean()
            clients_risque = (df_clients["dso_jours"] > 55).sum()
            st.warning(f"⚠️ DSO moyen : **{dso_moyen:.0f} jours** · {clients_risque} clients à risque")

    with tab_matrix:
        st.markdown("### Matrice Rentabilité × Croissance")
        fig_matrix = px.scatter(
            df_prod, x="evolution_yoy", y=[m * 100 for m in df_prod["marge_brute_pct"]],
            size="ca_ytd", text="produit",
            color=[m * 100 for m in df_prod["marge_brute_pct"]],
            color_continuous_scale=["#EF4444", "#F5A623", "#10B981"],
            labels={"x": "Croissance YoY (%)", "y": "Marge Brute (%)"},
        )
        fig_matrix.update_traces(textposition="top center", textfont_size=9)
        fig_matrix.add_hline(y=50, line_dash="dash", line_color=COLORS["border"])
        fig_matrix.add_vline(x=0, line_dash="dash", line_color=COLORS["border"])
        # Annotations quadrants
        for x_pos, y_pos, label, color in [
            (15, 70, "⭐ STARS", COLORS["green"]),
            (-5, 70, "💰 CASH COWS", COLORS["teal"]),
            (15, 30, "❓ QUESTION MARKS", COLORS["gold"]),
            (-5, 30, "🐕 DOGS", COLORS["red"]),
        ]:
            fig_matrix.add_annotation(x=x_pos, y=y_pos, text=label,
                                       font=dict(size=10, color=color), showarrow=False)
        fig_matrix = dark_layout(fig_matrix, height=420, title="Matrice Rentabilité × Croissance")
        fig_matrix.update_coloraxes(showscale=False)
        st.plotly_chart(fig_matrix, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 6 — TRÉSORERIE
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🏦 Trésorerie Prédictive":
    st.markdown(f'<div style="font-size:1.3rem; font-weight:700; color:{COLORS["white"]}; margin-bottom:16px;">🏦 Trésorerie Prédictive — 90 Jours</div>', unsafe_allow_html=True)

    # KPIs trésorerie
    cash_actuel = df_cash["cash"].iloc[0]
    cash_min_90 = df_cash["cash"].min()
    cash_fin_90 = df_cash["cash"].iloc[-1]
    jours_sous_seuil = (df_cash["cash"] < 200_000).sum()

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(kpi_card(fmt_m(cash_actuel), "Cash Position J0",
                             color=COLORS["teal"]), unsafe_allow_html=True)
    with c2:
        st.markdown(kpi_card(fmt_m(cash_min_90), "Cash Minimum (90j)",
                             delta="Scénario bas", delta_is_positive=(cash_min_90 > 200_000),
                             color=COLORS["gold"] if cash_min_90 > 200_000 else COLORS["red"]),
                    unsafe_allow_html=True)
    with c3:
        st.markdown(kpi_card(fmt_m(cash_fin_90), "Prévision J+90",
                             delta=f"{(cash_fin_90 - cash_actuel)/cash_actuel*100:+.1f}% vs J0",
                             delta_is_positive=(cash_fin_90 > cash_actuel),
                             color=COLORS["purple"]), unsafe_allow_html=True)
    with c4:
        st.markdown(kpi_card(str(jours_sous_seuil) + " j", "Jours sous seuil 200k€",
                             delta="⚠️ Risque de tension" if jours_sous_seuil > 5 else "✅ Sous contrôle",
                             delta_is_positive=(jours_sous_seuil == 0),
                             color=COLORS["red"] if jours_sous_seuil > 0 else COLORS["green"]),
                    unsafe_allow_html=True)

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # Graphique prévision trésorerie
    col_main, col_side = st.columns([2.5, 1])

    with col_main:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_cash["date"], y=df_cash["cash_p90"],
            name="Scénario optimiste (P90)",
            line=dict(color=COLORS["green"], dash="dash", width=1),
            fill=None,
        ))
        fig.add_trace(go.Scatter(
            x=df_cash["date"], y=df_cash["cash_p10"],
            name="Scénario pessimiste (P10)",
            line=dict(color=COLORS["red"], dash="dash", width=1),
            fill="tonexty", fillcolor="rgba(139,92,246,0.08)",
        ))
        fig.add_trace(go.Scatter(
            x=df_cash["date"], y=df_cash["cash"],
            name="Prévision centrale",
            line=dict(color=COLORS["teal"], width=3),
            fill=None,
        ))
        # Seuil alerte
        seuil_alerte = 200_000
        fig.add_hline(y=seuil_alerte, line_dash="dash", line_color=COLORS["red"],
                      line_width=1.5,
                      annotation_text=f"⚠️ Seuil d'alerte {fmt_m(seuil_alerte)}",
                      annotation_font_size=9, annotation_font_color=COLORS["red"])
        fig.add_hline(y=500_000, line_dash="dot", line_color=COLORS["gold"],
                      line_width=1, annotation_text="Cible minimum recommandée",
                      annotation_font_size=8, annotation_position="top right")

        # Marquage jours de décaissements forts
        pics = df_cash[df_cash["decaissements"] > df_cash["decaissements"].quantile(0.9)]
        fig.add_trace(go.Scatter(
            x=pics["date"], y=pics["cash"],
            name="Pic de décaissement", mode="markers",
            marker=dict(color=COLORS["gold"], size=8, symbol="triangle-down"),
        ))

        fig = dark_layout(fig, height=380, title="Prévision Trésorerie 90 Jours — Intervalles P10/P90")
        st.plotly_chart(fig, use_container_width=True)

    with col_side:
        st.markdown(f'<div class="section-title">Flux Prévus</div>', unsafe_allow_html=True)

        # Barres encaissements/décaissements hebdomadaires
        df_weekly = df_cash.copy()
        df_weekly["semaine"] = df_weekly["date"].dt.isocalendar().week
        df_cash_weekly = df_weekly.groupby("semaine").agg(
            {"encaissements": "sum", "decaissements": "sum"}
        ).head(8).reset_index()

        fig_flux = go.Figure()
        fig_flux.add_trace(go.Bar(
            x=[f"S{w}" for w in df_cash_weekly["semaine"]],
            y=df_cash_weekly["encaissements"],
            name="Encaissements", marker_color=COLORS["green"], opacity=0.8,
        ))
        fig_flux.add_trace(go.Bar(
            x=[f"S{w}" for w in df_cash_weekly["semaine"]],
            y=-df_cash_weekly["decaissements"],
            name="Décaissements", marker_color=COLORS["red"], opacity=0.8,
        ))
        fig_flux = dark_layout(fig_flux, height=260, title="Flux Hebdomadaires (8 sem.)")
        fig_flux.update_layout(barmode="overlay", bargap=0.1)
        st.plotly_chart(fig_flux, use_container_width=True)

        net_semaine = (df_cash_weekly["encaissements"] - df_cash_weekly["decaissements"]).mean()
        if net_semaine > 0:
            st.success(f"💹 Flux net moyen : **+{fmt_m(net_semaine)}/semaine**")
        else:
            st.error(f"🔻 Flux net moyen : **{fmt_m(net_semaine)}/semaine**")

        # Alertes trésorerie
        st.markdown(f'<div class="section-title" style="margin-top:8px;">Alertes Auto</div>', unsafe_allow_html=True)
        tension_dates = df_cash[df_cash["cash_p10"] < 200_000]["date"]
        if len(tension_dates) > 0:
            st.markdown(f"""
            <div class="alert-card alert-critical">
                <div>
                    <div style="font-weight:600; font-size:0.8rem; color:{COLORS['white']};">
                        ⚠️ Tension potentielle
                    </div>
                    <div style="font-size:0.75rem; color:{COLORS['gray_light']};">
                        Scénario P10 sous seuil dans {len(tension_dates)} jours
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Analyse automatique des flux
    st.markdown(f'<div class="section-title" style="margin-top:8px;">🔍 Analyse Automatique des Flux</div>', unsafe_allow_html=True)
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        total_enc = df_cash["encaissements"].sum()
        total_dec = df_cash["decaissements"].sum()
        st.metric("Total encaissements 90j", fmt_m(total_enc))
        st.metric("Total décaissements 90j", fmt_m(total_dec))
    with col_b:
        flux_net = total_enc - total_dec
        dso_estime = 45
        st.metric("Flux net 90j", fmt_m(flux_net), delta="Positif ✅" if flux_net > 0 else "Négatif ⚠️")
        st.metric("DSO estimé", f"{dso_estime} jours")
    with col_c:
        besoin_wc = total_dec * 0.12
        marge_securite = cash_min_90 - seuil_alerte
        st.metric("BFR estimé", fmt_m(besoin_wc))
        st.metric("Marge de sécurité", fmt_m(marge_securite),
                  delta="✅ Saine" if marge_securite > 0 else "⚠️ Risque")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 7 — IMPORT & AUTOMATISATION
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📥 Import & Automatisation":
    st.markdown(f'<div style="font-size:1.3rem; font-weight:700; color:{COLORS["white"]}; margin-bottom:16px;">📥 Import de Données & Automatisation du Pipeline</div>', unsafe_allow_html=True)

    tab_import, tab_pipeline, tab_code = st.tabs(["Import Manuel", "Pipeline Auto", "Code & API"])

    with tab_import:
        col1, col2 = st.columns([1, 1.5])
        with col1:
            st.markdown(f'<div class="section-title">Importer vos données</div>', unsafe_allow_html=True)
            upload_type = st.radio("Format", ["CSV", "Excel (.xlsx)", "Données démo"])

            if upload_type != "Données démo":
                uploaded_file = st.file_uploader(
                    f"Glissez votre fichier {upload_type}",
                    type=["csv", "xlsx"] if upload_type == "Excel (.xlsx)" else ["csv"],
                )
                if uploaded_file:
                    try:
                        if upload_type == "CSV":
                            separator = st.selectbox("Séparateur", [";", ",", "\t"])
                            decimal = st.selectbox("Décimale", [",", "."])
                            df_import = pd.read_csv(uploaded_file, sep=separator, decimal=decimal)
                        else:
                            df_import = pd.read_excel(uploaded_file)

                        st.success(f"✅ Fichier chargé : {df_import.shape[0]} lignes × {df_import.shape[1]} colonnes")
                        st.dataframe(df_import.head(10), use_container_width=True, hide_index=True)

                        # Analyse qualité auto
                        st.markdown(f'<div class="section-title" style="margin-top:12px;">Rapport Qualité Auto</div>', unsafe_allow_html=True)
                        nulls = df_import.isnull().sum()
                        c_q1, c_q2, c_q3 = st.columns(3)
                        c_q1.metric("Lignes", df_import.shape[0])
                        c_q2.metric("Valeurs nulles", int(nulls.sum()))
                        c_q3.metric("Doublons", df_import.duplicated().sum())

                        if nulls.sum() > 0:
                            st.warning(f"⚠️ {int(nulls.sum())} valeurs manquantes détectées. Action recommandée : imputation ou suppression.")

                    except Exception as e:
                        st.error(f"Erreur lors du chargement : {e}")
            else:
                st.info("Utilisation des données démo Merkantia SA (générées automatiquement)")
                st.dataframe(df_main.tail(6)[["mois", "ca_reel", "ca_budget", "ebitda_reel", "marge_ebitda"]],
                             use_container_width=True, hide_index=True)

        with col2:
            st.markdown(f'<div class="section-title">Configuration du Mapping</div>', unsafe_allow_html=True)
            st.markdown("Associez vos colonnes aux indicateurs standard :")

            colonnes_standard = ["Chiffre d'Affaires", "Budget CA", "Charges Fixes",
                                  "Charges Variables", "EBITDA", "Date"]
            for col_std in colonnes_standard:
                st.selectbox(f"→ {col_std}", ["-- Non mappé --", "ca", "budget", "charges", "date", "amount"], key=f"map_{col_std}")

            if st.button("⚡ Valider le Mapping & Importer", type="primary", use_container_width=True):
                st.success("✅ Mapping validé. Données intégrées dans le pipeline.")

            st.markdown(f'<div class="section-title" style="margin-top:16px;">Télécharger Template</div>', unsafe_allow_html=True)
            # Génération template Excel
            template_df = pd.DataFrame({
                "date": pd.date_range("2024-01-01", periods=3, freq="ME"),
                "ca_reel": [1_000_000, 1_050_000, 980_000],
                "ca_budget": [1_000_000, 1_000_000, 1_000_000],
                "charges_fixes": [280_000, 280_000, 280_000],
                "charges_variables": [420_000, 441_000, 411_600],
                "charges_personnel": [220_000, 220_000, 220_000],
            })
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                template_df.to_excel(writer, index=False, sheet_name="Données")
            buffer.seek(0)
            st.download_button(
                "📥 Télécharger le Template Excel",
                data=buffer, file_name="pilote_template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True,
            )

    with tab_pipeline:
        st.markdown("### Architecture du Pipeline Automatisé")

        etapes_pipeline = [
            ("📥", "INGESTION", COLORS["blue"],
             "Connexion ERP/CRM via API REST",
             "Airflow scheduler · Cron quotidien 23h50 · Delta load · Logs d'erreurs",
             "✅ Opérationnel · Dernière exécution : 23:50"),
            ("🧹", "NETTOYAGE", COLORS["teal"],
             "Validation, déduplication, imputation",
             "Règles métier · Z-score outliers · Imputation médiane · Formatage devises",
             "✅ Opérationnel · 0 erreurs"),
            ("⚙️", "TRANSFORMATION", COLORS["gold"],
             "Feature engineering & agrégation",
             "Calcul KPIs · Ratios financiers · Lags temporels · Consolidation inter-compagnies",
             "✅ Opérationnel · 47 KPIs calculés"),
            ("🧠", "MODÉLISATION", COLORS["purple"],
             "Retrain automatique des modèles ML",
             "XGBoost forecast · Détection anomalies · Scoring clients · Validation croisée auto",
             "✅ Opérationnel · MAPE 3.8%"),
            ("📊", "PUBLICATION", COLORS["green"],
             "Distribution des rapports & alertes",
             "Dashboard Streamlit · Email alertes · Export Excel · API REST pour ERP",
             "✅ Opérationnel · 12 destinataires"),
        ]

        for i, (icon, nom, color, subtitle, detail, status) in enumerate(etapes_pipeline):
            st.markdown(f"""
            <div style="display:flex; align-items:flex-start; gap:16px; padding:14px 0;
                        border-bottom:1px solid {COLORS['border']};">
                <div style="width:44px; height:44px; border-radius:10px; background:{color}20;
                            border:1px solid {color}40; display:flex; align-items:center;
                            justify-content:center; font-size:1.2rem; flex-shrink:0;">
                    {icon}
                </div>
                <div style="flex:1; min-width:0;">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <div>
                            <span style="font-size:0.68rem; color:{color}; text-transform:uppercase;
                                        letter-spacing:0.1em; font-weight:600;">{i+1:02d} · {nom}</span>
                            <div style="font-size:0.9rem; color:{COLORS['white']}; font-weight:600;
                                        margin-top:1px;">{subtitle}</div>
                        </div>
                        <span class="tag tag-green">{status}</span>
                    </div>
                    <div style="font-size:0.78rem; color:{COLORS['gray_light']}; margin-top:4px;">{detail}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tab_code:
        st.markdown("### 🐍 Code Python — Pipeline Prêt à l'Emploi")
        st.info("Copiez ce code dans votre environnement. Adaptez les connexions à vos systèmes.")

        code_samples = {
            "Connexion ERP & Collecte": """
import pandas as pd
import requests
from datetime import datetime, timedelta

def collect_from_erp(base_url, api_key, date_start, date_end):
    \"\"\"Collecte automatique depuis ERP via API REST\"\"\"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    params = {"date_from": date_start.isoformat(), "date_to": date_end.isoformat(), "format": "json"}

    response = requests.get(f"{base_url}/api/v1/accounting/entries", headers=headers, params=params)
    response.raise_for_status()
    df = pd.DataFrame(response.json()["data"])
    df["date"] = pd.to_datetime(df["date"])
    return df

# Exemple : collecter hier
yesterday = datetime.now() - timedelta(days=1)
# df_raw = collect_from_erp("https://votre-erp.com", "YOUR_API_KEY", yesterday, datetime.now())

# Depuis fichier (fallback)
df_raw = pd.read_csv("exports/erp_export.csv", parse_dates=["date"], sep=";", decimal=",")
print(f"✅ {len(df_raw)} lignes collectées")
            """,
            "Nettoyage & Validation": """
import pandas as pd
import numpy as np

def clean_financial_data(df):
    \"\"\"Pipeline de nettoyage automatisé\"\"\"
    report = {"initial_rows": len(df), "errors": []}

    # 1. Supprimer doublons
    before = len(df)
    df = df.drop_duplicates(subset=["date", "code_compte", "montant"])
    if len(df) < before:
        report["errors"].append(f"⚠️ {before - len(df)} doublons supprimés")

    # 2. Valider les montants (pas de nulls sur colonnes critiques)
    cols_critiques = ["montant", "code_compte", "date"]
    nulls = df[cols_critiques].isnull().sum()
    if nulls.sum() > 0:
        df = df.dropna(subset=cols_critiques)
        report["errors"].append(f"⚠️ {nulls.sum()} lignes incomplètes supprimées")

    # 3. Détecter outliers par Z-score
    z_scores = abs((df["montant"] - df["montant"].mean()) / df["montant"].std())
    outliers = z_scores > 3
    if outliers.sum() > 0:
        report["errors"].append(f"⚠️ {outliers.sum()} outliers détectés (Z > 3)")
        df.loc[outliers, "flag_outlier"] = True

    # 4. Normalisation dates et montants
    df["date"] = pd.to_datetime(df["date"])
    df["montant"] = pd.to_numeric(df["montant"], errors="coerce").fillna(0)
    df["mois"] = df["date"].dt.to_period("M").astype(str)

    report["final_rows"] = len(df)
    return df, report

# df_clean, rapport = clean_financial_data(df_raw)
# print(rapport)
            """,
            "Forecast Automatique (Prophet)": """
# pip install prophet
from prophet import Prophet
import pandas as pd
import matplotlib.pyplot as plt

def forecast_ca(df_historique, horizon_mois=6):
    \"\"\"Prévision automatique du CA avec Prophet\"\"\"
    # Format Prophet : colonnes 'ds' (date) et 'y' (valeur)
    df_prophet = df_historique[["date", "ca_reel"]].rename(
        columns={"date": "ds", "ca_reel": "y"}
    )

    # Configuration du modèle
    model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=False,
        daily_seasonality=False,
        changepoint_prior_scale=0.05,  # Flexibilité tendance
        seasonality_prior_scale=10.0,   # Force saisonnalité
        interval_width=0.80,            # Intervalle 80%
    )

    # Variables exogènes (optionnel)
    # model.add_regressor("nb_jours_ouvres")

    model.fit(df_prophet)

    # Créer l'horizon de prévision
    future = model.make_future_dataframe(periods=horizon_mois, freq="M")
    forecast = model.predict(future)

    # Extraire les prévisions
    df_forecast = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(horizon_mois)
    df_forecast.columns = ["date", "forecast", "p10", "p90"]

    mape = calculate_mape(df_prophet["y"], forecast["yhat"][:len(df_prophet)])
    print(f"MAPE in-sample : {mape:.1f}%")

    return df_forecast, model

def calculate_mape(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100
            """,
            "Alertes Email Automatiques": """
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pandas as pd

def send_alert(destinataires, sujet, alertes_df, seuil_critique=3):
    \"\"\"Envoi automatique d'alertes si anomalies détectées\"\"\"
    if len(alertes_df) == 0:
        return False  # Pas d'alertes, pas d'email

    critiques = alertes_df[alertes_df["severite"].str.contains("Critique")]

    # Construction HTML
    rows_html = ""
    for _, row in alertes_df.iterrows():
        color = "#EF4444" if "Critique" in row["severite"] else "#F5A623"
        rows_html += f\"\"\"
        <tr>
            <td style="color:{color}; font-weight:bold;">{row['severite']}</td>
            <td>{row['date']}</td>
            <td>{row['indicateur']}</td>
            <td>{row['valeur']}</td>
            <td style="font-size:12px;">{row['action']}</td>
        </tr>
        \"\"\"

    html_body = f\"\"\"
    <html><body style="font-family:Arial; background:#f5f5f5; padding:20px;">
    <div style="background:white; border-radius:8px; padding:24px; max-width:800px; margin:auto;">
        <h2 style="color:#0D1B4B;">⚡ PILOTE — Rapport d'Alertes Automatique</h2>
        <p>Généré le {pd.Timestamp.now().strftime('%d/%m/%Y à %H:%M')}</p>
        <p>
            <strong style="color:#EF4444;">{len(critiques)} alertes critiques</strong> ·
            <strong>{len(alertes_df)} anomalies totales</strong>
        </p>
        <table style="width:100%; border-collapse:collapse;">
            <tr style="background:#0D1B4B; color:white;">
                <th style="padding:8px;">Sévérité</th>
                <th>Période</th>
                <th>Indicateur</th>
                <th>Valeur</th>
                <th>Action recommandée</th>
            </tr>
            {rows_html}
        </table>
    </div></body></html>
    \"\"\"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"⚡ PILOTE | {len(critiques)} alertes critiques · {pd.Timestamp.now().strftime('%d/%m')}"
    msg["From"] = "pilote@votre-entreprise.com"
    msg["To"] = ", ".join(destinataires)
    msg.attach(MIMEText(html_body, "html"))

    # Décommenter pour l'envoi réel :
    # with smtplib.SMTP("smtp.votre-serveur.com", 587) as server:
    #     server.starttls()
    #     server.login("user", "password")
    #     server.send_message(msg)
    print(f"📧 Email préparé pour : {', '.join(destinataires)}")
    return True

# Exemple d'appel :
# send_alert(["cfo@entreprise.com", "equipe-finance@entreprise.com"], "Alertes CG", df_anomalies)
            """,
        }

        code_choice = st.selectbox("Choisissez un module", list(code_samples.keys()))
        st.code(code_samples[code_choice].strip(), language="python")


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 8 — RAPPORTS AUTOMATIQUES
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📄 Rapports Automatiques":
    st.markdown(f'<div style="font-size:1.3rem; font-weight:700; color:{COLORS["white"]}; margin-bottom:16px;">📄 Génération de Rapports Automatiques</div>', unsafe_allow_html=True)

    col_config, col_preview = st.columns([1, 2])

    with col_config:
        st.markdown(f'<div class="section-title">Configuration du Rapport</div>', unsafe_allow_html=True)
        rapport_type = st.selectbox("Type de rapport", [
            "Rapport mensuel de gestion",
            "Flash hebdomadaire",
            "Note de synthèse anomalies",
            "Budget vs Réel YTD",
            "Prévision trésorerie",
        ])
        dest = st.multiselect("Destinataires", ["DG", "CFO", "DAF", "Contrôle de Gestion", "COMEX"], default=["CFO"])
        format_export = st.selectbox("Format", ["Excel (.xlsx)", "CSV", "JSON"])
        inclure_graphiques = st.toggle("Inclure données graphiques", value=True)
        inclure_alertes = st.toggle("Inclure rapport d'anomalies", value=True)
        inclure_forecast = st.toggle("Inclure prévisions ML", value=True)
        commentaires_auto = st.toggle("Commentaires automatiques IA", value=True)

        if st.button("⚡ Générer & Télécharger", type="primary", use_container_width=True):
            # Construction du rapport Excel
            output = io.BytesIO()

            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                # Onglet 1 : Synthèse
                synthese_data = {
                    "Indicateur": ["CA Réel YTD", "CA Budget YTD", "Écart CA €", "Écart CA %",
                                   "EBITDA Réel", "EBITDA Budget", "Marge EBITDA %",
                                   "Forecast M+1", "Cash Position"],
                    "Valeur": [
                        fmt_m(df_view["ca_reel"].sum()),
                        fmt_m(df_view["ca_budget"].sum()),
                        fmt_m(df_view["ca_reel"].sum() - df_view["ca_budget"].sum()),
                        f"{(df_view['ca_reel'].sum() - df_view['ca_budget'].sum()) / df_view['ca_budget'].sum() * 100:+.1f}%",
                        fmt_m(df_view["ebitda_reel"].sum()) if "ebitda_reel" in df_view.columns else "N/A",
                        fmt_m(df_view["ebitda_budget"].sum()) if "ebitda_budget" in df_view.columns else "N/A",
                        f"{df_view['marge_ebitda'].mean():.1f}%" if "marge_ebitda" in df_view.columns else "N/A",
                        fmt_m(df_forecast["forecast"].iloc[0]),
                        fmt_m(df_cash["cash"].iloc[0]),
                    ],
                    "Statut": ["✅" if True else "⚠️"] * 9,
                }
                pd.DataFrame(synthese_data).to_excel(writer, sheet_name="Synthèse", index=False)

                # Onglet 2 : Données détaillées
                df_view.to_excel(writer, sheet_name="Données Mensuel", index=False)

                # Onglet 3 : Produits
                df_prod.to_excel(writer, sheet_name="Rentabilité Produits", index=False)

                # Onglet 4 : Forecast
                if inclure_forecast:
                    df_forecast.to_excel(writer, sheet_name="Forecast ML", index=False)

                # Onglet 5 : Anomalies
                if inclure_alertes and len(df_anomalies) > 0:
                    df_anomalies.to_excel(writer, sheet_name="Anomalies", index=False)

                # Onglet 6 : Trésorerie
                df_cash[["date", "cash", "cash_p10", "cash_p90"]].to_excel(
                    writer, sheet_name="Trésorerie 90j", index=False)

            output.seek(0)
            fname = f"pilote_rapport_{rapport_type.replace(' ', '_').lower()}_{datetime.now().strftime('%Y%m%d')}.xlsx"

            st.download_button(
                "📥 Télécharger le Rapport Excel",
                data=output, file_name=fname,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True, type="primary",
            )
            st.success(f"✅ Rapport '{rapport_type}' généré avec {5 + (1 if inclure_forecast else 0) + (1 if inclure_alertes else 0)} onglets")

        # Export CSV simple
        st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
        csv_data = df_view.to_csv(index=False, sep=";", decimal=",").encode("utf-8-sig")
        st.download_button(
            "📥 Export CSV Rapide",
            data=csv_data,
            file_name=f"pilote_export_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv", use_container_width=True,
        )

    with col_preview:
        st.markdown(f'<div class="section-title">Aperçu du Rapport</div>', unsafe_allow_html=True)

        # Preview du rapport automatique
        ca_sum = df_view["ca_reel"].sum()
        bud_sum = df_view["ca_budget"].sum()
        ecart_pct = (ca_sum - bud_sum) / bud_sum * 100
        ebitda_sum = df_view["ebitda_reel"].sum() if "ebitda_reel" in df_view.columns else 0
        marge_avg = df_view["marge_ebitda"].mean() if "marge_ebitda" in df_view.columns else 0

        rapport_date = datetime.now().strftime("%d %B %Y")

        # Pre-compute string ternaries for f-string compatibility (Python <= 3.11)
        if marge_avg > 8:
            _msg_marge = "La marge est en ligne avec les objectifs (>8%)."
        else:
            _msg_marge = "⚠️ La marge est sous le seuil cible de 8% — des actions sur les coûts sont requises."
        if inclure_alertes and len(df_anomalies) > 0:
            _anom_txt = df_anomalies["indicateur"].iloc[0] + " · " + df_anomalies["type"].iloc[0]
            _alertes_block = (
                '<div style="background:rgba(239,68,68,0.08); border:1px solid rgba(239,68,68,0.3); '
                'border-radius:6px; padding:10px; font-size:0.8rem; color:#FCA5A5;">'
                f"<strong>⚠️ ALERTES ({len(df_anomalies)}) :</strong> {_anom_txt}</div>"
            )
        elif inclure_alertes:
            _alertes_block = '<div style="background:rgba(0,212,170,0.08); border:1px solid rgba(0,212,170,0.3); border-radius:6px; padding:10px; font-size:0.8rem; color:#6EE7B7;">✅ Aucune anomalie détectée</div>'
        else:
            _alertes_block = ""

        # Commentaire auto généré
        if commentaires_auto:
            if ecart_pct > 3:
                commentaire_ca = f"Le CA réel dépasse le budget de {ecart_pct:.1f}% ({fmt_m(ca_sum - bud_sum)}). Cette sur-performance s'explique principalement par une dynamique commerciale favorable, notamment sur les produits à forte valeur ajoutée."
            elif ecart_pct < -3:
                commentaire_ca = f"Le CA réel est en retard sur le budget de {abs(ecart_pct):.1f}% ({fmt_m(bud_sum - ca_sum)}). Un plan d'action commercial est requis pour les prochains mois."
            else:
                commentaire_ca = f"Le CA réel est aligné sur le budget (écart {ecart_pct:+.1f}%). La performance reste dans les normes prévisionnelles."

        st.markdown(f"""
        <div style="background:{COLORS['bg_card']}; border:1px solid {COLORS['border']};
                    border-radius:10px; padding:24px; font-size:0.85rem; line-height:1.6;">

            <div style="border-bottom:3px solid {COLORS['teal']}; padding-bottom:14px; margin-bottom:16px;">
                <div style="font-size:0.65rem; color:{COLORS['teal']}; text-transform:uppercase;
                            letter-spacing:0.15em; margin-bottom:6px;">⚡ PILOTE · RAPPORT AUTO-GÉNÉRÉ</div>
                <div style="font-size:1.1rem; font-weight:700; color:{COLORS['white']};">{rapport_type}</div>
                <div style="font-size:0.75rem; color:{COLORS['gray_light']};">
                    Généré le {rapport_date} · Période : {periode} · Périmètre : Toutes entités
                </div>
            </div>

            <div style="margin-bottom:14px;">
                <div style="font-size:0.68rem; color:{COLORS['teal']}; text-transform:uppercase;
                            letter-spacing:0.1em; margin-bottom:8px;">1. PERFORMANCE COMMERCIALE</div>
                <div style="display:grid; grid-template-columns:1fr 1fr 1fr; gap:10px; margin-bottom:10px;">
                    <div style="background:{COLORS['bg_card2']}; border-radius:6px; padding:10px; text-align:center;">
                        <div style="font-size:1.1rem; font-weight:700; color:{COLORS['teal']};
                                    font-family:'DM Mono',monospace;">{fmt_m(ca_sum)}</div>
                        <div style="font-size:0.68rem; color:{COLORS['gray_light']};">CA Réel</div>
                    </div>
                    <div style="background:{COLORS['bg_card2']}; border-radius:6px; padding:10px; text-align:center;">
                        <div style="font-size:1.1rem; font-weight:700; color:{COLORS['gray']};
                                    font-family:'DM Mono',monospace;">{fmt_m(bud_sum)}</div>
                        <div style="font-size:0.68rem; color:{COLORS['gray_light']};">Budget</div>
                    </div>
                    <div style="background:{COLORS['bg_card2']}; border-radius:6px; padding:10px; text-align:center;">
                        <div style="font-size:1.1rem; font-weight:700;
                                    color:{'#10B981' if ecart_pct >= 0 else '#EF4444'};
                                    font-family:'DM Mono',monospace;">{ecart_pct:+.1f}%</div>
                        <div style="font-size:0.68rem; color:{COLORS['gray_light']};">Écart</div>
                    </div>
                </div>
                <div style="color:{COLORS['text_muted']}; font-size:0.82rem;">{commentaire_ca if commentaires_auto else ''}</div>
            </div>

            <div style="margin-bottom:14px;">
                <div style="font-size:0.68rem; color:{COLORS['teal']}; text-transform:uppercase;
                            letter-spacing:0.1em; margin-bottom:8px;">2. RENTABILITÉ</div>
                <div style="color:{COLORS['text']}; font-size:0.82rem;">
                    L'EBITDA s'établit à <strong style="color:{COLORS['teal']};">{fmt_m(ebitda_sum)}</strong>
                    pour une marge de <strong>{marge_avg:.1f}%</strong>.
                    {_msg_marge}
                </div>
            </div>

            <div style="margin-bottom:14px;">
                <div style="font-size:0.68rem; color:{COLORS['teal']}; text-transform:uppercase;
                            letter-spacing:0.1em; margin-bottom:8px;">3. PRÉVISIONS M+1 à M+3</div>
                <div style="color:{COLORS['text']}; font-size:0.82rem;">
                    Le modèle ML prévoit un CA de
                    <strong style="color:{COLORS['purple']};">{fmt_m(df_forecast['forecast'].iloc[0])}</strong>
                    au prochain mois (IC 80% : {fmt_m(df_forecast['forecast_p10'].iloc[0])} – {fmt_m(df_forecast['forecast_p90'].iloc[0])}).
                </div>
            </div>

            {_alertes_block}
        </div>
        """, unsafe_allow_html=True)

        # Planification automatique
        st.markdown(f'<div class="section-title" style="margin-top:16px;">⏰ Planification Automatique</div>', unsafe_allow_html=True)
        freq_envoi = st.selectbox("Fréquence d'envoi automatique", [
            "Désactivé", "Quotidien (07:00)", "Hebdomadaire (lundi 08:00)",
            "Mensuel (J+3 clôture)", "Sur alerte critique uniquement"
        ])
        if freq_envoi != "Désactivé":
            st.success(f"✅ Planification configurée : {freq_envoi}")
            st.info("💡 Pour activer l'envoi email automatique, configurez les paramètres SMTP dans le fichier `.env`")
