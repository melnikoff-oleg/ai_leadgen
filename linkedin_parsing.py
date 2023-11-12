from datetime import datetime
from typing import Optional
import requests
from settings import Settings


def get_profile(
    profile_url: str, settings: Settings, spendings_counter: dict
) -> Optional[dict]:
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    header_dic = {"Authorization": "Bearer " + settings.PROXYCURL_API_TOKEN}
    params = {
        "url": profile_url,
        # "extra": "include",
        # "github_profile_id": "include",
        # "facebook_profile_id": "include",
        # "twitter_profile_id": "include",
        # "personal_contact_number": "include",
        # "personal_email": "include",
        # "inferred_salary": "include",
        # "skills": "include",
        "use_cache": "if-recent",
        "fallback_to_cache": "on-error",
    }
    spendings_counter["proxycurl"]["requests count"] += 1
    spendings_counter["proxycurl"]["money spent $"] += spendings_counter["proxycurl"][
        "price per request $"
    ]
    try:
        response = requests.get(api_endpoint, params=params, headers=header_dic).json()
        return response
    except Exception as e:
        print("Something went wrong with this profile", profile_url, "Error:\n", e)
        return None


def get_company(
    company_url: str, settings: Settings, spendings_counter: dict
) -> Optional[dict]:
    api_endpoint = "https://nubela.co/proxycurl/api/linkedin/company"
    header_dict = {"Authorization": "Bearer " + settings.PROXYCURL_API_TOKEN}
    params = {
        "url": company_url,
        "use_cache": "if-recent",
        "fallback_to_cache": "on-error",
    }
    spendings_counter["proxycurl"]["requests count"] += 1
    spendings_counter["proxycurl"]["money spent $"] += spendings_counter["proxycurl"][
        "price per request $"
    ]
    try:
        response = requests.get(api_endpoint, params=params, headers=header_dict).json()
        return response
    except Exception as e:
        print("Something went wrong with this company", company_url, "Error:\n", e)
        return None


def parse_profile(
    profile_url: str, settings: Settings, spendings_counter: dict
) -> Optional[dict]:
    try:
        response = get_profile(profile_url, settings, spendings_counter)
        if response is None:
            return None
        res = dict()
        res["name"] = response.get("full_name", None)
        res["headline"] = response.get("headline", None)
        res["description"] = response.get("summary", None)
        res["work"] = []
        for i in range(min(2, len(response["experiences"]))):
            q = response["experiences"][i]
            for el in q:
                if q[el] is None:
                    q[el] = "None"
            res["work"] += [
                f"Company: {q['company']}, Role: {q['title']}, Description: {q['description']}"
            ]
        return res
    except Exception as e:
        print(
            "Something went wrong with this profile",
            profile_url,
            "Error:\n",
            e,
            "\nResponse:\n",
            response,
        )
        return None


def parse_company(
    company_url: str, settings: Settings, spendings_counter: dict
) -> Optional[dict]:
    try:
        response = get_company(company_url, settings, spendings_counter)
        if response is None:
            return None
        res = dict()
        res["name"] = response.get("name", None)
        res["headline"] = response.get("tagline", None)
        res["description"] = response.get("description", None)
        return res
    except Exception as e:
        print(
            "Something went wrong with this company",
            company_url,
            "Error:\n",
            e,
            "\nResponse:\n",
            response,
        )
        return None
