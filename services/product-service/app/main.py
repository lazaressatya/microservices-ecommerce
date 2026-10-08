from fastapi import FastAPI
import os
import psycopg2

app = FastAPI()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@product-postgres:5432/productsdb"
)


def get_connection():
    return psycopg2.connect(DATABASE_URL)


@app.on_event("startup")
def startup():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            price NUMERIC(10,2) NOT NULL
        )
    """)

    connection.commit()
    cursor.close()
    connection.close()


@app.get("/")
def root():
    return {
        "service": "Product Service",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "UP",
        "service": "product-service"
    }


@app.get("/products")
def get_products():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, name, price FROM products ORDER BY id"
    )

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return [
        {
            "id": row[0],
            "name": row[1],
            "price": float(row[2])
        }
        for row in rows
    ]


@app.post("/products")
def create_product(product: dict):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO products (name, price) VALUES (%s, %s) RETURNING id",
        (
            product["name"],
            product["price"]
        )
    )

    product_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()
    connection.close()

    return {
        "id": product_id,
        "name": product["name"],
        "price": product["price"]
    }