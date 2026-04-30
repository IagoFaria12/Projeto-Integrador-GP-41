from etl.transform import *
from etl.load import load_database
from config.logger import config_log, set_log
import pandas as pd

def run_pipeline():
    try:
        config_log()

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

        df.to_csv("data/processed/amazon_sales_dataset.csv", index=False)

        processed_df = pd.read_csv("data/processed/amazon_sales_dataset.csv")
        load_database(processed_df)
        
    except FileNotFoundError as file_error:
        set_log("error", f"arquivo de origem ou destino do dataseset nao encontrado: {file_error}")

    except KeyError as column_error:
        set_log("error", f"coluna do dataset nao encontrada: {column_error}")

if __name__ == "__main__":
    run_pipeline()
