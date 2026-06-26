import os
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, render_template_string
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

app = Flask(__name__)
app.secret_key = 'artisans_touch_ultra_secure_session_token_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///artisans_touch.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# ==============================================================================
# 4. DATABASE SCHEMA MODELS
# ==============================================================================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='Client') # 'Admin' or 'Client'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    orders = db.relationship('Order', backref='client', lazy=True)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(300), nullable=False)
    stock = db.Column(db.Integer, default=10)
    category = db.Column(db.String(50), nullable=False) # 'Clocks', 'Bookmarks', 'Custom Decor'

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Pending') # 'Pending', 'Processing', 'Shipped'
    shipping_address = db.Column(db.Text, nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    date_ordered = db.Column(db.DateTime, default=datetime.utcnow)
    items = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Float, nullable=False)
    product = db.relationship('Product')

# ==============================================================================
# 1. SECURITY MIDDLEWARE (RBAC)
# ==============================================================================

def login_required(role=None):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Authentication required. Please access credentials entry point.', 'danger')
                return redirect(url_for('login_view'))
            if role and session.get('role') != role:
                flash('Access Denied (403 Forbidden): Unauthorized Interface Scope.', 'danger')
                return redirect(url_for('login_view'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Context Processor for Global Cart Token Counters
@app.context_processor
def inject_cart_count():
    cart = session.get('cart', [])
    return dict(cart_count=len(cart))

# ==============================================================================
# 2. CLIENT CORE CONTROLLERS & ROUTES
# ==============================================================================

@app.route('/')
def home_view():
    featured = Product.query.limit(3).all()
    return render_template('home.html', featured=featured)

@app.route('/shop')
def shop_view():
    cat_filter = request.args.get('category')
    if cat_filter:
        products = Product.query.filter_by(category=cat_filter).all()
    else:
        products = Product.query.all()
    return render_template('shop.html', products=products, active_category=cat_filter)

@app.route('/shop/product/<int:id>')
def product_detail_view(id):
    product = Product.query.get_or_404(id)
    return render_template('product_detail.html', product=product)

@app.route('/cart')
def cart_view():
    cart_ids = session.get('cart', [])
    cart_items = []
    total_price = 0.0
    
    # Simple dynamic identification loop
    from collections import Counter
    counts = Counter(cart_ids)
    
    for pid, qty in counts.items():
        p = Product.query.get(int(pid))
        if p:
            subtotal = p.price * qty
            total_price += subtotal
            cart_items.append({'product': p, 'quantity': qty, 'subtotal': subtotal})
            
    return render_template('cart.html', cart_items=cart_items, total_price=total_price)

@app.route('/cart/add/<int:id>', methods=['POST'])
def add_to_cart_handler(id):
    if 'cart' not in session:
        session['cart'] = []
    cart = session['cart']
    cart.append(id)
    session['cart'] = cart
    flash('Item added to shopping frame successfully.', 'success')
    return redirect(url_for('shop_view'))

@app.route('/cart/clear')
def clear_cart_handler():
    session['cart'] = []
    return redirect(url_for('cart_view'))

@app.route('/checkout', methods=['GET', 'POST'])
@login_required(role='Client')
def checkout_view():
    cart_ids = session.get('cart', [])
    if not cart_ids:
        flash('Cannot process checkout with empty system parameters.', 'warning')
        return redirect(url_for('shop_view'))
        
    if request.method == 'POST':
        address = request.form.get('address')
        phone = request.form.get('phone')
        
        # Calculate pricing state arrays
        total_price = 0.0
        from collections import Counter
        counts = Counter(cart_ids)
        
        new_order = Order(
            user_id=session['user_id'],
            total_price=0.0,
            shipping_address=address,
            contact_number=phone,
            status='Pending'
        )
        db.session.add(new_order)
        db.session.flush() # Extract Order ID generated automatically
        
        for pid, qty in counts.items():
            p = Product.query.get(int(pid))
            if p:
                subtotal = p.price * qty
                total_price += subtotal
                item = OrderItem(order_id=new_order.id, product_id=p.id, quantity=qty, unit_price=p.price)
                db.session.add(item)
                
        new_order.total_price = total_price
        db.session.commit()
        session['cart'] = [] # Flush shopping context state parameters
        flash('Order processed securely into core system infrastructure.', 'success')
        return redirect(url_for('orders_view'))
        
    return render_template('checkout.html')

@app.route('/orders')
@login_required(role='Client')
def orders_view():
    user_orders = Order.query.filter_by(user_id=session['user_id']).order_by(Order.date_ordered.desc()).all()
    return render_template('orders.html', orders=user_orders)

@app.route('/about')
def about_view():
    return render_template('about.html')

# ==============================================================================
# AUTHENTICATION HANDLING UTILITIES
# ==============================================================================

@app.route('/auth/login', methods=['GET', 'POST'])
def login_view():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash(f'Session initialised for user: {user.username}', 'success')
            if user.role == 'Admin':
                return redirect(url_for('admin_dashboard_view'))
            return redirect(url_for('home_view'))
        flash('Invalid verification credentials provided.', 'danger')
    return render_template('login.html')

@app.route('/auth/register', methods=['GET', 'POST'])
def register_view():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Identifier conflict detected.', 'danger')
            return redirect(url_for('register_view'))
            
        hashed_pw = generate_password_hash(password)
        new_user = User(username=username, email=email, password_hash=hashed_pw, role='Client')
        db.session.add(new_user)
        db.session.commit()
        flash('Registration completed successfully.', 'success')
        return redirect(url_for('login_view'))
    return render_template('register.html')

@app.route('/auth/logout')
def logout_handler():
    session.clear()
    flash('System session destroyed safely.', 'info')
    return redirect(url_for('home_view'))

# ==============================================================================
# 3. ADMINISTRATIVE MASTER CORE ROUTING
# ==============================================================================

@app.route('/admin/dashboard')
@login_required(role='Admin')
def admin_dashboard_view():
    products = Product.query.all()
    orders = Order.query.order_by(Order.date_ordered.desc()).all()
    clients = User.query.filter_by(role='Client').all()
    return render_template('admin_dashboard.html', products=products, orders=orders, clients=clients)

@app.route('/admin/product/create', methods=['POST'])
@login_required(role='Admin')
def admin_product_create():
    name = request.form.get('name')
    desc = request.form.get('description')
    price = float(request.form.get('price'))
    img = request.form.get('image_url')
    cat = request.form.get('category')
    stock = int(request.form.get('stock'))
    
    p = Product(name=name, description=desc, price=price, image_url=img, category=cat, stock=stock)
    db.session.add(p)
    db.session.commit()
    flash('New Product instance written into state data arrays.', 'success')
    return redirect(url_for('admin_dashboard_view'))

@app.route('/admin/product/edit/<int:id>', methods=['POST'])
@login_required(role='Admin')
def admin_product_update(id):
    p = Product.query.get_or_404(id)
    p.name = request.form.get('name')
    p.description = request.form.get('description')
    p.price = float(request.form.get('price'))
    p.image_url = request.form.get('image_url')
    p.category = request.form.get('category')
    p.stock = int(request.form.get('stock'))
    db.session.commit()
    flash('Product properties modified accurately.', 'success')
    return redirect(url_for('admin_dashboard_view'))

@app.route('/admin/product/delete/<int:id>', methods=['POST'])
@login_required(role='Admin')
def admin_product_delete(id):
    p = Product.query.get_or_404(id)
    db.session.delete(p)
    db.session.commit()
    flash('Product database instance removed safely.', 'info')
    return redirect(url_for('admin_dashboard_view'))

@app.route('/admin/order/status/<int:id>', methods=['POST'])
@login_required(role='Admin')
def admin_order_status_update(id):
    o = Order.query.get_or_404(id)
    o.status = request.form.get('status')
    db.session.commit()
    flash('Order transactional tracking workflow flag modified.', 'success')
    return redirect(url_for('admin_dashboard_view'))

@app.route('/admin/client/report/<int:id>')
@login_required(role='Admin')
def admin_generate_client_report(id):
    # This route is specifically structured to open in a blank view panel (target="_blank")
    client = User.query.get_or_404(id)
    orders = Order.query.filter_by(user_id=client.id).all()
    total_spend = sum(o.total_price for o in orders)
    
    report_template = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Client Profile Summary Report: {{ client.username }}</title>
        <style>
            body { font-family: monospace; padding: 40px; background: #fff; color: #000; }
            .border-box { border: 2px dashed #000; padding: 20px; }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { border: 1px solid #000; padding: 8px; text-align: left; }
        </style>
    </head>
    <body onload="window.print()">
        <div class="border-box">
            <h2>THE ARTISAN'S TOUCH - ADMINISTRATIVE PROFILE REPORT</h2>
            <p><strong>Generation Timestamp:</strong> {{ timestamp }}</p>
            <p><strong>Customer ID Ref:</strong> ATC-00{{ client.id }}</p>
            <p><strong>Identifier Name:</strong> {{ client.username }}</p>
            <p><strong>Email Address:</strong> {{ client.email }}</p>
            <p><strong>Historical Cumulative Spend:</strong> PKR {{ total_spend }}</p>
            
            <h3>TRANSACTION RECORD DATA</h3>
            <table>
                <thead>
                    <tr>
                        <th>Order ID Reference</th>
                        <th>Execution Date</th>
                        <th>Shipping Destination</th>
                        <th>Financial Subtotal</th>
                        <th>Workflow Status</th>
                    </tr>
                </thead>
                <tbody>
                    {% for o in orders %}
                    <tr>
                        <td>ATO-00{{ o.id }}</td>
                        <td>{{ o.date_ordered.strftime('%Y-%m-%d') }}</td>
                        <td>{{ o.shipping_address }}</td>
                        <td>PKR {{ o.total_price }}</td>
                        <td>[{{ o.status }}]</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """
    return render_template_string(report_template, client=client, orders=orders, total_spend=total_spend, timestamp=datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'))

# ==============================================================================
# APPLICATION SEED AND INITIALIZATION ENGINE
# ==============================================================================

def seed_database():
    if User.query.filter_by(username='admin').first() is None:
        # Build Standard Admin Instance
        admin = User(username='admin', email='management@artisanstouch.com', password_hash=generate_password_hash('admin123'), role='Admin')
        db.session.add(admin)
        
        # Build Standard Demo Product Records
        p1 = Product(name="Ethereal Resin Wall Clock", description="Handcrafted dynamic fluid artwork clock measuring 14 inches with gold accents. Unbreakable crystal blend epoxy layer with high thermal thresholds.", price=3500.00, image_url="https://images.unsplash.com/photo-1563861826100-9cb868fdbe1c?auto=format&fit=crop&w=600&q=80", category="Clocks", stock=5)
        p2 = Product(name="Oceanic Shimmer Bookmark", description="Transparent high-gloss resin bookmark embedded with real dried seaweed, gold leaf fragments, and micro-glitter pigments.", price=450.00, image_url="https://images.unsplash.com/photo-1607604276583-eef5d076aa5f?auto=format&fit=crop&w=600&q=80", category="Bookmarks", stock=25)
        p3 = Product(name="Amethyst Core Display Block", description="Heavy geode style resin crystal matrix sculpture perfect for high-end counter accent decor solutions.", price=2200.00, image_url="https://images.unsplash.com/photo-1579783900882-c0d3dad7b119?auto=format&fit=crop&w=600&q=80", category="Custom Decor", stock=3)
        
        db.session.add_all([p1, p2, p3])
        db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        seed_database()
    app.run(host='127.0.0.1', port=5000, debug=True)