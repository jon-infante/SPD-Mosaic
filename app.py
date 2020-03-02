from flask import Flask, render_template
from google.cloud import vision
import os
import requests
import json
from dotenv import load_dotenv
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SPOONACULAR_API_KEY = os.getenv("SPOONACULAR_API_KEY")
#
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="env/key.json"
# image_uri = 'gs://cloud-samples-data/vision/using_curl/shanghai.jpeg'
# client = vision.ImageAnnotatorClient()
# image = vision.types.Image()
# image.source.image_uri = image_uri
#
# response = client.label_detection(image=image)
#
# print('Labels (and confidence score):')
# print('=' * 79)
# for label in response.label_annotations:
#     print(f'{label.description} ({label.score*100.:.2f}%)')
#
#
# curl -v -s -H "Content-Type: application/json" https://vision.googleapis.com/v1/images:annotate\?key\=AIzaSyDgxl6eCbmb-lAPrnd1NTcsCTTMQHd4_aU --data-binary @google_vision.json > results
# Retrieves raw scores
app = Flask(__name__)


##### GOOGLE VISION API #####
url = 'https://vision.googleapis.com/v1/images:annotate?'
payload = open("google_vision.json")
headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}
params = {
    'key': GOOGLE_API_KEY
    }
r = requests.post(url, data=payload, headers=headers, params=params)

labels = ['Food', 'Junk food', 'Dish', 'Cuisine', 'Fast food', 'Ingredient', 'Meat', 'Produce',
'Dessert', 'Frozen dessert', 'Baked goods', 'Comfort food', 'Staple food', 'Recipe', 'Italian food',
'Vegetarian food', 'American food', 'Vegetable', 'Plant', 'Natural foods', 'Fruit', 'Superfood',
'Red', 'Banana family', 'Yellow', 'Citrus', 'Citric acid', 'Side dish', 'Local food', 'Juice',
'Drink', 'Orange drink', 'Breakfast', 'Meal', 'Lunch', 'Dinner', 'Bilberry', 'Hendl', 'Kai yang'
'Roasting', 'Green', 'Leaf', 'Corn kernels', 'Animal fat', 'Crocus', 'Flower', 'Nut', 'Leaf vegetable',
'Herb', 'Grass']

# print(r.json())
#This returns the first label/tag based on topicality/closeness of what the image looks like
if r.json()['responses'][0]['labelAnnotations'][0]['description'] not in labels:
    food_item = r.json()['responses'][0]['labelAnnotations'][0]['description']

print(food_item)

##### SPOONACULAR API #####
url_s = 'https://api.spoonacular.com/recipes/findByIngredients'
params_s = {
    'apiKey': SPOONACULAR_API_KEY,
    'number': 1,
    'ingredients': food_item
    }
s = requests.get(url_s, params=params_s)

# print(s.json())
id = s.json()[0]['id']

url_s2 = f'https://api.spoonacular.com/recipes/{id}/analyzedInstructions'
params_s2 = {
    'apiKey': SPOONACULAR_API_KEY,
    }
s_recipe = requests.get(url_s2, params=params_s2)
# print(s_recipe.json())
instructions = s_recipe.json()[0]['steps']
url_s3 = f'https://api.spoonacular.com/recipes/{id}/information'
params_s3 = {
    'apiKey': SPOONACULAR_API_KEY,
    }
s_information = requests.get(url_s3, params=params_s3)
ingredients = s_information.json()['extendedIngredients']
# print(ingredients)

@app.route('/')
def home_page():
    return render_template("favorites.html", stuff=food_item, instructions=instructions,
    ingredients=ingredients)


