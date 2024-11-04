from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
import secrets
import requests,json
from .utils import *
session_key = secrets.token_hex(32)


# --------------------------------GEMINI API (OLD CODE)-----------------------------
# def bard(data):
#     key="AIzaSyCxa5DEoAezgHi6POcFvDeRoBxPWfHrN6Y"
#     url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={key}"
#     headers = {"Content-Type": "application/json"}
#     # data = {"contents":[{"parts":[{"text":f"My height is {data.get('height')}cm, current weight is {data.get('weight')}kg, gender is {data.get('gender')}, activity level is {data.get('activity_level')}, age is {data.get('age')} and want to {data.get('goal')} weight so prepare a Detailed diet chart for me. Don't give me calories intake or macronutrients. Note: I want details about 4 times a meal and some extra suggestions like  drinking water etc. Do not add any extra lines or intro in the beginning of the response."}]}]}
#     data = {
#     "contents": [
#         {
#             "parts": [
#                 {
#                     "text": (
#                         "Generate a detailed diet chart based on the following user information: "
#                         f"Height: {data.get('height')} cm, "
#                         f"Weight: {data.get('weight')} kg, "
#                         f"Gender: {data.get('gender')}, "
#                         f"Activity Level: {data.get('activity_level')}, "
#                         f"Age: {data.get('age')}, "
#                         f"Goal: {data.get('goal')}. "
#                         "Provide a diet plan that includes four meals throughout the day (breakfast, lunch, dinner, and a snack), "
#                         "and include extra suggestions for hydration and healthy habits. "
#                         "Do not include calorie intake or macronutrient details. "
#                         "Format the response clearly with headings for each meal and the extra suggestions. "
#                         "Avoid any introductory or extra lines."
#                     )
#                 }
#             ]
#         }
#     ]
#     }
#     response = requests.post(url, headers=headers, json=data)
#     print("API Response: ", response.text)
#     return dict(response.json()).get('candidates')[0].get('content').get('parts')[0].get('text') #read about webhooks in python flask


def bard(data):
    key = "VBHWST6PTCC5W6RS72ORMETOBZO6YSO4UQIA"  
    url = "https://api.vultrinference.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json"
    }
    
    prompt_text = (
        f"Generate a detailed diet chart based on the following user information: "
        f"Height: {data.get('height')} cm, "
        f"Weight: {data.get('weight')} kg, "
        f"Gender: {data.get('gender')}, "
        f"Activity Level: {data.get('activity_level')}, "
        f"Age: {data.get('age')}, "
        f"Goal: {data.get('goal')}. "
        "Provide a diet plan that includes four meals throughout the day (breakfast, lunch, dinner, and a snack), "
        "and include extra suggestions for hydration and healthy habits. "
        "Do not include calorie intake or macronutrient details. "
        "Format the response clearly with headings for each meal and the extra suggestions. "
        "Avoid any introductory or extra lines."
    )

    
    
    payload = {
        "model": "llama2-7b-chat-Q5_K_M",
        "messages": [
            {"role": "user", "content": prompt_text}
        ],
        "max_tokens": 200,
        "temperature": 0.7,
        "top_k": 40,
        "top_p": 0.9,
        "stream": False
    }
    
    response = requests.post(url, headers=headers, json=payload)
    
    print("from bard function")
    print("API Response:", response.json())  
    
    output = response.json().get('choices', [])[0].get('message', {}).get('content', '')
    return output

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




# def prepare(request):
#     if request.method == 'POST':
#         try:
#             data = json.loads(request.body)
#             print(request.headers)
#             data = dict(data)
#             if data.get('height') == None or data.get('weight')==None or data.get('gender')==None or data.get('activity_level') == None or data.get('age') ==None or data.get('goal') == None:
#                 return JsonResponse({'diet-chart'+session_key: "Fill all the values and submit then try again"})
            
#             chart = str(bard(data))
#             j=0
#             for i in range(len(chart)):
#                 if chart[i]=='*':
#                     j=i
#                     break
#             chart=chart[j::1]
#             chart=chart.replace('\n', '<br>')
#             chart=chart.replace("**", "1. ", 1)
#             chart=chart.replace("**", "", 1)
#             chart=chart.replace("**", "2. ", 1)
#             chart=chart.replace("**", "", 1)
#             chart=chart.replace("**", "3. ", 1)
#             chart=chart.replace("**", "", 1)
#             chart=chart.replace("**", "4. ", 1)
#             chart=chart.replace("**", "", 1)
#             return JsonResponse({'diet-chart'+session_key: chart}, status=200)
#         except json.JSONDecodeError:
#             return JsonResponse({"status": "error", "message": "Invalid JSON data provided"}, status=400)
#     else:
#         return JsonResponse({"status": "error", "message": "Only POST requests are allowed"}, status=405)
   

# --------------------NEW PREPARE FUNCTION --------------------------------
def prepare(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            data = dict(data)
            
            required_fields = ['height', 'weight', 'gender', 'activity_level', 'age', 'goal']
            if any(data.get(field) is None for field in required_fields):
                return JsonResponse({"status": "error", "message": "Please fill in all fields and try again"}, status=400)
            
            chart = bard(data)
            
            j = 0
            for i in range(len(chart)):
                if chart[i] == '*':
                    j = i
                    break
            chart = chart[j:].replace('\n', '<br>')
            chart = chart.replace("**", "1. ", 1).replace("**", "", 1)
            chart = chart.replace("**", "2. ", 1).replace("**", "", 1)
            chart = chart.replace("**", "3. ", 1).replace("**", "", 1)
            chart = chart.replace("**", "4. ", 1).replace("**", "", 1)
            
            return JsonResponse({"diet-chart": chart}, status=200)
        
        except json.JSONDecodeError:
            return JsonResponse({"status": "error", "message": "Invalid JSON data provided"}, status=400)
    else:
        return JsonResponse({"status": "error", "message": "Only POST requests are allowed"}, status=405)


def calculate(request):
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

    
