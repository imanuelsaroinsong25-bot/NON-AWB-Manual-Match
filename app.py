# =========================================================
# NON AWB MANUAL MATCH V3 - SPX ENTERPRISE UI
# FULL MODERN UI + MOBILE RESPONSIVE
# =========================================================

import streamlit as st
import pandas as pd
from rapidfuzz import fuzz
from urllib.parse import quote
import plotly.express as px

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="NON AWB MANUAL MATCH V3",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# HIDE STREAMLIT
# =========================================================

hide_streamlit = """
<style>

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

</style>
"""

st.markdown(hide_streamlit, unsafe_allow_html=True)

# =========================================================
# FULL CSS
# =========================================================

st.markdown("""

<style>

/* ===================================================== */
/* GLOBAL */
/* ===================================================== */

html, body, [class*="css"] {

    font-family: 'Segoe UI', sans-serif;
    background: #f5f5f5;

}

.block-container {

    padding-top: 1rem;
    padding-bottom: 0rem;
    padding-left: 1.5rem;
    padding-right: 1.5rem;

}

/* ===================================================== */
/* SIDEBAR */
/* ===================================================== */

[data-testid="stSidebar"] {

    background: white;
    border-right: 1px solid #eeeeee;

}

/* ===================================================== */
/* HEADER */
/* ===================================================== */

.main-header {

    background:
    linear-gradient(
        90deg,
        #EE4D2D,
        #FF6B3D
    );

    padding: 25px;

    border-radius: 24px;

    color: white;

    margin-bottom: 20px;

    box-shadow:
    0 10px 30px rgba(0,0,0,0.08);

}

.main-title {

    font-size: 36px;
    font-weight: 800;

}

.main-sub {

    opacity: 0.95;
    margin-top: 6px;

}

/* ===================================================== */
/* KPI CARD */
/* ===================================================== */

.kpi-card {

    background: white;

    border-radius: 22px;

    padding: 22px;

    border: 1px solid #f0f0f0;

    box-shadow:
    0 3px 12px rgba(0,0,0,0.04);

    transition: 0.3s;

}

.kpi-card:hover {

    transform: translateY(-3px);

}

.kpi-title {

    color: #777;
    font-size: 14px;

}

.kpi-value {

    font-size: 34px;
    font-weight: 700;

    margin-top: 10px;

    color: #111;

}

/* ===================================================== */
/* SEARCH BAR */
/* ===================================================== */

input {

    border-radius: 15px !important;
    border: 1px solid #e5e5e5 !important;

    padding: 12px !important;

}

/* ===================================================== */
/* BUTTON */
/* ===================================================== */

.stButton > button {

    background:
    linear-gradient(
        90deg,
        #EE4D2D,
        #FF6B3D
    );

    color: white;

    border: none;

    border-radius: 14px;

    font-weight: 600;

    transition: 0.2s;

}

.stButton > button:hover {

    transform: scale(1.02);

}

/* ===================================================== */
/* DATAFRAME */
/* ===================================================== */

[data-testid="stDataFrame"] {

    border-radius: 20px;
    overflow: hidden;
    border: 1px solid #f0f0f0;

}

/* ===================================================== */
/* MOBILE */
/* ===================================================== */

@media (max-width: 768px) {

    .main-title {

        font-size: 22px;

    }

    .kpi-value {

        font-size: 24px;

    }

    .block-container {

        padding-left: 0.8rem;
        padding-right: 0.8rem;

    }

}

</style>

""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.image(
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0e/Shopee_Express_logo.svg/2560px-Shopee_Express_logo.svg.png",
        width=180
    )

    st.markdown("## 📦 MENU")

    menu = st.radio(
        "",
        [
            "🏠 Dashboard",
            "📦 Shipment",
            "🧠 AI Category",
            "📮 Bulky Check",
            "🔎 Google Search",
            "📥 Export"
        ]
    )

# =========================================================
# HEADER
# =========================================================

st.markdown("""

<div class="main-header">

<div class="main-title">
📦 NON AWB MANUAL MATCH V3
</div>

<div class="main-sub">
SPX Internal Warehouse Tools
</div>

</div>

""", unsafe_allow_html=True)

# =========================================================
# UPLOAD
# =========================================================

uploaded_file = st.file_uploader(
    "📂 Upload XLSX / CSV",
    type=["xlsx", "csv"]
)

# =========================================================
# CATEGORY AI
# =========================================================

def detect_category(text):

    text = str(text).lower()

    categories = {

        "Fashion": [
            "baju","celana","kaos",
            "hoodie","sepatu","kemeja"
        ],

        "Elektronik": [
            "hp","laptop","tv",
            "monitor","mouse"
        ],

        "Furniture": [
            "lemari","rak","kursi","meja"
        ],

        "Rumah Tangga": [
            "gelas","blender",
            "rice cooker","kompor"
        ],

        "Peralatan Kerja": [
            "bor","obeng",
            "tool","kabel"
        ]

    }

    scores = {}

    for cat, keys in categories.items():

        score = 0

        for k in keys:

            if k in text:
                score += 1

        scores[cat] = score

    best = max(scores, key=scores.get)

    if scores[best] == 0:
        return "Lainnya"

    return best

# =========================================================
# BULKY
# =========================================================

def detect_bulky(text):

    text = str(text).lower()

    bulky = [
        "lemari",
        "rak",
        "kursi",
        "meja",
        "tv"
    ]

    for b in bulky:

        if b in text:
            return "Bulky"

    return "Non Bulky"

# =========================================================
# SMART SEARCH
# =========================================================

def smart_search(df, search):

    if not search:
        return df

    search = search.lower()

    shortcut = {

        "cd":"celana dalam",
        "hp":"handphone"

    }

    for k,v in shortcut.items():

        search = search.replace(k,v)

    def check(row):

        row_text = " ".join(
            map(str,row)
        ).lower()

        if search in row_text:
            return True

        score = fuzz.partial_ratio(
            search,
            row_text
        )

        return score >= 70

    return df[
        df.apply(
            check,
            axis=1
        )
    ]

# =========================================================
# MAIN
# =========================================================

if uploaded_file:

    # =====================================================
    # READ FILE
    # =====================================================

    if uploaded_file.name.endswith(".csv"):

        df = pd.read_csv(uploaded_file)

    else:

        df = pd.read_excel(uploaded_file)

    # =====================================================
    # CLEAN
    # =====================================================

    df.columns = [
        str(c).strip()
        for c in df.columns
    ]

    # =====================================================
    # AI SORTING
    # =====================================================

    st.success("🔥 AI sedang menyortir kategori...")

    df["AI_Category"] = df.astype(str).apply(

        lambda row:
        detect_category(
            " ".join(map(str,row))
        ),

        axis=1

    )

    df["Bulky_Type"] = df.astype(str).apply(

        lambda row:
        detect_bulky(
            " ".join(map(str,row))
        ),

        axis=1

    )

    # =====================================================
    # KPI
    # =====================================================

    total = len(df)

    bulky = len(
        df[df["Bulky_Type"]=="Bulky"]
    )

    non_bulky = len(
        df[df["Bulky_Type"]=="Non Bulky"]
    )

    category = df["AI_Category"].nunique()

    c1,c2,c3,c4 = st.columns(4)

    with c1:

        st.markdown(f"""

        <div class="kpi-card">

        <div class="kpi-title">
        TOTAL DATA
        </div>

        <div class="kpi-value">
        {total:,}
        </div>

        </div>

        """, unsafe_allow_html=True)

    with c2:

        st.markdown(f"""

        <div class="kpi-card">

        <div class="kpi-title">
        CATEGORY
        </div>

        <div class="kpi-value">
        {category}
        </div>

        </div>

        """, unsafe_allow_html=True)

    with c3:

        st.markdown(f"""

        <div class="kpi-card">

        <div class="kpi-title">
        BULKY
        </div>

        <div class="kpi-value">
        {bulky:,}
        </div>

        </div>

        """, unsafe_allow_html=True)

    with c4:

        st.markdown(f"""

        <div class="kpi-card">

        <div class="kpi-title">
        NON BULKY
        </div>

        <div class="kpi-value">
        {non_bulky:,}
        </div>

        </div>

        """, unsafe_allow_html=True)

    st.write("")

    # =====================================================
    # SEARCH
    # =====================================================

    search = st.text_input(
        "🔍 Cari SKU / Resi / Produk"
    )

    filtered = smart_search(df, search)

    # =====================================================
    # FILTER
    # =====================================================

    f1,f2 = st.columns(2)

    with f1:

        cat_filter = st.multiselect(
            "🧠 Filter Category",
            filtered["AI_Category"].unique()
        )

    with f2:

        bulky_filter = st.multiselect(
            "📦 Filter Bulky",
            filtered["Bulky_Type"].unique()
        )

    if cat_filter:

        filtered = filtered[
            filtered["AI_Category"]
            .isin(cat_filter)
        ]

    if bulky_filter:

        filtered = filtered[
            filtered["Bulky_Type"]
            .isin(bulky_filter)
        ]

    st.divider()

    # =====================================================
    # CHART
    # =====================================================

    g1,g2 = st.columns(2)

    with g1:

        cat_count = (
            filtered["AI_Category"]
            .value_counts()
            .reset_index()
        )

        cat_count.columns = [
            "Category",
            "Count"
        ]

        fig = px.pie(
            cat_count,
            names="Category",
            values="Count",
            hole=0.6
        )

        fig.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="white",
            height=450
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with g2:

        bulky_count = (
            filtered["Bulky_Type"]
            .value_counts()
            .reset_index()
        )

        bulky_count.columns = [
            "Type",
            "Count"
        ]

        fig2 = px.pie(
            bulky_count,
            names="Type",
            values="Count",
            hole=0.6
        )

        fig2.update_layout(
            paper_bgcolor="white",
            plot_bgcolor="white",
            height=450
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    st.divider()

    # =====================================================
    # TABLE
    # =====================================================

    st.subheader("📋 Shipment Data")

    st.dataframe(
        filtered,
        use_container_width=True,
        height=650
    )

    # =====================================================
    # GOOGLE SEARCH
    # =====================================================

    st.divider()

    st.subheader("🔎 Quick Search")

    possible = [
        "sku_name",
        "model_name",
        "product_name"
    ]

    search_col = None

    for c in possible:

        if c in filtered.columns:
            search_col = c
            break

    if search_col:

        for i,row in filtered.head(10).iterrows():

            sku = str(row[search_col])

            encoded = quote(sku)

            google = (
                f"https://www.google.com/search?q={encoded}"
            )

            shopee = (
                f"https://shopee.co.id/search?keyword={encoded}"
            )

            image = (
                f"https://www.google.com/search?tbm=isch&q={encoded}"
            )

            with st.expander(f"📦 {sku[:90]}"):

                b1,b2,b3 = st.columns(3)

                with b1:
                    st.link_button(
                        "🔎 Google",
                        google,
                        use_container_width=True
                    )

                with b2:
                    st.link_button(
                        "🛒 Shopee",
                        shopee,
                        use_container_width=True
                    )

                with b3:
                    st.link_button(
                        "🖼 Images",
                        image,
                        use_container_width=True
                    )

    # =====================================================
    # DOWNLOAD
    # =====================================================

    st.divider()

    csv = filtered.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(

        "⬇ DOWNLOAD RESULT",

        csv,

        "NON_AWB_RESULT.csv",

        "text/csv",

        use_container_width=True

    )

else:

    st.info("📂 Upload XLSX / CSV dulu")
