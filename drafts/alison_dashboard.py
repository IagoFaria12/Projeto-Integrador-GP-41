import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

# código terminal para acesso dashboard: cd "c:\Users\moret\OneDrive\Documentos\Projeto-Integrador-GP-41" >> .\.venv\Scripts\python.exe -m streamlit run etl/alison_etl.py --server.port 8501
df = pd.read_csv('data/raw/amazon_sales_dataset.csv')

df_limpo = df.dropna()
print("=" * 60)
print("1. RECEITA E VENDAS")
print("=" * 60)

receita_total = df_limpo['total_revenue'].sum()
print(f"\nReceita Total: R$ {receita_total:,.2f}")

receita_categoria = df_limpo.groupby('product_category')['total_revenue'].sum().sort_values(ascending=False)
print("\nReceita por Categoria:")
print(receita_categoria)

receita_regiao = df_limpo.groupby('customer_region')['total_revenue'].sum().sort_values(ascending=False)
print("\nReceita por Região:")
print(receita_regiao)

produtos_mais_vendidos = df_limpo.groupby('product_id')['quantity_sold'].sum().sort_values(ascending=False).head(10)
print("\nTop 10 Produtos mais vendidos (por quantidade):")
print(produtos_mais_vendidos)
print("\n" + "=" * 60)
print("2. DESCONTOS E PRECIFICAÇÃO")
print("=" * 60)

media_desconto = df_limpo['discount_percent'].mean()
print(f"\nMédia de Desconto: {media_desconto:.2f}%")

desconto_por_categoria = df_limpo.groupby('product_category').agg({
    'discount_percent': 'mean',
    'total_revenue': 'sum'
}).sort_values('total_revenue', ascending=False)
print("\nDesconto Médio por Categoria:")
print(desconto_por_categoria)

relacao_desconto_qtd = df_limpo.groupby('discount_percent')['quantity_sold'].sum().head(10)
print("\nQuantidade Vendida por Percentual de Desconto (primeiros 10):")
print(relacao_desconto_qtd)
print("\n" + "=" * 60)
print("3. AVALIAÇÕES E REVIEWS")
print("=" * 60)

produtos_avaliados = df_limpo.groupby('product_id').agg({
    'rating': 'mean',
    'review_count': 'sum',
    'quantity_sold': 'sum'
}).sort_values('rating', ascending=False).head(10)
print("\nTop 10 Produtos melhor avaliados:")
print(produtos_avaliados)

correlacao = df_limpo['rating'].corr(df_limpo['quantity_sold'])
print(f"\nCorrelação entre Rating e Quantidade Vendida: {correlacao:.4f}")
rating_categoria = df_limpo.groupby('product_category')['rating'].mean().sort_values(ascending=False)
print("\nMédia de Rating por Categoria:")
print(rating_categoria)
print("\n" + "=" * 60)
print("4. MÉTODOS DE PAGAMENTO")
print("=" * 60)

dist_pagamento = df_limpo['payment_method'].value_counts()
print("\nDistribuição por Método de Pagamento:")
print(dist_pagamento)

receita_pagamento = df_limpo.groupby('payment_method')['total_revenue'].sum().sort_values(ascending=False)
print("\nReceita por Método de Pagamento:")
print(receita_pagamento)
print("\n" + "=" * 60)
print("5. ANÁLISE TEMPORAL")
print("=" * 60)

df_limpo['order_date'] = pd.to_datetime(df_limpo['order_date'])

vendas_mes = df_limpo.set_index('order_date').resample('ME')['total_revenue'].sum()
print("\nReceita por Mês:")
print(vendas_mes)

mes_maior_receita = vendas_mes.idxmax()
receita_mes_maior = vendas_mes.max()
print(f"\nMês com maior receita: {mes_maior_receita.strftime('%Y-%m')} - R$ {receita_mes_maior:,.2f}")

pedidos_mes = df_limpo.set_index('order_date').resample('ME')['order_id'].count()
print("\nQuantidade de Pedidos por Mês:")
print(pedidos_mes)

"""
Dashboard Interativo - Amazon Sales Analytics
Para executar: streamlit run dashboard.py
"""

st.set_page_config(
    page_title="Amazon Sales Dashboard",
    page_icon="📊",
    layout="wide"
)
@st.cache_data
def carregar_dados():
    df = pd.read_csv('data/raw/amazon_sales_dataset.csv')
    df_limpo = df.dropna()
    df_limpo['order_date'] = pd.to_datetime(df_limpo['order_date'])
    return df_limpo

df = carregar_dados()

st.title("📊 Amazon Sales Dashboard")
st.markdown("---")

receita_total = df['total_revenue'].sum()
media_desconto = df['discount_percent'].mean()
produtos_unicos = df['product_id'].nunique()
pedidos_unicos = df['order_id'].nunique()

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Receita Total", f"R$ {receita_total:,.0f}", delta=None)

with col2:
    st.metric("Média de Desconto", f"{media_desconto:.1f}%", delta=None)

with col3:
    st.metric("Produtos Únicos", f"{produtos_unicos}", delta=None)

with col4:
    st.metric("Total de Pedidos", f"{pedidos_unicos:,}", delta=None)

st.markdown("---")
st.header("1. Receita e Vendas")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Receita por Categoria")
    receita_categoria = df.groupby('product_category')['total_revenue'].sum().reset_index()
    receita_categoria = receita_categoria.sort_values('total_revenue', ascending=True)
    
    fig_categoria = px.bar(
        receita_categoria, 
        x='total_revenue', 
        y='product_category',
        orientation='h',
        color='total_revenue',
        color_continuous_scale='Blues',
        text='total_revenue',
        text_auto='.2s',
        title="Receita por Categoria de Produto"
    )
    fig_categoria.update_layout(yaxis_title="", xaxis_title="Receita (R$)")
    st.plotly_chart(fig_categoria, width='stretch')

with col2:
    st.subheader("Receita por Região")
    receita_regiao = df.groupby('customer_region')['total_revenue'].sum().reset_index()
    receita_regiao = receita_regiao.sort_values('total_revenue', ascending=True)
    
    fig_regiao = px.bar(
        receita_regiao, 
        x='total_revenue', 
        y='customer_region',
        orientation='h',
        color='total_revenue',
        color_continuous_scale='Greens',
        text='total_revenue',
        text_auto='.2s',
        title="Receita por Região do Cliente"
    )
    fig_regiao.update_layout(yaxis_title="", xaxis_title="Receita (R$)")
    st.plotly_chart(fig_regiao, width='stretch')

st.markdown("---")
st.header("2. Descontos e Precificação")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Desconto Médio por Categoria")
    desconto_cat = df.groupby('product_category').agg({
        'discount_percent': 'mean',
        'total_revenue': 'sum'
    }).reset_index()
    desconto_cat = desconto_cat.sort_values('discount_percent', ascending=False)
    
    fig_desconto = px.bar(
        desconto_cat,
        x='product_category',
        y='discount_percent',
        color='discount_percent',
        color_continuous_scale='Reds',
        title="Desconto Médio por Categoria (%)",
        text_auto='.1f'
    )
    fig_desconto.update_layout(xaxis_title="", yaxis_title="Desconto (%)")
    st.plotly_chart(fig_desconto, width='stretch')

with col2:
    st.subheader("Desconto vs Quantidade Vendida")
    desconto_qtd = df.groupby('discount_percent')['quantity_sold'].sum().reset_index()
    
    fig_desconto_qtd = px.bar(
        desconto_qtd,
        x='discount_percent',
        y='quantity_sold',
        title="Quantidade Vendida por % de Desconto",
        color='quantity_sold',
        color_continuous_scale='Viridis',
        text='quantity_sold'
    )
    fig_desconto_qtd.update_layout(xaxis_title="Desconto (%)", yaxis_title="Quantidade Vendida")
    st.plotly_chart(fig_desconto_qtd, width='stretch')

st.markdown("---")
st.header("3. Avaliações e Reviews")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Rating Médio por Categoria")
    rating_cat = df.groupby('product_category')['rating'].mean().reset_index()
    rating_cat = rating_cat.sort_values('rating', ascending=False)
    
    fig_rating = px.bar(
        rating_cat,
        x='product_category',
        y='rating',
        title="Rating Médio por Categoria",
        color='rating',
        color_continuous_scale='RdYlGn',
        range_color=[2.5, 3.5],
        text='rating',
        text_auto='.2f'
    )
    fig_rating.update_layout(xaxis_title="", yaxis_title="Rating (0-5)")
    st.plotly_chart(fig_rating, width='stretch')

with col2:
    st.subheader("Rating vs Quantidade Vendida")
    fig_dispersao = px.scatter(
        df.sample(min(1000, len(df))),
        x='rating',
        y='quantity_sold',
        color='product_category',
        title="Relação entre Rating e Quantidade Vendida",
        opacity=0.6
    )
    fig_dispersao.update_layout(xaxis_title="Rating", yaxis_title="Quantidade Vendida")
    st.plotly_chart(fig_dispersao, width='stretch')

st.markdown("---")
st.header("4. Métodos de Pagamento")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribuição de Pedidos por Método")
    pagamento_dist = df['payment_method'].value_counts().reset_index()
    pagamento_dist.columns = ['payment_method', 'count']
    
    fig_pizza = px.pie(
        pagamento_dist,
        values='count',
        names='payment_method',
        title="Distribuição por Método de Pagamento",
        hole=0.4
    )
    st.plotly_chart(fig_pizza, width='stretch')

with col2:
    st.subheader("Receita por Método de Pagamento")
    pagamento_receita = df.groupby('payment_method')['total_revenue'].sum().reset_index()
    pagamento_receita = pagamento_receita.sort_values('total_revenue', ascending=False)
    
    fig_pag_rec = px.bar(
        pagamento_receita,
        x='payment_method',
        y='total_revenue',
        color='total_revenue',
        color_continuous_scale='Purples',
        title="Receita por Método de Pagamento",
        text='total_revenue',
        text_auto='.2s'
    )
    fig_pag_rec.update_layout(xaxis_title="", yaxis_title="Receita (R$)")
    st.plotly_chart(fig_pag_rec, width='stretch')

st.markdown("---")
st.header("5. Análise Temporal")

vendas_mes = df.set_index('order_date').resample('ME')['total_revenue'].sum().reset_index()
vendas_mes['order_date'] = vendas_mes['order_date'].dt.strftime('%Y-%m')

fig_linha = px.line(
    vendas_mes,
    x='order_date',
    y='total_revenue',
    title="Evolução da Receita Mensal",
    markers=True,
    line_shape='spline'
)
fig_linha.update_layout(xaxis_title="Mês", yaxis_title="Receita (R$)")
fig_linha.update_traces(line_color='#4361ee', line_width=3)
st.plotly_chart(fig_linha, width='stretch')

st.markdown("---")
st.header("💡 Insights Principais")

insights = """
| # | Insight | Ação Recomendada |
|---|---------|-------------------|
| 1 | **Beauty** é a categoria mais lucrativa (R$ 5,5M) | Manter investimento em estoque e marketing |
| 2 | **Middle East** lidera em receita (R$ 8,3M) | Considerar campanhas específicas para a região |
| 3 | **Descontos não impactam significativamente** as vendas | Revisar estratégia de precificação |
| 4 | **Wallet** é o método mais utilizado (20%) | Garantir experiência fluida de pagamento digital |
| 5 | **Janeiro/2023** teve a maior receita (R$ 1,4M) | Planejar promoções para início do ano |
| 6 | **Rating não influencia** volume de vendas | Focar em outros fatores (preço, logística) |
"""
st.markdown(insights)
st.markdown("---")
st.caption("Dashboard desenvolvido para o Projeto Integrador GP-41")
