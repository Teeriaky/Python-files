import argparse
import pandas
import json


def main():
    # Receiving files
    objects = get_args()
    # The final dictionary for an output data
    output_data = {}
    
    # Getting the information from each file
    for file_name in objects.files:
        with open(file_name, encoding='utf-8') as file:
            data = json.loads(file.read())
            data = pandas.json_normalize(data)
            received_data = get_data(data)
        # Creating the final dictionary if it's empty
        if not output_data:
            output_data = received_data
        # Appending data to the "output_data" in the case of using several files
        else:
            for key, value in received_data.items():
                output_data[key] += value              

    # Creating .xlsx file with data     
    with pandas.ExcelWriter("intermediary_version.xlsx") as writer:
        pandas.DataFrame(output_data).to_excel(writer, index=False)

# Parsing arguments
def get_args():
    parser = argparse.ArgumentParser(description="Usage: json_to_csv.py file1 [file2 [... fileN]]")
    parser.add_argument(action="store", default="", dest="files", metavar="files", type=str, nargs="+")
    args = parser.parse_args()
    if not args:
        parser.error("At least one of a file's name is required.")
    return args            

# Getting required data from file
def get_data(obj):
    required_objects = {"MBH": [], "MBH_ID": [], "VRF": [], "Service": [], "Port": [], 
                        "ip_address": [], "gw": [], "mask": [], "vlan": [], "bs": [], "type": []}

    for _, row in obj.iterrows():
        # Filling in "VRF" row in required_objects
        for vrf_policy_array in row["vrf"]:
            for key, value in vrf_policy_array.items():
                if key == "vrf":
                    required_objects["VRF"].append(value)
                
        # Filling in "ip_address", "Port" and "vlan" rows in required_objects
        for arp_array in row["arp"]:
            for key, value in arp_array.items():
                if key == "address":
                    required_objects["ip_address"].append(value)
                if key == "interface":
                    if value.startswith("B"):
                        required_objects["Port"].append(value[0:3])
                    else:
                        rear_char = value[22]
                        required_objects["Port"].append(f"Gi{value[15:22]}" + rear_char if rear_char.isdigit()
                                                        else f"Gi{value[15:22]}")
                    required_objects["vlan"].append(int(value[-4:] if value[-4].isdigit() else value[-3:]))

    # Filling in "gw" row in required_objects
    for value in required_objects["ip_address"]:
        ip_address = value.split(".")
        last_digits = int(ip_address[3]) - 1
        gw = f"{'.'.join(ip_address[0:3])}.{last_digits}"
        required_objects["gw"].append(gw)
    
    # Filling in empty rows
    for key, values in required_objects.items():
        for _ in range(len(required_objects["ip_address"])):
            if len(values) != len(required_objects["ip_address"]):
                required_objects[key].append('')

    return required_objects
    
main()
