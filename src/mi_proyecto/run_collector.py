from mi_proyecto.collector import FinancialDataCollector

if __name__ == "__main__":
    collector = FinancialDataCollector("AAPL")
    collector.run()
