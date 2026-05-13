from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI(title="持续测试学习项目")

VALID_USERNAME = "admin"
VALID_PASSWORD = "password123"
TOKEN = "demo-token"

PRODUCTS = [
    {"id": 1, "name": "接口测试入门课", "price": 99.0},
    {"id": 2, "name": "UI 自动化实战课", "price": 129.0},
    {"id": 3, "name": "持续测试流水线课", "price": 159.0},
]


CART_ITEMS: list[dict[str,Any]] = []



class LoginRequest(BaseModel):
    username: str
    password: str


class CartRequest(BaseModel):
    product_id: int
    quantity: int = 1


@app.get("/", response_class=HTMLResponse)
def home() -> str:
    return """
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>持续测试练习商城</title>
  <style>
    body {
      margin: 0;
      font-family: Arial, "Microsoft YaHei", sans-serif;
      background: #f5f7fb;
      color: #172033;
    }
    main {
      max-width: 880px;
      margin: 48px auto;
      padding: 0 20px;
    }
    h1 {
      font-size: 30px;
      margin-bottom: 8px;
    }
    .panel {
      background: #fff;
      border: 1px solid #dfe5ef;
      border-radius: 8px;
      padding: 24px;
      margin-top: 20px;
      box-shadow: 0 8px 24px rgb(23 32 51 / 8%);
    }
    label {
      display: block;
      font-weight: 700;
      margin: 14px 0 6px;
    }
    input {
      width: 100%;
      box-sizing: border-box;
      padding: 10px 12px;
      border: 1px solid #c9d3e2;
      border-radius: 6px;
      font-size: 16px;
    }
    button {
      margin-top: 18px;
      padding: 10px 16px;
      border: 0;
      border-radius: 6px;
      background: #2454d6;
      color: #fff;
      font-size: 16px;
      cursor: pointer;
    }
    .status {
      min-height: 24px;
      margin-top: 14px;
      font-weight: 700;
    }
    .error {
      color: #b42318;
    }
    .success {
      color: #067647;
    }
    .products {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 12px;
      margin-top: 16px;
    }
    .product {
      border: 1px solid #dfe5ef;
      border-radius: 8px;
      padding: 14px;
      background: #fbfcff;
    }
  </style>
</head>
<body>
  <main>
    <h1>持续测试练习商城</h1>
    <p>用于练习接口测试、UI 自动化测试和 GitHub Actions 流水线。</p>

    <section class="panel" aria-label="登录区域">
      <h2>登录</h2>
      <label for="username">用户名</label>
      <input id="username" name="username" autocomplete="username" />

      <label for="password">密码</label>
      <input id="password" name="password" type="password" autocomplete="current-password" />

      <button id="login-button" type="button">登录</button>
      <div id="message" class="status" role="status"></div>
    </section>

    <section id="products-panel" class="panel" aria-label="商品列表" hidden>
      <h2>商品列表</h2>
      <div id="products" class="products"></div>
    </section>
  </main>

  <script>
    const message = document.querySelector("#message");
    const productsPanel = document.querySelector("#products-panel");
    const productsContainer = document.querySelector("#products");

    async function loadProducts() {
      const response = await fetch("/products");
      const products = await response.json();
      productsContainer.innerHTML = products.map((product) => `
        <article class="product">
          <strong>${product.name}</strong>
          <p>价格：¥${product.price}</p>
        </article>
      `).join("");
      productsPanel.hidden = false;
    }

    document.querySelector("#login-button").addEventListener("click", async () => {
      message.textContent = "";
      message.className = "status";
      productsPanel.hidden = true;

      const payload = {
        username: document.querySelector("#username").value,
        password: document.querySelector("#password").value,
      };

      const response = await fetch("/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify(payload),
      });

      if (response.ok) {
        message.textContent = "登录成功";
        message.classList.add("success");
        await loadProducts();
      } else {
        message.textContent = "用户名或密码错误";
        message.classList.add("error");
      }
    });
  </script>
</body>
</html>
"""


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/login")
def login(payload: LoginRequest) -> dict[str, str]:
    if payload.username == VALID_USERNAME and payload.password == VALID_PASSWORD:
        return {"token": TOKEN, "username": payload.username}

    raise HTTPException(status_code=401, detail="Invalid username or password")


@app.get("/products")
def products() -> list[dict[str, Any]]:
    return PRODUCTS


@app.post("/cart")
def add_to_cart(payload: CartRequest) -> dict[str, Any]:
    if payload.quantity < 1:
        raise HTTPException(status_code=422, detail="Quantity must be greater than 0")

    product = next((item for item in PRODUCTS if item["id"] == payload.product_id), None)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    cart_item = {
        "product_id": payload.product_id,
        "name": product["name"],
        "quantity": payload.quantity,
    }
    CART_ITEMS.append(cart_item)

    return {
        "message": "Added to cart",
        "item": cart_item,
    }

@app.get("/cart")
def get_cart() -> list[dict[str, Any]]:
    return CART_ITEMS

