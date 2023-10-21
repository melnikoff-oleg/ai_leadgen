import openai


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
Write a short summary of this person's career path (ONLY 7 SENTENCES MAXIMUM), include notable and unusual facts about him/her. Mention details on hir/her development studio:
"""
    print(prompt, "\n")
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.8,
        )
    except:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000,
            temperature=0.8,
        )
    summary = completion.choices[0].message.content
    return summary
