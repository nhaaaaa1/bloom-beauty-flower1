from flask import Flask, render_template, request, flash, redirect, url_for
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key-123')

# Your Telegram credentials
TELEGRAM_BOT_TOKEN = "8429689872:AAFM2FjlcpNrQObzeLErl0X6rI1wBb8XU2w"
TELEGRAM_CHAT_ID = "@testlg_channel1"

# Sample product data
products = [
    {
        'id': 1,
        'name': 'Red Roses Bouquet',
        'price': 49.99,
        'image': 'https://images.unsplash.com/photo-1563241527-3004b7be0ffd?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
        'category': 'romantic',
        'description': 'Beautiful red roses perfect for romantic occasions',
        'details': '12 fresh red roses with baby breath and greenery, delivered in elegant packaging. Perfect for anniversaries, Valentine\'s Day, or just to show someone you care.'
    },
    {
        'id': 2,
        'name': 'Sunflower Arrangement',
        'price': 39.99,
        'image': 'https://images.unsplash.com/photo-1597848212624-e6d4bd7d1327?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
        'category': 'cheerful',
        'description': 'Bright sunflowers to bring sunshine to any room',
        'details': '5 large sunflowers with seasonal greens in a rustic vase. Perfect for birthdays, get-well wishes, or to brighten someone\'s day.'
    },
    {
        'id': 3,
        'name': 'Orchid Plant',
        'price': 34.99,
        'image': 'https://images.unsplash.com/photo-1578990735188-16fdc76ff9d1?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
        'category': 'elegant',
        'description': 'Elegant orchid plant for sophisticated decor',
        'details': 'Beautiful purple orchid in a ceramic pot, perfect for home or office decor. Low maintenance and long-lasting beauty.'
    },
    {
        'id': 4,
        'name': 'Mixed Spring Bouquet',
        'price': 45.99,
        'image': 'https://images.unsplash.com/photo-1582794543139-8ac9cad0c8e2?ixlib=rb-4.0.3&auto=format&fit=crop&w=400&q=80',
        'category': 'seasonal',
        'description': 'Colorful mix of spring flowers',
        'details': 'Seasonal flowers including tulips, daffodils, and hyacinths. A vibrant arrangement that captures the essence of spring.'
    }
]


def send_telegram_message(message):
    """Send notification to Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

        payload = {
            'chat_id': TELEGRAM_CHAT_ID,
            'text': message,
            'parse_mode': 'HTML'
        }

        response = requests.post(url, json=payload, timeout=10)

        if response.status_code == 200:
            print("Telegram message sent successfully!")
            return True
        else:
            print(f"Telegram API error: {response.status_code} - {response.text}")
            return False

    except Exception as e:
        print(f"Error sending Telegram message: {e}")
        return False


@app.route('/')
def index():
    """Home page route - renders index.html"""
    return render_template('index.html', products=products)


@app.route('/home')
def home():
    """Alternative home page route"""
    return redirect(url_for('index'))


@app.route('/products')
def all_products():
    """All products page"""
    return render_template('index.html', products=products)


@app.route('/product/<int:product_id>')
def product_details(product_id):
    """Product details page route"""
    product = next((p for p in products if p['id'] == product_id), None)
    if product is None:
        flash('Product not found!', 'error')
        return redirect(url_for('index'))
    return render_template('product_details.html', product=product)


@app.route('/about')
def about():
    """About us page route"""
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact us page route with Telegram notifications"""
    if request.method == 'POST':
        # Get form data
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()

        # Basic validation
        if not all([name, email, subject, message]):
            flash('Please fill in all fields!', 'error')
            return render_template('contact.html')

        # Create formatted Telegram message
        telegram_message = f"""
🌸 <b>New Contact Form Submission - Bloom & Beauty</b> 🌸

<b>Name:</b> {name}
<b>Email:</b> {email}
<b>Subject:</b> {subject}
<b>Message:</b>
{message}

<b>Timestamp:</b> {request.environ.get('HTTP_DATE', 'Unknown')}
        """

        # Send to Telegram
        telegram_sent = send_telegram_message(telegram_message)

        if telegram_sent:
            flash('✅ Thank you for your message! We have received it and will get back to you soon.', 'success')
        else:
            flash('✅ Message received! We will get back to you soon. (Telegram notification failed)', 'success')

        return redirect(url_for('contact'))

    return render_template('contact.html')


@app.route('/test-telegram')
def test_telegram():
    """Test route to check Telegram integration"""
    test_message = """
🔔 <b>Test Message - Bloom & Beauty</b> 🔔

This is a test message from your flower shop website.
If you can see this message, Telegram integration is working correctly!

<b>Website:</b> Bloom & Beauty Flower Shop
<b>Status:</b> ✅ Operational
    """

    if send_telegram_message(test_message):
        return "Telegram test message sent successfully!"
    else:
        return "Failed to send Telegram test message."


@app.route('/api/products', methods=['GET'])
def api_products():
    """API endpoint to get products"""
    return {'products': products}


@app.route('/api/contact', methods=['POST'])
def api_contact():
    """API endpoint for contact form"""
    try:
        data = request.get_json()

        if not data:
            return {'error': 'No data provided'}, 400

        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        subject = data.get('subject', '').strip()
        message = data.get('message', '').strip()

        if not all([name, email, subject, message]):
            return {'error': 'Missing required fields'}, 400

        # Send Telegram notification
        telegram_message = f"""
🌐 <b>New API Contact Form Submission</b>

<b>Name:</b> {name}
<b>Email:</b> {email}
<b>Subject:</b> {subject}
<b>Message:</b> {message}
        """

        telegram_sent = send_telegram_message(telegram_message)

        return {
            'message': 'Contact form submitted successfully',
            'telegram_sent': telegram_sent
        }, 200

    except Exception as e:
        return {'error': str(e)}, 500


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('500.html'), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=os.environ.get('DEBUG', False))