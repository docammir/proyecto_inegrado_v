import yfinance as yf
import pandas as pd
import sqlite3
import os
from logger import get_logger


class FinancialDataCollector:
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.logger = get_logger()
        self.data_dir = os.path.join(os.path.dirname(__file__), "static", "data")
        os.makedirs(self.data_dir, exist_ok=True)
        self.csv_path = os.path.join(self.data_dir, "historical.csv")
        self.db_path = os.path.join(self.data_dir, "historical.db")

    def fetch_data(self):
        self.logger.info(f"Descargando datos para: {self.symbol}")
        df = yf.download(self.symbol, progress=False)
        df.reset_index(inplace=True)
        df['Symbol'] = self.symbol
        return df

    def save_to_csv(self, df):
        if os.path.exists(self.csv_path):
            df.to_csv(self.csv_path, mode='a', header=False, index=False)
        else:
            df.to_csv(self.csv_path, index=False)
        self.logger.info(f"Datos guardados en CSV: {self.csv_path}")

    def save_to_db(self, df):
        conn = sqlite3.connect(self.db_path)
        df.to_sql("historical_data", conn, if_exists="append", index=False)
        conn.close()
        self.logger.info(f"Datos guardados en SQLite: {self.db_path}")

    def run(self):
        try:
            df = self.fetch_data()
            self.save_to_csv(df)
            self.save_to_db(df)
        except Exception as e:
            self.logger.error(f"Error al ejecutar el colector: {e}")


if __name__ == "__main__":
    collector = FinancialDataCollector("NASDAQ")  
    collector.run()