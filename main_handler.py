import os
import csv
import yaml
from netmiko import ConnectHandler
from jinja2 import Environment, FileSystemLoader
from netmiko.ssh_autodetect import SSHDetect
import threading
import openpyxl

def render_template(template_path, context):
    env = Environment(loader=FileSystemLoader(os.path.dirname(template_path)))
    template = env.get_template(os.path.basename(template_path))
    return template.render(context)


def apply_config(device_info, template_folder, golden_yaml_path):
    device_type = device_info["device_type"]

    with open(golden_yaml_path) as golden_yaml_file:
        golden_yaml_data = yaml.safe_load(golden_yaml_file)

    for driver, driver_data in golden_yaml_data.items():
        if device_type.lower() in driver.lower():
            # Use only driver_data in the context
            context = driver_data

            # Render and apply golden J2 configuration to device
            template_path = os.path.join(template_folder, f"{driver.lower()}_template.j2")
            golden_j2_template = render_template(template_path, context)

            # Use information from the device_list.txt file
            device_info.pop("device_type")  # Remove device_type from device_info

            # Connect to the device using information from device_list.txt
            net_connect = ConnectHandler(**device_info)
            print(f"Applying golden J2 template to {device_type} device...")
            net_connect.send_config_set(golden_j2_template.splitlines())
            net_connect.disconnect()
            print(f"Golden J2 template applied to {device_type} device.")


def read_device_list(file_path):
    device_info_list = []

    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    header = [cell.value for cell in sheet[1]]

    for row in sheet.iter_rows(min_row=2, values_only=True):
        device_info_list.append(dict(zip(header, row)))

    return device_info_list


def main():
    template_folder = "golden_files"
    golden_yaml_path = "golden_files/golden_yaml_file.yml"

    # Read device information from a CSV file
    device_info_list = read_device_list(os.path.join(template_folder, "device_list.xlsx"))

    for device_info in device_info_list:
        # Autodetect device type
        guesser = SSHDetect(device_type="autodetect", username=device_info["username"],
                            password=device_info["password"], ip=device_info["ip_address"])
        device_info["device_type"] = guesser.autodetect()
        # Apply configuration using golden YAML file
        apply_config(device_info, template_folder, golden_yaml_path)

def main_threaded():
    thread = threading.Thread(target=main)
    thread.start()
    thread.join()

if __name__ == "__main__":
    main_threaded()





