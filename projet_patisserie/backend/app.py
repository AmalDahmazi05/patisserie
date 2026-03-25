from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import os, sqlite3, json as _json
from datetime import datetime

FRONTEND_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'frontend')
app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
CORS(app)

# ── Sert le frontend (index.html) ─────────────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

# ── Base de données SQLite ────────────────────────────────────────────────────
DATA_DIR    = os.path.dirname(os.path.abspath(__file__))
DATA_FOLDER = os.path.join(DATA_DIR, "data")
DB_PATH     = os.path.join(DATA_FOLDER, "patisserie.db")

os.makedirs(DATA_FOLDER, exist_ok=True)

ADMIN_USER = "admin"
ADMIN_PASS = "patisserie123"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c    = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT NOT NULL,
            price       REAL NOT NULL,
            description TEXT,
            image       TEXT,
            category    TEXT DEFAULT 'autre'
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id      INTEGER PRIMARY KEY AUTOINCREMENT,
            name    TEXT NOT NULL,
            phone   TEXT NOT NULL,
            address TEXT NOT NULL,
            items   TEXT NOT NULL,
            total   REAL NOT NULL,
            status  TEXT DEFAULT 'en attente',
            date    TEXT NOT NULL
        )
    """)
    c.execute("SELECT COUNT(*) FROM products")
    if c.fetchone()[0] == 0:
        defaults = [
            ("Tarte aux Fraises",     25,  "Pâte sablée croustillante garnie de crème pâtissière et de fraises fraîches.",           "https://i.pinimg.com/736x/4a/2c/ce/4a2cced70fd06dd6ce9eb9727f58d103.jpg", "tartes"),
            ("Éclair au Chocolat",   12,  "Pâte à choux légère, fourrée de crème au chocolat et nappée de glaçage.",                            "https://i.pinimg.com/736x/81/e1/9e/81e19e9417a160c2b914fae54cdbaac5.jpg", "gâteaux"),
            ("Macaron Framboise",    10,  "Coques croustillantes et fondantes, garnies d’une crème à la framboise.",                        "https://i.pinimg.com/1200x/8f/1d/74/8f1d74387eee8b9d36636d6065e6b9c3.jpg","cookies"),
            ("Mille-Feuille Vanille", 20,   "Feuilletage croustillant alterné avec une crème vanille onctueuse.",                           "https://i.pinimg.com/736x/30/1a/9d/301a9d508af1a959f055b3a5d3f583e7.jpg", "desserts"),
            ("Fondant Chocolat",      18,   "Gâteau au chocolat avec un cœur fondant et intense.",                                         "https://i.pinimg.com/736x/fd/e4/75/fde4754d968d33518820dc8e61eb8920.jpg", "desserts"),
            ("Cookie Noisette",      8,  "Biscuit moelleux aux éclats de noisettes et pépites de chocolat.",                      "https://i.pinimg.com/1200x/7a/7a/84/7a7a84e5710e6efa3ef741ef6e5181ea.jpg","cookies"),
            ("Opéra Classique",      22,  "Gâteau fin au café et chocolat, composé de couches de biscuit et de crème.",       "https://i.pinimg.com/1200x/5b/14/bb/5b14bb3919ad3ea1727f152305f0d11c.jpg","gâteaux"),
            ("Paris-Brest",           20,  "Pâte à choux en couronne garnie de crème pralinée aux amandes/noisettes.", "https://i.pinimg.com/736x/84/10/32/841032f2bada8943364dba173d938dce.jpg", "gâteaux"),
            ("Tarte Citron Meringuée",23, "Tarte au citron acidulée recouverte d’une meringue légère et dorée.","https://i.pinimg.com/1200x/e1/1e/d5/e11ed58e0003008e3e6c2876b4c4b2c8.jpg","tartes"),
        ]
        c.executemany(
            "INSERT INTO products (name, price, description, image, category) VALUES (?,?,?,?,?)",
            defaults
        )
    conn.commit()
    conn.close()

# ── PRODUITS ──────────────────────────────────────────────────────────────────

@app.route("/api/products", methods=["GET"])
def get_products():
    conn = get_db()
    rows = conn.execute("SELECT * FROM products").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route("/api/products", methods=["POST"])
def add_product():
    d     = request.json or {}
    name  = d.get("name",  "").strip()
    price = float(d.get("price", 0))
    if not name or price <= 0:
        return jsonify({"error": "Nom et prix obligatoires"}), 400
    conn = get_db()
    cur  = conn.execute(
        "INSERT INTO products (name, price, description, image, category) VALUES (?,?,?,?,?)",
        (name, price, d.get("description","").strip(), d.get("image",""), d.get("category","autre"))
    )
    conn.commit()
    row = conn.execute("SELECT * FROM products WHERE id=?", (cur.lastrowid,)).fetchone()
    conn.close()
    return jsonify(dict(row)), 201

@app.route("/api/products/<int:pid>", methods=["PUT"])
def update_product(pid):
    d    = request.json or {}
    conn = get_db()
    row  = conn.execute("SELECT * FROM products WHERE id=?", (pid,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "Introuvable"}), 404
    conn.execute(
        "UPDATE products SET name=?, price=?, description=?, image=?, category=? WHERE id=?",
        (
            d.get("name",        row["name"]).strip(),
            float(d.get("price", row["price"])),
            d.get("description", row["description"]).strip(),
            d.get("image",       row["image"]),
            d.get("category",    row["category"]),
            pid
        )
    )
    conn.commit()
    updated = conn.execute("SELECT * FROM products WHERE id=?", (pid,)).fetchone()
    conn.close()
    return jsonify(dict(updated))

@app.route("/api/products/<int:pid>", methods=["DELETE"])
def delete_product(pid):
    conn   = get_db()
    result = conn.execute("DELETE FROM products WHERE id=?", (pid,))
    conn.commit()
    conn.close()
    if result.rowcount == 0:
        return jsonify({"error": "Introuvable"}), 404
    return jsonify({"ok": True})

# ── COMMANDES ─────────────────────────────────────────────────────────────────

@app.route("/api/orders", methods=["GET"])
def get_orders():
    conn   = get_db()
    rows   = conn.execute("SELECT * FROM orders ORDER BY id DESC").fetchall()
    conn.close()
    orders = []
    for r in rows:
        o          = dict(r)
        o["items"] = _json.loads(o["items"])
        orders.append(o)
    return jsonify(orders)

@app.route("/api/orders", methods=["POST"])
def create_order():
    d       = request.json or {}
    name    = d.get("name",    "").strip()
    phone   = d.get("phone",   "").strip()
    address = d.get("address", "").strip()
    items   = d.get("items",   [])

    errors = []
    if not name:                    errors.append("Nom requis")
    if not phone or len(phone) < 8: errors.append("Téléphone invalide")
    if not address:                 errors.append("Adresse requise")
    if not items:                   errors.append("Panier vide")
    if errors:
        return jsonify({"error": "; ".join(errors)}), 400

    total = sum(i.get("price", 0) * i.get("qty", 1) for i in items)
    date  = datetime.now().strftime("%d/%m/%Y %H:%M")
    conn  = get_db()
    cur   = conn.execute(
        "INSERT INTO orders (name, phone, address, items, total, status, date) VALUES (?,?,?,?,?,?,?)",
        (name, phone, address, _json.dumps(items, ensure_ascii=False), total, "en attente", date)
    )
    conn.commit()
    row        = conn.execute("SELECT * FROM orders WHERE id=?", (cur.lastrowid,)).fetchone()
    conn.close()
    o          = dict(row)
    o["items"] = _json.loads(o["items"])
    return jsonify(o), 201

@app.route("/api/orders/<int:oid>", methods=["PUT"])
def update_order(oid):
    d    = request.json or {}
    conn = get_db()
    row  = conn.execute("SELECT * FROM orders WHERE id=?", (oid,)).fetchone()
    if not row:
        conn.close()
        return jsonify({"error": "Introuvable"}), 404
    conn.execute("UPDATE orders SET status=? WHERE id=?", (d.get("status", row["status"]), oid))
    conn.commit()
    conn.close()
    return jsonify({"ok": True})

# ── AUTH ──────────────────────────────────────────────────────────────────────

@app.route("/api/admin/login", methods=["POST"])
def admin_login():
    d = request.json or {}
    if d.get("username") == ADMIN_USER and d.get("password") == ADMIN_PASS:
        return jsonify({"ok": True})
    return jsonify({"error": "Identifiants incorrects"}), 401

# ── Démarrage ─────────────────────────────────────────────────────────────────

init_db()

if __name__ == "__main__":
    print(f"\n📁 Base de données : {DB_PATH}")
    conn = get_db()
    nb   = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
    conn.close()
    print(f"✅ {nb} commande(s) dans la base\n")
    app.run(debug=True, host="0.0.0.0", port=5000)
