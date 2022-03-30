# -----------------------------------------------------------
#
# Class SailPortal
#
# -----------------------------------------------------------
import requests
from utils.helpers import get_response_values


class SailPortalApi:
    """
    Sail Portal Api Class
    """

    def __init__(self, base_url, email, password):
        self.base_url = base_url
        self.email = email
        self.password = password
        self.headers = {"Content-Type": "application/json", "Accept": "application/json"}

    # TODO Remote Attestation Certificate

    def login(self):
        """
        Login to Sail Api portal

        :returns: response, response.json(), user_eosb
        :rtype: (string, string, string)
        """
        json_params = {"Email": self.email, "Password": self.password}
        # query_params = url_encoded({"Email": self.email, "Password": self.password})
        # Attempt to login to SAIL PORTAL via POST request
        try:
            #  params as json
            response = requests.post(
                f"{self.base_url}/SAIL/AuthenticationManager/User/Login", json=json_params, verify=False
            )
            # params query string
            # response = requests.post(
            #     f"{self.base_url}/SAIL/AuthenticationManager/User/Login", params=query_params, verify=False
            # )
            # response.raise_for_status()
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output and user eosb
        return get_response_values(response)

    def get_basic_user_info(self):
        """
        Get basic user information from  Sail Api portal

        :return: response, response.json()
        :rtype: (string, string)
        """
        _, _, user_eosb = self.login()
        json_params = {"Eosb": user_eosb}
        # query_params = url_encoded({"Eosb": user_eosb})
        # Attempt to get basic user information
        try:
            #  params as json
            response = requests.get(
                f"{self.base_url}/SAIL/AuthenticationManager/GetBasicUserInformation", json=json_params, verify=False
            )
            # params query string
            # response = requests.get(
            #     f"{self.base_url}/SAIL/AuthenticationManager/GetBasicUserInformation", params=query_params, verify=False
            # )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    def update_password(self, current_password, new_password):
        """
        Get update user password from  Sail Api portal

        :param current_password:
        :type current_password: string
        :param new_password:
        :type new_password: string
        :return: response, response.json()
        :rtype: (string, string)
        """
        self.password = current_password
        _, _, user_eosb = self.login()
        #  params as json
        json_params = {
            "Eosb": user_eosb,
            "Email": self.email,
            "CurrentPassword": current_password,
            "NewPassword": new_password,
        }
        # query_params = url_encoded(
        #     {"Eosb": user_eosb, "Email": self.email, "CurrentPassword": current_password, "NewPassword": new_password}
        # )
        # Attempt to update user password
        try:
            #  params as json
            response = requests.patch(
                f"{self.base_url}/SAIL/AuthenticationManager/User/Password", json=json_params, verify=False
            )
            # params query string
            # response = requests.patch(
            #     f"{self.base_url}/SAIL/AuthenticationManager/User/Password", params=query_params, verify=False
            # )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    def check_eosb(self, eosb):
        """
        Call the CheckEosb API in the Sail portal

        :param eosb:
        :type eosb: string
        :param new_password:
        :type new_password: string
        :return: response, response.json(), user_eosb
        :rtype: (string, string, user_eosb)
        """
        #  params as json
        json_params = {"Eosb": eosb}
        try:
            #  params as json
            response = requests.get(
                f"{self.base_url}/SAIL/AuthenticationManager/CheckEosb", json=json_params, verify=False
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code, output, and user eosb
        return get_response_values(response)
