import click

from flask.cli import with_appcontext

from faker import Faker


@click.command("init")
@with_appcontext
def init():
    """Create a new user"""
    from ecommerce.extensions import db
    from ecommerce.models import User
    
    fake = Faker()
    for i in range(10):
        user = User(
            name=fake.name(),
            email=fake.email(),
            password=fake.password(),
            phone_number=fake.phone_number(),
            address=fake.address(),
            city=fake.city(),
            balance=fake.random_int(0, 10000000),
            is_admin=fake.boolean(chance_of_getting_true=10),
        )
        db.session.add(user)
    db.session.commit()