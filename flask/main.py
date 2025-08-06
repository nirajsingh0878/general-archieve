from flask import Flask, request, jsonify
from pydantic import BaseModel, ValidationError
from typing import Optional

app = Flask(__name__)

db = {
    1: {"name": "Apple", "price": 50},
    2: {"name": "Banana", "price": 20},
    3: {"name": "Mango", "price": 70},
    4: {"name": "Grapes", "price": 40},
    5: {"name": "Orange", "price": 35}
}

class Item(BaseModel):
    name: str
    price: float

class PartialItem(BaseModel):
    name: Optional[str]
    price: Optional[float]

@app.errorhandler(ValidationError)
def handle_validation_error(e):
    return f"<h3>Validation Error</h3><pre>{e}</pre>", 400

@app.errorhandler(400)
def handle_bad_request(e):
    return "<h3>400 Bad Request</h3>", 400

@app.errorhandler(404)
def handle_not_found(e):
    return "<h3>404 Not Found</h3>", 404



@app.route('/')
def home():
    return "Enhanced Flask API (no abort, clean error HTML)"

@app.route('/items', methods=['GET'])
def get_all():
    return jsonify(db)

@app.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = db.get(item_id)
    if not item:
        return "<h3>Item not found</h3>", 404
    return jsonify({item_id: item})

@app.route('/items', methods=['POST'])
def create_item():
    item = Item(**request.json)
    new_id = max(db.keys()) + 1 if db else 1
    db[new_id] = item.dict()
    return jsonify({new_id: db[new_id]}), 201

@app.route('/items/<int:item_id>', methods=['PUT'])
def put_item(item_id):
    if item_id not in db:
        return "<h3>Item not found</h3>", 404
    item = Item(**request.json)
    db[item_id] = item.dict()
    return jsonify({item_id: db[item_id]})

@app.route('/items/<int:item_id>', methods=['PATCH'])
def patch_item(item_id):
    if item_id not in db:
        return "<h3>Item not found</h3>", 404
    update = PartialItem(**request.json)
    db[item_id].update(update.dict(exclude_none=True))
    return jsonify({item_id: db[item_id]})

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    if item_id not in db:
        return "<h3>Item not found</h3>", 404
    deleted = db.pop(item_id)
    return jsonify({"deleted": {item_id: deleted}})

@app.route('/search', methods=['GET'])
def search_items():
    query = request.args.get('name', '').lower()
    results = {i: item for i, item in db.items() if query in item['name'].lower()}
    return jsonify(results)

@app.route('/total', methods=['GET'])
def get_total_price():
    total = sum(item['price'] for item in db.values())
    return jsonify({"total_price": total})

@app.route('/stats', methods=['GET'])
def get_stats():
    count = len(db)
    avg = sum(item['price'] for item in db.values()) / count if count else 0
    return jsonify({"count": count, "average_price": round(avg, 2)})

@app.route('/clear', methods=['DELETE'])
def clear_all():
    db.clear()
    return jsonify({"status": "all items deleted"})



if __name__ == '__main__':
    app.run(debug=True)



'''
| Method    | Purpose               | Behavior                                                   |
| --------- | --------------------- | ---------------------------------------------------------- |
| **PUT**   | Replace full resource | You must send the **entire object**, even unchanged fields |
| **PATCH** | Partial update        | You send **only the fields you want to change**            |

curl http://127.0.0.1:5000/items

curl http://127.0.0.1:5000/items/1
curl -X DELETE http://127.0.0.1:5000/items/2
curl http://127.0.0.1:5000/stats
curl http://127.0.0.1:5000/items | jq

curl -X POST http://127.0.0.1:5000/items -H "Content-Type: application/json" -d "{\"name\": \"Mango\", \"price\": 30}"
curl -X PUT http://127.0.0.1:5000/items/1 -H "Content-Type: application/json" -d "{\"name\": \"Apple\", \"price\": 60}"
curl -X PATCH http://127.0.0.1:5000/items/1 -H "Content-Type: application/json" -d "{\"price\": 55}"
curl -X DELETE http://127.0.0.1:5000/items/1

'''