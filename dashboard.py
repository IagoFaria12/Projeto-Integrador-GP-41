import streamlit as st
import pandas as pd
import plotly.express as px

# IMPORTS DO PROJETO (BACK + FILTROS)
from config.connection import get_connection
from business.queries import (
    items_per_order,
    gross_evolution_over_time,
    order_top_sales,
    gross_by_category,
    gross_discount_comparison,
    gross_price_range_distribution,
    gross_total_revenue,
    total_revenue_with_discount,
    total_number_of_orders,
    average_evaluation_of_products,
    order_discount_comparison,
    avarege_tickets,
    gross_by_region
)

# CONFIGURAÇÃO DA PÁGINA
st.set_page_config(
    page_title="Amazon Performance Dashboard",
    layout="wide"
)

# MAPEAMENTO DE CORES PARA AS CATEGORIAS
CORES_CATEGORIAS = {
    "Electronics": "#37475a",
    "Books": "#ff9900",
    "Fashion": "#232f3e",
    "Home & Kitchen": "#48607f",
    "Beauty": "#5e7999",
    "Sports": "#ffc266"
}

# MAPEAMENTO DE CORES PARA AS REGIÕES
CORES_REGIOES = {
    "Asia": "#FFD700",
    "Europe": "#000080",
    "North America": "#880808",
    "Middle East": "#FF9900"
}


# ==========================================
# ====== SIDEBAR - PAINEL DE CONTROLE ======
# ==========================================
st.sidebar.header("PAINEL DE CONTROLE")

# FILTRO DE CATEGORIAS
conn, cursor = get_connection()
try:
    df_cats = pd.read_sql_query("SELECT id, name FROM categories", conn)
finally:
    cursor.close()
    conn.close()

opcoes_categorias = df_cats['name'].tolist()

categorias_nomes = st.sidebar.multiselect(
    "Categorias de Produtos",
    options=opcoes_categorias,
    default=opcoes_categorias
)

categorias_ids = df_cats[df_cats['name'].isin(categorias_nomes)]['id'].tolist()

# FILTROS DE TEMPO
lista_anos = ["Todos", "2022", "2023"]
ano_sel = st.sidebar.selectbox("Ano de Análise", lista_anos)
ano_backend = None if ano_sel == "Todos" else ano_sel

lista_meses = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
mes_ini = st.sidebar.selectbox("Mês Inicial", options=lista_meses, index=0)

opcoes_mes_fim = ["Apenas este mês"] + lista_meses[lista_meses.index(mes_ini):]
mes_fim_sel = st.sidebar.selectbox("Mês Final", options=opcoes_mes_fim, index=0)
mes_fim = "" if mes_fim_sel == "Apenas este mês" else mes_fim_sel

# ==========================================
# ========== DADOS DOS KPIS ================
# ==========================================

row_gross = gross_total_revenue(categorias_ids, ano_backend, mes_ini, mes_fim)
row_liquid = total_revenue_with_discount(categorias_ids, ano_backend, mes_ini, mes_fim)
row_orders = total_number_of_orders(categorias_ids, ano_backend, mes_ini, mes_fim)
row_rating = average_evaluation_of_products(categorias_ids, ano_backend, mes_ini, mes_fim)
row_items = items_per_order(categorias_ids, ano_backend, mes_ini, mes_fim)

if row_items and row_items.get('average_items_per_order') is not None:
    val_items = row_items['average_items_per_order']
else:
    val_items = 0.0

val_gross = row_gross['total_gross_revenue'] if row_gross and row_gross['total_gross_revenue'] is not None else 0
val_liquid = row_liquid['total_revenue'] if row_liquid and row_liquid['total_revenue'] is not None else 0
val_orders = row_orders['quantity_total_orders'] if row_orders and row_orders['quantity_total_orders'] is not None else 0
val_rating = row_rating['average_product_evaluation'] if row_rating and row_rating['average_product_evaluation'] is not None else 0.0

valor_desconto = val_gross - val_liquid


# ==========================================
# ======== RENDERIZAÇÃO DOS KPIS ===========
# ==========================================

# Título Principal
st.title("📊 Amazon Sales & Marketing Analytics")
st.markdown("---")

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.metric(label="Faturamento Bruto", value=f"U$ {val_gross:,.2f}")

with kpi2:
    st.metric(
        label="Faturamento (c/ Desconto)",
        value=f"U$ {val_liquid:,.2f}",
        delta=f"-U$ {valor_desconto:,.2f}",
        delta_color="inverse"
    )

with kpi3:
    st.metric(label="Total de Pedidos", value=f"{val_orders:,}")

with kpi4:
    st.metric(label="Avaliação Média", value=f"⭐ {val_rating:.1f}")

with kpi5:
    st.metric(label="Itens por Pedido (Média)", value=f"{val_items:.1f}")

st.markdown("---")

# ==========================================
# ====== DIVISÃO DO DASHBOARD EM ABAS ======
# ==========================================
tab_financeiro, tab_produtos, tab_precificacao = st.tabs([
    "📈 Performance Financeira",
    "📦 Análise de Produtos",
    "🎯 Precificação & Estratégia"
])

# ---- ABA 1: PERFORMANCE FINANCEIRA ----
with tab_financeiro:
    col_fin1, col_fin2 = st.columns([2, 1])

    with col_fin1:
        st.subheader("Evolução Temporal do Faturamento")

        raw_evolucao = gross_evolution_over_time(categorias_ids, ano_backend, mes_ini, mes_fim)

        if raw_evolucao:
            df_ev = pd.DataFrame([dict(r) for r in raw_evolucao])
            df_ev['date'] = pd.to_datetime(df_ev['date'])
            df_ev = df_ev.sort_values('date')

            fig_ev = px.line(
                df_ev,
                x='date',
                y='gross_total',
                labels={'date': 'Data', 'gross_total': 'Faturamento Bruto (U$)'},
                template="plotly_white"
            )
            fig_ev.update_traces(line={"color": "#FF9900", "width": 3})
            st.plotly_chart(fig_ev, use_container_width=True)
        else:
            st.info("Sem dados de evolução temporal para os filtros selecionados.")

    with col_fin2:
        st.subheader("Faturamento por Região")

        raw_regiao = gross_by_region(ano_backend, mes_ini, mes_fim)

        if raw_regiao:
            df_regiao = pd.DataFrame([dict(r) for r in raw_regiao])

            fig_regiao = px.bar(
                df_regiao,
                x='name',
                y='gross_total',
                color='name',
                color_discrete_map=CORES_REGIOES,
                labels={'name': 'Região', 'gross_total': 'Faturamento (U$)'},
                template="plotly_white"
            )

            fig_regiao.update_layout(showlegend=False)
            st.plotly_chart(fig_regiao, use_container_width=True)
        else:
            st.info("Sem dados de faturamento por região.")

# ---- ABA 2: ANÁLISE DE PRODUTOS ----
with tab_produtos:
    col_prod1, col_prod2 = st.columns([3, 2])

    with col_prod1:
        st.subheader("Top 10 Produtos Mais Vendidos")

        raw_top = order_top_sales(categorias_ids, ano_backend, mes_ini, mes_fim)

        if raw_top:
            df_top = pd.DataFrame([dict(r) for r in raw_top])


            def colorir_categoria(val):
                cor = CORES_CATEGORIAS.get(val, "transparent")
                return f'background-color: {cor}; color: white; font-weight: bold;'

            df_estilizado = df_top.rename(columns={
                'product_id': 'ID',
                'category': 'Categoria',
                'price': 'Preço (U$)',
                'average_rating': 'Avaliação',
                'quantity_sold': 'Qtd Vendida'
            })

            df_final = (df_estilizado.style
            .map(colorir_categoria, subset=['Categoria'])
            .format({
                'Preço (U$)': 'U$ {:.2f}',
                'Avaliação': '{:.1f}'
            })
            .set_table_styles([
                {
                    'selector': 'th',
                    'props': [
                        ('background-color', '#262730'),
                        ('color', 'white'),
                        ('font-weight', 'bold')
                    ]
                }
            ]))

            st.dataframe(df_final, hide_index=True, use_container_width=True)
        else:
            st.info("Sem dados de top produtos para os filtros selecionados.")

    with col_prod2:
        st.subheader("Faturamento por Categoria")

        raw_cat = gross_by_category(ano_backend, mes_ini, mes_fim)

        if raw_cat:
            df_cat = pd.DataFrame([dict(r) for r in raw_cat])

            fig_cat = px.pie(
                df_cat,
                names='name',
                values='gross_total',
                hole=0.4,
                color='name',
                color_discrete_map=CORES_CATEGORIAS,
                template="plotly_white"
            )
            st.plotly_chart(fig_cat, use_container_width=True)
        else:
            st.info("Sem dados de faturamento por categoria.")

# ---- ABA 3: PRECIFICAÇÃO & ESTRATÉGIA ----
with tab_precificacao:
    col_pre1, col_pre2 = st.columns(2)

    with col_pre1:
        st.subheader("Distribuição por Faixa de Preço")

        raw_price = gross_price_range_distribution(categorias_ids, ano_backend, mes_ini, mes_fim)

        if raw_price:
            df_price = pd.DataFrame([dict(r) for r in raw_price])
            df_price['price_range'] = pd.Categorical(
                df_price['price_range'],
                categories=['Low', 'Mid', 'High'],
                ordered=True
            )
            df_price = df_price.sort_values('price_range')

            degrade_laranja = ["#FFE0B2", "#FF9900", "#E65100"]

            fig_price = px.bar(
                df_price,
                x='price_range',
                y='gross_total',
                color='price_range',
                color_discrete_sequence=degrade_laranja,
                labels={'price_range': 'Faixa de Preço', 'gross_total': 'Faturamento Total (U$)'},
                template="plotly_white",
            )

            fig_price.update_layout(showlegend=False)
            st.plotly_chart(fig_price, use_container_width=True)
        else:
            st.info("Sem dados de distribuição por faixa de preço.")

    with col_pre2:
        st.subheader("Impacto das Campanhas no Volume de Pedidos")

        raw_desc = order_discount_comparison(categorias_ids, ano_backend, mes_ini, mes_fim)

        if raw_desc:
            df_desc = pd.DataFrame([dict(r) for r in raw_desc])

            df_desc['category_discount'] = df_desc['category_discount'].map({
                'with_discount': 'Com Desconto',
                'without_discount': 'Preço Regular'
            })

            fig_desc = px.pie(
                df_desc,
                names='category_discount',
                values='order_total',
                hole=0.4,
                color='category_discount',
                color_discrete_map={'Com Desconto': '#FF9900', 'Preço Regular': '#232F3E'},
                template="plotly_white"
            )

            fig_desc.update_traces(textinfo='percent+value')

            st.plotly_chart(fig_desc, use_container_width=True)
        else:
            st.info("Sem dados de impacto de descontos para os filtros selecionados.")

    # ---- SEÇÃO: TICKET MÉDIO ----
    st.markdown("---")
    st.subheader("📊 Agrupamento Estatístico de Ticket Médio")

    raw_tickets = avarege_tickets(categorias_ids, ano_backend, mes_ini, mes_fim)

    if raw_tickets:
        df_tk = pd.DataFrame([dict(r) for r in raw_tickets])

        fig_tk = px.bar(
            df_tk,
            x='average_ticket',
            y='category',
            orientation='h',
            text='average_ticket',
            labels={'average_ticket': 'Valor Médio (U$)', 'category': 'Faixa de Custo'},
            template="plotly_white",
            color_discrete_sequence=['#FF9900']
        )

        fig_tk.update_traces(texttemplate='U$ %{text:.2f}', textposition='outside')

        fig_tk.update_layout(margin=dict(r=50))

        st.plotly_chart(fig_tk, use_container_width=True)
    else:
        st.info("Sem dados de ticket médio para os filtros selecionados.")

