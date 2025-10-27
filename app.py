from flask import Flask, render_template, request, flash
import requests
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Telegram configuration
TELEGRAM_TOKEN = "8429689872:AAFM2FjlcpNrQObzeLErl0X6rI1wBb8XU2w"
TELEGRAM_CHAT_ID = "@testlg_channel1"
TELEGRAM_BASE_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

# Sample product data with actual image links
products = [
    {
        'id': 1,
        'name': 'Purple Lavender Bouquet',
        'price': 29.99,
        'image': 'https://cdn.shopify.com/s/files/1/0507/3754/5401/files/R5522D_LOL_preset_proflowers-mx-tile-wide-sv-new.jpg?v=1738126465&width=768',
        'description': 'Beautiful fresh lavender bouquet with seasonal greens. Perfect for home decoration or as a gift.'
    },
    {
        'id': 2,
        'name': 'Violet Dreams Arrangement',
        'price': 39.99,
        'image': 'https://cdn.shopify.com/s/files/1/0507/3754/5401/files/R5549D_LOL_preset_proflowers-mx-tile-wide-sv-new.jpg?v=1750770212&width=768',
        'description': 'Elegant violet arrangement perfect for special occasions and celebrations.'
    },
    {
        'id': 3,
        'name': 'Purple Orchid Plant',
        'price': 34.99,
        'image': 'https://cdn.shopify.com/s/files/1/0507/3754/5401/files/R5559D_LOL_preset_proflowers-mx-tile-wide-sv-new.jpg?v=1746483459&width=768',
        'description': 'Exotic purple orchid in decorative pot. Long-lasting beauty for your home.'
    },
    {
        'id': 4,
        'name': 'Lilac Symphony',
        'price': 45.99,
        'image': 'https://cdn.shopify.com/s/files/1/0507/3754/5401/files/R5544D_LOL_preset_proflowers-mx-tile-wide-sv-new.jpg?v=1745879025&width=768',
        'description': 'Mixed lilac bouquet with complementary flowers creating a symphony of purple hues.'
    },
    {
        'id': 5,
        'name': 'Yellow Rose Collection',
        'price': 49.99,
        'image': 'https://cdn.shopify.com/s/files/1/0507/3754/5401/files/R5551D_LOL_preset_proflowers-mx-tile-wide-sv-new.jpg?v=1712917512&width=768',
        'description': 'Luxurious purple roses arranged with elegant foliage. Perfect for romantic occasions.'
    },
    {
        'id': 6,
        'name': 'Spring Purple Mix',
        'price': 37.99,
        'image': 'https://cdn.shopify.com/s/files/1/0507/3754/5401/files/R5549D_LOL_preset_proflowers-mx-tile-wide-sv-new.jpg?v=1750770212&width=768',
        'description': 'Vibrant spring flowers in various shades of purple. Bring spring indoors!'
    }
]


def send_telegram_message(message):
    """Send notification to Telegram channel"""
    url = f"{TELEGRAM_BASE_URL}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHAT_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    try:
        response = requests.post(url, json=payload)
        return response.status_code == 200
    except Exception as e:
        print(f"Telegram error: {e}")
        return False


@app.route('/')
def home():
    return render_template('index.html', products=products)


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in products if p['id'] == product_id), None)
    if product:
        return render_template('product.html', product=product)
    return "Product not found", 404


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Send notification to Telegram
        telegram_msg = f"🆕 New Contact Form Submission:\n\n👤 Name: {name}\n📧 Email: {email}\n💬 Message: {message}"

        if send_telegram_message(telegram_msg):
            flash('Thank you for your message! We will get back to you soon.', 'success')
        else:
            flash('Your message has been received. We will contact you soon.', 'info')

        return render_template('contact.html')

    return render_template('contact.html')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('DEBUG', False))