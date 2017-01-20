from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_httpauth import HTTPBasicAuth


app = Flask(__name__)

meals = [
    {
        'id': 1,
        'title': u'Meal1 ',
        'description': u'Rest Day Meal1', 
        'protein': u'3 oz',
        'carb': u'20 g',
        'Veggies': u'2 cups',
        'fat': u'1/2 serv',
        'done': False
    },
    {
        'id': 2,
        'title': u'Meal2',
        'description': u'Rest Day Meal2', 
        'protein': u'3 oz',
        'carb': u'20 g',
        'Veggies': u'2 cups',
        'fat': u'1 serv',
        'done': False
    }
]

auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'sakti':
        return 'python'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)

def make_public(meal):
    new_meal = {}
    for field in meal:
        if field == 'id':
            new_meal['uri'] = url_for('get_meal', meal_id=meal['id'], _external=True)
        else:
            new_meal[field] = meal[field]
    return new_meal

@app.route('/mealplan/api/v1.0/meals', methods=['GET'])
@auth.login_required
def get_meals():
    return jsonify({'meals': [make_public(meal) for meal in meals]})

@app.route('/mealplan/api/v1.0/meals/<int:meal_id>', methods=['GET'])
def get_meal(meal_id):
    meal = [meal for meal in meals if meal['id'] == meal_id]
    if len(meal) == 0:
        abort(404)
    return jsonify({'meal': meal[0]})

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

'''
curl -i -H "Content-Type: application/json" -X POST -d  
    '{"title": "Meal3",
    "description": "Rest day meal3", 
    "protein": "4oz",
    "carb": "0 g",
    "Veggies": "2 cups",
    "fat": "2 serving", 
    "done": "False"}' 
http://0.0.0.0:5000/mealplan/api/v1.0/meals
'''
@app.route('/mealplan/api/v1.0/meals', methods=['POST'])
def create_meal():
    if not request.json or not 'title' in request.json:
        abort(400)
    meal = {
        'id': meals[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ''),
        'protein': request.json.get('protein', ''),
        'carb': request.json.get('carb', ''),
        'Veggies': request.json.get('Veggies', ''),
        'fat': request.json.get('fat', ''),       
        'done': False
    }
    meals.append(meal)
    return jsonify({'meal': meal}), 201


'''
curl -i -H "Content-Type: application/json" -X PUT -d  '{"carb": "20 g"}' http://0.0.0.0:5000/mealplan/api/v1.0/meals/3
'''
@app.route('/mealplan/api/v1.0/meals/<int:meal_id>', methods=['PUT'])
def update_meal(meal_id):
    meal = [meal for meal in meals if meal['id'] == meal_id]
    if len(meal) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    if 'description' in request.json and type(request.json['description']) != unicode:
        abort(400)
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    if 'protein' in request.json and type(request.json['protein']) != unicode:
        abort(400)
    if 'carb' in request.json and type(request.json['carb']) != unicode:
        abort(400)
    if 'fat' in request.json and type(request.json['fat']) != unicode:
        abort(400)
    meal[0]['title'] = request.json.get('title', meal[0]['title'])
    meal[0]['description'] = request.json.get('description', meal[0]['description'])
    meal[0]['carb'] = request.json.get('carb', meal[0]['carb'])
    meal[0]['protein'] = request.json.get('protein', meal[0]['protein'])
    meal[0]['fat'] = request.json.get('fat', meal[0]['fat'])
    meal[0]['done'] = request.json.get('done', meal[0]['done'])
    return jsonify({'meal': meal[0]})

# curl -i -H "Content-Type: application/json" -X DELETE http://0.0.0.0:5000/mealplan/api/v1.0/meals/3
@app.route('/mealplan/api/v1.0/meals/<int:meal_id>', methods=['DELETE'])
def remove_meal(meal_id):
    meal = [meal for meal in meals if meal['id'] == meal_id]
    if len(meal) == 0:
        abort(404)
    meals.remove(meal[0])
    return jsonify({'meals': [make_public(meal) for meal in meals]})

if __name__ == '__main__':
    # Initialize app.run to reach the API by hostname
    app.run(host='0.0.0.0',debug=True)