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
        "extra": "include",
        "github_profile_id": "include",
        "facebook_profile_id": "include",
        "twitter_profile_id": "include",
        "personal_contact_number": "include",
        "personal_email": "include",
        "inferred_salary": "include",
        "skills": "include",
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
    except:
        print("Something went wrong with this profile", profile_url)
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
        res["country"] = response.get("country_full_name", None)
        res["work"] = []
        for i in range(min(2, len(response["experiences"]))):
            q = response["experiences"][i]
            for el in q:
                if q[el] is None:
                    q[el] = "None"
            res["work"] += [
                f"Company: {q['company']}, Role: {q['title']}, Description: {q['description']}"
            ]
        res["education"] = []
        for i in range(min(2, len(response["education"]))):
            q = response["education"][i]
            for el in q:
                if q[el] is None:
                    q[el] = "None"
            res["education"] += [
                f"School: {q['school']}, Field of study: {q['field_of_study']}, Description: {q['description']}"
            ]
        if len(response["skills"]) > 0:
            res["skills"] = ", ".join(response["skills"])
        if len(response["experiences"]) > 0:
            res["years"] = 20 + (
                datetime.now().year - response["experiences"][-1]["starts_at"]["year"]
            )
        return res
    except:
        print("Something went wrong with this profile", profile_url)
        return None
