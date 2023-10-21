import json
import openai


def autocomplete(prompt: str) -> str:
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.8,
        )
    except:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.8,
        )
    return completion.choices[0].message.content


def get_linkedin_profile_summary(profile: dict) -> str:
    work_experience = ""
    for i, job in enumerate(profile["work"]):
        work_experience += f"Role {i+1}:{job}\n"
    # education = ""
    # for i, school in enumerate(profile["education"]):
    #     education += f"Education {i+1}:{school}\n"
    # Education from the latest to the earliest:
    # {education}
    age = f", Age: {profile['years']}" if profile.get("years", None) is not None else ""
    prompt = f"""Here is a LinkedIn profile of a person. Please write a short summary of the career path of this person.
Name: {profile['name']}{age}, Country: {profile['country']}
Headline: {profile['headline']}
Description: {profile['description']}
Work experience from the latest to the earliest:
{work_experience}
Write a short summary of this person's career path (ONLY 7 SENTENCES MAXIMUM), include notable and unusual facts about him/her. Mention details on his/her development studio:
"""
    print(prompt, "\n")
    return autocomplete(prompt)


def get_marketing_letter(personal_summmary: str) -> str:
    prompt = f"""You're a professional marketing and cold b2b outreach expert. Your task is to write an email letter promoting b2b lead generation service for software development company.
    REQUIREMENTS:
    - write a personalised subject line (max 50 characters) that stands out and makes the recipient want to open the email. use small letters to stand out. assume familiarity with the recipient
    - write a short email body (max 100 words) that makes the recipient want to reply
    - use AIDA framework (Attention, Interest, Desire, Action) to structure your email
    - in the beginning of email give a small compliment to recipient, don't be lame
    - in the end if email say that if the recipient is interested in our offer, we can schedule a call
    - in the end write 'Kind regards, Oleg Melnikov | www.evolva.ai'
    - don't mention evolva ai in the email body
    What exact services that you're selling:
    - booking meetings with qualified potential clients for software development companies
    - we use cold email for it, but we do it in a very personalized way
    - we work on performance basis, so we charge only for actual meetings with qualified leads
    - we guarantee at the vert least 5 meetings with qualified leads per month, otherwise you don't pay
    - there's no work on the client's side, we do everything ourselves
    Summary of the person that we're reaching out to and his/her company:
    {personal_summmary}
    Write an email letter according to the REQUIREMENTS above, also add TWO follow-up letters WITHOUT a subject line, address a pain point there and mention a call again:"""
    print(prompt, "\n")
    return autocomplete(prompt)


def get_json_packaged_marketing_letters(letters: str) -> dict:
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
    print(prompt, "\n")
    return json.loads(autocomplete(prompt))