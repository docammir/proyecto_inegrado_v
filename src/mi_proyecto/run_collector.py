from mi_proyecto.collector import FinancialDataCollector
import sys

if __name__ == "__main__":
    try:
        print("[INFO] Iniciando colector para AAPL")
        collector = FinancialDataCollector("AAPL")
        collector.run()
        print("[INFO] Finalizó correctamente")
    except Exception as e:
        print(f"[ERROR] Falló el colector: {e}")
        sys.exit(1)
