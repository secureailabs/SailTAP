# -----------------------------------------------------------
#
# Python Script to quickly delete azure vms
#
# Written by Stanley Lin 11/18/2021
# -----------------------------------------------------------

import requests
import sys
import time

from json import dumps

# declare values for script
tennant_id = "3e74e5ef-7e6a-4cf0-8573-680ca49b64d8"
resource_group = "ScratchpadRg"
subscription_id = "3d2b9951-a0c8-4dc3-8114-2776b047b15c"
payload = {}


def pretty_print(msg=None, data=None, indent=4):
    """
    Pretty Print Human readable json format

    :param msg: Specified message, defaults to None
    :param data: Data to be formatted, defaults to None
    :param indent: Specified indentation for format, defaults to 4
    :type indent: int, optional
    """
    to_json = dumps(data, indent=indent)
    if not msg:
        print(f"\n{to_json}")
    else:
        print(f"\n{msg}\n {to_json}")


def yes_or_no(question):
    """
    Helper for yes or no questions

    :param question: [description]
    :type question: [type]
    :return: [description]
    :rtype: [type]
    """
    answer = input(f"{question} (y/n): ").lower().strip()
    print("")
    while not (answer == "y" or answer == "yes" or answer == "n" or answer == "no"):
        print("Input yes or no")
        answer = input(question + "(y/n):").lower().strip()
        print("")
    if answer[0] == "y":
        return True
    else:
        return False


def get_access_token():
    """
    Get accesstoken using Tennant ID

    :return: access_token
    :rtype: string
    """
    url = f"https://login.microsoftonline.com:443/{tennant_id}/oauth2/token"
    appid = "4f909fab-ad4c-4685-b7a9-7ddaae4efb22"
    password = "1YEn1Y.bVTVk-dzm9voTWyf7DrgQF29xL2"
    payload = f"grant_type=client_credentials&client_id={appid}&client_secret={password}&resource=https%3A%2F%2Fmanagement.core.windows.net%2F"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": "esctx=AQABAAAAAAD--DLA3VO7QrddgJg7WevrwFa5Vd2CRODerYX5Cft7ZbG2oI5eopwekshW1r9eC7QCt2K6zgDA4OBADxOr2ZOB1OA-mv7F_FbV3HN9ghS4ONkTiJOtoTJU7vXpeucT4QEdsxwNLg7HBAQIoWTP6n16l_EMjI8whRpgpBi9sLELg9uisSfIWhxABvzgA9LND3AgAA; fpc=AoEcDfB-HWRKj27yI2peVttMtT7WAQAAAO3CKNkOAAAA; stsservicecookie=estsfd; x-ms-gateway-slice=estsfd",
    }
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
    except requests.exceptions.RequestException as error:
        print(f"\n{error}")

    access_token = response.json().get("access_token")
    print(f"Current access token: {access_token}\n")
    return access_token


def get_rg(access_token):
    """
    get resource group of subscription
    """
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourcegroups?api-version=2021-04-01"
    payload = {}
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
    except requests.exceptions.RequestException as error:
        print(f"\n{error}")
    return response


def get_all_vm_ips(access_token):
    """
    Get all vm ips in resourcegroup of subscriptions
    """
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Compute/virtualMachines?api-version=2021-07-01"
    payload = {}
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
    except requests.exceptions.RequestException as error:
        print(f"\n{error}")

    all_vms = response.json().get("value")
    map_vm_ip = {}

    for vm in all_vms:
        current_vm_name = vm.get("name")
        vm_ip = get_vm_public_ip(access_token, vm_name=current_vm_name)
        map_vm_ip.update({vm_ip: current_vm_name})
    return map_vm_ip


def get_vm_nic_info(access_token, vm_name=None):
    """
    Get vm nic information
    """
    url = f"https://management.azure.com//subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Network/networkInterfaces/{vm_name}-nic?api-version=2021-03-01"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
    except requests.exceptions.RequestException as error:
        print(f"\n{error}")
    return response, response.json()


def get_vm_public_ip(access_token, vm_name=None):
    """
    get vm public ip information
    """
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Network/publicIPAddresses/{vm_name}-ip?api-version=2021-03-01"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
    except requests.exceptions.RequestException as error:
        print(f"\n{error}")

    output = response.json()
    return output.get("properties").get("ipAddress")


def get_vm_status(access_token, vm_name):
    """
    get current specified azure vm resource status
    """
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Compute/virtualMachines/{vm_name}/instanceView?api-version=2021-07-01"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.request("GET", url, headers=headers, data=payload)
    except requests.exceptions.RequestException as error:
        print(f"\n{error}")
    vm_state = response.json().get("statuses")[1].get("displayStatus")
    return vm_state


def stop_vm(access_token, vm_name):
    """
    Stop specified azure vm resource
    """
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Compute/virtualMachines/{vm_name}/deallocate?api-version=2021-07-01"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
    except requests.exceptions.RequestException as error:
        print(f"\n{error}")
    return response


def del_vm(access_token, vm_name):
    """
    Delete specified azure vm resource
    """
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Compute/virtualMachines/{vm_name}?api-version=2021-07-01"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.request("DELETE", url, headers=headers, data=payload)
    except requests.exceptions.RequestException as error:
        print(f"\n{error}")
    return response


def del_vm_disk(access_token, vm_name):
    """
    Delete specified azure vm disk resource
    """
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Compute/disks/{vm_name}-disk?api-version=2020-12-01"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.request("DELETE", url, headers=headers, data=payload)
    except requests.exceptions.RequestException as error:
        print(f"\n{error}")
    return response


def del_vm_nic(access_token, vm_name):
    """
    Delete specified azure vm nic resource
    """
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Network/networkInterfaces/{vm_name}-nic?api-version=2021-03-01"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.request("DELETE", url, headers=headers, data=payload)
    except requests.exceptions.RequestException as error:
        print(f"\n{error}")
    return response


def del_vm_ip(access_token, vm_name):
    """
    Delete specified azure vm ip resource
    """
    url = f"https://management.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Network/publicIPAddresses/{vm_name}-ip?api-version=2021-03-01"
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.request("DELETE", url, headers=headers, data=payload)
    except requests.exceptions.RequestException as error:
        print(f"\n{error}")
    return response


def main() -> int:
    """
    main
    states: 'VM deallocated', 'VM running', 'VM deallocating',
    state of 'None' may happen... low chance. and I am unclear how to handle
    """
    # get subsciption access token
    current_token = get_access_token()
    resource_groups = get_rg(current_token)
    print(resource_groups)
    # list all vms and their ips
    map_vm_ip = get_all_vm_ips(current_token)
    print(dumps(map_vm_ip, indent=4))
    print("Please note if vm does not have ip, it is represented by null")

    # Ask user what enter name associated to ip of their machine
    user_vm_name = input("Please enter the vm name associated to ip of your vm:  ")
    if yes_or_no(f"The vm to be deleted is: {user_vm_name}"):
        if user_vm_name in map_vm_ip.values():
            deallocate_vm_name = user_vm_name
            # check vm status
            print(f"Getting status of vm: {deallocate_vm_name}")
            response = get_vm_status(current_token, deallocate_vm_name)
            print(f"VM:{deallocate_vm_name} state is: {response}")

            if response == "VM running":
                # Stop vm
                print(f"Stopping VM: {deallocate_vm_name}")
                test_response = stop_vm(current_token, deallocate_vm_name)
                print(f"response status for stop is : {test_response.status_code}")
                assert test_response.status_code == 202
                while response != "VM deallocated":
                    response = get_vm_status(current_token, deallocate_vm_name)
                    print(f"VM:{deallocate_vm_name} state is: {response}")
                    time.sleep(2)
                print("The vm has stopped!!")
            elif response == "VM deallocating":
                while response != "VM deallocated":
                    # wait until vm is deallocated
                    response = get_vm_status(current_token, deallocate_vm_name)
                    print(f"VM:{deallocate_vm_name} state is: {response}")
                    time.sleep(2)
                print("The vm has stopped!!")
            else:
                # vm is currently stopped and deallocated
                print(f"VM:{deallocate_vm_name} state is: {response}")
                print("The vm has stopped!!")

            print(f"Deleting VM: {deallocate_vm_name}")
            # Delete VM
            test_response = del_vm(current_token, deallocate_vm_name)
            print(f"response status for deletion of vm is : {test_response.status_code}")
            assert test_response.status_code == 202
            # Delete VM DISK
            test_response = del_vm_disk(current_token, deallocate_vm_name)
            print(f"response status for deletion of vm disk is : {test_response.status_code}")
            assert test_response.status_code == 202
            # Delete vm NIC
            test_response = del_vm_nic(current_token, deallocate_vm_name)
            print(f"response status for deletion of vm nic is : {test_response.status_code}")
            assert test_response.status_code == 202
            # Delete VM IP
            test_response = del_vm_ip(current_token, deallocate_vm_name)
            print(f"response status for deletion of vm ip is : {test_response.status_code}")
            assert test_response.status_code == 202
            print("\nPlease wait an additional 1 min to ensure azure resources cleanup correctly")
            time.sleep(60)
            print("Script Completed!!")

    else:
        print("Please start program over")


if __name__ == "__main__":
    sys.exit(main())
