# =========================================================
# NON AWB MANUAL MATCH V2 ENTERPRISE UI
# SPX STYLE DASHBOARD
# MOBILE + DESKTOP RESPONSIVE
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
    page_title="NON AWB MANUAL MATCH V2",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CSS UI
# =========================================================

st.markdown("""

<style>

/* ===================================================== */
/* GLOBAL */
/* ===================================================== */

html, body, [class*="css"] {

    background-color: #F6F6F6;
    font-family: sans-serif;

}

.block-container {

    padding-top: 1rem;
    padding-bottom: 1rem;
    padding-left: 1rem;
    padding-right: 1rem;

}

/* ===================================================== */
/* HEADER */
/* ===================================================== */

.main-header {

    background: linear-gradient(
        90deg,
        #EE4D2D,
        #FF6B3D
    );

    padding: 20px;
    border-radius: 18px;
    color: white;
    margin-bottom: 20px;

    box-shadow: 0 5px 15px rgba(0,0,0,0.1);

}

.main-title {

    font-size: 32px;
    font-weight: bold;

}

.main-sub {

    opacity: 0.9;

}

/* ===================================================== */
/* CARD */
/* ===================================================== */

.metric-card {

    background: white;
    padding: 18px;
    border-radius: 18px;

    box-shadow:
    0 2px 10px rgba(0,0,0,0.05);

    border: 1px solid #EEEEEE;

}

/* ===================================================== */
/* BUTTON */
/* ===================================================== */

.stButton > button {

    background-color: #EE4D2D;
    color: white;
    border: none;
    border-radius: 10px;

}

.stDownloadButton > button {

    background-color: #EE4D2D;
    color: white;
    border: none;
    border-radius: 10px;

}

/* ===================================================== */
/* SEARCH */
/* ===================================================== */

input {

    border-radius: 12px !important;

}

/* ===================================================== */
/* MOBILE */
/* ===================================================== */

@media (max-width: 768px) {

    .main-title {

        font-size: 22px;

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
📦 NON AWB MANUAL MATCH V2
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
# CATEGORY DETECTOR
# =========================================================

def detect_category(text):

    text = str(text).lower()

    categories = {

        "Fashion": [

            "celana",
            "baju",
            "hoodie",
            "kaos",
            "sepatu",
            "kemeja"

        ],

        "Elektronik": [

            "hp",
            "tv",
            "monitor",
            "laptop",
            "mouse"

        ],

        "Rumah Tangga": [

            "kompor",
            "gelas",
            "blender",
            "rice cooker"

        ],

        "Furniture": [

            "lemari",
            "rak",
            "kursi",
            "meja"

        ],

        "Peralatan Kerja": [

            "tool",
            "bor",
            "obeng",
            "kabel"

        ]

    }

    scores = {}

    for category, keywords in categories.items():

        score = 0

        for keyword in keywords:

            if keyword in text:

                score += 1

        scores[category] = score

    best = max(
        scores,
        key=scores.get
    )

    if scores[best] == 0:

        return "Lainnya"

    return best

# =========================================================
# BULKY DETECTOR
# =========================================================

def detect_bulky(text):

    text = str(text).lower()

    bulky_keywords = [

        "lemari",
        "rak",
        "kursi",
        "meja",
        "tv",
        "monitor"

    ]

    for keyword in bulky_keywords:

        if keyword in text:

            return "Bulky"

    return "Non Bulky"

# =========================================================
# SMART SEARCH
# =========================================================

def smart_search_dataframe(dataframe, search):

    if not search:
        return dataframe

    search_text = search.lower()

    shortcuts = {

        "cd": "celana dalam",
        "hp": "handphone"

    }

    for short, full in shortcuts.items():

        if short in search_text:

            search_text = search_text.replace(
                short,
                full
            )

    def smart_search(row):

        row_text = " ".join(
            map(str, row)
        ).lower()

        if search_text in row_text:
            return True

        similarity = fuzz.partial_ratio(
            search_text,
            row_text
        )

        return similarity >= 70

    return dataframe[
        dataframe.apply(
            smart_search,
            axis=1
        )
    ]

# =========================================================
# MAIN APP
# =========================================================

if uploaded_file:

    # =====================================================
    # READ FILE
    # =====================================================

    if uploaded_file.name.endswith(".csv"):

        df = pd.read_csv(uploaded_file)

    else:

        df = pd.read_excel(uploaded_file)

    df.columns = [

        str(col).strip()

        for col in df.columns

    ]

    # =====================================================
    # AI CATEGORY
    # =====================================================

    st.success(
        "🔥 AI sedang menyortir data..."
    )

    df["AI_Category"] = df.astype(str).apply(

        lambda row: detect_category(
            " ".join(map(str, row))
        ),

        axis=1
    )

    # =====================================================
    # BULKY
    # =====================================================

    df["Bulky_Type"] = df.astype(str).apply(

        lambda row: detect_bulky(
            " ".join(map(str, row))
        ),

        axis=1
    )

    # =====================================================
    # KPI
    # =====================================================

    total_rows = len(df)

    total_category = df["AI_Category"].nunique()

    total_bulky = len(
        df[
            df["Bulky_Type"] == "Bulky"
        ]
    )

    total_non_bulky = len(
        df[
            df["Bulky_Type"] == "Non Bulky"
        ]
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.markdown(f"""

        <div class="metric-card">

        <h4>Total Data</h4>
        <h2>{total_rows:,}</h2>

        </div>

        """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"""

        <div class="metric-card">

        <h4>Kategori</h4>
        <h2>{total_category}</h2>

        </div>

        """, unsafe_allow_html=True)

    with col3:

        st.markdown(f"""

        <div class="metric-card">

        <h4>Bulky</h4>
        <h2>{total_bulky:,}</h2>

        </div>

        """, unsafe_allow_html=True)

    with col4:

        st.markdown(f"""

        <div class="metric-card">

        <h4>Non Bulky</h4>
        <h2>{total_non_bulky:,}</h2>

        </div>

        """, unsafe_allow_html=True)

    st.divider()

    # =====================================================
    # SEARCH
    # =====================================================

    search = st.text_input(
        "🔍 Cari SKU / Resi / Produk"
    )

    filtered_df = smart_search_dataframe(
        df,
        search
    )

    # =====================================================
    # FILTER
    # =====================================================

    col1, col2 = st.columns(2)

    with col1:

        category_filter = st.multiselect(

            "🧠 Filter Category",

            filtered_df["AI_Category"]
            .unique()

        )

    with col2:

        bulky_filter = st.multiselect(

            "📦 Filter Bulky",

            filtered_df["Bulky_Type"]
            .unique()

        )

    if category_filter:

        filtered_df = filtered_df[
            filtered_df["AI_Category"]
            .isin(category_filter)
        ]

    if bulky_filter:

        filtered_df = filtered_df[
            filtered_df["Bulky_Type"]
            .isin(bulky_filter)
        ]

    st.divider()

    # =====================================================
    # CHARTS
    # =====================================================

    chart1, chart2 = st.columns(2)

    with chart1:

        category_count = (
            filtered_df["AI_Category"]
            .value_counts()
            .reset_index()
        )

        category_count.columns = [
            "Category",
            "Count"
        ]

        fig = px.pie(

            category_count,

            names="Category",
            values="Count",
            hole=0.5

        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with chart2:

        bulky_count = (
            filtered_df["Bulky_Type"]
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
            hole=0.5

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

        filtered_df,

        use_container_width=True,
        height=600

    )

    st.divider()

    # =====================================================
    # QUICK SEARCH
    # =====================================================

    st.subheader("🔥 Quick Google Search")

    possible_columns = [

        "sku_name",
        "model_name",
        "product_name"

    ]

    search_column = None

    for col in possible_columns:

        if col in filtered_df.columns:

            search_column = col
            break

    if search_column:

        for index, row in filtered_df.head(10).iterrows():

            sku = str(
                row[search_column]
            )

            encoded = quote(sku)

            google_url = (
                f"https://www.google.com/search?q={encoded}"
            )

            shopee_url = (
                f"https://shopee.co.id/search?keyword={encoded}"
            )

            image_url = (
                f"https://www.google.com/search?tbm=isch&q={encoded}"
            )

            with st.expander(
                f"📦 {sku[:80]}"
            ):

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.link_button(
                        "🔎 Google",
                        google_url,
                        use_container_width=True
                    )

                with col2:

                    st.link_button(
                        "🛒 Shopee",
                        shopee_url,
                        use_container_width=True
                    )

                with col3:

                    st.link_button(
                        "🖼 Images",
                        image_url,
                        use_container_width=True
                    )

    st.divider()

    # =====================================================
    # DOWNLOAD
    # =====================================================

    csv = filtered_df.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(

        "⬇ Download CSV",

        csv,

        "NON_AWB_RESULT.csv",

        "text/csv",

        use_container_width=True

    )

else:

    st.info(
        "📂 Upload XLSX / CSV dulu"
    )
