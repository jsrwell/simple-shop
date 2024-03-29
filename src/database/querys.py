from .models import Product
from .connection import create_connection

def get_products():
    """Retrieve all products from the database."""
    conn = create_connection()
    session = Session(bind=conn)
    products = session.query(Product).all()
    session.close()
    return products