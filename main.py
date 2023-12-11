from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=["*"],
    allow_headers=["*"]
)
# This should be a different database
redis=get_redis_connection(
    host="redis-10113.c300.eu-central-1-1.ec2.cloud.redislabs.com",
    port=10113,
    password="chuYMXpnr7md2AIHsTeLXKICkL0u5QWY",
    #decode_responses=True  
)

class Product(HashModel):
    name:str
    price:float
    quantity:int
    
    class Meta:
        database=redis

class Order(HashModel):
    product_id:str
    price:float
    fee:float
    total:float
    quantity:int
    status:str # pending, completed, refunded
    
    class Meta:
        database = redis
    
# Get all values 756400074
@app.get("/products")
def all():
    return [format(pk) for pk in Product.all_pks()]

def format(pk:str):
    product = Product.get(pk)
    return {
        'id':product.pk,
        'name':product.name,
        'price':product.price,
        'quantity':product.quantity
    }

@app.post("/products")
def create(product: Product):
    return product.save()

@app.get('/products/{pk}')
def get(pk:str):
    return Product.get(pk)

@app.delete('/products/{pk}')
def delete(pk:str):
    return Product.delete(pk)
    
