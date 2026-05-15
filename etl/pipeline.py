from .transform import *
from .load import load_database
import pandas as pd

def run_pipeline():
    df = pd.read_csv("data/raw/amazon_sales_dataset.csv")

    df = (df
        .pipe(header_sanitize)
        .pipe(drop_columns)
        .pipe(drop_nulls)
        .pipe(drop_duplicates)
        .pipe(sanitize_and_typed)
        .pipe(clean_negatives)
        .pipe(clean_outliers)
    )

    load_database(df)

    