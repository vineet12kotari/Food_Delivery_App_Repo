#IMPORTS

import streamlit as st
import pandas as pd
import snowflake.connector
import plotly.express as px
import plotly.graph_objects as go
from datetime import date
from io import BytesIO
import base64, tempfile
import plotly.io as pio
import os


#THEME TOGGLE (Light / Dark Mode)

if "theme" not in st.session_state:
    st.session_state["theme"] = "light"

def switch_theme():
    st.session_state["theme"] = "dark" if st.session_state["theme"] == "light" else "light"

st.sidebar.markdown("---")
if st.sidebar.button("🌙 Switch to Dark Mode" if st.session_state["theme"] == "light" else "🌞 Switch to Light Mode"):
    switch_theme()
    st.rerun()

theme_mode = st.session_state["theme"]


# PROFESSIONAL BLUE-GREEN THEME (DARK MODE & LIGHT MODE)

if theme_mode == "dark":
    bg = "#0B1120"
    ink = "#E2E8F0"
    muted = "#94A3B8"
    card = "#1E293B"
    kpi_bg = "#1B2A44"
    border = "#334155"
    brand = "#1E40AF"       # dark blue
    accent = "#22C55E"      # light green
    header_grad = "linear-gradient(90deg, #1E3A8A 0%, #1E40AF 50%, #1D4ED8 100%)"
else:
    bg = "#F8FAFC"
    ink = "#1E293B"
    muted = "#64748B"
    card = "#FFFFFF"
    kpi_bg = "#F1F5F9"
    border = "#E2E8F0"
    brand = "#0A66C2"
    accent = "#059669"      # dark green
    header_grad = "linear-gradient(90deg, #0A66C2 0%, #2563EB 100%)"


# GLOBAL UI STYLING

st.markdown(f"""
<style>
body, .stApp {{
  background-color: {bg};
  color: {ink};
  transition: background-color 0.4s ease, color 0.4s ease;
}}
.stTabs [data-baseweb="tab-list"] {{
  display: flex; flex-wrap: nowrap; overflow-x: auto; white-space: nowrap;
  scroll-behavior: smooth; gap: 6px; background: {card};
  padding: 8px 12px; border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}}
.stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {{
  height: 6px;
}}
.stTabs [data-baseweb="tab-list"]::-webkit-scrollbar-thumb {{
  background-color: {brand}; border-radius: 10px;
}}
.stTabs [data-baseweb="tab"] {{
  background: {bg}; color: {muted}; border: 1px solid {border};
  border-radius: 10px; padding: 8px 14px; flex: 0 0 auto;
  transition: all 0.25s ease-in-out;
}}
.stTabs [data-baseweb="tab"]:hover {{
  color: {brand}; border-color: {brand};
}}
.stTabs [aria-selected="true"] {{
  background: {brand}; color: white; font-weight: 700;
  box-shadow: 0 4px 10px rgba(59,130,246,0.3);
}}
.header {{
  background: {header_grad}; color: white; border-radius: 16px;
  padding: 18px 22px; box-shadow: 0 6px 18px rgba(0,0,0,0.15);
  margin-bottom: 18px;
}}
.kpi {{
  background: {kpi_bg}; border: 1px solid {border};
  border-radius: 14px; padding: 14px 16px;
  box-shadow: 0 6px 14px rgba(0,0,0,0.08);
}}
.kpi-label {{ color: {muted}; font-size:13px; font-weight:700; }}
.kpi-value {{ font-size:26px; font-weight:800; color: {accent}; }}
.kpi-sub {{ font-size:12px; color: {muted}; margin-top:4px; }}
.card {{
  background: {card}; border: 1px solid {border};
  border-radius: 14px; padding: 16px 16px 8px 16px;
  box-shadow: 0 6px 16px rgba(2,12,27,0.06);
}}
.section-title {{
  margin: 6px 0 8px 2px; padding-left: 10px;
  border-left: 4px solid {brand}; color: {ink};
  font-weight: 800;
}}
.insight {{
  border-left: 4px solid {accent};
  background: rgba(34,197,94,0.15);
  color: {accent}; padding: 12px; border-radius: 10px;
  font-size: 14px; margin-bottom: 6px; font-weight: 500;
}}
section[data-testid="stSidebar"] {{
  background: {card}; border-right: 1px solid {border};
}}
.block-container {{
  padding-top: 0.5rem !important; padding-left: 1rem !important;
  padding-right: 1rem !important; max-width: 100% !important;
}}
</style>
""", unsafe_allow_html=True)



# 🌓 THEME TOGGLE (Light / Dark Mode)

if "theme" not in st.session_state:
    st.session_state["theme"] = "light"

# This line ensures theme_mode is defined for the subsequent logic
theme_mode = st.session_state["theme"]

# Initialize plotly_template with a safe default to prevent NameError if logic flow is interrupted
plotly_template = "plotly_white" 

# Using a set of highly contrasting colors for lines/pies/bars
plotly_colors_contrasting = [
    "#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", 
    "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"
]

# --- PLOTLY TEMPLATE DEFINITIONS ---

if theme_mode == "dark":
    # Dark Mode Colors (Re-defined for clarity, assuming they are set globally)
    bg = "#0B1120"
    ink = "#E2E8F0"
    border = "#334155"
    
    # Define Dark Template
    pio.templates["custom_dark"] = go.layout.Template(
        layout=go.Layout(
            paper_bgcolor=bg, 
            plot_bgcolor="#1E293B",
            font=dict(color=ink, family="Inter, sans-serif"),
            title=dict(font=dict(color="#F8FAFC", size=18)),
            xaxis=dict(showgrid=True, gridcolor=border, zeroline=False),
            yaxis=dict(showgrid=True, gridcolor=border, zeroline=False),
            colorway=plotly_colors_contrasting
        )
    )
    plotly_template = "custom_dark"
    
else:
    # Light Mode Colors (Re-defined for clarity, assuming they are set globally)
    bg = "#F8FAFC"
    ink = "#1E293B"
    border = "#E2E8F0"

    # Define Light Template
    pio.templates["custom_light"] = go.layout.Template(
        layout=go.Layout(
            paper_bgcolor=bg, 
            plot_bgcolor="#FFFFFF",
            font=dict(color=ink, family="Inter, sans-serif"),
            title=dict(font=dict(color="#0F172A", size=18)),
            xaxis=dict(showgrid=True, gridcolor=border, zeroline=False),
            yaxis=dict(showgrid=True, gridcolor=border, zeroline=False),
            colorway=plotly_colors_contrasting
        )
    )
    plotly_template = "custom_light"

# Set the default template for all subsequent Plotly charts
pio.templates.default = plotly_template


# UI HELPERS 

def _ensure_defined(name):
    return name in globals() and callable(globals()[name])

if not _ensure_defined("banner"):
    def banner(title: str, subtitle: str):
        st.markdown(f"""
        <div class="card" style="
            background:linear-gradient(90deg,#0A66C2 0%,#125ea7 60%,#0A66C2 100%);
            color:white;border:none;padding:20px 24px;margin-bottom:16px;
            border-radius:16px;box-shadow:0 4px 12px rgba(0,0,0,0.25);">
            <h1 style="margin:0;font-size:26px;font-weight:800;">{title}</h1>
            <p style="margin:4px 0 0 0;opacity:.95;">{subtitle}</p>
        </div>
        """, unsafe_allow_html=True)

if not _ensure_defined("kpi_tile"):
    def kpi_tile(label, value, subtitle):
        st.markdown(f"""
        <div class="kpi">
          <div class="kpi-label">{label}</div>
          <div class="kpi-value">{value}</div>
          <div class="kpi-sub" style="font-size:12px;">{subtitle}</div>
        </div>
        """, unsafe_allow_html=True)

if not _ensure_defined("start_card"):
    def start_card(title: str, info: str = ""):
        info_html = f"<span style='color:var(--muted);font-size:13px;'>({info})</span>" if info else ""
        st.markdown(f"<div class='card'><h3 style='font-weight:800;'>{title} {info_html}</h3>", unsafe_allow_html=True)

if not _ensure_defined("end_card"):
    def end_card():
        st.markdown("</div>", unsafe_allow_html=True)


#HELPERS


def fmt_number(x):
    """Standardized formatter for all KPIs and charts."""
    try:
        x = float(x)
        if abs(x) >= 1_000_000_000:
            return f"{x/1_000_000_000:.2f}B"
        elif abs(x) >= 1_000_000:
            return f"{x/1_000_000:.2f}M"
        elif abs(x) >= 1_000:
            return f"{x/1_000:.2f}K"
        else:
            return f"{x:.2f}"
    except:
        return "0.00"

def fmt_money(x):
    """Currency formatter consistent with fmt_number."""
    try:
        x = float(x)
        if abs(x) >= 1_000_000_000:
            return f"₹{x/1_000_000_000:.2f}B"
        elif abs(x) >= 1_000_000:
            return f"₹{x/1_000_000:.2f}M"
        elif abs(x) >= 1_000:
            return f"₹{x/1_000:.2f}K"
        else:
            return f"₹{x:.2f}"
    except:
        return "₹0.00"

def fmt_int(x):
    try:
        return fmt_number(x)
    except:
        return "0"

def calc_share(series):
    total = series.sum()
    return (series / total * 100).round(2) if total else pd.Series([0]*len(series))

def safe_to_datetime(s):
    return pd.to_datetime(s, errors="coerce")


# HELPER COMPONENTS FOR DASHBOARD UI


def banner(title: str, subtitle: str):
    """Stylized header banner for each tab."""
    st.markdown(f"""
    <div class="card" style="
        background:linear-gradient(90deg,#0A66C2 0%,#125ea7 60%,#0A66C2 100%);
        color:white;border:none;padding:20px 24px;margin-bottom:16px;
        border-radius:16px;box-shadow:0 4px 12px rgba(0,0,0,0.25);">
        <h1 style="margin:0;font-size:26px;font-weight:800;">{title}</h1>
        <p style="margin:4px 0 0 0;opacity:.95;">{subtitle}</p>
    </div>
    """, unsafe_allow_html=True)


def kpi_tile(label, value, subtitle):
    """Renders a uniform KPI tile with title, value, and description."""
    st.markdown(f"""
    <div class="kpi">
      <div class="kpi-label">{label}</div>
      <div class="kpi-value">{value}</div>
      <div class="kpi-sub" style="font-size:12px;">{subtitle}</div>
    </div>
    """, unsafe_allow_html=True)


def start_card(title: str, info: str = ""):
    """Begin a visual card container."""
    info_html = f"<span style='color:var(--muted);font-size:13px;'>({info})</span>" if info else ""
    st.markdown(f"<div class='card'><h3 style='font-weight:800;'>{title} {info_html}</h3>", unsafe_allow_html=True)


def end_card():
    """Close a card container."""
    st.markdown("</div>", unsafe_allow_html=True)

def get_selected_filters():
    """
    Get the current selections from sidebar filters.
    """
    return {
        "city": selected_city,
        "restaurant": selected_rest,
        "cuisine": selected_cuisine,
        "date_range": (start_date, end_date)
    }


def generate_filtered_data(filters):
    """
    Dynamically generates separate filtered DataFrames based on
    whichever filter (city, cuisine, or restaurant) has multiple selections.
    """
    city_filter = filters["city"]
    rest_filter = filters["restaurant"]
    cuisine_filter = filters["cuisine"]
    start_date, end_date = filters["date_range"]

    base_query = """
        SELECT * FROM V_PLATFORM_PROFITABILITY
        WHERE ORDER_TIMESTAMP BETWEEN '{start}' AND '{end}'
    """.format(start=start_date, end=end_date)

    # Append remaining filters
    if cuisine_filter:
        base_query += " AND CUISINE_TYPE IN (" + ", ".join(f"'{x}'" for x in cuisine_filter) + ")"
    if rest_filter:
        base_query += " AND RESTAURANT_NAME IN (" + ", ".join(f"'{x}'" for x in rest_filter) + ")"
    if city_filter:
        base_query += " AND CITY IN (" + ", ".join(f"'{x}'" for x in city_filter) + ")"

    # Detect main comparison dimension
    if len(city_filter) > 1:
        main_field = "CITY"
        loop_values = city_filter
    elif len(cuisine_filter) > 1:
        main_field = "CUISINE_TYPE"
        loop_values = cuisine_filter
    elif len(rest_filter) > 1:
        main_field = "RESTAURANT_NAME"
        loop_values = rest_filter
    else:
        main_field = None
        loop_values = ["All Data"]

    # Generate one dataset per selected value
    data_dict = {}
    for val in loop_values:
        q = base_query
        if main_field:
            q += f" AND {main_field} = '{val}'"
        df = run_query(q)
        data_dict[val] = df

    return data_dict




# SNOWFLAKE CONNECTION 

@st.cache_resource
def init_connection():
    # If using Streamlit in Snowflake, use the native connection for security
    # We will still load st.secrets to check for configuration, but not for connection itself.
    
    try:
        # Check if the native Snowpark session is available (typical in Streamlit in Snowflake)
        # We rely on the automatic connection established by the environment.
        session = st.connection("snowflake").session()
        st.info("Connected successfully using native Snowpark connection.")
        return session
        
    except Exception as e:
        # Fallback for when st.connection fails or if we are connecting to a different/external account.
        st.warning(f"Native connection failed. Attempting connection via secrets. Error: {e}")
        
        try:
            # Attempt to load credentials from the [snowflake] section of secrets.toml
            creds = st.secrets["snowflake"]
        except KeyError:
            st.error("Snowflake credentials not found in st.secrets.")
            return None 

        # If secrets are available, use snowflake.connector
        return snowflake.connector.connect(
            user=creds["user"], 
            password=creds["password"], 
            account=creds["account"], 
            warehouse=creds["warehouse"],
            database=creds["database"],
            schema=creds["schema"]
        )

conn = init_connection()

# Check if connection failed (due to missing secrets or failed connection attempt)
if conn is None:
    st.stop()



# QUERY RUNNER (UPDATED for Snowpark Session compatibility)

@st.cache_data(ttl=600)
def run_query(q):
    global conn # Use the global connection object

    # 1. Check if the connection object is a Snowpark Session (returned by st.connection)
    if hasattr(conn, 'sql'):
        # --- Handle Snowpark Session (Recommended for Streamlit in Snowflake) ---
        
        # Execute the query and collect the results as a list of Snowpark Rows
        snowpark_df = conn.sql(q)
        rows = snowpark_rows = snowpark_df.collect()
        
        # Get column names from the Snowpark DataFrame structure
        cols = [col.name for col in snowpark_df.schema.fields]
        
        # Convert Snowpark Rows to a list of lists for pandas DataFrame creation
        data = [[r[col] for col in cols] for r in rows]
        
        return pd.DataFrame(data, columns=cols)
    
    # 2. Fallback to Traditional Python Connector (Returned by snowflake.connector.connect)
    else:
        # --- Handle Traditional Python Connector ---
        cur = conn.cursor()
        cur.execute(q)
        rows, cols = cur.fetchall(), [d[0] for d in cur.description]
        cur.close()
        return pd.DataFrame(rows, columns=cols)


# SIDEBAR FILTERS

with st.sidebar:
    st.markdown("### 🔍 Filter Your Insights")

    city_list = run_query("SELECT DISTINCT CITY FROM V_PLATFORM_PROFITABILITY;")["CITY"].tolist()
    rest_list = run_query("SELECT DISTINCT RESTAURANT_NAME FROM V_PLATFORM_PROFITABILITY;")["RESTAURANT_NAME"].tolist()
    cuisine_list = run_query("SELECT DISTINCT CUISINE_TYPE FROM V_PLATFORM_PROFITABILITY;")["CUISINE_TYPE"].tolist()

    selected_city = st.multiselect("🏙️ City", city_list)
    selected_rest = st.multiselect("🍽️ Restaurant", rest_list)
    selected_cuisine = st.multiselect("🍱 Cuisine", cuisine_list)


    mind = run_query("SELECT MIN(ORDER_TIMESTAMP) AS MIN_DATE FROM V_PLATFORM_PROFITABILITY;")["MIN_DATE"][0]
    maxd = run_query("SELECT MAX(ORDER_TIMESTAMP) AS MAX_DATE FROM V_PLATFORM_PROFITABILITY;")["MAX_DATE"][0]

    try:
        mind_date, maxd_date = pd.to_datetime(mind).date(), pd.to_datetime(maxd).date()
    except:
        mind_date, maxd_date = date(2020, 1, 1), date.today()

    start_date, end_date = st.date_input(
        "📅 Order Date Range",
        value=(mind_date, maxd_date),
        min_value=mind_date,
        max_value=maxd_date
    )


#  FILTER WHERE CLAUSES

def base_where_simple():
    f = []
    if selected_city:
        f.append("CITY IN (" + ", ".join([f"'{x}'" for x in selected_city]) + ")")
    if selected_rest:
        f.append("RESTAURANT_NAME IN (" + ", ".join([f"'{x}'" for x in selected_rest]) + ")")
    if selected_cuisine:
        f.append("CUISINE_TYPE IN (" + ", ".join([f"'{x}'" for x in selected_cuisine]) + ")")
    if start_date and end_date:
        f.append(f"ORDER_TIMESTAMP BETWEEN '{start_date}' AND '{end_date}'")
    return " WHERE " + " AND ".join(f) if f else ""


#  HELPER: GET COMPARISON DIMENSION (Needed to resolve NameError)

def get_comparison_dimension():
    """
    Determines the field to use for grouping/coloring charts based on which
    multi-select filter has been applied (City, Cuisine, or Restaurant).
    Priority: City > Cuisine > Restaurant.
    """
    # NOTE: This relies on the global sidebar variables (selected_city, etc.)
    if selected_city and len(selected_city) > 0 and len(selected_city) > 1:
        return "CITY"
    if selected_cuisine and len(selected_cuisine) > 0 and len(selected_cuisine) > 1:
        return "CUISINE_TYPE"
    if selected_rest and len(selected_rest) > 0 and len(selected_rest) > 1:
        return "RESTAURANT_NAME"
    return None

    
def base_where_joined():
    f = []
    if selected_city:
        f.append("R.CITY IN (" + ", ".join([f"'{x}'" for x in selected_city]) + ")")
    if selected_rest:
        f.append("R.RESTAURANT_NAME IN (" + ", ".join([f"'{x}'" for x in selected_rest]) + ")")
    if selected_cuisine:
        f.append("R.CUISINE_TYPE IN (" + ", ".join([f"'{x}'" for x in selected_cuisine]) + ")")
    if start_date and end_date:
        f.append(f"O.ORDER_TIMESTAMP BETWEEN '{start_date}' AND '{end_date}'")
    return " WHERE " + " AND ".join(f) if f else ""


#TABS 

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📰 Portal Summary", # <-- NEW TAB 1
    "🚀 Executive Dashboard", # <-- Old Tab 1 is now Tab 2
    "🍽️ Restaurant Deep Dive", # <-- Old Tab 2 is now Tab 3
    "🧠 AI Analyst", # <-- Old Tab 3 is now Tab 4
    "👥 Customer Insights", # <-- Old Tab 4 is now Tab 5
    "🧩 Conclusion & Recommendations" # <-- Old Tab 5 is now Tab 6
])



# TAB 1: PORTAL SUMMARY (Cortex AI Driven)

with tab1:
    banner(
        "📰 Food Delivery Analytics Portal Summary",
        "A brief overview of the dashboard's objective and underlying data structure."
    )

    st.markdown("### 🤖 Portal Overview (Generated by Cortex AI)")
    
   
    cortex_prompt = """
    You are an AI Analyst summarizing a Snowflake-based analytics portal for food delivery.
    The portal is designed to analyze **Platform Profitability, Restaurant Performance, and Customer Loyalty**.

    The underlying data structure includes the following main tables:
    1. DIM_CUSTOMER: Customer demographics, join dates.
    2. DIM_RESTAURANT: Restaurant details, cuisine type, ratings, and commission rates.
    3. FACT_ORDERS: Order transactions, total GMV, Delivery Fees, Commission Revenue, Discount Amount, Net Profit.
    4. FACT_ORDER_ITEMS: Links orders to specific menu items and quantities.

    Provide a concise, engaging summary (max 200 words) of the portal's purpose and the key insights the user will gain from analyzing this data.
    """
    
    @st.cache_data(ttl=3600) 
    def get_cortex_summary(prompt):
        """Fetches the dynamic summary text using Snowflake Cortex AI."""
        
        
        safe_prompt = prompt.replace("'", "''")

        cortex_query = f"""
            SELECT SNOWFLAKE.CORTEX.COMPLETE('llama3-8b', '{safe_prompt}') AS SUMMARY;
        """
        try:
            result_df = run_query(cortex_query)
            if not result_df.empty and result_df.iloc[0]['SUMMARY']:
                return result_df.iloc[0]['SUMMARY']
            return "AI summary failed to load or returned empty content."
        except Exception as e:
          
            st.error(f"Failed to fetch summary from Cortex AI. Error: {e}")
            return None

    summary_text = get_cortex_summary(cortex_prompt)
    
    if summary_text:
        
        st.markdown(f"""
            <div style="background: {card}; border-left: 5px solid {brand}; padding: 15px; border-radius: 10px; margin-top: 10px;">
                <p style="font-size: 16px; line-height: 1.6;">{summary_text}</p>
            </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    st.markdown("### 📊 Dashboard Structure & Objectives")
    st.markdown("""
        This portal provides a multi-dimensional view of the food delivery business. Use the tabs to navigate:
        
        * **Executive Dashboard (Tab 2):** High-level **financial (GMV, Profit)** and operational KPIs, with powerful **side-by-side comparison** of Cities, Cuisines, or Restaurants.
        * **Restaurant Deep Dive (Tab 3):** Detailed analysis of restaurant profitability, commission impact, menu category performance, and rating correlation with order volume.
        * **Cortex AI Executive Q&A (Tab 4):** Ask your business question — Cortex AI generates SQL, executes it live, analyzes results, and **summarizes insights** in natural language.
        * **Customer Insights (Tab 5):** Key metrics on **customer loyalty, repeat rate, monthly activity**, and satisfaction distribution.
        * **Strategic Conclusion & Recommendations (Tab 6):** An executive overview combining insights from all dashboards with **data-backed next actions** for strategic planning.
        
        All data is securely sourced from the **Snowflake Data Cloud**, ensuring real-time accuracy and performance.
    """)
    st.markdown("---")


#TAB 2: EXECUTIVE DASHBOARD (Aggregated View with Dynamic Multi-Line Chart)

with tab2:
    banner(
        "🚀 Executive Dashboard",
        "Operational insights and profitability overview powered by Snowflake"
    )

   
    st.markdown("""
    <div style="background: rgba(255, 165, 0, 0.1); padding: 10px; border-radius: 8px; border: 1px solid #FFA500; margin-bottom: 15px;">
        ⚠️ **Cross-Filter Warning:** Applying filters (City/Cuisine/Restaurant) may result in errors if the selections are contradictory (e.g., selecting a restaurant not found in the chosen city). Clear one filter before applying a dependency.
    </div>
    """, unsafe_allow_html=True)
    
  
    top_n = st.slider("Select Top N records for charts:", 3, 20, 10, key="tab2_agg_top_n_final")


   
    where_clause = base_where_simple()
    data_query = f"SELECT * FROM V_PLATFORM_PROFITABILITY {where_clause}"
    df = run_query(data_query)
    
    if df.empty:
        st.warning("No data found for selected filters.")
    else:
        
        df.columns = [c.upper() for c in df.columns]
        df["GMV"] = pd.to_numeric(df["GMV"], errors="coerce")
        df["NET_PROFIT"] = pd.to_numeric(df["NET_PROFIT"], errors="coerce")
        df["ORDER_TIMESTAMP"] = safe_to_datetime(df["ORDER_TIMESTAMP"])
        df["MONTH"] = df["ORDER_TIMESTAMP"].dt.to_period("M").astype(str)
        
        
        comparison_dim = get_comparison_dimension()
        bar_group_col = comparison_dim if comparison_dim else "CITY"

        
        total_gmv = df["GMV"].sum()
        total_orders = df["ORDER_ID"].nunique()
        total_net_profit = df["NET_PROFIT"].sum()
        avg_order_value = total_gmv / total_orders if total_orders else 0
        profit_margin = (total_net_profit / total_gmv * 100) if total_gmv else 0

        st.markdown('<h2 class="section-title">Executive KPIs</h2>', unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        with c1: kpi_tile("💰 Total GMV", fmt_money(total_gmv), "Gross Merchandise Value")
        with c2: kpi_tile("🛒 Total Orders", fmt_int(total_orders), "Unique Orders")
        with c3: kpi_tile("🧾 Avg Order Value", fmt_money(avg_order_value), "GMV / Orders")
        with c4: kpi_tile("📈 Profit Margin", f"{profit_margin:.2f} %", "Net Profit / GMV")

        st.markdown('<h2 class="section-title">Trends & Breakdowns</h2>', unsafe_allow_html=True)
        
        
        
        # 1. MONTHLY GMV TREND 
     
        
        start_card(f"📅 Monthly GMV Trend (Grouped by {comparison_dim.replace('_', ' ').title() if comparison_dim else 'Overall'})", "Tracks month-over-month revenue trajectory")
        
        grouping_cols = ["MONTH"]
        color_col = None
        
        if comparison_dim and df[comparison_dim].nunique() > 1:
            grouping_cols.append(comparison_dim)
            color_col = comparison_dim
        
        monthly_trend = df.groupby(grouping_cols, as_index=False)["GMV"].sum().round(2)
        
        fig1 = px.line(monthly_trend, 
                       x="MONTH", 
                       y="GMV", 
                       color=color_col, 
                       markers=True, 
                       template=plotly_template)

        fig1.update_traces(line=dict(width=3))
        fig1.update_layout(height=400, margin=dict(l=8, r=8, t=30, b=8), yaxis_tickformat='s')
        
      
        st.plotly_chart(fig1, use_container_width=True, key="exec_trend_line") 
       
        end_card()


        
        # 2. ORDER SHARE BY PRIMARY DIMENSION (PIE CHART)
       
        start_card(f"🏙️ Top {top_n} Order Share by {bar_group_col.replace('_', ' ').title()}", "Distribution of order volume across segments")
        
        order_share = (
            df.groupby(bar_group_col, as_index=False)["ORDER_ID"]
            .nunique()
            .rename(columns={"ORDER_ID": "ORDERS"})
            .sort_values("ORDERS", ascending=False)
            .head(top_n) 
        )
        
        if not order_share.empty:
            fig2 = px.pie(order_share, names=bar_group_col, values="ORDERS", hole=0.45, template=plotly_template)
            fig2.update_layout(height=400, margin=dict(l=8, r=8, t=30, b=8))
           
            st.plotly_chart(fig2, use_container_width=True, key="exec_order_pie") 
          
        else:
            st.info("No order share data found for this grouping.")
        end_card()

       
        # 3. GMV ANALYSIS BY PRIMARY DIMENSION (Bar Chart)
        
        start_card(f"💰 Top {top_n} {bar_group_col.replace('_', ' ').title()} by GMV", "Where sales value is concentrated")
        
        group_gmv = (
            df.groupby(bar_group_col, as_index=False)["GMV"]
            .sum()
            .sort_values("GMV", ascending=False)
            .head(top_n) 
        )
        
        if not group_gmv.empty:
            fig_gmv = px.bar(group_gmv, 
                             x=bar_group_col, 
                             y="GMV", 
                             text=group_gmv["GMV"].apply(fmt_money),
                             template=plotly_template)
            fig_gmv.update_traces(textposition='outside')
            fig_gmv.update_layout(height=400, margin=dict(l=8, r=8, t=8, b=8), yaxis_tickformat='s')
           
            st.plotly_chart(fig_gmv, use_container_width=True, key="exec_gmv_bar")
           
        else:
            st.info("No GMV data found for this grouping.")
        end_card()
        
      
        # 4. PROFIT COMPARISON BY PRIMARY DIMENSION (Bar Chart)
        
        start_card(f"💹 Top {top_n} {bar_group_col.replace('_', ' ').title()} by Net Profit", "Ranking segments based on total net profit")
        
        group_profit = (
            df.groupby(bar_group_col, as_index=False)["NET_PROFIT"]
            .sum()
            .sort_values("NET_PROFIT", ascending=False)
            .head(top_n) 
        )
        
        if not group_profit.empty:
            fig_profit = px.bar(group_profit, 
                             x=bar_group_col, 
                             y="NET_PROFIT", 
                             text=group_profit["NET_PROFIT"].apply(fmt_money),
                             template=plotly_template)
            fig_profit.update_traces(textposition='outside')
            fig_profit.update_layout(height=400, margin=dict(l=8, r=8, t=8, b=8), yaxis_tickformat='s')
            
            st.plotly_chart(fig_profit, use_container_width=True, key="exec_profit_bar")
          
        else:
            st.info("No Net Profit data found for this grouping.")
        end_card()

#TAB 3
        
with tab3:
    banner("🍽️ Restaurant Deep Dive", "Profitability, ratings, cuisine performance, and commission dynamics")

    
    st.markdown("""
    <div style="background: rgba(255, 165, 0, 0.1); padding: 10px; border-radius: 8px; border: 1px solid #FFA500; margin-bottom: 15px;">
        ⚠️ **Cross-Filter Warning:** Applying filters (City/Cuisine/Restaurant) may result in errors if the selections are contradictory (e.g., selecting a restaurant not found in the chosen city). Clear one filter before applying a dependency.
    </div>
    """, unsafe_allow_html=True)
    

   
    top_n = st.slider("Select Top N records for Top Lists:", 3, 20, 10, key="tab3_list_n_agg")

   
    where_clause = base_where_joined()
    
   
    #RATING OVERVIEW (Aggregated KPIs)
  
    st.markdown('<h2 class="section-title">Ratings Overview</h2>', unsafe_allow_html=True)

    rating_kpi_query = f"""
        SELECT 
            ROUND(AVG(O.ORDER_RATING), 2) AS AVG_RATING,
            MAX(O.ORDER_RATING) AS MAX_RATING,
            MIN(O.ORDER_RATING) AS MIN_RATING
        FROM FACT_ORDERS O
        JOIN DIM_RESTAURANT R ON O.RESTAURANT_ID = R.RESTAURANT_ID
        {where_clause} AND O.ORDER_RATING IS NOT NULL;
    """
    rating_kpi_df = run_query(rating_kpi_query)
    
   
    avg_rating = float(rating_kpi_df.iloc[0]["AVG_RATING"]) if not rating_kpi_df.empty and rating_kpi_df.iloc[0]["AVG_RATING"] is not None else 0
    
    
    highest_rest_df = run_query(f"""
        SELECT R.RESTAURANT_NAME, ROUND(AVG(O.ORDER_RATING),2) AS AVG_RATING
        FROM FACT_ORDERS O JOIN DIM_RESTAURANT R ON O.RESTAURANT_ID = R.RESTAURANT_ID
        {where_clause} AND O.ORDER_RATING IS NOT NULL
        GROUP BY R.RESTAURANT_NAME ORDER BY AVG_RATING DESC LIMIT 1;
    """)
    lowest_rest_df = run_query(f"""
        SELECT R.RESTAURANT_NAME, ROUND(AVG(O.ORDER_RATING),2) AS AVG_RATING
        FROM FACT_ORDERS O JOIN DIM_RESTAURANT R ON O.RESTAURANT_ID = R.RESTAURANT_ID
        {where_clause} AND O.ORDER_RATING IS NOT NULL
        GROUP BY R.RESTAURANT_NAME ORDER BY AVG_RATING ASC LIMIT 1;
    """)
    highest_name = highest_rest_df.iloc[0]["RESTAURANT_NAME"] if not highest_rest_df.empty else "N/A"
    highest_rating_val = highest_rest_df.iloc[0]["AVG_RATING"] if not highest_rest_df.empty else 0
    lowest_name = lowest_rest_df.iloc[0]["RESTAURANT_NAME"] if not lowest_rest_df.empty else "N/A"
    lowest_rating_val = lowest_rest_df.iloc[0]["AVG_RATING"] if not lowest_rest_df.empty else 0

    c1, c2, c3 = st.columns(3)
    with c1: kpi_tile("⭐ Avg Platform Rating", f"{avg_rating:.2f}", "Mean order rating")
    with c2: kpi_tile("🔥 Highest Rated", f"{highest_name} ({highest_rating_val:.2f})", "Top average rating")
    with c3: kpi_tile("❄️ Lowest Rated", f"{lowest_name} ({lowest_rating_val:.2f})", "Lowest average rating")
    
    st.markdown("---")

    
    # 2. TOP RESTAURANTS BY PROFIT (Uses Top N)

    start_card(f"💰 Top {top_n} Restaurants by Profit", "Which restaurants contribute the most profit")
    top_profit_df = run_query(f"""
        SELECT R.RESTAURANT_NAME,
                SUM((O.DELIVERY_FEE + O.COMMISSION_REVENUE) -
                    (O.DISCOUNT_AMOUNT + O.PAYMENT_PROCESSING_FEE)) AS TOTAL_PROFIT
        FROM FACT_ORDERS O
        JOIN DIM_RESTAURANT R ON O.RESTAURANT_ID = R.RESTAURANT_ID
        {where_clause}
        GROUP BY R.RESTAURANT_NAME
        ORDER BY TOTAL_PROFIT DESC
        LIMIT {top_n};
    """)
    if not top_profit_df.empty:
        fig_profit = px.bar(top_profit_df, x="RESTAURANT_NAME", y="TOTAL_PROFIT", 
                           text=top_profit_df["TOTAL_PROFIT"].apply(fmt_money), 
                           template=plotly_template)
        fig_profit.update_traces(textposition='outside')
        fig_profit.update_layout(height=400, margin=dict(l=8, r=8, t=8, b=8), yaxis_tickformat='s')
        st.plotly_chart(fig_profit, use_container_width=True)
    else:
        st.info("No profit data found for restaurants.")
    end_card()

   
    # 3. TOP RESTAURANTS BY GMV (Uses Top N)
  
    start_card(f"💸 Top {top_n} Restaurants by GMV", "Restaurants driving the highest gross sales value")
    top_gmv_df = run_query(f"""
        SELECT R.RESTAURANT_NAME,
                SUM(O.TOTAL_AMOUNT) AS TOTAL_GMV
        FROM FACT_ORDERS O
        JOIN DIM_RESTAURANT R ON O.RESTAURANT_ID = R.RESTAURANT_ID
        {where_clause}
        GROUP BY R.RESTAURANT_NAME
        ORDER BY TOTAL_GMV DESC
        LIMIT {top_n};
    """)
    if not top_gmv_df.empty:
        fig_gmv = px.bar(top_gmv_df, x="RESTAURANT_NAME", y="TOTAL_GMV", 
                         text=top_gmv_df["TOTAL_GMV"].apply(fmt_money), 
                         template=plotly_template)
        fig_gmv.update_traces(textposition='outside')
        fig_gmv.update_layout(height=400, margin=dict(l=8, r=8, t=8, b=8), yaxis_tickformat='s')
        st.plotly_chart(fig_gmv, use_container_width=True)
    else:
        st.info("No GMV data found for restaurants.")
    end_card()

 
    # 4. CUISINE PERFORMANCE BY NET PROFIT (Uses Top N)
    
    
    start_card(f"🍛 Top {top_n} Cuisine Performance by Net Profit", "Which cuisines drive profitability")
    cuisine_profit_df = run_query(f"""
        SELECT R.CUISINE_TYPE,
                SUM((O.DELIVERY_FEE + O.COMMISSION_REVENUE) -
                    (O.DISCOUNT_AMOUNT + O.PAYMENT_PROCESSING_FEE)) AS TOTAL_NET_PROFIT
        FROM FACT_ORDERS O
        JOIN DIM_RESTAURANT R ON O.RESTAURANT_ID = R.RESTAURANT_ID
        {where_clause}
        GROUP BY R.CUISINE_TYPE
        ORDER BY TOTAL_NET_PROFIT DESC
        LIMIT {top_n};
    """)
    if not cuisine_profit_df.empty:
        fig = px.bar(cuisine_profit_df, x="CUISINE_TYPE", y="TOTAL_NET_PROFIT", 
                     text=cuisine_profit_df["TOTAL_NET_PROFIT"].apply(fmt_money), 
                     template=plotly_template)
        fig.update_traces(textposition='outside')
        fig.update_layout(height=360, margin=dict(l=8, r=8, t=8, b=8), yaxis_tickformat='s')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No cuisine profit data found.")
    end_card()

   
    # 5. CUISINE COMPARISON BY GMV (Uses Top N)
   
    
    start_card(f"🍱 Top {top_n} Cuisine Comparison by GMV", "Top cuisines by total GMV")
    cuisine_gmv_df = run_query(f"""
        SELECT R.CUISINE_TYPE, SUM(O.TOTAL_AMOUNT) AS TOTAL_GMV
        FROM FACT_ORDERS O
        JOIN DIM_RESTAURANT R ON O.RESTAURANT_ID = R.RESTAURANT_ID
        {where_clause}
        GROUP BY R.CUISINE_TYPE
        ORDER BY TOTAL_GMV DESC
        LIMIT {top_n};
    """)
    if not cuisine_gmv_df.empty:
        fig = px.bar(cuisine_gmv_df, x="CUISINE_TYPE", y="TOTAL_GMV", 
                     text=cuisine_gmv_df["TOTAL_GMV"].apply(fmt_money), 
                     template=plotly_template)
        fig.update_traces(textposition='outside')
        fig.update_layout(height=360, margin=dict(l=8, r=8, t=8, b=8), yaxis_tickformat='s')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No cuisine GMV data found.")
    end_card()

   
    # 6. TOP N HIGH VALUE CUSTOMERS BY GMV (Uses Top N)
   
    start_card(f"👑 Top {top_n} High Value Customers by GMV", "Who are your biggest spenders")
    customer_df = run_query(f"""
        SELECT C.CUSTOMER_NAME, SUM(O.TOTAL_AMOUNT) AS TOTAL_GMV
        FROM FACT_ORDERS O
        JOIN DIM_CUSTOMER C ON O.CUSTOMER_ID = C.CUSTOMER_ID
        JOIN DIM_RESTAURANT R ON O.RESTAURANT_ID = R.RESTAURANT_ID
        {where_clause}
        GROUP BY C.CUSTOMER_NAME
        ORDER BY TOTAL_GMV DESC
        LIMIT {top_n};
    """)
    if not customer_df.empty:
        fig_cust = px.bar(customer_df, x="CUSTOMER_NAME", y="TOTAL_GMV", 
                          text=customer_df["TOTAL_GMV"].apply(fmt_money), 
                          template=plotly_template)
        fig_cust.update_traces(textposition='outside')
        fig_cust.update_layout(height=400, margin=dict(l=8, r=8, t=8, b=8), yaxis_tickformat='s')
        st.plotly_chart(fig_cust, use_container_width=True)
    else:
        st.info("No customer GMV data found.")
    end_card()

   
    # 7. COMMISSION RATE VS PROFITABILITY (Scatter Plot)
  
    start_card("⚖️ Commission Rate vs Profitability (r)", "Do higher commission rates drive more profit?")
    comm_df = run_query(f"""
        SELECT R.COMMISSION_RATE,
                SUM((O.DELIVERY_FEE + O.COMMISSION_REVENUE) - 
                    (O.DISCOUNT_AMOUNT + O.PAYMENT_PROCESSING_FEE)) AS TOTAL_NET_PROFIT
        FROM FACT_ORDERS O 
        JOIN DIM_RESTAURANT R ON O.RESTAURANT_ID = R.RESTAURANT_ID
        {where_clause} AND R.COMMISSION_RATE IS NOT NULL
        GROUP BY R.COMMISSION_RATE
        HAVING COUNT(O.ORDER_ID) > 10;
    """)
    comm_correlation = None
    if not comm_df.empty:
        comm_df["COMMISSION_RATE"] = pd.to_numeric(comm_df["COMMISSION_RATE"], errors="coerce").fillna(0)
        comm_df["TOTAL_NET_PROFIT"] = pd.to_numeric(comm_df["TOTAL_NET_PROFIT"], errors="coerce").fillna(0)
        corr = comm_df["COMMISSION_RATE"].corr(comm_df["TOTAL_NET_PROFIT"])
        comm_correlation = round(corr, 2)
        
      
        fig_comm = px.scatter(comm_df, x="COMMISSION_RATE", y="TOTAL_NET_PROFIT", color="TOTAL_NET_PROFIT",
                                 color_continuous_scale='Viridis',
                                 size_max=15, height=380, template=plotly_template)
        fig_comm.update_layout(xaxis_title="Commission Rate", yaxis_title="Total Net Profit (₹)",
                               margin=dict(l=8, r=8, t=8, b=8))
        fig_comm.update_xaxes(tickformat=".2%")
        fig_comm.update_yaxes(tickformat='s')
        st.plotly_chart(fig_comm, use_container_width=True)
        
        direction = "positive" if corr > 0.15 else "negative" if corr < -0.15 else "weak/no clear"
        st.markdown(f"<div class='insight'>*Correlation (r):* **{comm_correlation}** ({direction})</div>", unsafe_allow_html=True)
    else:
        st.info("No commission data available.")
    end_card()

   
    # 8. COMMISSION COMPARISON PER CUISINE TYPE (Uses Top N)
   
    start_card(f"📊 Top {top_n} Avg Commission by Cuisine Type", "Average commission rate across cuisines")
    comm_cuisine_df = run_query(f"""
        SELECT R.CUISINE_TYPE, ROUND(AVG(R.COMMISSION_RATE), 3) AS AVG_COMMISSION
        FROM DIM_RESTAURANT R
        JOIN FACT_ORDERS O ON O.RESTAURANT_ID = R.RESTAURANT_ID
        {where_clause}
        GROUP BY R.CUISINE_TYPE
        ORDER BY AVG_COMMISSION DESC
        LIMIT {top_n};
    """)
    if not comm_cuisine_df.empty:
        fig_cc = px.bar(comm_cuisine_df, x="CUISINE_TYPE", y="AVG_COMMISSION", 
                         text=comm_cuisine_df["AVG_COMMISSION"].apply(lambda x: f"{float(x):.2%}"),
                         template=plotly_template)
        fig_cc.update_traces(textposition='outside')
        fig_cc.update_layout(height=360, margin=dict(l=8, r=8, t=8, b=8))
        fig_cc.update_yaxes(tickformat=".2%")
        st.plotly_chart(fig_cc, use_container_width=True)
    else:
        st.info("No commission per cuisine data found.")
    end_card()


    
    # 9. TOP N MENU CATEGORIES BY REVENUE (Uses Top N)
   
    start_card(f"📦 Top {top_n} Menu Categories by Revenue", "Most revenue-generating food categories")
    cat_df = run_query(f"""
        SELECT M.CATEGORY,
                SUM(I.ITEM_PRICE_AT_ORDER * I.QUANTITY) AS TOTAL_REVENUE
        FROM FACT_ORDER_ITEMS I
        JOIN DIM_MENU_ITEM M ON I.MENU_ITEM_ID = M.MENU_ITEM_ID
        JOIN FACT_ORDERS O ON I.ORDER_ID = O.ORDER_ID
        JOIN DIM_RESTAURANT R ON O.RESTAURANT_ID = R.RESTAURANT_ID
        {where_clause}
        GROUP BY M.CATEGORY
        ORDER BY TOTAL_REVENUE DESC
        LIMIT {top_n};
    """)
    if not cat_df.empty:
        fig_cat = px.bar(cat_df, x="CATEGORY", y="TOTAL_REVENUE", 
                         text=cat_df["TOTAL_REVENUE"].apply(fmt_money),
                         template=plotly_template)
        fig_cat.update_traces(textposition='outside')
        fig_cat.update_layout(height=360, margin=dict(l=8, r=8, t=8, b=8), yaxis_tickformat='s')
        st.plotly_chart(fig_cat, use_container_width=True)
    else:
        st.info("No category revenue data found.")
    end_card()

    
    # 10. RATING VS ORDER VOLUME (Scatter Plot)
    
    start_card("⭐ Restaurant Rating vs Order Volume (r)", "Do higher ratings correlate with more orders?")
    rating_volume_df = run_query(f"""
        SELECT R.RESTAURANT_NAME, R.AVERAGE_RATING, COUNT(O.ORDER_ID) AS ORDER_VOLUME
        FROM FACT_ORDERS O
        JOIN DIM_RESTAURANT R ON O.RESTAURANT_ID = R.RESTAURANT_ID
        {where_clause}
        GROUP BY R.RESTAURANT_NAME, R.AVERAGE_RATING
        HAVING COUNT(O.ORDER_ID) > 3;
    """)
    rating_corr = None
    if not rating_volume_df.empty:
        
        fig_rv = px.scatter(rating_volume_df, x="AVERAGE_RATING", y="ORDER_VOLUME", color="AVERAGE_RATING",
                                 size="ORDER_VOLUME", color_continuous_scale="Viridis", 
                                 height=380, template=plotly_template)
        fig_rv.update_layout(xaxis_title="Average Rating (0.00)", yaxis_title="Order Volume",
                             margin=dict(l=8, r=8, t=8, b=8))
        fig_rv.update_xaxes(tickformat=".2f")
        fig_rv.update_yaxes(tickformat='s')
        st.plotly_chart(fig_rv, use_container_width=True)
        
        corr = rating_volume_df["AVERAGE_RATING"].corr(rating_volume_df["ORDER_VOLUME"])
        rating_corr = round(corr, 2)
        relation = "positive" if corr > 0.15 else "negative" if corr < -0.15 else "weak/no clear"
        st.markdown(f"<div class='insight'>*Correlation (r):* **{rating_corr}** ({relation})</div>", unsafe_allow_html=True)
    else:
        st.info("No rating/order volume data found.")
    end_card()




#TAB 4: CORTEX AI EXECUTIVE Q&A

with tab4:
    banner("🤖 Cortex AI Executive Q&A", 
           "Ask your business question — Cortex AI generates SQL, executes it live, visualizes results, and summarizes insights.")

    st.markdown("""
    **Examples:**
    - What is the total GMV for Ahmedabad city in 2024?  
    - Which cuisine has the highest net profit?  
    - Show me average rating by restaurant.  
    - Compare profit across cities.  
    """)

    st.markdown("---")

    question = st.text_area(
        "💬 Ask your business question:",
        height=120,
        placeholder="e.g. What is the total GMV for Ahmedabad city in 2024?"
    )

   
    st.markdown("""
    <div style="background: rgba(255, 193, 7, 0.1); padding: 10px; border-radius: 8px; border: 1px solid #FFC107; margin-bottom: 15px;">
        💡 **IMPORTANT NOTE:** Ensure that **no filters** are applied in the sidebar (City, Date, etc.) while using this section to ensure correct results. Filters may cause the AI to generate overly restricted or incorrect SQL.
    </div>
    """, unsafe_allow_html=True)
    

    # Keywords to detect irrelevant questions (UNCHANGED)
    irrelevant_keywords = [
        "driver", "rider", "bike", "vehicle", "delivery boy", "speed", "distance",
        "location", "map", "gps", "coordinates", "otp", "pin", "tracking", "warehouse",
        "postman", "time taken", "latitude", "longitude", "region", "delivery time"
    ]

    if st.button("🔍 Generate Insight"):
        if not question.strip():
            st.warning("Please enter a valid question.")
        elif any(k in question.lower() for k in irrelevant_keywords):
            st.warning("This information (like drivers, GPS, or delivery time) does not exist in the dataset.")
        else:
            with st.spinner("Analyzing your question using Snowflake Cortex AI..."):
                try:
        
                    # STEP 1 — Schema Context
                   
                    schema_context = """
Table: V_PLATFORM_PROFITABILITY
Columns: ORDER_ID, ORDER_TIMESTAMP, CUSTOMER_ID, CUSTOMER_NAME, RESTAURANT_ID, RESTAURANT_NAME,
CITY, CUISINE_TYPE, GMV, DELIVERY_FEE, COMMISSION_REVENUE, DISCOUNT_AMOUNT,
PAYMENT_PROCESSING_FEE, NET_PROFIT, ORDER_RATING

Table: DIM_RESTAURANT
Columns: RESTAURANT_ID, RESTAURANT_NAME, CITY, CUISINE_TYPE, AVERAGE_RATING, COMMISSION_RATE

Table: DIM_CUSTOMER
Columns: CUSTOMER_ID, CUSTOMER_NAME, CITY, JOIN_DATE, EMAIL, PHONE

Table: FACT_ORDERS
Columns: ORDER_ID, CUSTOMER_ID, RESTAURANT_ID, COUPON_ID, ORDER_TIMESTAMP, DELIVERY_FEE, SUB_TOTAL_AMOUNT,
DISCOUNT_AMOUNT, COMMISSION_REVENUE, PAYMENT_PROCESSING_FEE, TOTAL_AMOUNT, ORDER_RATING
"""

                    where_clause = base_where_simple() 
                    sql_prompt = f"""
You are a Snowflake SQL expert analyzing a food delivery analytics dataset.

Schema context:
{schema_context}

Current dashboard filters: {where_clause or 'No filters applied'}

User Question: "{question}"

Guidelines:
- For GMV, profit, or city-level metrics -> use V_PLATFORM_PROFITABILITY.
- CITY column exists directly in V_PLATFORM_PROFITABILITY.
- For restaurant-level questions -> use DIM_RESTAURANT.
- **CRITICAL:** Every aggregate function (SUM, COUNT, AVG, MAX) MUST be explicitly aliased (e.g., SUM(GMV) AS TOTAL_GMV, COUNT(*) AS TOTAL_ORDERS).
- Return only the SQL query. Do not include any commentary, explanations, or markdown formatting (e.g., ```sql).
- If the question is irrelevant or cannot be answered from the schema, **return exactly: OUT-OF-SCOPE**
                    """

                    
                    #Generate SQL with Cortex & Clean
                   
                    st.info("🧠 Generating SQL query using Cortex...")
                    cortex_sql = f"""
                    SELECT SNOWFLAKE.CORTEX.COMPLETE('llama3-8b', $${sql_prompt}$$) AS GENERATED_SQL;
                    """
                    sql_result = run_query(cortex_sql)
                    raw_sql = sql_result["GENERATED_SQL"].iloc[0].strip()
                    
                   
                    if raw_sql.upper().startswith("OUT-OF-SCOPE"):
                        st.warning("⚠️ **This question is outside the scope of the current dataset.** The AI confirmed this is not traceable with the available data (e.g., driver details, GPS, or complex unmodeled metrics).")
                        st.stop()
                    
                    
                    import re
                    clean_sql = re.sub(r"```sql|```", "", raw_sql, flags=re.IGNORECASE)
                    clean_sql = clean_sql.replace("V_PLATFORM_FILTERED", "V_PLATFORM_PROFITABILITY")
                    
                    match = re.search(r"(?is)^(?:.*?)(SELECT|WITH|SHOW|CALL)\b.*", clean_sql, re.IGNORECASE | re.DOTALL)
                    
                    if match:
                        ai_generated_sql = match.group(0).strip()
                        last_semicolon = ai_generated_sql.rfind(';')
                        if last_semicolon != -1:
                            ai_generated_sql = ai_generated_sql[:last_semicolon + 1]
                        ai_generated_sql = re.sub(r"\s+", " ", ai_generated_sql).strip()
                    else:
                        st.error("❌ **SQL Generation Failed:** Cortex did not return a recognizable SQL query (SELECT/WITH/SHOW/CALL).")
                        st.code(raw_sql, language="text")
                        st.stop()
                        
                    st.markdown("### 🧩 Generated SQL (post-validation)")
                    st.code(ai_generated_sql, language="sql")

                  
                    # STEP 4 — Execute SQL
                   
                    st.info("🧾 Executing generated SQL on Snowflake...")
                    
                    try:
                        result_df = run_query(ai_generated_sql)
                        st.success("✅ Query executed successfully.")
                    except Exception as e:
                      
                        st.error(f"❌ **SQL Execution Error:** The generated query caused an error in Snowflake. Please review the SQL above.\n\nError Details:\n{e}")
                        st.stop()

                    if result_df.empty:
                        st.warning("⚠️ Query executed successfully, but **No data returned** for this query. Try widening your date range or adjusting the filters.")
                        
                        st.stop()

                    st.dataframe(result_df, use_container_width=True)

                   
                    #Auto Visualization
                  
                    st.markdown("### 📊 Visual Insight")

                    chart_displayed = False
                    
                    cols = [c.upper() for c in result_df.columns]
                    result_df.columns = [c.upper() for c in result_df.columns] 

                    try:
                       
                        group_col = None
                        metric_col = None

                        if "CITY" in cols: group_col = "CITY"
                        elif "CUISINE_TYPE" in cols: group_col = "CUISINE_TYPE"
                        elif "RESTAURANT_NAME" in cols: group_col = "RESTAURANT_NAME"

                        if "GMV" in cols or "TOTAL_GMV" in cols: metric_col = next((c for c in cols if 'GMV' in c), None)
                        elif "NET_PROFIT" in cols or "TOTAL_PROFIT" in cols: metric_col = next((c for c in cols if 'PROFIT' in c), None)
                        elif "ORDERS" in cols or "TOTAL_ORDERS" in cols: metric_col = next((c for c in cols if 'ORDER' in c), None)
                        
                        # General Bar Chart Logic
                        if group_col and metric_col:
                            fig = px.bar(result_df, x=group_col, y=metric_col, 
                                         text=result_df[metric_col].apply(fmt_money if 'GMV' in metric_col or 'PROFIT' in metric_col else fmt_int),
                                         title=f"{metric_col.replace('_', ' ').title()} by {group_col.replace('_', ' ').title()}", 
                                         template=plotly_template)
                            fig.update_traces(textposition='outside')
                            fig.update_layout(height=400, yaxis_tickformat='s')
                            st.plotly_chart(fig, use_container_width=True, key="ai_bar_chart")
                            chart_displayed = True
                        
                        # 2. Time Trend (Line Chart Logic)
                        elif any(c in cols for c in ["ORDER_TIMESTAMP", "MONTH"]) and metric_col:
                             x_col = next((c for c in cols if 'TIMESTAMP' in c or 'MONTH' in c), None)
                             if x_col:
                                fig = px.line(result_df, x=x_col, y=metric_col, markers=True, 
                                              title=f"{metric_col} Trend", template=plotly_template)
                                fig.update_layout(height=400, yaxis_tickformat='s')
                                st.plotly_chart(fig, use_container_width=True, key="ai_line_chart")
                                chart_displayed = True

                        if not chart_displayed:
                            st.info("No suitable visualization detected for this query. Showing raw results above.")

                    except Exception as viz_err:
                        st.warning(f"Visualization skipped due to error: {viz_err}")

                except Exception as top_level_err:
                    st.error(f"An unexpected error occurred during Cortex analysis: {top_level_err}")






# 👥 TAB 5: CUSTOMER INSIGHTS (Aggregated View)

with tab5:
    banner("👥 Customer Insights", "Loyalty, ratings, and monthly active users")

   
    st.markdown("""
    <div style="background: rgba(255, 165, 0, 0.1); padding: 10px; border-radius: 8px; border: 1px solid #FFA500; margin-bottom: 15px;">
        ⚠️ **Cross-Filter Warning:** Applying filters (City/Cuisine/Restaurant) may result in errors if the selections are contradictory (e.g., selecting a restaurant not found in the chosen city). Clear one filter before applying a dependency.
    </div>
    """, unsafe_allow_html=True)
   

    
    top_n = st.slider("Select Top N records for Loyal Customer List:", 3, 20, 10, key="tab5_list_n_agg")
    st.markdown("---")

   
   
    where_clause = base_where_joined()

    # ============================================================
    # 🧾 1. CUSTOMER KPIs (Aggregated)
    # ============================================================
    st.markdown('<h2 class="section-title">Customer KPIs</h2>', unsafe_allow_html=True)
    
   
    customer_kpi_query = f"""
    SELECT 
        COUNT(DISTINCT SUB.CUSTOMER_ID) AS TOTAL_CUSTOMERS,
        COUNT(DISTINCT CASE WHEN SUB.CUSTOMER_ORDER_COUNT > 1 THEN SUB.CUSTOMER_ID END) AS REPEAT_CUSTOMERS,
        ROUND((COUNT(DISTINCT CASE WHEN SUB.CUSTOMER_ORDER_COUNT > 1 THEN SUB.CUSTOMER_ID END) / NULLIF(COUNT(DISTINCT SUB.CUSTOMER_ID)::FLOAT, 0)) * 100, 2) AS REPEAT_RATE,
        ROUND(AVG(SUB.CUSTOMER_ORDER_COUNT), 2) AS AVG_ORDERS_PER_CUSTOMER,
        ROUND(AVG(SUB.CUSTOMER_GMV), 2) AS AVG_GMV_PER_CUSTOMER
    FROM (
        SELECT O.CUSTOMER_ID, COUNT(O.ORDER_ID) AS CUSTOMER_ORDER_COUNT, SUM(O.TOTAL_AMOUNT) AS CUSTOMER_GMV
        FROM FACT_ORDERS O
        JOIN DIM_RESTAURANT R ON O.RESTAURANT_ID = R.RESTAURANT_ID
        {where_clause}
        GROUP BY O.CUSTOMER_ID
    ) SUB;
    """
    
    try:
        customer_kpi_df = run_query(customer_kpi_query)
        
        total_customers = repeat_customers = repeat_rate = avg_orders = avg_gmv = 0
        if not customer_kpi_df.empty and customer_kpi_df.iloc[0]["TOTAL_CUSTOMERS"] is not None:
            k = customer_kpi_df.iloc[0]
            total_customers = int(k["TOTAL_CUSTOMERS"])
            repeat_customers = int(k["REPEAT_CUSTOMERS"])
            repeat_rate = float(k["REPEAT_RATE"])
            avg_orders = float(k["AVG_ORDERS_PER_CUSTOMER"])
            avg_gmv = float(k["AVG_GMV_PER_CUSTOMER"])

            c1, c2, c3, c4, c5 = st.columns(5)
            with c1: kpi_tile("👤 Total Customers", fmt_int(total_customers), "Unique customers in scope")
            with c2: kpi_tile("🔁 Repeat Customers", fmt_int(repeat_customers), "Placed >1 orders")
            with c3: kpi_tile("📈 Repeat Rate", f"**{repeat_rate:.2f}** %", "Repeat / total customers")
            with c4: kpi_tile("🛍️ Avg Orders/Customer", f"{avg_orders:.2f}", "Order frequency")
            with c5: kpi_tile("💰 Avg GMV/Customer", fmt_money(avg_gmv), "Spend per customer")

            st.markdown(
                f"<div class='insight'>💡 Across the filter scope, **{fmt_int(total_customers)}** customers are active, "
                f"with a repeat rate of **{repeat_rate:.2f}%**.</div>",
                unsafe_allow_html=True
            )
        else:
            st.info("No customer KPI data found for selected filters.")
    except Exception as e:
        st.error(f"Error fetching Customer KPIs: {e}")


    
    # MONTHLY ACTIVE CUSTOMERS (Dynamic Line Chart)
    
    start_card("📅 Monthly Active Customers (MAC)", "Unique customers placing orders each month")
    
    # --- Dynamic Grouping Logic ---
    comparison_dim = get_comparison_dimension()
    
    grouping_cols = ["MONTH"]
    color_col = None
    
    # Check if we should split the line by a comparison dimension
    if comparison_dim and (len(selected_city) > 1 or len(selected_cuisine) > 1 or len(selected_rest) > 1):
        # We assume get_comparison_dimension() handles the priority (City > Cuisine > Restaurant)
        # and we only split if one of the multiselect filters has >1 item selected.
        if comparison_dim not in grouping_cols: # Ensure the column is present if we use it
            grouping_cols.append(comparison_dim)
        color_col = comparison_dim
    # --- End Dynamic Grouping Logic ---
    
    # Note: We must join DIM_RESTAURANT (R) to get the grouping column (R.CITY, R.CUISINE_TYPE)
    # when we are not grouping by the standard columns already present in FACT_ORDERS.
    # The where_clause ensures the join is available for R.
    
    # Dynamically build the SELECT and GROUP BY parts
    select_cols = [f"TO_CHAR(O.ORDER_TIMESTAMP, 'YYYY-MM') AS MONTH"]
    group_by_cols = ["MONTH"]
    
    if color_col:
        # If splitting, we need the column in the SELECT and GROUP BY clauses, using the joined table R
        if color_col == "CITY":
            select_cols.append("R.CITY")
            group_by_cols.append("R.CITY")
        elif color_col == "CUISINE_TYPE":
            select_cols.append("R.CUISINE_TYPE")
            group_by_cols.append("R.CUISINE_TYPE")
        elif color_col == "RESTAURANT_NAME":
            select_cols.append("R.RESTAURANT_NAME")
            group_by_cols.append("R.RESTAURANT_NAME")
            
    
    mac_query = f"""
    SELECT 
        {', '.join(select_cols)},
        COUNT(DISTINCT O.CUSTOMER_ID) AS ACTIVE_CUSTOMERS
    FROM FACT_ORDERS O
    JOIN DIM_RESTAURANT R ON O.RESTAURANT_ID = R.RESTAURANT_ID
    {where_clause}
    GROUP BY {', '.join(group_by_cols)}
    ORDER BY MONTH;
    """
    
    mac_df = run_query(mac_query)
    
    latest_delta = 0
    if not mac_df.empty:
        # Create Line Chart
        fig_mac = px.line(mac_df, 
                          x="MONTH", 
                          y="ACTIVE_CUSTOMERS", 
                          color=color_col,  # Dynamically set the color field
                          markers=True, 
                          template=plotly_template)
        
        fig_mac.update_traces(line=dict(width=3))
        fig_mac.update_layout(height=360, margin=dict(l=8, r=8, t=8, b=8), yaxis_tickformat='s')
        
        st.plotly_chart(fig_mac, use_container_width=True, key="cust_mac_trend") 

        if len(mac_df) >= 2 and not color_col: # Only calculate delta if not split by color
            # NOTE: Delta calculation relies on aggregated data, so we avoid it when split by color
            last = mac_df.iloc[-1]["ACTIVE_CUSTOMERS"]
            prev = mac_df.iloc[-2]["ACTIVE_CUSTOMERS"]
            latest_delta = last - prev
            dirn = "increased 📈" if latest_delta > 0 else "decreased 📉" if latest_delta < 0 else "stable"
            st.markdown(
                f"<div class='insight'>💡 Monthly active customers have {dirn} by **{abs(latest_delta)}** compared to the previous month.</div>",
                unsafe_allow_html=True
            )
    else:
        st.info("No monthly active customer data found for selected filters.")
    end_card()

   
    # TOP N LOYAL CUSTOMERS (Dynamic Top N)
   
    start_card(f"🏆 Top {top_n} Loyal Customers (Most Orders)", "Most orders placed")
    loyal_df = run_query(f"""
    SELECT 
        C.CUSTOMER_NAME,
        COUNT(O.ORDER_ID) AS TOTAL_ORDERS,
        ROUND(SUM(O.TOTAL_AMOUNT),2) AS TOTAL_SPENT
    FROM FACT_ORDERS O
    JOIN DIM_CUSTOMER C ON O.CUSTOMER_ID = C.CUSTOMER_ID
    JOIN DIM_RESTAURANT R ON O.RESTAURANT_ID = R.RESTAURANT_ID
    {where_clause}
    GROUP BY C.CUSTOMER_NAME
    ORDER BY TOTAL_ORDERS DESC
    LIMIT {top_n};
    """)
    if not loyal_df.empty:
        fig_loyal = px.bar(loyal_df, x="CUSTOMER_NAME", y="TOTAL_ORDERS", 
                           text=loyal_df["TOTAL_ORDERS"].apply(fmt_int),
                           hover_data={"TOTAL_SPENT": True, "TOTAL_ORDERS": False},
                           template=plotly_template)
        fig_loyal.update_layout(height=360, margin=dict(l=8, r=8, t=8, b=8), yaxis_tickformat='s')
        fig_loyal.update_traces(textposition='outside')
        
        st.plotly_chart(fig_loyal, use_container_width=True, key="cust_loyal_bar")
        
        top_loyal = loyal_df.iloc[0]
        st.markdown(
            f"<div class='insight'>💡 **{top_loyal['CUSTOMER_NAME']}** is the most loyal customer with "
            f"**{fmt_int(top_loyal['TOTAL_ORDERS'])} orders** totaling **{fmt_money(top_loyal['TOTAL_SPENT'])}** spent.</div>",
            unsafe_allow_html=True
        )
    else:
        st.info("No loyal customer data available for selected filters.")
    end_card()

  
    # CUSTOMER RATING DISTRIBUTION
   
    start_card("⭐ Customer Rating Distribution", "How customers rate their orders")
    rating_dist_df = run_query(f"""
    SELECT 
        CASE 
            WHEN O.ORDER_RATING BETWEEN 4.5 AND 5 THEN 'Excellent (4.5–5)'
            WHEN O.ORDER_RATING BETWEEN 3.5 AND 4.49 THEN 'Good (3.5–4.49)'
            WHEN O.ORDER_RATING BETWEEN 2.5 AND 3.49 THEN 'Average (2.5–3.49)'
            WHEN O.ORDER_RATING IS NOT NULL THEN 'Poor (<2.5)'
            ELSE 'No Rating'
        END AS RATING_CATEGORY,
        COUNT(O.ORDER_ID) AS RATING_COUNT
    FROM FACT_ORDERS O
    JOIN DIM_RESTAURANT R ON O.RESTAURANT_ID = R.RESTAURANT_ID
    {where_clause}
    GROUP BY RATING_CATEGORY
    HAVING RATING_CATEGORY != 'No Rating'
    ORDER BY RATING_COUNT DESC;
    """)
    if not rating_dist_df.empty:
        fig_rating = px.bar(rating_dist_df, x="RATING_CATEGORY", y="RATING_COUNT", 
                            text=rating_dist_df["RATING_COUNT"].apply(fmt_int),
                            template=plotly_template)
        fig_rating.update_layout(height=360, margin=dict(l=8, r=8, t=8, b=8), yaxis_tickformat='s')
        fig_rating.update_traces(textposition='outside')
        # FIX: Added unique key
        st.plotly_chart(fig_rating, use_container_width=True, key="cust_rating_dist")

        top_rating_cat = rating_dist_df.iloc[0]["RATING_CATEGORY"]
        st.markdown(
            f"<div class='insight'>💡 Majority of customer ratings fall in the **{top_rating_cat}** category.</div>",
            unsafe_allow_html=True
        )
    else:
        st.info("No rating data available for selected filters.")
    end_card()


with tab6:
    banner("🧩 Strategic Conclusion & Recommendations",
           "An executive overview combining insights from all dashboards with data-backed next actions.")

  
    #  Disclaimer Notice
 
    st.markdown("""
    <div style="
        background-color:#fff8e1;
        border-left:6px solid #f59e0b;
        padding:12px 16px;
        border-radius:8px;
        margin-bottom:20px;
        color:#92400e;
        font-size:14px;">
        ⚠️ <b>Note:</b> The insights and recommendations shown on this page dynamically update based on the filters you apply.<br>
        To view the overall, platform-wide strategic summary, please clear all filters in the sidebar.
    </div>
    """, unsafe_allow_html=True)

    where_clause = base_where_joined()

   
    #  Aggregate Key Metrics Across the Platform

    kpi_df = run_query(f"""
        SELECT 
            SUM(O.TOTAL_AMOUNT) AS TOTAL_GMV,
            COUNT(DISTINCT O.ORDER_ID) AS TOTAL_ORDERS,
            ROUND(AVG(O.ORDER_RATING),2) AS AVG_RATING,
            COUNT(DISTINCT O.CUSTOMER_ID) AS UNIQUE_CUSTOMERS
        FROM FACT_ORDERS O
        JOIN DIM_RESTAURANT R ON O.RESTAURANT_ID = R.RESTAURANT_ID
        {where_clause};
    """)

    total_gmv = fmt_money(kpi_df.iloc[0]["TOTAL_GMV"]) if not kpi_df.empty else "₹0"
    total_orders = fmt_int(kpi_df.iloc[0]["TOTAL_ORDERS"]) if not kpi_df.empty else "0"
    avg_rating = kpi_df.iloc[0]["AVG_RATING"] if not kpi_df.empty else 0
    total_customers = fmt_int(kpi_df.iloc[0]["UNIQUE_CUSTOMERS"]) if not kpi_df.empty else "0"

    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_tile("💰 Total GMV", total_gmv, "Overall platform revenue")
    with c2: kpi_tile("🛒 Total Orders", total_orders, "Orders completed")
    with c3: kpi_tile("⭐ Avg Rating", f"{avg_rating:.2f}", "Customer satisfaction index")
    with c4: kpi_tile("👥 Unique Customers", total_customers, "Active customer base")

    st.markdown("<br>", unsafe_allow_html=True)

  
    # 🔹 2. Identify Key Performing Dimensions
  
    top_city_df = run_query(f"""
        SELECT R.CITY, SUM((O.DELIVERY_FEE + O.COMMISSION_REVENUE) -
                           (O.DISCOUNT_AMOUNT + O.PAYMENT_PROCESSING_FEE)) AS PROFIT
        FROM FACT_ORDERS O JOIN DIM_RESTAURANT R ON O.RESTAURANT_ID = R.RESTAURANT_ID
        {where_clause}
        GROUP BY R.CITY ORDER BY PROFIT DESC LIMIT 1;
    """)
    top_city = top_city_df.iloc[0]["CITY"] if not top_city_df.empty else None

    top_cuisine_df = run_query(f"""
        SELECT R.CUISINE_TYPE, SUM(O.TOTAL_AMOUNT) AS GMV
        FROM FACT_ORDERS O JOIN DIM_RESTAURANT R ON O.RESTAURANT_ID = R.RESTAURANT_ID
        {where_clause}
        GROUP BY R.CUISINE_TYPE ORDER BY GMV DESC LIMIT 1;
    """)
    top_cuisine = top_cuisine_df.iloc[0]["CUISINE_TYPE"] if not top_cuisine_df.empty else None

    top_rest_df = run_query(f"""
        SELECT R.RESTAURANT_NAME, SUM(O.TOTAL_AMOUNT) AS GMV
        FROM FACT_ORDERS O JOIN DIM_RESTAURANT R ON O.RESTAURANT_ID = R.RESTAURANT_ID
        {where_clause}
        GROUP BY R.RESTAURANT_NAME ORDER BY GMV DESC LIMIT 1;
    """)
    top_restaurant = top_rest_df.iloc[0]["RESTAURANT_NAME"] if not top_rest_df.empty else None

    loyal_df = run_query(f"""
        SELECT C.CUSTOMER_NAME, COUNT(O.ORDER_ID) AS ORDERS
        FROM FACT_ORDERS O JOIN DIM_CUSTOMER C ON O.CUSTOMER_ID = C.CUSTOMER_ID
        JOIN DIM_RESTAURANT R ON O.RESTAURANT_ID = R.RESTAURANT_ID
        {where_clause}
        GROUP BY C.CUSTOMER_NAME ORDER BY ORDERS DESC LIMIT 1;
    """)
    top_customer = loyal_df.iloc[0]["CUSTOMER_NAME"] if not loyal_df.empty else None

   
    # 3. Correlation Check (Commission vs Profit)
    
    comm_corr_df = run_query(f"""
        SELECT R.COMMISSION_RATE,
               SUM((O.DELIVERY_FEE + O.COMMISSION_REVENUE) -
                   (O.DISCOUNT_AMOUNT + O.PAYMENT_PROCESSING_FEE)) AS PROFIT
        FROM FACT_ORDERS O JOIN DIM_RESTAURANT R ON O.RESTAURANT_ID = R.RESTAURANT_ID
        WHERE R.COMMISSION_RATE IS NOT NULL
        GROUP BY R.COMMISSION_RATE;
    """)
    comm_corr = None
    if not comm_corr_df.empty:
        comm_corr_df["COMMISSION_RATE"] = pd.to_numeric(comm_corr_df["COMMISSION_RATE"], errors="coerce")
        comm_corr_df["PROFIT"] = pd.to_numeric(comm_corr_df["PROFIT"], errors="coerce")
        comm_corr = comm_corr_df["COMMISSION_RATE"].corr(comm_corr_df["PROFIT"])

   
    # 4. Generate Contextual Business Recommendations
 
    st.markdown('<h2 class="section-title">💡 Data-Driven Recommendations</h2>', unsafe_allow_html=True)

    insights = []

    if top_city:
        insights.append(f"Focus expansion and marketing on **{top_city}**, which currently delivers the highest profit contribution.")
    if top_cuisine:
        insights.append(f"Promote **{top_cuisine}** cuisine — it drives the highest GMV share across all orders.")
    if top_restaurant:
        insights.append(f"Feature **{top_restaurant}** as a flagship partner and replicate its operational model in other cities.")
    if top_customer:
        insights.append(f"Reward loyal customer **{top_customer}** through personalized offers or premium engagement tiers.")
    if comm_corr is not None:
        if comm_corr > 0.3:
            insights.append("Higher commission rates correlate positively with profit — maintain incentive-based partner models.")
        elif comm_corr < -0.3:
            insights.append("Profitability decreases as commission rates rise — consider revising commission slabs for low-margin categories.")
        else:
            insights.append("Commission rate impact on profit is neutral — keep rates stable but continue monitoring partner satisfaction.")

    for i in insights:
        st.markdown(f"<div class='insight'>{i}</div>", unsafe_allow_html=True)

  
    # 🔹 5. Strategic Next Steps for Stakeholders
    
    st.markdown('<h2 class="section-title">🎯 Strategic Next Steps</h2>', unsafe_allow_html=True)
    start_card("🚀 Platform Growth & Optimization")
    st.markdown(f"""
    - Expand coverage in **{top_city or 'key markets'}** and replicate success frameworks from **{top_restaurant or 'leading restaurants'}**.  
    - Strengthen promotions for **{top_cuisine or 'popular cuisines'}** and incentivize loyal users like **{top_customer or 'repeat customers'}**.  
    - Re-evaluate commission structures periodically to sustain balanced profitability.  
    - Integrate predictive dashboards and real-time Snowflake analytics for proactive decisions.  
    """)
    end_card()

    st.markdown("""
    <div class="insight">
    💡 <b>In summary:</b> Centering strategies on the most profitable cities, cuisines, and customers — 
    while optimizing commissions and leveraging loyalty — can drive both sustainable revenue growth 
    and improved partner relationships.
    </div>
    """, unsafe_allow_html=True)
