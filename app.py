import streamlit as st

# ----- CONFIG -----
st.set_page_config(page_title="DISCIPLINEDTRADE", layout="wide")

# ----- THEME SOMBRE + STYLE DU HEADER COMPACT -----
dark_css = """
<style>
    body {
        background-color: #141414; /* noir mais pas trop foncé */
    }

    /* Conteneur header compact dans la sidebar */
    .sidebar-header-compact {
        display: flex;
        align-items: center;
        gap: 10px;
        justify-content: flex-start; /* start pour rester parallèle avec la flèche */
        padding-top: 0px;            /* <-- changé : remonté */
        padding-bottom: 6px;
        width: 100%;
        white-space: nowrap; /* une seule ligne */
    }

    /* Petit logo triangle */
    .triangle-logo {
        width   : 0 ;
        height  : 0 ;
        border-left: 8px solid transparent;
        border-right: 8px solid transparent;
        border-bottom: 18px solid #ff4d4d; /* couleur rouge clair */
        filter: drop-shadow(-2px 2px 3px rgba(0,0,0,0.6)); /* ombre côté gauche */
        transform: translateY(5px); /* léger ajustement vertical */
    }

    /* Texte compact du nom de l'app - une seule ligne */
    .app-name-compact {
        font-size: 16px;   /* plus petit et compact */
        font-weight: 800;
        letter-spacing: 0.6px;
        color: #ffffff;
        display: inline-flex;
        align-items: center;
        transform: translateY(-4px); /* <-- ajouté : ajuste finement la position vers le haut */
    }

    /* "TRADE" en dégradé rouge clair */
    .app-name-compact .trade {
        margin-left: 2px;
        background: linear-gradient(90deg, #ffb3b3, #ff4d4d);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 900;
    }

    /* Petit padding pour la sidebar afin d'éviter que la flèche Streamlit ne chevauche */
    [data-testid="stSidebar"] > div:first-child {
        padding-top: 6px;
        padding-left: 10px;
    }
</style>
"""
st.markdown(dark_css, unsafe_allow_html=True)

# ----- SIDEBAR -----
with st.sidebar:
    # Header compact (logo + nom sur une ligne)
    st.markdown(
        """
        <div class="sidebar-header-compact">
            <div class="triangle-logo"></div>
            <div class="app-name-compact">DISCIPLINED<span class="trade">TRADE</span></div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Menu (reste inchangé)
    st.write("Dashboard")
    st.write("Journal")
    st.write("Playbook")
    st.write("Notes")
    st.write("Settings")
