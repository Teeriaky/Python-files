import requests
import pandas

def main():
    response = requests.get("https://api.thecatapi.com/v1/breeds")
    text = response.json()
    cats_data = get_data(text)
    output_data = cats_to_xlsx(cats_data)
    
    with pandas.ExcelWriter("cats_breeds.xlsx") as writer:
        pandas.DataFrame(output_data).to_excel(writer, index=False)

def get_data(text):
    cats_data = {}
    for breed in text:
        for attribute, characteristic in breed.items():
            if attribute == "name":
                cats_data[characteristic] = breed
    return cats_data

def cats_to_xlsx(data):
    required_objects = {"breeds'_names": [], "weight": [], "id": [], "temperament": [], "origin": [], "country_codes": [], 
                    "description": [], "life_span": [], "indoor": [], "adaptability": [], "affection_level": [], 
                    "child_friendly": [], "dog_friendly": [], "energy_level": [], "grooming": [], "health_issues": [], "intelligence": [], 
                    "shedding_level": [], "social_needs": [], "stranger_friendly": [], "vocalisation": [], "hairless": []}
    required_keys = [key for key in required_objects.keys()]
    
    for breed_name, breed_chars in data.items():
        required_objects["breeds'_names"].append(breed_name)
        for breed_char, attribute in breed_chars.items():
            if breed_char in required_keys:
                required_objects[breed_char].append(attribute)
                
    return required_objects

main()