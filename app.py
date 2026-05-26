# =========================================================
# NON AWB MANUAL MATCH V1
# SPX STYLE UI + MOBILE + DESKTOP
# FULL VERSION
# =========================================================

import streamlit as st
import pandas as pd
from rapidfuzz import fuzz
from urllib.parse import quote

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="NON AWB MANUAL MATCH V1",
    page_icon="📦",
    layout="wide"
)

# =========================================================
# MOBILE DETECTOR
# =========================================================

mobile = st.query_params.get("mobile")

if mobile == "1":
    IS_MOBILE = True
else:
    IS_MOBILE = False

# =========================================================
# SPX CSS UI
# =========================================================

st.markdown("""

<style>

/* ===================================================== */
/* GLOBAL */
/* ===================================================== */

html, body, [class*="css"] {

    background-color: #FFF7F2;
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

.spx-header {

    background: linear-gradient(
        90deg,
        #EE4D2D,
        #FF6B3D
    );

    padding: 20px;
    border-radius: 18px;
    color: white;
    margin-bottom: 20px;

    box-shadow: 0px 5px 15px rgba(0,0,0,0.1);

}

.spx-title {

    font-size: 32px;
    font-weight: bold;

}

.spx-subtitle {

    opacity: 0.9;
    margin-top: 5px;

}

/* ===================================================== */
/* METRIC */
/* ===================================================== */

div[data-testid="metric-container"] {

    background: white;
    border-radius: 14px;
    padding: 15px;
    border: 2px solid #FFE1D9;

}

/* ===================================================== */
/* BUTTON */
/* ===================================================== */

.stButton > button {

    background-color: #EE4D2D;
    color: white;
    border-radius: 10px;
    border: none;

}

.stDownloadButton > button {

    background-color: #EE4D2D;
    color: white;
    border-radius: 10px;
    border: none;

}

/* ===================================================== */
/* SEARCH */
/* ===================================================== */

input {

    border-radius: 10px !important;

}

/* ===================================================== */
/* MOBILE */
/* ===================================================== */

@media (max-width: 768px) {

    .spx-title {

        font-size: 22px;

    }

}

</style>

""", unsafe_allow_html=True)

# =========================================================
# HEADER UI
# =========================================================

device_text = (
    "📱 Mobile Mode"
    if IS_MOBILE
    else "💻 Desktop Mode"
)

st.markdown(f"""

<div class="spx-header">

<div class="spx-title">
📦 NON AWB MANUAL MATCH V1
</div>

<div class="spx-subtitle">
SPX Internal Warehouse Tools
</div>

<div style="margin-top:8px;">
{device_text}
</div>

</div>

""", unsafe_allow_html=True)

# =========================================================
# FILE UPLOAD
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

        "👕 Fashion": [

            "celana",
            "baju",
            "hoodie",
            "kaos",
            "sepatu",
            "kemeja",
            "tas"

        ],

        "📱 Elektronik": [

            "hp",
            "laptop",
            "monitor",
            "tv",
            "mouse",
            "keyboard"

        ],

        "🍳 Rumah Tangga": [

            "rice cooker",
            "gelas",
            "blender",
            "kompor",
            "ember"

        ],

        "🪑 Furniture": [

            "lemari",
            "meja",
            "kursi",
            "rak"

        ],

        "🧰 Peralatan Kerja": [

            "tool",
            "bor",
            "obeng",
            "safety",
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

    best_category = max(
        scores,
        key=scores.get
    )

    if scores[best_category] == 0:

        return "📦 Lainnya"

    return best_category

# =========================================================
# BULKY DETECTOR
# =========================================================

def detect_bulky(text):

    text = str(text).lower()

    bulky_keywords = [

        "lemari",
        "meja",
        "kursi",
        "rak",
        "tv",
        "monitor",
        "kipas"

    ]

    for keyword in bulky_keywords:

        if keyword in text:

            return "📦 Bulky"

    return "📮 Non Bulky"

# =========================================================
# SMART SEARCH
# =========================================================

def smart_search_dataframe(dataframe, search):

    if not search:
        return dataframe

    search_text = search.lower()

    shortcuts = {

        "cd": "celana dalam",
        "hp": "handphone",
        "tv": "television"

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

        if similarity >= 70:
            return True

        return False

    filtered = dataframe[
        dataframe.apply(
            smart_search,
            axis=1
        )
    ]

    return filtered

# =========================================================
# MAIN APP
# =========================================================

if uploaded_file:

    try:

        if uploaded_file.name.endswith(".csv"):

            df = pd.read_csv(uploaded_file)

        else:

            df = pd.read_excel(uploaded_file)

        df.columns = [

            str(col).strip()

            for col in df.columns

        ]

    except Exception as e:

        st.error(f"Error membaca file: {e}")
        st.stop()

    # =====================================================
    # AUTO AI SORT
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

    df["Bulky_Type"] = df.astype(str).apply(

        lambda row: detect_bulky(
            " ".join(map(str, row))
        ),

        axis=1
    )

    # =====================================================
    # METRICS
    # =====================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Rows",
            len(df)
        )

    with col2:

        st.metric(
            "Kategori",
            df["AI_Category"].nunique()
        )

    with col3:

        st.metric(
            "Bulky",
            len(
                df[
                    df["Bulky_Type"] == "📦 Bulky"
                ]
            )
        )

    st.divider()

    # =====================================================
    # SEARCH
    # =====================================================

    search = st.text_input(
        "🔍 Smart Search SKU / AWB"
    )

    filtered_df = smart_search_dataframe(
        df,
        search
    )

    # =====================================================
    # FILTER CATEGORY
    # =====================================================

    categories = sorted(
        filtered_df["AI_Category"]
        .unique()
    )

    selected_category = st.multiselect(
        "🧠 Filter Category",
        categories
    )

    if selected_category:

        filtered_df = filtered_df[
            filtered_df["AI_Category"]
            .isin(selected_category)
        ]

    # =====================================================
    # FILTER BULKY
    # =====================================================

    bulky_filter = st.multiselect(

        "📦 Filter Bulky",

        [

            "📦 Bulky",
            "📮 Non Bulky"

        ]

    )

    if bulky_filter:

        filtered_df = filtered_df[
            filtered_df["Bulky_Type"]
            .isin(bulky_filter)
        ]

    st.divider()

    # =====================================================
    # RESULT TABLE
    # =====================================================

    st.subheader("📋 Shipment Result")

    st.write(
        f"Total Result: {len(filtered_df)}"
    )

    table_height = (
        400
        if IS_MOBILE
        else 650
    )

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=table_height
    )

    st.divider()

    # =====================================================
    # QUICK SEARCH ITEM
    # =====================================================

    st.subheader(
        "🔥 Quick Search Item"
    )

    possible_columns = [

        "sku_name",
        "model_name",
        "product_name",
        "item_name"

    ]

    search_column = None

    for col in possible_columns:

        if col in filtered_df.columns:

            search_column = col
            break

    if search_column:

        limit_show = (
            5
            if IS_MOBILE
            else 15
        )

        for index, row in filtered_df.head(limit_show).iterrows():

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

                if IS_MOBILE:

                    st.link_button(
                        "🔎 Google",
                        google_url,
                        use_container_width=True
                    )

                    st.link_button(
                        "🛒 Shopee",
                        shopee_url,
                        use_container_width=True
                    )

                    st.link_button(
                        "🖼 Images",
                        image_url,
                        use_container_width=True
                    )

                else:

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
        "Upload XLSX / CSV dulu 🔥"
    )
