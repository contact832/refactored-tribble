"""Integration Stripe pour Les Jardins D'Arabie.

Gere le checkout, les webhooks et la gestion des produits.

Variables d'environnement requises :
    STRIPE_SECRET_KEY       Cle secrete Stripe (sk_test_... ou sk_live_...)
    STRIPE_PUBLISHABLE_KEY  Cle publique Stripe (pk_test_... ou pk_live_...)
    STRIPE_WEBHOOK_SECRET   Secret du webhook Stripe (whsec_...)
    STRIPE_SUCCESS_URL      URL de redirection apres paiement reussi
    STRIPE_CANCEL_URL       URL de redirection apres annulation
"""

from __future__ import annotations

import logging
import os

import stripe
from flask import Blueprint, jsonify, request, render_template_string

logger = logging.getLogger(__name__)

# --- Configuration Stripe ---
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "")

# Produits Les Jardins D'Arabie
PRODUCTS = [
    {
        "id": "dattes-ajwa-250g",
        "name": "Dattes Ajwa Premium - 250g",
        "description": "Dattes Ajwa de Medine, qualite premium. Boite de 250g.",
        "price": 1490,  # en centimes (14.90 EUR)
        "currency": "eur",
        "image": "",
    },
    {
        "id": "dattes-ajwa-500g",
        "name": "Dattes Ajwa Premium - 500g",
        "description": "Dattes Ajwa de Medine, qualite premium. Boite de 500g.",
        "price": 2490,  # en centimes (24.90 EUR)
        "currency": "eur",
        "image": "",
    },
    {
        "id": "dattes-ajwa-1kg",
        "name": "Dattes Ajwa Premium - 1kg",
        "description": "Dattes Ajwa de Medine, qualite premium. Boite de 1kg.",
        "price": 4490,  # en centimes (44.90 EUR)
        "currency": "eur",
        "image": "",
    },
]


def create_stripe_blueprint() -> Blueprint:
    """Cree un blueprint Flask pour les paiements Stripe."""
    bp = Blueprint("stripe_payments", __name__, url_prefix="/shop")

    @bp.route("/")
    def shop_page():
        """Page boutique avec les produits."""
        publishable_key = os.environ.get("STRIPE_PUBLISHABLE_KEY", "")
        return render_template_string(SHOP_HTML, products=PRODUCTS, stripe_key=publishable_key)

    @bp.route("/create-checkout-session", methods=["POST"])
    def create_checkout_session():
        """Cree une session Stripe Checkout."""
        data = request.get_json(force=True)
        product_id = data.get("product_id", "")

        product = next((p for p in PRODUCTS if p["id"] == product_id), None)
        if not product:
            return jsonify({"error": "Produit introuvable."}), 404

        quantity = data.get("quantity", 1)
        if not isinstance(quantity, int) or quantity < 1 or quantity > 99:
            return jsonify({"error": "Quantite invalide (1-99)."}), 400

        base_url = request.host_url.rstrip("/")
        success_url = os.environ.get("STRIPE_SUCCESS_URL", f"{base_url}/shop/success")
        cancel_url = os.environ.get("STRIPE_CANCEL_URL", f"{base_url}/shop/cancel")

        try:
            session = stripe.checkout.Session.create(
                payment_method_types=["card"],
                line_items=[
                    {
                        "price_data": {
                            "currency": product["currency"],
                            "product_data": {
                                "name": product["name"],
                                "description": product["description"],
                            },
                            "unit_amount": product["price"],
                        },
                        "quantity": quantity,
                    }
                ],
                mode="payment",
                success_url=success_url + "?session_id={CHECKOUT_SESSION_ID}",
                cancel_url=cancel_url,
                shipping_address_collection={"allowed_countries": ["FR", "BE", "CH", "LU", "MC"]},
            )
            return jsonify({"checkout_url": session.url})
        except stripe.StripeError as e:
            logger.error("Erreur Stripe: %s", e)
            return jsonify({"error": str(e)}), 500

    @bp.route("/webhook", methods=["POST"])
    def stripe_webhook():
        """Webhook Stripe pour recevoir les evenements de paiement."""
        payload = request.get_data(as_text=True)
        sig_header = request.headers.get("Stripe-Signature", "")
        webhook_secret = os.environ.get("STRIPE_WEBHOOK_SECRET", "")

        if not webhook_secret:
            logger.warning("STRIPE_WEBHOOK_SECRET non configure.")
            return jsonify({"error": "Webhook non configure."}), 500

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        except ValueError:
            return jsonify({"error": "Payload invalide."}), 400
        except stripe.SignatureVerificationError:
            return jsonify({"error": "Signature invalide."}), 400

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            logger.info(
                "Paiement reussi! Session: %s, Client: %s, Montant: %s %s",
                session["id"],
                session.get("customer_email", "N/A"),
                session["amount_total"] / 100,
                session["currency"].upper(),
            )

        elif event["type"] == "payment_intent.payment_failed":
            intent = event["data"]["object"]
            logger.warning("Paiement echoue: %s", intent.get("last_payment_error", {}).get("message", ""))

        return jsonify({"status": "ok"})

    @bp.route("/success")
    def payment_success():
        """Page de confirmation apres paiement reussi."""
        return render_template_string(SUCCESS_HTML)

    @bp.route("/cancel")
    def payment_cancel():
        """Page d'annulation de paiement."""
        return render_template_string(CANCEL_HTML)

    @bp.route("/products", methods=["GET"])
    def list_products():
        """API JSON listant les produits disponibles."""
        return jsonify({"products": PRODUCTS})

    return bp


# --- Templates HTML ---

SHOP_HTML = """<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Les Jardins D'Arabie - Boutique</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Open+Sans:wght@400;600&display=swap');
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Open Sans', sans-serif;
      background: linear-gradient(135deg, #fdf6e3 0%, #f5e6c8 100%);
      min-height: 100vh;
      color: #2c1810;
    }
    header {
      background: linear-gradient(135deg, #2c1810 0%, #4a2c1a 100%);
      color: #f5e6c8;
      padding: 40px 20px;
      text-align: center;
    }
    header h1 {
      font-family: 'Playfair Display', serif;
      font-size: 2.8em;
      margin-bottom: 8px;
      letter-spacing: 2px;
    }
    header p {
      font-size: 1.1em;
      opacity: 0.85;
      letter-spacing: 1px;
    }
    .products {
      max-width: 1000px;
      margin: 40px auto;
      padding: 0 20px;
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 30px;
    }
    .product-card {
      background: white;
      border-radius: 16px;
      overflow: hidden;
      box-shadow: 0 4px 20px rgba(44, 24, 16, 0.1);
      transition: transform 0.2s, box-shadow 0.2s;
    }
    .product-card:hover {
      transform: translateY(-4px);
      box-shadow: 0 8px 30px rgba(44, 24, 16, 0.18);
    }
    .product-image {
      height: 200px;
      background: linear-gradient(135deg, #8B6914 0%, #D4A847 50%, #8B6914 100%);
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 4em;
    }
    .product-info {
      padding: 24px;
    }
    .product-info h3 {
      font-family: 'Playfair Display', serif;
      font-size: 1.3em;
      margin-bottom: 8px;
      color: #2c1810;
    }
    .product-info p {
      color: #666;
      font-size: 0.95em;
      margin-bottom: 16px;
      line-height: 1.5;
    }
    .price {
      font-size: 1.6em;
      font-weight: 700;
      color: #8B6914;
      margin-bottom: 16px;
    }
    .quantity-row {
      display: flex;
      align-items: center;
      gap: 12px;
      margin-bottom: 16px;
    }
    .quantity-row label { font-size: 0.9em; color: #666; }
    .quantity-row select {
      padding: 6px 12px;
      border: 1px solid #ddd;
      border-radius: 8px;
      font-size: 1em;
    }
    .buy-btn {
      width: 100%;
      padding: 14px;
      background: linear-gradient(135deg, #2c1810 0%, #4a2c1a 100%);
      color: #f5e6c8;
      border: none;
      border-radius: 10px;
      font-size: 1.05em;
      font-weight: 600;
      cursor: pointer;
      letter-spacing: 1px;
      transition: opacity 0.2s;
    }
    .buy-btn:hover { opacity: 0.9; }
    .buy-btn:disabled { opacity: 0.5; cursor: wait; }
    footer {
      text-align: center;
      padding: 30px;
      color: #888;
      font-size: 0.85em;
    }
    .secure-badge {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 6px;
      margin-top: 10px;
      font-size: 0.8em;
      color: #888;
    }
  </style>
</head>
<body>
  <header>
    <h1>Les Jardins D'Arabie</h1>
    <p>Dattes Ajwa Premium de Medine</p>
  </header>

  <div class="products">
    {% for product in products %}
    <div class="product-card">
      <div class="product-image">🌴</div>
      <div class="product-info">
        <h3>{{ product.name }}</h3>
        <p>{{ product.description }}</p>
        <div class="price">{{ "%.2f"|format(product.price / 100) }} &euro;</div>
        <div class="quantity-row">
          <label for="qty-{{ product.id }}">Quantite :</label>
          <select id="qty-{{ product.id }}">
            {% for i in range(1, 11) %}
            <option value="{{ i }}">{{ i }}</option>
            {% endfor %}
          </select>
        </div>
        <button class="buy-btn" onclick="checkout('{{ product.id }}')">
          Commander
        </button>
        <div class="secure-badge">
          &#128274; Paiement securise par Stripe
        </div>
      </div>
    </div>
    {% endfor %}
  </div>

  <footer>
    &copy; 2026 Les Jardins D'Arabie - Tous droits reserves
  </footer>

  <script>
    async function checkout(productId) {
      const qtySelect = document.getElementById('qty-' + productId);
      const quantity = parseInt(qtySelect.value, 10);
      const btn = event.target;
      btn.disabled = true;
      btn.textContent = 'Redirection...';

      try {
        const resp = await fetch('/shop/create-checkout-session', {
          method: 'POST',
          headers: {'Content-Type': 'application/json'},
          body: JSON.stringify({product_id: productId, quantity: quantity})
        });
        const data = await resp.json();
        if (data.checkout_url) {
          window.location.href = data.checkout_url;
        } else {
          alert('Erreur: ' + (data.error || 'Erreur inconnue'));
          btn.disabled = false;
          btn.textContent = 'Commander';
        }
      } catch (err) {
        alert('Erreur de connexion. Veuillez reessayer.');
        btn.disabled = false;
        btn.textContent = 'Commander';
      }
    }
  </script>
</body>
</html>"""

SUCCESS_HTML = """<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Paiement reussi - Les Jardins D'Arabie</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Open+Sans:wght@400;600&display=swap');
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Open Sans', sans-serif;
      background: linear-gradient(135deg, #fdf6e3 0%, #f5e6c8 100%);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .card {
      background: white;
      border-radius: 20px;
      padding: 50px;
      text-align: center;
      box-shadow: 0 4px 20px rgba(44, 24, 16, 0.1);
      max-width: 500px;
    }
    .check { font-size: 4em; margin-bottom: 20px; }
    h1 {
      font-family: 'Playfair Display', serif;
      color: #2c1810;
      margin-bottom: 12px;
    }
    p { color: #666; line-height: 1.6; margin-bottom: 24px; }
    a {
      display: inline-block;
      padding: 12px 30px;
      background: #2c1810;
      color: #f5e6c8;
      text-decoration: none;
      border-radius: 10px;
      font-weight: 600;
    }
  </style>
</head>
<body>
  <div class="card">
    <div class="check">&#10003;</div>
    <h1>Merci pour votre commande !</h1>
    <p>Votre paiement a ete effectue avec succes. Vous recevrez un email de confirmation sous peu.</p>
    <a href="/shop">Retour a la boutique</a>
  </div>
</body>
</html>"""

CANCEL_HTML = """<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Commande annulee - Les Jardins D'Arabie</title>
  <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Open+Sans:wght@400;600&display=swap');
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body {
      font-family: 'Open Sans', sans-serif;
      background: linear-gradient(135deg, #fdf6e3 0%, #f5e6c8 100%);
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .card {
      background: white;
      border-radius: 20px;
      padding: 50px;
      text-align: center;
      box-shadow: 0 4px 20px rgba(44, 24, 16, 0.1);
      max-width: 500px;
    }
    .icon { font-size: 4em; margin-bottom: 20px; }
    h1 {
      font-family: 'Playfair Display', serif;
      color: #2c1810;
      margin-bottom: 12px;
    }
    p { color: #666; line-height: 1.6; margin-bottom: 24px; }
    a {
      display: inline-block;
      padding: 12px 30px;
      background: #2c1810;
      color: #f5e6c8;
      text-decoration: none;
      border-radius: 10px;
      font-weight: 600;
    }
  </style>
</head>
<body>
  <div class="card">
    <div class="icon">&#8635;</div>
    <h1>Commande annulee</h1>
    <p>Votre commande a ete annulee. Aucun montant n'a ete debite. N'hesitez pas a revenir !</p>
    <a href="/shop">Retour a la boutique</a>
  </div>
</body>
</html>"""
