
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- IN MEMORY DB ----------------
admins = {"admin@mdk.com": {"password": "123456", "name": "Admin"}}
products = {}
categories = [{"id": "1", "name": "Sports"}, {"id": "2", "name": "Tech"}]

# ---------------- MODELS ----------------
class Login(BaseModel):
    email: str
    password: str

class Product(BaseModel):
    name: str
    price: float
    category_id: str

# ---------------- AUTH ----------------
@app.post("/api/admin/login")
def login(data: Login):
    admin = admins.get(data.email)
    if not admin or admin["password"] != data.password:
        raise HTTPException(401, "Invalid credentials")
    return {"token": "fake-token", "admin": admin}

# ---------------- DASHBOARD ----------------
@app.get("/api/admin/dashboard/stats")
def stats():
    return {
        "total_products": len(products),
        "total_categories": len(categories),
        "total_orders": 5,
        "total_revenue": 1200
    }

# ---------------- PRODUCTS ----------------
@app.get("/api/admin/products")
def get_products():
    return list(products.values())

@app.post("/api/admin/products")
def create_product(p: Product):
    pid = str(uuid.uuid4())
    products[pid] = {"id": pid, **p.dict()}
    return products[pid]

@app.put("/api/admin/products/{pid}")
def update_product(pid: str, p: Product):
    if pid not in products:
        raise HTTPException(404)
    products[pid].update(p.dict())
    return products[pid]

@app.delete("/api/admin/products/{pid}")
def delete_product(pid: str):
    products.pop(pid, None)
    return {"ok": True}

@app.get("/api/categories")
def get_categories():
    return categories

@app.get("/api/")
def root():
    return {"message": "MDK GROUP API Running"}
