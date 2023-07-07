import pandas
import json
import os
import sys


def main():
    dir_path = sys.argv[1]
    # The final dictionary for an output data
    output_data = {}
    
    # Getting the information from each file
    for file_name in os.listdir(dir_path):
        if not file_name.endswith(".json"):
            continue
        with open(os.path.join(dir_path, file_name)) as file:
            data = json.loads(file.read())
            data = pandas.json_normalize(data)
            received_data = get_data(data, file_name)
        # Creating the final dictionary if it's empty
        if not output_data:
            output_data = received_data
        # Appending data to the "output_data" in the case of using several files
        else:
            for key, value in received_data.items():
                output_data[key] += value              

    # Creating .xlsx file with data     
    with pandas.ExcelWriter("test.xlsx") as writer:
        pandas.DataFrame(output_data).to_excel(writer, index=False)

# Getting required data from file
def get_data(obj, file_name):
    required_objects = {"file_name": [], "Location": [], "Fan": [], "Speed": [], "state": []}
    
    for _, row in obj.iterrows():
        # Filling in all rows in required_objects
        for location in row["fan"]:
            for key, value in location.items():
                if key == "Location":
                    location = value        
                if key == "Fan":
                    fan = value
                if key == "Speed" and int(value) > 24000:
                    required_objects["file_name"].append(file_name)
                    required_objects["Location"].append(location)
                    required_objects["Fan"].append(fan)
                    required_objects["Speed"].append(int(value))
                    required_objects["state"].append("error")
    return required_objects
    
main()
