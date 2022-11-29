import click

from flask.cli import with_appcontext

from faker import Faker


@click.command("init")
@with_appcontext
def init():
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
    
    fake = Faker('id_ID')
    user_id = []
    product_id = []
    order_id = []
    image_id = []
    category_id = []
    
    # Create 1 admin user
    admin = User(
        name="Admin",
        email="admin@gmail.com",
        password="password",
        phone_number="081314569839",
        address="Jl. Jendral Sudirman",
        city="Jakarta",
        balance=1000000,
        is_admin=True
    )
    db.session.add(admin)
    db.session.commit()
    print("Admin created")
    
    for _ in range(1):
        user = User(
            id = fake.uuid4(),
            name=fake.name(),
            email=fake.email(),
            password=fake.password(),
            phone_number=fake.phone_number(),
            address=fake.address(),
            city=fake.city(),
            balance=fake.random_int(min=0, max=1000000),
            is_admin=fake.boolean(chance_of_getting_true=10),
        )
        db.session.add(user)
        user_id.append(user.id)
    db.session.commit()
    print("User created")
        
    for _ in range(1):
        category = Categories(
            id = fake.uuid4(),
            title=fake.word(),
        )
        db.session.add(category)
        category_id.append(category.id)
    db.session.commit()
    print("Category created")
    
    for _ in range(1):
        product = Products(
            id = fake.uuid4(),
            title=fake.name(),
            product_detail=fake.text(),
            size=fake.random_element(elements=("S", "M", "L", "XL")),
            price=fake.random_int(min=0, max=1000000),
            condition=fake.random_element(elements=('new', 'used')),
            category_id=fake.random_element(elements=category_id),
        )
        db.session.add(product)
        product_id.append(product.id)
    db.session.commit()
    print("Product created")
    
    for _ in range(1):
        image = Images(
            id = fake.uuid4(),
            name=fake.name(),
            image_url=fake.image_url(),
        )
        db.session.add(image)
        image_id.append(image.id)
    db.session.commit()
    print("Image created")
    
    for _ in range(1):
        cart = Carts(
            user_id=fake.random_element(elements=user_id),
            product_id=fake.random_element(elements=product_id),
            quantity=fake.pyint(min_value=1, max_value=10),
            size=fake.random_element(elements=("S", "M", "L", "XL")),
        )
        db.session.add(cart)
    db.session.commit()
    print("Cart created")
    
    for _ in range(30):
        order = Orders(
            id = fake.uuid4(),
            user_id=fake.random_element(elements=user_id),
            status=fake.random_element(elements=("pending", "paid", "shipped", "delivered")),
            address=fake.address(),
            address_name=fake.city(),
            city=fake.city(),
            shipping_price=fake.random_int(min=1000, max=100000),
            shipping_method=fake.random_element(elements=("Same Day", "Next Day", "Regular")),
        
        )
        db.session.add(order)
        order_id.append(order.id)
    db.session.commit()
    print("Order created")
    
    for _ in range(1):
        order_product = Order_Products(
            order_id=fake.random_element(elements=order_id),
            product_id=fake.random_element(elements=product_id),
            quantity=fake.pyint(min_value=1, max_value=5),
            size=fake.random_element(elements=("S", "M", "L", "XL")),
        )
        db.session.add(order_product)
    db.session.commit()
    print("Order_Product created")
    
    for _ in range(1):
        product_image = Product_Images(
            product_id=fake.random_element(elements=product_id),
            image_id=fake.random_element(elements=image_id),
        )
        db.session.add(product_image)
    db.session.commit()
    print("Product_Image created")
    
    for _ in range(1):
        banner = Banners(
            id = fake.uuid4(),
            title=fake.name(),
            image_id=fake.random_element(elements=image_id),
        )
        db.session.add(banner)
    db.session.commit()
    print("Banner created")