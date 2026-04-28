import logging as lg
import pandas as pd

def header_sanitize(df):
    df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df

def drop_columns(df):
    colums_drop = ["discount_percent", "payment_method", "review_count", "discounted_price", "total_revenue"]
    df = df.drop(columns=colums_drop)
    return df

def drop_nulls(df):
    null_rows = df.isna().sum().sum()
    if null_rows > 0:
        df = df.dropna()
        lg.info(f"foram excluidas um total de {null_rows} linhas consideradas NaN e None")
    return df

def drop_duplicates(df):
    duplicated_rows = df.duplicated(subset=["order_id"]).sum()
    if duplicated_rows > 0:
        df = df.drop_duplicates(subset=["order_id"])
        lg.info(f"foram excluidas um total de {duplicated_rows} linhas com vendas duplicadas")
    return df

def sanitize_and_typed(df):
    columns_string = ["product_category", "customer_region"]
    for column in columns_string:
        df[column] = df[column].str.strip().str.title().astype('str')

    columns_integer = ["order_id", "product_id", "quantity_sold"]
    for column in columns_integer:
        df[column] = df[column].astype('int')

    df["price"] = df["price"].astype('float')
    df["order_date"] = df['order_date'].astype("str")
    df["order_date"]= df["order_date"].str.strip().str[0:7]
    return df

def clean_negatives(df):
    total_rows_negative = (df["price"] <= 0.0).sum() + (df['quantity_sold'] <= 0).sum()
    if total_rows_negative > 0:
        df = df[(df["price"] > 0) & (df["quantity_sold"] > 0)]
        lg.info(f"foram excluidas um total de {total_rows_negative} linhas de preco e quantidade negativas")
    return df

def clean_outliers(df):
    total_old_rows = len(df)
    lower_limit = df['price'].quantile(0.1)
    upper_limit = df['price'].quantile(0.9)

    df = df[(df['price'] > lower_limit) & (df['price'] < upper_limit)]
    total_after_cut_rows = len(df)
    rows_difference = total_old_rows - total_after_cut_rows

    lg.info(f"foram eliminados um total de {rows_difference} linhas que interfeririram na analise das medias")  

    return df

def return_category(value):
        if value > 4.5:
            return "Excellent"
        elif value >= 4.0 and value <= 4.4:
            return "Good"
        elif value >= 3.0 and value <= 3.9:
            return "Average"
        else:
            return "Poor"

def add_review_category(df: pd.DataFrame):
    df["rating_category"] = df["rating"].apply(return_category)
    return df