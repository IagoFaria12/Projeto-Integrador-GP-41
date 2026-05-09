import calendar
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Amazon Sales Analysis",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        .stApp {
            background: #0e1117;
            color: #f4f6fb;
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #252733 0%, #1f2130 100%);
            border-right: 1px solid rgba(255,255,255,0.06);
        }
        .sidebar-title {
            font-size: 1.0rem;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 0.2rem;
        }
        .sidebar-subtitle {
            font-size: 0.80rem;
            color: #a8b0c2;
            margin-bottom: 0.75rem;
        }
        .main-title {
            font-size: 2.1rem;
            font-weight: 800;
            color: #ffffff;
            margin: 0.2rem 0 0.3rem 0;
        }
        .main-subtitle {
            color: #98a2b3;
            margin-bottom: 0.5rem;
        }
        .section-divider {
            border-top: 1px solid rgba(255,255,255,0.12);
            margin: 0.75rem 0 1.0rem 0;
        }
        .metric-card {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 18px;
            padding: 14px 16px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.18);
        }
        .metric-label {
            font-size: 0.78rem;
            color: #b8c0d0;
            margin-bottom: 0.15rem;
        }
        .metric-value {
            font-size: 1.45rem;
            font-weight: 800;
            color: #ffffff;
            line-height: 1.1;
        }
        .metric-delta {
            font-size: 0.75rem;
            color: #7f8aa3;
            margin-top: 0.2rem;
        }
        .stTabs [data-baseweb="tab-list"] {
            gap: 22px;
            border-bottom: 1px solid rgba(255,255,255,0.10);
        }
        .stTabs [data-baseweb="tab"] {
            color: #cbd5e1;
            font-weight: 600;
            padding-bottom: 10px;
        }
        .stTabs [aria-selected="true"] {
            color: #ff4d4d !important;
        }
        div[data-testid="stMetric"] {
            background: rgba(255,255,255,0.03);
            border: 1px solid rgba(255,255,255,0.06);
            border-radius: 16px;
            padding: 12px 12px 8px 12px;
        }
        div[data-testid="stMetric"] label {
            color: #b8c0d0 !important;
        }
        .small-note {
            color: #8f99ab;
            font-size: 0.82rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

DATA_PATH = Path("data/raw/amazon_sales_dataset.csv")


@st.cache_data(show_spinner=False)
def load_data(path: Path = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.dropna().copy()
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df = df.dropna(subset=["order_date"]).copy()
    return df


def money_br(value: float) -> str:
    """Formata moeda em padrão brasileiro."""
    return f"R$ {value:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")


def money_br_2(value: float) -> str:
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def add_chart_style(fig, height=420, legend_title=None):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#e5e7eb"),
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(title=legend_title or "", font=dict(color="#e5e7eb")),
    )
    fig.update_xaxes(showgrid=True, gridcolor="rgba(255,255,255,0.06)", zeroline=False)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(255,255,255,0.06)", zeroline=False)
    return fig


def metric_card(label: str, value: str, delta: str | None = None):
    delta_html = f'<div class="metric-delta">{delta}</div>' if delta else ""
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            {delta_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

df = load_data()

# filtros disponíveis
regions = sorted(df["customer_region"].dropna().unique().tolist())
categories = sorted(df["product_category"].dropna().unique().tolist())

st.sidebar.markdown('<div class="sidebar-title">Global Filters</div>', unsafe_allow_html=True)
st.sidebar.markdown('<div class="sidebar-subtitle">Aplique filtros para atualizar o dashboard</div>', unsafe_allow_html=True)

selected_regions = st.sidebar.multiselect(
    "Region",
    options=regions,
    default=regions,
)
selected_categories = st.sidebar.multiselect(
    "Category",
    options=categories,
    default=categories,
)

years = sorted(df["order_date"].dt.year.dropna().unique().astype(int).tolist())
month_names = list(calendar.month_name)[1:]

selected_years = st.sidebar.multiselect(
    "Year",
    options=years,
    default=years,
)
if not selected_years:
    selected_years = years

selected_month_start = st.sidebar.selectbox(
    "Start Month",
    options=month_names,
    index=0,
)
selected_month_end = st.sidebar.selectbox(
    "End Month",
    options=month_names,
    index=len(month_names) - 1,
)

month_numbers = {name: idx for idx, name in enumerate(month_names, start=1)}
start_month = month_numbers[selected_month_start]
end_month = month_numbers[selected_month_end]
if start_month > end_month:
    start_month, end_month = end_month, start_month

filtered = df[
    df["customer_region"].isin(selected_regions)
    & df["product_category"].isin(selected_categories)
    & df["order_date"].dt.year.isin(selected_years)
    & df["order_date"].dt.month.between(start_month, end_month)
].copy()

st.markdown('<div class="main-title">🚀 Amazon Sales Analysis</div>', unsafe_allow_html=True)
st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# Tabs iguais à referência
main_tab, product_tab, behavior_tab = st.tabs([
    "Main Indicators",
    "Product Analysis",
    "Customer Behavior",
])

with main_tab:
    col_left, col_right = st.columns([1.15, 0.95])

    with col_left:
        st.subheader("Sales Evolution Over Time")
        sales_time = (
            filtered.set_index("order_date")
            .resample("ME")["total_revenue"]
            .sum()
            .reset_index()
        )
        sales_time["order_date"] = sales_time["order_date"].dt.strftime("%b %Y")
        fig_line = px.line(
            sales_time,
            x="order_date",
            y="total_revenue",
            markers=True,
            line_shape="spline",
        )
        fig_line.update_traces(line=dict(color="#f59e0b", width=3), marker=dict(size=8))
        fig_line.update_layout(xaxis_title="order_date", yaxis_title="total_revenue")
        add_chart_style(fig_line, height=430)
        st.plotly_chart(fig_line, width="stretch")

    with col_right:
        st.subheader("Sales by Region")
        by_region = filtered.groupby("customer_region", as_index=False)["total_revenue"].sum()
        by_region = by_region.sort_values("total_revenue", ascending=True)
        fig_region = px.bar(
            by_region,
            x="total_revenue",
            y="customer_region",
            orientation="h",
            color="customer_region",
            color_discrete_sequence=["#2dd4bf", "#22c55e", "#a855f7", "#fde047"],
        )
        fig_region.update_layout(showlegend=False, xaxis_title="total_revenue", yaxis_title="customer_region")
        add_chart_style(fig_region, height=430)
        st.plotly_chart(fig_region, width="stretch")

with product_tab:

    st.subheader("Top 10 Best Selling Products")

    top_products = (
        filtered.groupby("product_id", as_index=False)
        .agg(
            quantity_sold=("quantity_sold", "sum"),
            total_revenue=("total_revenue", "sum"),
            avg_rating=("rating", "mean"),
        )
        .round({
            "avg_rating": 2,
            "total_revenue": 2,
        })
        .sort_values(
            "quantity_sold",
            ascending=False
        )
        .head(10)
    )

    top_products["label"] = (
        top_products["quantity_sold"].astype(int).astype(str)
        + " units | ⭐ "
        + top_products["avg_rating"].map("{:.2f}".format)
    )

    fig_top = px.bar(
        top_products,
        x="product_id",
        y="quantity_sold",
        text="label",
        color="avg_rating",
        color_continuous_scale="Blues",
        hover_data={
            "avg_rating": ":.2f",
            "total_revenue": ":,.2f",
        },
    )

    fig_top.update_traces(
        textposition="outside",
    )

    fig_top.update_layout(
        xaxis_title="Product ID",
        yaxis_title="Quantity Sold",
        coloraxis_colorbar_title="Avg Rating",
    )

    add_chart_style(fig_top, height=450)

    st.plotly_chart(
        fig_top,
        use_container_width=True,
    )

with behavior_tab:
    items_per_order = filtered.groupby("order_id")["quantity_sold"].sum().mean()
    metric_card("Items per Order", f"{items_per_order:.2f}")

    col1 = st.columns(1)[0]

    with col1:
        st.subheader("Discount vs Non-Discount Sales")
        discount_flag = filtered["discount_percent"].fillna(0).gt(0).map({True: "Discount", False: "Non-Discount"})
        discount_share = discount_flag.value_counts().reset_index()
        discount_share.columns = ["discount", "count"]
        fig_discount = px.bar(
            discount_share,
            x="discount",
            y="count",
            text="count",
            color="discount",
            color_discrete_map={"Discount": "#c47b00", "Non-Discount": "#1f2a44"},
        )
        fig_discount.update_layout(showlegend=False, xaxis_title="", yaxis_title="Count")
        add_chart_style(fig_discount, height=420)
        st.plotly_chart(fig_discount, width="stretch")

st.markdown("---")
st.caption("Dashboard desenvolvido para o Projeto Integrador GP-41")
