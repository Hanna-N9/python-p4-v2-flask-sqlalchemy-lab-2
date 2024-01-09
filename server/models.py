from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

    
class Customer(db.Model, SerializerMixin):
    __tablename__ = "customers"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    
    # Relationship
    reviews = db.relationship("Review", back_populates="customer")

    # Association proxy - get a list of items that customers reviewed
    items = association_proxy("reviews", "item", creator=lambda item_obj: Review(item=item_obj))
    
    # Add serialization rules to avoid errors involving recursion depth (be careful about tuple commas)
    serialize_rules = ("-reviews.customer",)

    def __repr__(self):
        return f"<Customer {self.id}, {self.name}>"

    
class Item(db.Model, SerializerMixin):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    # Relationship
    reviews = db.relationship("Review", back_populates="item")
    
    # Add serialization rules to avoid errors involving recursion depth (be careful about tuple commas)
    serialize_rules = ("-reviews.item",)

    def __repr__(self):
        return f"<Item {self.id}, {self.name}, {self.price}>"
    
    
class Review(db.Model, SerializerMixin):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)

    # Foreign key 
    customer_id = db.Column(db.Integer, db.ForeignKey("customers.id"))
    item_id = db.Column(db.Integer, db.ForeignKey("items.id"))

    # Relationship
    customer = db.relationship("Customer", back_populates="reviews")
    item = db.relationship("Item", back_populates="reviews")
    
    # Add serialization rules to avoid errors involving recursion depth (be careful about tuple commas)
    serialize_rules = ("-customer.reviews", "-item.reviews")

    def __repr__(self):
        return f"<Review {self.id}, {self.comment}, {self.customer.name}, {self.item.name}>"
