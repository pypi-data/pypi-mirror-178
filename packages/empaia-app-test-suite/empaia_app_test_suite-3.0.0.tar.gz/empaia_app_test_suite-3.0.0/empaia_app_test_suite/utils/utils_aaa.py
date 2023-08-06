from datetime import datetime

import requests

from empaia_app_test_suite.constants import STATIC_ORGANIZATION_ID, STATIC_ORGANIZATION_KEYCLOAK_ID


def aaa_post_organization(aaa_url, data):
    url = f"{aaa_url}/api/custom-mock/organization"
    r = requests.post(url, json=data)
    return r


def generate_organization_json(name: str):
    now = str(datetime.now())
    data = {
        "organization_id": STATIC_ORGANIZATION_ID,
        "keycloak_id": STATIC_ORGANIZATION_KEYCLOAK_ID,
        "name": name,
        "normalized_name": name,
        "street_name": "string",
        "street_number": "string",
        "zip_code": "string",
        "place_name": "string",
        "country_code": "string",
        "department": "string",
        "email": "string",
        "phone_number": "string",
        "fax_number": "string",
        "website": "string",
        "picture": "https://upload.wikimedia.org/wikipedia/commons/c/ca/Microscope_icon_%28black_OCL%29.svg",
        "organization_role": "AI_VENDOR",
        "account_state": "ACTIVE",
        "date_created": now,
        "date_last_change": now,
        "contact_person_user_id": 0,
        "clientGroups": [
            {
                "client_group_id": 0,
                "group_organization_id": 0,
                "group_type": "AAA_SERVICE",
                "group_namespace": "string",
                "group_authorization_from": [
                    {"client_group_authorization_id": 0, "authorization_from": 0, "authorization_for": 0}
                ],
                "group_authorization_for": [
                    {"client_group_authorization_id": 0, "authorization_from": 0, "authorization_for": 0}
                ],
                "clients": [
                    {
                        "client_id": "string",
                        "name": "string",
                        "url": "string",
                        "group_id": 0,
                        "keycloak_id": "string",
                        "description": "string",
                        "token_lifetime_in_seconds": 0,
                        "redirect_uris": ["string"],
                    }
                ],
            }
        ],
        "solutions": [{"organization_id": 0, "solution_id": 0}],
        "user_count": 0,
    }
    return data
