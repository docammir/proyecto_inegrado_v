import os
import pandas as pd
import pickle
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
import numpy as np


class PricePredictor:
    def __init__(self):
        self.model_path = os.path.join(os.path.dirname(__file__), "..", "static", "models", "model.pkl")
        self.data_path = os.path.join(os.path.dirname(__file__), "..", "static", "data", "historical.csv")
        self.model = None

    def entrenar(self):
        df = pd.read_csv(self.data_path)

        # Limpiar NaNs generados por cálculos rolling/pct_change
        df = df.dropna()

        # Variables predictoras (features)
        X = df[["Open", "High", "Low", "Volume", "Media Móvil 20", "Volatilidad 20", "Tasa de Variación"]]
        y = df["Close"]

        # Dividir en entrenamiento y prueba
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

        # Entrenar modelo
        model = LinearRegression()
        model.fit(X_train, y_train)
        self.model = model

        # Guardar modelo
        os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
        with open(self.model_path, "wb") as f:
            pickle.dump(model, f)

        # Evaluar rendimiento
        y_pred = model.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        print(f"Modelo entrenado y guardado. RMSE: {rmse:.4f}")

        # Justificación:
        print("\n✅ Usamos RMSE porque penaliza más los errores grandes y es útil cuando los errores grandes son costosos.")

    def predecir(self, df_nuevo):
        # Asegurarse de que el modelo esté cargado
        if self.model is None:
            with open(self.model_path, "rb") as f:
                self.model = pickle.load(f)

        df_nuevo = df_nuevo.dropna()
        X_nuevo = df_nuevo[["Open", "High", "Low", "Volume", "Media Móvil 20", "Volatilidad 20", "Tasa de Variación"]]
        predicciones = self.model.predict(X_nuevo)
        return predicciones


if __name__ == "__main__":
    predictor = PricePredictor()
    predictor.entrenar()
