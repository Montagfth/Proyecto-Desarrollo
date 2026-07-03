import os
import joblib
import pandas as pd
import numpy as np
from dotenv import load_dotenv
import libsql_client

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# ============================================
# Configuración
# ============================================

load_dotenv()

TURSO_DATABASE_URL = os.getenv("TURSO_DATABASE_URL", "file:local.db")
TURSO_AUTH_TOKEN = os.getenv("TURSO_AUTH_TOKEN", "")

if "your-database-name.turso.io" in TURSO_DATABASE_URL or not TURSO_DATABASE_URL:
    TURSO_DATABASE_URL = "file:local.db"

FEATURES = [
    "TipoTrabajo",
    "Cantidad",
    "Tamaño",
    "Material",
    "Color"
]

TARGET = "TiempoMinutos"


# ============================================
# Obtener datos desde Turso
# ============================================

def fetch_training_data(client):
    print("Extrayendo datos históricos...")

    query = """
    SELECT
        t.print_type AS TipoTrabajo,
        o.quantity AS Cantidad,
        s.print_size AS Tamaño,
        m.print_material AS Material,
        o.colored AS Color,
        o.final_time AS TiempoMinutos
    FROM orders o
    JOIN print_types t
        ON o.print_type = t.type_id
    JOIN print_sizes s
        ON o.print_size = s.size_id
    JOIN print_materials m
        ON o.print_material = m.material_id
    WHERE
        o.status = 'Completado'
        AND o.final_time IS NOT NULL;
    """

    result = client.execute(query)

    if len(result.rows) < 30:
        print("⚠ Muy pocos datos reales para entrenar.")
        print("Usando datos simulados...")
        return generate_mock_data()

    columns = list(result.columns)
    data = [list(row) for row in result.rows]

    return pd.DataFrame(data, columns=columns)


# ============================================
# Datos simulados
# ============================================

def generate_mock_data():
    np.random.seed(42)

    n = 500

    df = pd.DataFrame({
        "TipoTrabajo": np.random.choice(
            ["Banner", "Documento", "Flyer", "Plano", "Tarjeta"],
            n
        ),
        "Cantidad": np.random.randint(5, 500, n),
        "Tamaño": np.random.choice(
            ["A2", "A3", "A4", "Grande"],
            n
        ),
        "Material": np.random.choice(
            ["Bond", "Cartulina", "Couche", "Vinil"],
            n
        ),
        "Color": np.random.choice([0, 1], n)
    })

    tipo = {
        "Banner": 30,
        "Documento": 10,
        "Flyer": 18,
        "Plano": 22,
        "Tarjeta": 14
    }

    tamaño = {
        "A4": 2,
        "A3": 6,
        "A2": 12,
        "Grande": 25
    }

    material = {
        "Bond": 2,
        "Cartulina": 8,
        "Couche": 6,
        "Vinil": 20
    }

    ruido = np.random.randint(0, 8, n)

    df[TARGET] = (
        df["Cantidad"] * 0.12
        + df["Color"] * 10
        + df["TipoTrabajo"].map(tipo)
        + df["Tamaño"].map(tamaño)
        + df["Material"].map(material)
        + ruido
    )

    return df


# ============================================
# Programa principal
# ============================================

def main():
    print(f"Conectando a la base de datos: {TURSO_DATABASE_URL}")

    try:
        if TURSO_DATABASE_URL.startswith("file:"):
            client = libsql_client.create_client_sync(TURSO_DATABASE_URL)
        else:
            client = libsql_client.create_client_sync(
                TURSO_DATABASE_URL,
                auth_token=TURSO_AUTH_TOKEN
            )

    except Exception as e:
        print(f"Error de conexión: {e}")
        return

    try:
        df = fetch_training_data(client)

        print(f"Registros utilizados para entrenamiento: {len(df)}")

        X = df[FEATURES]
        y = df[TARGET]

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42
        )

        categorical_features = [
            "TipoTrabajo",
            "Tamaño",
            "Material"
        ]

        preprocessor = ColumnTransformer(
            transformers=[
                (
                    "categorical",
                    OneHotEncoder(handle_unknown="ignore"),
                    categorical_features
                )
            ],
            remainder="passthrough"
        )

        models = {
            "linear_regression": LinearRegression(),

            "decision_tree": DecisionTreeRegressor(
                max_depth=6,
                random_state=42
            ),

            "random_forest": RandomForestRegressor(
                n_estimators=300,
                random_state=42,
                n_jobs=-1
            )
        }

        os.makedirs("models", exist_ok=True)

        print("\n========== Entrenamiento ==========\n")

        for name, model in models.items():

            pipeline = Pipeline([
                ("preprocessor", preprocessor),
                ("model", model)
            ])

            pipeline.fit(X_train, y_train)

            predictions = pipeline.predict(X_test)

            mae = mean_absolute_error(y_test, predictions)
            r2 = r2_score(y_test, predictions)

            print("=" * 45)
            print(name.upper())
            print(f"MAE : {mae:.2f} minutos")
            print(f"R²  : {r2:.4f}")

            model_path = os.path.join(
                "models",
                f"{name}_model.pkl"
            )

            joblib.dump(pipeline, model_path)

            print(f"Modelo guardado en: {model_path}")

        print("\n====================================")
        print("Entrenamiento finalizado correctamente.")
        print("====================================")

    finally:
        client.close()


if __name__ == "__main__":
    main()