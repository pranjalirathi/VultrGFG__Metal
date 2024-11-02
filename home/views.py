from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
import secrets
import requests,json
from .utils import *
session_key = secrets.token_hex(32)

def bard(data):
    key="AIzaSyCxa5DEoAezgHi6POcFvDeRoBxPWfHrN6Y"
    url = f"https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText?key={key}"
    headers = {"Content-Type": "application/json"}
    data = {"prompt": {"text": f"My height is {data.get('height')}cm, current weight is {data.get('weight')}kg, gender is {data.get('gender')}, activity level is {data.get('activity_level')}, age is {data.get('age')} and want to {data.get('goal')} weight so prepare a Detailed diet chart for me. Don't give me calories intake or macronutrients"}}
    response = requests.post(url, headers=headers, json=data)
    return dict(response.json()).get('candidates')[0].get('output') #read about webhooks in python flask


# def personalized_diet_chart(data):
#     key="VBHWST6PTCC5W6RS72ORMETOBZO6YSO4UQIA"
#     vultr_api_url = "url  ..."
#     headers = {
#              "Content-Type": "application/json",
#              "Authorization": f"Bearer {api_key}"}

#     payload = {
#         "height": data.get("height"),
#         "weight": data.get("weight"),
#         "gender": data.get("gender"),
#         "activity_level": data.get("activity_level"),
#         "age": data.get("age"),
#         "goal": data.get("goal")
#     }
#     response = requests.post(vultr_api_url, headers=headers, json=payload)
#     if response.status_code == 200:
#         return response.json().get('diet_chart')
#     else:
#         return {"error": "Failed to retrieve diet chart"}

# Create your views here
def index(request):
    return render(request, 'home/home.html', context={'page': "home"})

def about(request):
    context = {'page': 'about'}
    return render(request, 'home/about.html', context=context)

def forms(request):
    lstofmuscles = ["Biceps", "Forearms", "Shoulders", "Triceps", "Quads", "Glutes", "Lats", "Lower back",
        "Hamstrings", "Chest", "Abdominals", "Obliques", "Traps", "Calves"]
    lstofequipments = ['Barbell', 'Dumbbells', 'Bodyweight', 'Machine', 'Medicine-Ball', 'Kettlebells', 
        'Stretches', 'Cables', 'Band', 'Plate', 'TRX', 'Yoga', 'Bosu', 'Bosu-Ball', 'Cardio', 'Smith-Machine']
    context = {
        'lstofmuscles': lstofmuscles,
        'lstofequipments': lstofequipments,
        'page': "forms",
        'imglink' : "/static/bgstarted.jpg?raw=true",
        'key': session_key
    }
    if request.method == "POST":
        muscle = request.POST.get('muscle')
        equipment=  request.POST.get('equipment')
        if muscles.get(muscle) != None and equipments.get(equipment)!=None:
            results = get_exercise(muscle=str(muscles.get(muscle)['id']), category=str(equipments.get(equipment)['id']))
            context = {'page': "exercise", 'results': results}
            return render(request, 'home/exercise.html', context=context)

        messages.add_message(request, level=50, message='Oops! No exercise found. Please try again with different filters', extra_tags="red")
    return render(request, 'home/forms.html', context=context)

def exercise(request, slug):
    url = "https://musclewiki.com/newapi/exercise/exercises/"
    payload={"slug": slug}
    res = requests.get(url=url, params=payload)
    res = res.json()
    result = {}
    if res.get("results")!=None and len(res.get("results")) > 0:
        content = video(res.get("results")[0].get("name"))
        if (content==None):
            result = {
                "difficulty": res.get("results")[0].get("difficulty"),
                "correct_steps": res.get("results")[0].get("correct_steps"),
                "content": "https://www.youtube.com/embed/wvjK5vJlpuI"
            }
        else:
            result = {
                "difficulty": res.get("results")[0].get("difficulty"),
                "correct_steps": res.get("results")[0].get("correct_steps"),
                "content": content
            }
        return JsonResponse(data={"status":1, 'result': result}, status=200)
        
    else :
        return JsonResponse(data={"status":0, 'result': {}}, status=400)

def prepare(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(request.headers)
            data = dict(data)
            if data.get('height') == None or data.get('weight')==None or data.get('gender')==None or data.get('activity_level') == None or data.get('age') ==None or data.get('goal') == None:
                return JsonResponse({'diet-chart'+session_key: "Fill all the values and submit then try again"})
            
            chart = str(bard(data))
            j=0
            for i in range(len(chart)):
                if chart[i]=='*':
                    j=i
                    break
            chart=chart[j::1]
            chart=chart.replace('\n', '<br>')
            chart=chart.replace("**", "1. ", 1)
            chart=chart.replace("**", "", 1)
            chart=chart.replace("**", "2. ", 1)
            chart=chart.replace("**", "", 1)
            chart=chart.replace("**", "3. ", 1)
            chart=chart.replace("**", "", 1)
            chart=chart.replace("**", "4. ", 1)
            chart=chart.replace("**", "", 1)
            return JsonResponse({'diet-chart'+session_key: chart}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data provided"}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Only POST requests are allowed"}, status=405)
   
    


def calculate(request):
    print("Request method:", request.method)
    if request.method == 'POST':
        try:
            # Decode the JSON data sent in the request body
            data = json.loads(request.body)
            data = dict(data)
            print("from headers: ", request.headers)
            print("session_key: ", session_key)
            bmi = Bmi.calculate_bmi_with_info(data['weight'], data['height'] / 100, "en")
            calories = calculate_calorie_needs(age=data.get('age'), weight=data.get('weight'),
                                          target_weight=data.get('target_weight'),
                                          height=data.get('height'), time_frame=data.get('time frame'),
                                          activity_level=data.get('activity_level'), goal=data.get('goal'),
                                          gender=data.get('gender'))
            macros = macro_needs(age=data.get('age'), weight=data.get('weight'),
                                          target_weight=data.get('target_weight'),
                                          height=data.get('height'), time_frame=data.get('time frame'),
                                          activity_level=data.get('activity_level'), goal=data.get('goal'),
                                          gender=data.get('gender'))
            result = {
            'bmi': "{:.2f}".format(bmi[0]),
            'category': bmi[1],
            'calories': int(calories),
            'target_weight': data.get('target_weight'),
            'carb': macros.get('carbs'),
            'fat': macros.get('fat'),
            'protein': macros.get('protein'),
            'carb_per': macros['carb_per'],
            'protein_per': macros.get('protein_per'),
            'fat_per': macros.get('fat_per')
            }
            return JsonResponse(result)
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data provided"}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Only POST requests are allowed"}, status=405)

    
