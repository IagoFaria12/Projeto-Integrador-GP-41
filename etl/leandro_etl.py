import pandas as pd

df = pd.read_csv("../data/raw/amazon_sales_dataset.csv")

# Limpar colunas desnecessárias para as métricas correspondentes ao briefing do projeto constados na documentação
colums_drop = ["discount_percent", "payment_method", "rating", "review_count", "discounted_price", "total_revenue"]
for colum_drop in colums_drop:
    df = df.drop(colum_drop, axis=1)

# Limpar linhas vazias que tem ao menos um valor correspondente a NaN, None ou null
null_rows = df.isna().sum().sum()
if null_rows > 0:
    df = df.dropna()

#  Limpa linhas que contém preco ou quantidade inferiores a zero
df = df[(df["price"] > 0) | (df["quantity_sold"] > 0)]

# Limpr linhas com informações duplicadas
duplicated_rows = df.duplicated().sum()
if duplicated_rows > 0:
    df = df.drop_duplicates()

# Padorinza a data realizando o sliced para apenas pegar ano e mês
df["order_date"] = df['order_date'].str[0:7]

# Realiza aparo nos 20& dos dados para reduzir outliers
df = df.sort_values(by="price" ,ascending=True)
lower_limit = df['price'].quantile(0.1)
upper_limit = df['price'].quantile(0.90)
df = df[(df['price'] > lower_limit) & (df['price'] < upper_limit)]


print(df)