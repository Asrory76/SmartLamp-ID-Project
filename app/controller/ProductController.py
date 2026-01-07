from app.model.product import Products
from app import response, db
from flask import request

def singleTransform(p):
    return {
        'id': p.id,
        'name': p.name,
        'price': float(p.price),
        'category': p.category,
        'description': p.description,
        'specs': p.specs,
        'image': p.image
    }

def index():
    try:
        products = Products.query.all()
        data = [singleTransform(p) for p in products]
        return response.success(data, "Success")
    except Exception as e:
        print(e)
        return response.badRequest([], "Error")

def store():
    try:
        data = request.json
        new_product = Products(
            name=data['name'], 
            price=data['price'], 
            category=data.get('category'),
            description=data.get('description'),
            specs=data.get('specs'),
            image='logo.png'
        )
        db.session.add(new_product)
        db.session.commit()
        return response.success(singleTransform(new_product), "Product Created")
    except Exception as e:
        print(e)
        return response.badRequest([], "Error creating product")

def show(id):
    try:
        product = Products.query.filter_by(id=id).first()
        if not product: return response.badRequest([], 'Product not found')
        return response.success(singleTransform(product), "Success")
    except Exception as e:
        return response.badRequest([], "Error")

def update(id):
    try:
        product = Products.query.filter_by(id=id).first()
        if not product: return response.badRequest([], 'Product not found')
        
        data = request.json
        if 'name' in data: product.name = data['name']
        if 'price' in data: product.price = data['price']
        
        db.session.commit()
        return response.success(singleTransform(product), "Product Updated")
    except Exception as e:
        return response.badRequest([], "Error")

def delete(id):
    try:
        product = Products.query.filter_by(id=id).first()
        if not product: return response.badRequest([], 'Product not found')
        db.session.delete(product)
        db.session.commit()
        return response.success([], "Product Deleted")
    except Exception as e:
        return response.badRequest([], "Error")