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
payment_methods = sorted(df["payment_method"].dropna().unique().tolist())

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
selected_payment = st.sidebar.multiselect(
    "Payment Method",
    options=payment_methods,
    default=payment_methods,
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
    & df["payment_method"].isin(selected_payment)
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
    total_revenue = filtered["total_revenue"].sum()
    total_orders = filtered["order_id"].nunique()
    avg_ticket = filtered["total_revenue"].sum() / max(total_orders, 1)
    avg_rating = filtered["rating"].mean()
    items_per_order = filtered.groupby("order_id")["quantity_sold"].sum().mean()

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        metric_card("Total Revenue", money_br(total_revenue))
    with c2:
        metric_card("Total Orders", f"{total_orders:,}".replace(",", "."))
    with c3:
        metric_card("Avg Ticket", money_br(avg_ticket))
    with c4:
        metric_card("Avg Rating", f"{avg_rating:.2f} ⭐")
    with c5:
        metric_card("Items per Order", f"{items_per_order:.2f}")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

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
    left, right = st.columns(2)

    with left:
        st.subheader("Top 10 Best Selling Products")
        top_products = (
            filtered.groupby("product_id", as_index=False)["quantity_sold"].sum()
            .sort_values("quantity_sold", ascending=False)
            .head(10)
        )
        fig_top = px.bar(
            top_products,
            x="product_id",
            y="quantity_sold",
            color="product_id",
            text="quantity_sold",
        )
        fig_top.update_traces(marker_color="#2563eb", showlegend=False)
        fig_top.update_layout(xaxis_title="Product ID", yaxis_title="Quantity Sold")
        add_chart_style(fig_top, height=430)
        st.plotly_chart(fig_top, width="stretch")

    with right:
        st.subheader("Sales by Category")
        by_cat = filtered.groupby("product_category", as_index=False)["total_revenue"].sum()
        fig_donut = go.Figure(
            data=[
                go.Pie(
                    labels=by_cat["product_category"],
                    values=by_cat["total_revenue"],
                    hole=0.45,
                    textinfo="percent",
                    textfont=dict(color="#0f172a", size=12),
                )
            ]
        )
        fig_donut.update_traces(
            marker=dict(
                colors=["#0b6bd3", "#fca5a5", "#ff3b30", "#86efac", "#2dd4bf", "#93c5fd", "#c084fc", "#f59e0b"]
            )
        )
        fig_donut.update_layout(showlegend=False)
        add_chart_style(fig_donut, height=430)
        st.plotly_chart(fig_donut, width="stretch")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Avg Rating & Review Classification")
        product_ratings = (
            filtered.groupby("product_id", as_index=False)["rating"]
            .mean()
            .round(2)
            .sort_values("rating", ascending=False)
            .head(10)
        )
        product_ratings["review_classification"] = pd.cut(
            product_ratings["rating"],
            bins=[0, 2.5, 3.5, 4.5, 5],
            labels=["Ruim", "Regular", "Bom", "Excelente"],
            include_lowest=True,
        )
        st.dataframe(
            product_ratings.rename(
                columns={
                    "product_id": "Product ID",
                    "rating": "Avg Rating",
                    "review_classification": "Review Classification",
                }
            ),
            use_container_width=True,
        )

    with c2:
        st.subheader("Top Categories by Revenue")
        by_cat_rev = by_cat.sort_values("total_revenue", ascending=True)
        fig_cat_rev = px.bar(
            by_cat_rev,
            x="total_revenue",
            y="product_category",
            orientation="h",
        )
        fig_cat_rev.update_traces(marker_color="#14b8a6")
        fig_cat_rev.update_layout(xaxis_title="total_revenue", yaxis_title="product_category")
        add_chart_style(fig_cat_rev, height=360)
        st.plotly_chart(fig_cat_rev, width="stretch")

with behavior_tab:
    metric_card("Items per Order", f"{items_per_order:.2f}")

    col1, col2 = st.columns(2)

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

    with col2:
        st.subheader("Price Range Distribution")
        if "price_range" in filtered.columns:
            price_range = filtered["price_range"].value_counts().reset_index()
            price_range.columns = ["price_range", "count"]
            fig_price = px.bar(
                price_range,
                x="price_range",
                y="count",
                text="count",
            )
            fig_price.update_traces(marker_color="#1f77b4")
            fig_price.update_layout(xaxis_title="price_range", yaxis_title="count")
            add_chart_style(fig_price, height=420)
            st.plotly_chart(fig_price, width="stretch")
        else:
            st.info("A coluna `price_range` não existe no dataset atual.")

    st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

    col3, col4 = st.columns(2)

    with col3:
        st.subheader("Rating vs Quantity Sold")
        sample_n = min(1200, len(filtered))
        scatter_df = filtered.sample(sample_n, random_state=42) if sample_n > 0 else filtered
        fig_scatter = px.scatter(
            scatter_df,
            x="rating",
            y="quantity_sold",
            color="product_category",
            opacity=0.65,
        )
        fig_scatter.update_layout(xaxis_title="rating", yaxis_title="quantity_sold")
        add_chart_style(fig_scatter, height=360)
        st.plotly_chart(fig_scatter, width="stretch")

    with col4:
        st.subheader("Revenue by Payment Method")
        payment_rev = filtered.groupby("payment_method", as_index=False)["total_revenue"].sum()
        payment_rev = payment_rev.sort_values("total_revenue", ascending=True)
        fig_payment_rev = px.bar(
            payment_rev,
            x="total_revenue",
            y="payment_method",
            orientation="h",
        )
        fig_payment_rev.update_traces(marker_color="#a855f7")
        fig_payment_rev.update_layout(xaxis_title="total_revenue", yaxis_title="payment_method")
        add_chart_style(fig_payment_rev, height=360)
        st.plotly_chart(fig_payment_rev, width="stretch")

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
st.subheader("Insights Principais")

c1, c2, c3 = st.columns(3)

best_category = (
    filtered.groupby("product_category")["total_revenue"].sum().sort_values(ascending=False).index[0]
    if not filtered.empty else "-"
)
best_region = (
    filtered.groupby("customer_region")["total_revenue"].sum().sort_values(ascending=False).index[0]
    if not filtered.empty else "-"
)
most_used_payment = (
    filtered["payment_method"].value_counts().index[0]
    if not filtered.empty else "-"
)
best_month = (
    filtered.set_index("order_date").resample("ME")["total_revenue"].sum().idxmax().strftime("%b/%Y")
    if not filtered.empty else "-"
)

with c1:
    st.info(f"**Categoria mais lucrativa:** {best_category}")
with c2:
    st.info(f"**Região líder em receita:** {best_region}")
with c3:
    st.info(f"**Método de pagamento mais usado:** {most_used_payment}")

c4, c5 = st.columns(2)
with c4:
    st.success(f"**Melhor mês no recorte atual:** {best_month}")
with c5:
    avg_discount = filtered["discount_percent"].mean()
    st.warning(f"**Desconto médio no recorte atual:** {avg_discount:.2f}%")

st.markdown("---")
st.caption("Dashboard desenvolvido para o Projeto Integrador GP-41")
