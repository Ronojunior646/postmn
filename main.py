from flask import Flask,render_template,redirect,url_for,request,jsonify,session
from sqlalchemy import SQLAlchemy
from sqlalchemy import func,select
import sentry_sdk

sentry_sdk.init(
    dsn="https://04fce712893c9870e96943104c7869aa@o4507805055057920.ingest.us.sentry.io/4507805084090368",
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for tracing.
    traces_sample_rate=1.0,
    # Set profiles_sample_rate to 1.0 to profile 100%
    # of sampled transactions.
    # We recommend adjusting this value in production.
    profiles_sample_rate=1.0,
)

app = Flask(__name__)

app =  Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql://postgres:6979@localhost/postmandb'
db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__='products'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String,nullable= False)
    buying_price = db.Column(db.Integer,nullable= False)
    selling_price = db.Column(db.Integer,nullable= False)
    stock_quantity= db.Column(db.Integer,nullable= False)
    sale = db.relationship('Sale',backref='product')


class Sale(db.Model):
    __tablename__ ='sales'
    id = db.Column(db.Integer,primary_key=True)
    pid =db.Column(db.Integer,db.ForeignKey('products.id'))
    quantity = db.Column(db.Integer,nullable= False)
    created_at = db.Column(db.DateTime,server_default = func.now())

with app.app_context():
    db.create_all()



@app.route('/',methods=['GET','POST'])
def product():
    if request.method == 'POST':
        try:
            data = request.json
            name = data['name']
            buying_price = data['buying_price']
            selling_price = data['selling_price']
            stock_quantity = data['stock_quantity']
            product = Product(name=name,buying_price=buying_price,selling_price=selling_price,stock_quantity=stock_quantity)
            db.session.add(product)
            db.session.commit()
            return jsonify({"message":"product added successfully"}),201
        except Exception as e:
            return jsonify({'error':str(e)}),500
    elif request.method == 'GET':
        products = db.session.execute(db.select(Product).order_by(Product.name)).scalars()
        for product in products:
            prods = [{
                
                "name":product.name,
                "buying_price":product.buying_price,
                "selling_price":product.selling_price,
                "stock_quantity":product.stock_quantity

            }]
        return jsonify({"products": prods}) ,200


@app.route('/sales',methods=['GET','POST'])
def sales():
    if request.method == 'POST':
        try:
            data = request.json
            pid = data['pid']
            quantity = data['quantity']
            sale = Sale(pid=pid,quantity=quantity)
            db.session.add(sale)
            db.session.commit()
            return jsonify({"message":"Sale made successfully"}),201
        except Exception as e:
            return jsonify({"error":str(e)}),500
    elif request.method == 'GET':
        sales = db.session.execute(db.select(Sale).order_by(Sale.pid)).scalars()
        for sale in sales:
            sall =[{
                'product': sale.product.name,
                'quantity':sale.quantity
            }]
        return jsonify({"sales":sall}),200
@app.route("/")
def hello_world():
    try:
        1/0
    except Exception as e:
        sentry_sdk.capture_exception(e)
    return "<p>Hello, World!</p>"
if __name__ == '__main__':
    app.run(debug=True)
        







# @app.route('/')
# def home():
#     r = requests.get('https://jsonplaceholder.typicode.com/todos')
#     return jsonify(r.json())


# @app.route('/person')
# def person():
#     person = {
#         'id'
#     }