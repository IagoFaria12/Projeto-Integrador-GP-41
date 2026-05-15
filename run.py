from etl.pipeline import run_pipeline
from config.logger import config_log, set_log
from config.connection import init_database

try:
    config_log()
    init_database()
    run_pipeline()
except Exception as generic_error:
    set_log("error", f"Erro encontrado durante a execucao: {generic_error}")