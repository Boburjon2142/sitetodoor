from datetime import datetime
import os
import random
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

IMAGE_POOL = [
    "https://images.unsplash.com/photo-1599707254554-027aeb4deacd?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1590247813693-5541d1c609fd?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1489515217757-5fd1be406fef?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1541888946425-d81bb19240f5?auto=format&fit=crop&w=1200&q=80",
    "https://images.unsplash.com/photo-1503387762-592deb58ef4e?auto=format&fit=crop&w=1200&q=80",
]

MATERIALS = [
    ("Sement", "M400 sement"),
    ("Sement", "M500 sement"),
    ("Armatura", "Armatura"),
    ("Quruq aralashma", "Gips suvoq"),
    ("Quruq aralashma", "Shpaklyovka"),
    ("G'isht", "Qizil g'isht"),
    ("Blok", "Gazoblok"),
]

SPECS = ["25kg", "40kg", "50kg", "8mm", "10mm", "12mm", "20kg", "1 dona"]


def random_price(category: str) -> int:
    if category == "Armatura":
        return random.randint(12000, 22000)
    if category == "Sement":
        return random.randint(65000, 98000)
    if category == "Quruq aralashma":
        return random.randint(30000, 70000)
    if category == "G'isht":
        return random.randint(1800, 3500)
    if category == "Blok":
        return random.randint(15000, 28000)
    return random.randint(10000, 90000)


def generate_products(count: int = 20):
    items = []
    for i in range(1, count + 1):
        category, base_name = random.choice(MATERIALS)
        spec = random.choice(SPECS)
        items.append(
            {
                "id": i,
                "name": f"{base_name} {spec}",
                "category": category,
                "price": random_price(category),
                "image": f"{random.choice(IMAGE_POOL)}&sig={i}",
            }
        )
    return items


PRODUCTS = generate_products(20)


def next_id() -> int:
    return max((p["id"] for p in PRODUCTS), default=0) + 1


@app.context_processor
def inject_globals():
    return {"year": datetime.now().year}


@app.get("/")
def home():
    q = request.args.get("q", "").strip().lower()
    if q:
        items = [p for p in PRODUCTS if q in p["name"].lower() or q in p["category"].lower()]
    else:
        items = PRODUCTS
    return render_template("index.html", products=items, q=q)


@app.get("/product/<int:product_id>")
def product_detail(product_id: int):
    product = next((p for p in PRODUCTS if p["id"] == product_id), None)
    if not product:
        return render_template("404.html"), 404
    return render_template("detail.html", product=product)


@app.get("/create")
def create_form():
    return render_template("create.html")


@app.post("/create")
def create_product():
    name = request.form.get("name", "").strip()
    category = request.form.get("category", "").strip()
    price_raw = request.form.get("price", "").strip()
    image = request.form.get("image", "").strip()

    if not name or not category or not price_raw.isdigit():
        return render_template("create.html", error="Ma'lumotlar noto'g'ri. Qayta kiriting.")

    PRODUCTS.append(
        {
            "id": next_id(),
            "name": name,
            "category": category,
            "price": int(price_raw),
            "image": image or "https://images.unsplash.com/photo-1489515217757-5fd1be406fef?auto=format&fit=crop&w=1200&q=80",
        }
    )
    return redirect(url_for("home"))


@app.errorhandler(404)
def not_found(_):
    return render_template("404.html"), 404


if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "5050"))
    debug = os.getenv("FLASK_DEBUG", "1") == "1"
    app.run(host=host, port=port, debug=debug)
