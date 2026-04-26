import pandas as pd
import logging as lg

lg.basicConfig(
    level=lg.DEBUG,
    format="%(levelname)s - %(message)s - %(asctime)s",
    filename="../logs/etl.log",
    filemode="a"
)

try:

    df = pd.read_csv("../data/raw/amazon_sales_dataset.csv")

    colums_drop = ["discount_percent", "payment_method", "rating", "review_count", "discounted_price", "total_revenue"]
    df = df.drop(columns=colums_drop)

    df.columns.str.strip().str.lower().str.replace(" ", "_")

    null_rows = df.isna().sum().sum()
    if null_rows > 0:
        df = df.dropna()
        lg.info(f"foram excluidas um total de {null_rows} linhas consideradas NaN e None")

    duplicated_rows = df.duplicated(subset=["order_id"]).sum()
    if duplicated_rows > 0:
        df = df.drop_duplicates(subset=["order_id"])
        lg.info(f"foram excluidas um total de {duplicated_rows} linhas com vendas duplicadas")

    columns_string = ["product_category", "customer_region"]
    for column in columns_string:
        df[column] = df[column].str.strip().str.title().astype('str')

    columns_integer = ["order_id", "product_id", "quantity_sold"]
    for column in columns_integer:
        df[column] = df[column].astype('int')

    df["price"] = df["price"].astype('float')
    df["order_date"] = df['order_date'].astype("str")

    df["order_date"]= df["order_date"].str.strip().str[0:7]

    total_rows_negative = (df["price"] <= 0.0).sum() + (df['quantity_sold'] <= 0).sum()
    if total_rows_negative > 0:
        df = df[(df["price"] > 0) & (df["quantity_sold"] > 0)]
        lg.info(f"foram excluidas um total de {total_rows_negative} linhas de preco e quantidade negativas")

    total_old_rows = len(df)
    lower_limit = df['price'].quantile(0.1)
    upper_limit = df['price'].quantile(0.9)
    df = df[(df['price'] > lower_limit) & (df['price'] < upper_limit)]
    total_after_cut_rows = len(df)
    rows_difference = total_old_rows - total_after_cut_rows

    lg.info(f"foram eliminados um total de {rows_difference} linhas que interfeririram na analise das medias")  

    df.to_csv("../data/processed/processed_leandro.csv", index=False)

except FileNotFoundError as file_error:
    lg.error(f"arquivo de origem ou destino do dataseset nao encontrado: {file_error}")

except KeyError as column_error:
    lg.error(f"coluna do dataset nao encontrada: {column_error}")