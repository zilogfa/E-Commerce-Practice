from flask import Flask, url_for, redirect, render_template, request, current_app
from flask_sqlalchemy import SQLAlchemy
from WTForms import AddProductForm

import stripe

import os
import secrets
from PIL import Image

from flask_ckeditor import CKEditor, CKEditorField, upload_success, upload_fail

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static'
db = SQLAlchemy(app)
ckeditor = CKEditor(app)

stripe.api_key = 'sk_test_51OKlN3E5N7yAlN3NVXIYfw2fc7o5QTDmzA6Yf7pJAtAcBcqN8K3JreLE8Hb6WMKFOfMnHvepnLg0CO6yUWNPWL5700W5vohRZF'


#>>>>>>>>>> DataBase
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    pic = db.Column(db.String(20), nullable=True)
    body = db.Column(db.Text, nullable=False)
    

#>>>>>>>>>>>>>>>>>> Save picture
def save_product_picture(file):
    if hasattr(file, 'filename') and file.filename != '':
        random_hex = secrets.token_hex(8)
        _, file_extension = os.path.splitext(file.filename)
        new_filename = random_hex + file_extension
        destination = os.path.join(
            current_app.root_path, 'static/images/product_pictures', new_filename)

        output_size = (600, 600) 
        image = Image.open(file)
        width, height = image.size
        size = min(width, height)
        left = (width - size) / 2
        top = (height - size) / 2
        right = (width + size) / 2
        bottom = (height + size) / 2
        image = image.crop((left, top, right, bottom))
        image.thumbnail(output_size)
        image.save(destination)
        return new_filename
    else:
        return file
#>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>



@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products)

@app.route('/view_product/<int:product_id>')
def view_product(product_id):
    product = Product.query.filter_by(id=product_id).first()
    return render_template('view_product.html', product=product)


@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = AddProductForm()
    if form.validate_on_submit():
        new_product = Product(
            name = form.name.data,
            price = form.price.data,
            pic=save_product_picture(
                form.pic.data) if form.pic.data else None,
            body=form.body.data
        )
        db.session.add(new_product)
        db.session.commit()
        print(form.pic.data)
        print(f'New Product added; {form.name.data}')
        return redirect(url_for('index'))
    return render_template('add_product.html', form=form)


#>>>>>>>>>>>>>>>>>>>>>>>>>> checkout
@app.route('/create-checkout-session', methods=['POST'])
def create_checkout_session():
    """
    Test the Payment Integration: Use Stripe's test card numbers 
    (e.g., 4242 4242 4242 4242 with any future expiration date and any CVC)     
    """
    product_name = request.form.get('product_name')
    product_price = int(float(request.form.get('product_price')) * 100) #converting price to required float format 
 

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': product_name,
                        },
                        'unit_amount': product_price,
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=url_for('success', _external=True),
            cancel_url=url_for('cancel', _external=True),
        )
        return redirect(checkout_session.url, code=303)
    except Exception as e:
        return str(e)
    

@app.route('/success')
def success():
    return 'Payment succeeded!'

@app.route('/cancel')
def cancel():
    return 'Payment canceled.'    


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)