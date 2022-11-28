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
    # [POST] /login
    def login(self):
        """
        Login to Sail Api portal

        :returns: response, response.json(), user_eosb
        :rtype: (string, string, string)
        """
        json_params = {"username": self.email, "password": self.password}
        
        # Attempt to login to SAIL PORTAL via POST request
        try:
            #  params as json
            response = requests.post(
                f"{self.base_url}/login", json_params, verify=False
            )
            print("\nAttempting to login...")
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        
        # Return request response: status code, output and user eosb
        return get_response_values(response)

    # [POST] /refresh-token
    def get_basic_user_info(self, access_token):
        """
        Get basic user information from Sail Api portal

        :return: response, response.json()
        :rtype: (string, string)
        """
        request_headers = {
            "Authorization": f"Bearer {access_token}"
            }
        
        # Attempt to get basic user information
        try:
            #  params as json
            response = requests.get(
                f"{self.base_url}/me", verify=False, headers=request_headers
            )
            print("\nAttempting to get basic user info...")
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        
        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    # [GET] /me
    def get_refresh_token(self, refresh_token):
        """
        Refresh access token for Sail Api portal

        :return response, response.json()
        :rtype: (string, string)
        """

        request_headers = {
            "refresh_token": refresh_token
        }

        # Attempt to get new access token using the refresh token
        try:
            #  params as json
            response = requests.post(
                f"{self.base_url}/refresh-token", json=request_headers, verify=False
            )
            print("\nAttempting to get refresh token...")
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    # [GET] /organizations
    def get_all_organizations(self, access_token):
        """
        Get all organizations from Sail Api portal

        :return: response, response.json()
        :rtype: (string, string)
        """
        request_headers = {
            "Authorization": f"Bearer {access_token}"
            }
        
        # Attempt to get all organizations
        try:
            #  params as json
            response = requests.get(
                f"{self.base_url}/organizations", verify=False, headers=request_headers
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    # [GET] /organizations/{organization_id}
    def get_organization_by_id(self, access_token, org_id):
        """
        Get update user password from  Sail Api portal

        :param current_password:
        :type current_password: string
        :param new_password:
        :type new_password: string
        :return: response, response.json()
        :rtype: (string, string)
        """
        request_headers = {
            "Authorization": f"Bearer {access_token}"
        }

        # Attempt to get an organization by ID
        try:
            #  params as json
            response = requests.get(
                f"{self.base_url}/organizations/{org_id}", verify=False, headers=request_headers
            )
            print("\nAttempting to get organization by ID...")
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")
        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    # [POST] /organizations
    def register_new_organization(self, access_token, new_name, new_description, new_avatar, new_admin_name, new_admin_job_title, new_admin_email, new_admin_password, new_admin_avatar):
        """
        Register a new organization using the Sail Api portal.

        :return: response, response.json()
        :rtype: (string, string)
        """
        request_headers = {
            "Authorization": f"Bearer {access_token}"
        }

        json_params = {
            "name": new_name,
            "description": new_description,
            "avatar": new_avatar,
            "admin_name": new_admin_name,
            "admin_job_title": new_admin_job_title,
            "admin_email": new_admin_email,
            "admin_password": new_admin_password,
            "admin_avatar": new_admin_avatar,
        }
        
        # Attempt to register a new organization
        try:
            #  params as json
            response = requests.post(
                f"{self.base_url}/organizations", verify=False, headers=request_headers, json=json_params
            )
            print("\nAttempting to register a new organization...")
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    # [PUT] /organizations/{organization_id}
    def update_organization_info(self, access_token, org_id, new_name, new_description, new_avatar):
        """
        Register a new organization using the Sail Api portal.

        :return: response, response.json()
        :rtype: (string, string)
        """
        request_headers = {
            "Authorization": f"Bearer {access_token}"
        }

        json_params = {
            "name": new_name,
            "description": new_description,
            "avatar": new_avatar,
        }
        
        # Attempt to update organization info
        try:
            #  params as json
            response = requests.put(
                f"{self.base_url}/organizations/{org_id}", verify=False, headers=request_headers, json=json_params
            )
            print("\nAttempting to update organization info...")
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    # TODO: Verify organization is deleted
    # [DELETE] /organizations/{organization_id}
    def delete_organization(self, access_token, org_id):
        """
        Delete an organization using the Sail Api portal.

        :return: response, response.json()
        :rtype: (string, string)
        """
        request_headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        # Attempt to delete an organization
        try:
            #  params as json
            response = requests.delete(
                f"{self.base_url}/organizations/{org_id}", verify=False, headers=request_headers
            )
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    # [GET] /organizations/{organization_id}/users
    def get_organization_users(self, access_token, org_id):
        """
        Get users of an organization using the Sail Api portal.

        :return: response, response.json()
        :rtype: (string, string)
        """
        request_headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        # Attempt to get an organizations users
        try:
            #  params as json
            response = requests.get(
                f"{self.base_url}/organizations/{org_id}/users", verify=False, headers=request_headers
            )
            print("\nAttempting to get organization users...")
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    # [POST] /organizations/{organization_id}/users/{user_id}
    def register_new_user_to_organization(self, access_token, org_id, user_name, user_email, user_job_title, user_role, user_avatar, user_password):
        """
        Get users of an organization using the Sail Api portal.

        :return: response, response.json()
        :rtype: (string, string)
        """
        request_headers = {
            "Authorization": f"Bearer {access_token}"
        }

        json_params = {
            "name": user_name,
            "email": user_email,
            "job_title": user_job_title,
            "role": user_role,
            "avatar": user_avatar,
            "password": user_password,
        }

        
        # Attempt to register a new user to the organization
        try:
            #  params as json
            response = requests.post(
                f"{self.base_url}/organizations/{org_id}/users", verify=False, headers=request_headers, json=json_params
            )
            print("\nAttempting to register new user to organization...")
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    # [GET] /organizations/{organization_id}/users/{user_id}
    def get_organization_user_by_id(self, access_token, org_id, user_id):
        """
        Get user of an organization by ID using the Sail Api portal.

        :return: response, response.json()
        :rtype: (string, string)
        """
        request_headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        # Attempt to get organization user by ID
        try:
            #  params as json
            response = requests.get(
                f"{self.base_url}/organizations/{org_id}/users/{user_id}", verify=False, headers=request_headers
            )
            print("\nAttempting to get organization user by ID...")
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    # [PUT] /organizations/{organizations_id}/users/{user_id}
    def update_organization_user(self, access_token, org_id, user_id, new_job_title, new_role, new_account_state, new_avatar):
        """
        Update user of an organization by ID using the Sail Api portal.

        :return: response, response.json()
        :rtype: (string, string)
        """
        request_headers = {
            "Authorization": f"Bearer {access_token}"
        }

        json_params = {
            "job_title": new_job_title,
            "role": new_role,
            "account_state": new_account_state,
            "avatar": new_avatar,
        }
        
        # Attempt to update organization user info
        try:
            #  params as json
            response = requests.put(
                f"{self.base_url}/organizations/{org_id}/users/{user_id}", verify=False, headers=request_headers, json=json_params
            )
            print("\nAttempting to update organization user info...")
        except requests.exceptions.RequestException as error:
            print(f"\n{error}")

        # Return request response: status code, output, and user eosb
        return get_response_values(response)

    # TODO: Verify organization user is deleted
    # [DELETE] /organizations/{organizations_id}/users/{user_id}
    def delete_organization_user_by_id(self, access_token, org_id, user_id):
        """
        Delete an organization user using the Sail Api portal.

        :return: response, response.json()
        :rtype: (string, string)
        """
        request_headers = {
            "Authorization": f"Bearer {access_token}"
        }
        
        # Attempt to delete user from organization
        try:
            #  params as json
            response = requests.delete(
                f"{self.base_url}/organizations/{org_id}/users/{user_id}", verify=False, headers=request_headers
            )
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
