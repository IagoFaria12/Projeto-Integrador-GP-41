from etl.transform import header_sanitize, drop_columns, drop_nulls, drop_duplicates,sanitize_and_typed, clean_negatives, clean_outliers
import pandas as pd
import logging as lg

lg.basicConfig(
    level=lg.DEBUG,
    format="%(levelname)s - %(message)s - %(asctime)s",
    filename="logs/etl.log",
    filemode="a"
)

def run_pipeline():
    try:
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
    except FileNotFoundError as file_error:
        lg.error(f"arquivo de origem ou destino do dataseset nao encontrado: {file_error}")

    except KeyError as column_error:
        lg.error(f"coluna do dataset nao encontrada: {column_error}")

if __name__ == "__main__":
    run_pipeline()
