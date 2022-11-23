import click

from flask.cli import with_appcontext

from faker import Faker


@click.command("init")
@with_appcontext
def init():
    """Create a new user"""
    from ecommerce.extensions import db
    from ecommerce.models import User
    from ecommerce.models import TokenBlocklist
    from ecommerce.models import Products
    from ecommerce.models import Orders
    from ecommerce.models import Order_Products
    from ecommerce.models import Product_Images
    from ecommerce.models import Images
    from ecommerce.models import Categories
    from ecommerce.models import Banners
    from ecommerce.models import Carts
    
    fake = Faker()
    user_id = []
    product_id = []
    order_id = []
    image_id = []
    category_id = []
    
    for _ in range(10):
        user = User(
            name=fake.name(),
            email=fake.email(),
            password=fake.password(),
            phone_number=fake.phone_number(),
            address=fake.address(),
            city=fake.city(),
            balance=fake.random_int(min=0, max=1000000),
            is_admin=fake.boolean(chance_of_getting_true=50),
        )
        db.session.add(user)
        user_id.append(user.id)
    db.session.commit()
    print("User created")
        
    for _ in range(10):
        category = Categories(
            title=fake.name(),
            type=fake.random_int(min=0, max=1000000),
        )
        db.session.add(category)
        category_id.append(category.id)
    db.session.commit()
    print("Category created")
    
    for _ in range(10):
        product = Products(
            title=fake.name(),
            price=fake.random_int(min=0, max=1000000),
            condition=fake.random_int(min=0, max=1000000),
            description=fake.text(),
            category_id=fake.random_int(min=1, max=10),
        )
        db.session.add(product)
        product_id.append(product.id)
    db.session.commit()
    print("Product created")
    
    for _ in range(10):
        image = Images(
            name=fake.name(),
            image_url=fake.image_url(),
        )
        db.session.add(image)
        image_id.append(image.id)
    db.session.commit()
    print("Image created")
    
    for _ in range(10):
        cart = Carts(
            user_id=user.id,
            product_id=fake.random_int(min=1, max=10),
            quantity=fake.random_int(min=0, max=1000000),
            size=fake.name(),
        )
        db.session.add(cart)
    db.session.commit()
    print("Cart created")
    
    # for _ in range(10):
    #     order = Orders(
    #         user_id=fake.uuid4(),
    #         status=fake.random_int(min=0, max=1000000),
    #         address=fake.address(),
    #         city=fake.city(),
    #         shipping_price=fake.random_int(min=0, max=1000000),
    #         shipping_method=fake.random_int(min=0, max=1000000),
    #     )
    #     db.session.add(order)
    #     order_id.append(order.id)
    
    # for _ in range(10):
    #     image = Images(
    #         name=fake.name(),
    #         image_url=fake.image_url(),
    #     )
    #     db.session.add(image)
    #     image_id.append(image.id)
        
    # for _ in range(10):
    #     banner = Banners(
    #         title=fake.name(),
    #         image_id=fake.random_int(min=0, max=10),
    #     )
    #     db.session.add(banner)
        
    # for _ in range(10):
    #     order_product = Order_Products(
    #         order_id=fake.random_int(min=1, max=10),
    #         product_id=fake.random_int(min=1, max=10),
    #         quantity=fake.random_int(min=0, max=1000000),
    #         size=fake.name(),
    #     )
    #     db.session.add(order_product)
        
    # for _ in range(10):
    #     product_image = Product_Images(
    #         product_id=fake.random_int(min=1, max=10),
    #         image_id=fake.random_int(min=1, max=10),
    #     )
    #     db.session.add(product_image)
        
    
    
    
    
    
    
    
    
    
    
    
    
    # =================================
    
    # for i in range(10):
    #     category = Categories(
    #         title=fake.name(),
    #         type=fake.name(),
    #     )
    #     db.session.add(category)
    # db.session.commit()
    
    # for i in range(10):
    #     product = Products(
    #         tittle=fake.name(),
    #         price=fake.random_int(0, 10000000),
    #         condition=fake.name(),
    #         description=fake.name(),
    #         category_id=fake.random_int(1, 10),
    #     )
    #     db.session.add(product)
    # db.session.commit()
    
    # for i in range(10):
    #     order = Orders(
    #         user_id=
    #         status=fake.name(),
    #         address=fake.address(),
    #         city=fake.city(),
    #         shipping_price=fake.random_int(0, 10000000),
    #         shipping_method=fake.name(),
    #     )
    #     db.session.add(order)
    # db.session.commit()
    
    # for i in range(10):
    #     order_product = Order_Products(
    #         order_id=fake.random_int(1, 10),
    #         product_id=fake.random_int(1, 10),
    #         quantity=fake.random_int(0, 10000000),
    #         size=fake.name(),
    #     )
    #     db.session.add(order_product)
    # db.session.commit()
    
    # for i in range(10):
    #     product_image = Product_Images(
    #         product_id=fake.random_int(1, 10),
    #         image_id=fake.random_int(1, 10),
    #     )
    #     db.session.add(product_image)
    # db.session.commit()

    # for i in range(10):
    #     image = Images(
    #         name=fake.name(),
    #         image_url=fake.name(),
    #     )
    #     db.session.add(image)
    # db.session.commit()
    
    # for i in range(10):
    #     banner = Banners(
    #         tittle=fake.name(),
    #         image_id=fake.random_int(1, 10),
    #     )
    #     db.session.add(banner)
    # db.session.commit()
    
    # for i in range(10):
    #     cart = Carts(
    #         user_id=user_id,
    #         product_id=fake.random_int(1, 10),
    #         quantity=fake.random_int(0, 10000000),
    #         size=fake.name(),
    #     )
    #     db.session.add(cart)
    # db.session.commit()
        