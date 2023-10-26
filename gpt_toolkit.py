import json
from typing import Optional
import openai


def add_spending(model: str, spendings_counter: dict) -> dict:
    spendings_counter["openai"][model]["requests count"] += 1
    spendings_counter["openai"][model]["money spent $"] += spendings_counter["openai"][
        model
    ]["price per request $"]


def autocomplete(
    prompt: str, spendings_counter: dict, model: str = "gpt-3.5-turbo"
) -> str:
    another_model = "gpt-4" if model == "gpt-3.5-turbo" else "gpt-3.5-turbo"
    try:
        completion = openai.ChatCompletion.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500,
            temperature=0.8,
        )
        add_spending(model, spendings_counter)
    except:
        completion = openai.ChatCompletion.create(
            model=another_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500,
            temperature=0.8,
        )
        add_spending(another_model, spendings_counter)
    return completion.choices[0].message.content


def get_linkedin_profile_summary(
    profile: Optional[dict], spendings_counter: dict
) -> Optional[str]:
    if profile is None:
        return None
    try:
        work_experience = ""
        for i, job in enumerate(profile["work"]):
            work_experience += f"Role {i+1}:{job}\n"
        education = ""
        for i, school in enumerate(profile["education"]):
            education += f"Education {i+1}:{school}\n"
        age = (
            f", Age: {profile['years']}"
            if profile.get("years", None) is not None
            else ""
        )
        prompt = f"""Here is a LinkedIn profile of a person. Please write a short summary of the career path of this person.
    Name: {profile['name']}{age}, Country: {profile['country']}
    Headline: {profile['headline']}
    Description: {profile['description']}
    Work experience from the latest to the earliest:
    {work_experience}
    Education from the latest to the earliest:
    {education}
    Write a short summary of this person's career path (ONLY 10 SENTENCES MAXIMUM), include notable and unusual facts about him/her, include detailed description of his/her development studio and DETERMINE THEIR INDUSTRY as narrowly as possible:
    """
        # print(prompt, "\n")
        return autocomplete(prompt, spendings_counter)
    except:
        print("Something went wrong with this profile", profile)
        return None


def get_marketing_letter(
    personal_summmary: Optional[str], spendings_counter: dict
) -> Optional[str]:
    if personal_summmary is None:
        return None
    try:
        prompt = f"""You're a THE BEST marketing and cold b2b outreach expert ON EARTH. Your task is to write an email letter promoting b2b lead generation service for software development company.
        REQUIREMENTS:
        - ALL EMAIL SHOULD BE HYPER PERSONALIZED
        - write a personalised subject line (HARD LIMIT 50 CHARACTERS) that stands out and makes the recipient want to open the email. use small letters to stand out
        - write a short email body (max 100 words) that makes the recipient want to reply
        - use AIDA framework (Attention, Interest, Desire, Action) to structure your email
        - in the beginning of email give a small, NOT FAKE, NOT CHEESY personal note to the recipient (DON'T SAY YOU LIKE THEIR WORK, OR THAT YOU'RE FOLLOWING THEM)
        - in the end of email say that if the recipient is interested in our offer, we can schedule a call
        - in the end write 'Kind regards, Oleg Melnikov | Evolva.ai'
        - don't mention evolva ai in the email body
        - don't use complex english words, keep in mind that the recipient may be a non-native english speaker
        - add new lines so it would be very easy to read, and text should look like mountain peaks - short sentences interspersed with long ones
        What exact services that you're selling:
        - booking meetings with qualified potential clients for software development companies
        - we use cold email for it, but we do it in a very personalized way using AI, that is our secret sauce, we stand out and can get a response from a potential client even if it's a big company and they get 100s of emails per day
        - we work on performance basis, so we charge only for actual meetings with qualified leads
        - we guarantee at the very least 5 meetings with qualified leads per month, otherwise you don't pay
        - there's no work on the client's side, we do everything ourselves
        Summary of the person that we're reaching out to and his/her company:
        {personal_summmary}
        Write an email letter according to the REQUIREMENTS above, also add TWO follow-up letters WITHOUT a subject line, make it short (HARD LIMIT 25 WORDS), BE CREATIVE and refer to their industry:"""
        # print(prompt, "\n")
        return autocomplete(prompt, spendings_counter, "gpt-4")
    except:
        print("Something went wrong with this profile", personal_summmary)
        return None


def get_json_packaged_marketing_letters(
    letters: Optional[str], spendings_counter: dict
) -> Optional[dict]:
    if letters is None:
        return None
    try:
        prompt = f"""Take given text and package it into a JSON file in the following format:
    {{
        "subject": "Subject line of the email",
        "body": "Hi Name, 
        ....
        ...",
        "follow_up_1": "First follow-up email
        ....",
        "follow_up_2": "Second follow-up email
        ..."
    }}
    Given text:
    {letters}
    JSON file:
    """
        # print(prompt, "\n")
        return json.loads(autocomplete(prompt, spendings_counter))
    except:
        print("Something went wrong with this profile", letters)
        return None
