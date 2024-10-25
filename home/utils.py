import requests, json

from bs4 import BeautifulSoup
import logging.config
from os import path
from requests import Session
logger = logging.getLogger('bmi')
def sec(time_str:str):
    parts = time_str.split(":")
    hours = 0
    minutes = 0
    seconds = 0
    if len(parts) == 2:
        minutes = int(parts[0])
        seconds = int(parts[1])
    elif len(parts) == 1:
        seconds = int(parts[0])
    return hours * 3600 + minutes * 60 + seconds

def video(name:str):
    url = "https://www.youtube.com/results"
    payloads = { "search_query":name+" @puregym" }
    headers = { "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36" }
    session = Session()
    response = session.get(url=url, headers=headers, params=payloads)
    html_content = response.text
    session.close()
    soup = BeautifulSoup(html_content,'lxml')
    script_tag = soup.find('script', text=lambda text: text and 'var ytInitialData' in text)
    script_content = script_tag.string
    start_index = script_content.find('var ytInitialData = ') + len('var ytInitialData = ')
    end_index = script_content.find('};', start_index) + 1
    yt_initial_data = script_content[start_index:end_index]
    data = json.loads(yt_initial_data)
    l = []
    for i in data.get("contents").get("twoColumnSearchResultsRenderer").get("primaryContents").get("sectionListRenderer").get("contents")[0].get("itemSectionRenderer").get("contents"):
        if i.get("videoRenderer")!=None:
            if sec(i["videoRenderer"]["lengthText"]["simpleText"]) <= 29:
                return {
                    "id": i["videoRenderer"]["videoId"], 
                    "title": i["videoRenderer"]["title"]["runs"][0]["text"], 
                    "thumbnail": i["videoRenderer"]["thumbnail"][ "thumbnails"][0]["url"]
                }   
    return None

def get_exercise(muscle:str, category:str):
# category is the equipments and muscles are muscles I mean that's readable
    url = f"https://musclewiki.com/newapi/exercise/exercises/?limit=20&muscles={muscle}&category={category}"
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
    response = requests.request(method="GET", url=url, headers=headers)    
    res = response.json()
    result = []
    for i in res.get("results"):
        if i.get("name")!=None:
            result.append({
                "id": i["id"],
                "name": i["name"],
                "difficulty": i.get("difficulty"),
                "correct_steps": i.get("correct_steps"),
                "muscles": i.get("muscles"),
                "url": "/exercise/"+((i["name"]).replace(' ', '-')).lower()
        })
    
    return result

def calculate_calorie_needs(weight: float, target_weight: float, height: float, age: int, gender: str, goal: str, time_frame: int, activity_level: str) -> float:
    s = 5 if gender == 'male' else -161
    bmr = 10 * weight + 6.25 * height - 5 * age + s
    if activity_level == 'sedentary':
        cal = bmr * 1.2
    elif activity_level == 'lightly active':
        cal = bmr * 1.375
    elif activity_level == 'moderately active':
        cal = bmr * 1.55
    elif activity_level == 'very active':
        cal = bmr * 1.725
    else:
        cal = bmr * 1.9
    if goal == 'maintain':
        return cal
    else:
        weight_diff = abs(target_weight - weight)
        cal_diff_per_day = weight_diff * 7700 / time_frame
        if goal == 'loose':
            return cal - cal_diff_per_day
        else:
            return cal + cal_diff_per_day
        
def macro_needs(weight: float, target_weight: float, height: float, age: int, gender: str, goal: str, time_frame: int, activity_level: str) -> dict:
    s = 5 if gender == 'male' else -161
    bmr = (10 * weight) + (6.25 * height) - (5 * age) + s
    if activity_level == 'sedentary':
        cal = bmr * 1.2
    elif activity_level == 'lightly active':
        cal = bmr * 1.375
    elif activity_level == 'moderately active':
        cal = bmr * 1.55
    elif activity_level == 'very active':
        cal = bmr * 1.725
    else:
        cal = bmr * 1.9
    if goal != 'maintain':
        weight_diff = abs(target_weight - weight)
        cal_diff_per_day = weight_diff * 7700 / time_frame
        if goal == 'loose':
            cal -= cal_diff_per_day
        else:
            cal += cal_diff_per_day
    protein = weight * 0.8
    fat = cal * 0.25 / 9
    carbs = (cal - protein * 4 - fat * 9) / 4
    carb_per = round((carbs / (carbs + fat + protein)) * 100)
    protein_per = round((protein / (carbs + fat + protein)) * 100)
    fat_per = round((fat / (carbs + fat + protein)) * 100)
    return {
        'protein': "{:.2f}".format(protein),
        'fat': "{:.2f}".format(fat),
        'carbs': "{:.2f}".format(carbs),
        'carb_per': carb_per,
        'protein_per': protein_per,
        'fat_per': fat_per
    }

muscle_groups = {
    "Biceps": [
        {"id": 1, "name": "Biceps"},
        {"id": 16, "name": "Long Head Bicep"},
        {"id": 17, "name": "Short Head Bicep"}
    ],
    "Traps": [
        {"id": 14, "name": "Traps (mid-back)"},
        {"id": 4, "name": "Traps"},
        {"id": 41, "name": "Upper Traps"},
        {"id": 42, "name": "Lower Traps"}
    ],
    "Lower back": [
        {"id": 13, "name": "Lower back"}
    ],
    "Abdominals": [
        {"id": 12, "name": "Abdominals"},
        {"id": 21, "name": "Lower Abdominals"},
        {"id": 22, "name": "Upper Abdominals"}
    ],
    "Calves": [
        {"id": 11, "name": "Calves"},
        {"id": 31, "name": "Tibialis"},
        {"id": 32, "name": "Soleus"},
        {"id": 33, "name": "Gastrocnemius"}
    ],
    "Forearms": [
        {"id": 10, "name": "Forearms"},
        {"id": 25, "name": "Wrist Extensors"},
        {"id": 26, "name": "Wrist Flexors"}
    ],
    "Glutes": [
        {"id": 9, "name": "Glutes"},
        {"id": 37, "name": "Gluteus Medius"},
        {"id": 38, "name": "Gluteus Maximus"}
    ],
    "Hamstrings": [
        {"id": 8, "name": "Hamstrings"},
        {"id": 39, "name": "Medial Hamstrings"},
        {"id": 40, "name": "Lateral Hamstrings"}
    ],
    "Lats": [
        {"id": 7, "name": "Lats"}
    ],
    "Shoulders": [
        {"id": 6, "name": "Shoulders"},
        {"id": 18, "name": "Lateral Deltoid"},
        {"id": 19, "name": "Anterior Deltoid"},
        {"id": 20, "name": "Posterior Deltoid"}
    ],
    "Triceps": [
        {"id": 5, "name": "Triceps"},
        {"id": 34, "name": "Long Head Tricep"},
        {"id": 35, "name": "Lateral Head Triceps"},
        {"id": 36, "name": "Medial Head Triceps"}
    ],
    "Quads": [
        {"id": 3, "name": "Quads"},
        {"id": 27, "name": "Inner Thigh"},
        {"id": 28, "name": "Inner Quadriceps"},
        {"id": 29, "name": "Outer Quadricep"},
        {"id": 30, "name": "Rectus Femoris"}
    ],
    "Chest": [
        {"id": 2, "name": "Chest"},
        {"id": 23, "name": "Upper Pectoralis"},
        {"id": 24, "name": "Mid and Lower Chest"}
    ],
    "Obliques": [
        {"id": 15, "name": "Obliques"}
    ],
    "Hands": [
        {"id": 43, "name": "Hands"}
    ],
    "Feet": [
        {"id": 46, "name": "Feet"}
    ],
    "Front Shoulders": [
        {"id": 47, "name": "Front Shoulders"}
    ],
    "Rear Shoulders": [
        {"id": 48, "name": "Rear Shoulders"}
    ]
}
muscles = {
    "Biceps": {
        "id": 1, 
        "name": "Biceps"
    },
    "Traps": {
        "id": 4, 
        "name": "Traps"
    },
    "Lower back": {
        "id": 13, 
        "name": "Lower back"
    },
    "Abdominals": {
        "id": 12, 
        "name": "Abdominals"
    },
    "Calves": {
        "id": 11, 
        "name": "Calves"
    },
    "Forearms": {
        "id": 10, 
        "name": "Forearms"
    },
    "Glutes": {
        "id": 9, 
        "name": "Glutes"
    },
    "Hamstrings": {
        "id": 8, 
        "name": "Hamstrings"
    },
    "Lats": {
        "id": 7, 
        "name": "Lats"
    },
    "Shoulders": {
        "id": 6, 
        "name": "Shoulders"
    },
    "Triceps": {
        "id": 5, 
        "name": "Triceps"
    },
    "Quads": {
        "id": 3, 
        "name": "Quads"
    },
    "Chest": {
        "id": 2, 
        "name": "Chest"
    },
    "Obliques": {
        "id": 15, 
        "name": "Obliques"
    }
}

equipments = {
        "Barbell":{
            "id": 1,
            "name": "Barbell"
        },
        "Dumbbells":{
            "id": 2,
            "name": "Dumbbells"
        },
        "Bodyweight": {
            "id": 3,
            "name": "Bodyweight"
        },
        "Machine": {
            "id": 4,
            "name": "Machine"
        },
        "Medicine-Ball": {
            "id": 6,
            "name": "Medicine-Ball"
        },
        "Kettlebells": {
            "id": 7,
            "name": "Kettlebells"
        },
        "Stretches": {
            "id": 8,
            "name": "Stretches"
        },
        "Cables": {
            "id": 9,
            "name": "Cables"
        },
        "Band": {
            "id": 10,
            "name": "Band"
        },
        "Plate": {
            "id": 11,
            "name": "Plate"
        },
        "TRX": {
            "id": 12,
            "name": "TRX"
        },
        "Yoga": {
            "id": 13,
            "name": "Yoga"
        },
        "Bosu": {
            "id": 16,
            "name": "Bosu"
        },
        "Bosu-Ball": {
            "id": 24,
            "name": "Bosu-Ball"
        },
        "Cardio": {
            "id": 27,
            "name": "Cardio"
        },
        "Smith-Machine":{
            "id": 85,
            "name": "Smith-Machine"
        }
}


# BMI copied from BMI module

class Bmi:

    boundaries = [
        0,
        18.5,
        25,
        30,
        35,
        40
    ]

    ranges_i18n = {
        0: {
            "en": "Underweight",
            "es": "Bajo peso"
        },
        1: {
            "en": "Healthy",
            "es": "Peso saludable"
        },
        2: {
            "en": "Overweight",
            "es": "Sobrepeso"
        },
        3: {
            "en": "Obese, Class I",
            "es": "Obesidad, Clase I"
        },
        4: {
            "en": "Obese, Class II",
            "es": "Obesidad, Clase II"
        },
        5: {
            "en": "Obese, Class III",
            "es": "Obesidad, Clase III"
        }
    }

    @staticmethod
    def calculate_bmi(weight_kg, height_m):
        exact_value = weight_kg / pow(height_m, 2)
        rounded_value = round(exact_value, 1)
        logger.debug("Calculated BMI: Exact value: " + str(exact_value) + "; Rounded value: " + str(rounded_value))
        return rounded_value

    @classmethod
    def calculate_bmi_with_info(cls, weight_kg, height_m, lang="en"):
        bmi = cls.calculate_bmi(weight_kg, height_m)
        range = cls.get_bmi_range_info(bmi, lang)
        return bmi, range

    @classmethod
    def get_bmi_range_info(cls, bmi, lang="en"):
        if bmi < cls.boundaries[1]:
            return cls.ranges_i18n[0][lang]
        elif (bmi >= cls.boundaries[1]) and (bmi < cls.boundaries[2]):
            return cls.ranges_i18n[1][lang]
        elif (bmi >= cls.boundaries[2]) and (bmi < cls.boundaries[3]):
            return cls.ranges_i18n[2][lang]
        elif (bmi >= cls.boundaries[3]) and (bmi < cls.boundaries[4]):
            return cls.ranges_i18n[3][lang]
        elif (bmi >= cls.boundaries[4]) and (bmi < cls.boundaries[5]):
            return cls.ranges_i18n[4][lang]
        else:
            return cls.ranges_i18n[5][lang]

    @classmethod
    def get_bmi_ranges_with_info(cls, lang="en"):
        detailed_ranges = []
        logger.debug("Ranges with information")
        for i, boundary in enumerate(cls.boundaries):
            if i + 1 < len(cls.boundaries):
                detailed_ranges.append({"From": boundary, "To": cls.boundaries[i + 1],
                                        "Info": cls.get_bmi_range_info(boundary, lang)})
                logger.debug("From: " + str(boundary) + "; To: " + str(cls.boundaries[i + 1]) +
                             "; Info: " + cls.get_bmi_range_info(boundary, lang))
            else:
                detailed_ranges.append({"From": boundary, "To": "", "Info": cls.get_bmi_range_info(boundary, lang)})
                logger.debug("From: " + str(boundary) + "; To: " + "; Info: " + cls.get_bmi_range_info(boundary, lang))
        return detailed_ranges

    @staticmethod
    def calculate_weight(height_m, bmi):
        weight = bmi * pow(height_m, 2)
        rounded_weight = round(weight, 1)
        logger.debug("Inputs are height: " + str(height_m) + " and bmi: " + str(bmi))
        logger.debug("Exact weight value is: " + str(weight) + "; And rounded weight: " + str(rounded_weight))
        return rounded_weight

    @classmethod
    def calculate_weight_boundaries(cls, height_m):
        weight_per_range = [
            cls.calculate_weight(height_m, cls.boundaries[0]),
            cls.calculate_weight(height_m, cls.boundaries[1]),
            cls.calculate_weight(height_m, cls.boundaries[2]),
            cls.calculate_weight(height_m, cls.boundaries[3]),
            cls.calculate_weight(height_m, cls.boundaries[4]),
            cls.calculate_weight(height_m, cls.boundaries[5])
        ]
        return weight_per_range

    @classmethod
    def calculate_weight_ranges_with_info(cls, height_m, lang="en"):
        weight_boundaries = cls.calculate_weight_boundaries(height_m)
        detailed_weight_boundaries = []
        logger.debug("Ranges weight boundaries information for height: " + str(height_m))
        for i, boundary in enumerate(weight_boundaries):
            if i + 1 < len(weight_boundaries):
                detailed_weight_boundaries.append({"From": boundary, "To": weight_boundaries[i + 1],
                                                   "Info": cls.ranges_i18n[i][lang]})
                logger.debug("From: " + str(boundary) + "; To: " + str(weight_boundaries[i + 1]) +
                             "; Info: " + cls.ranges_i18n[i][lang])
            else:
                detailed_weight_boundaries.append({"From": boundary, "To": "", "Info": cls.ranges_i18n[i][lang]})
                logger.debug("From: " + str(boundary) + "; To: " + "; Info: " + cls.ranges_i18n[i][lang])
        return detailed_weight_boundaries

    @classmethod
    def calculate_healthy_weight(cls, height_m):
        your_weight_boundaries = (cls.calculate_weight_boundaries(height_m))[1:3]
        logger.debug("For height: " + str(height_m) + ", your healthy boundaries are: " + str(your_weight_boundaries))
        return your_weight_boundaries

