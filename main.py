import json
from settings import Settings
import openai
from linkedin_parsing import parse_profile
from gpt_toolkit import *
import pandas as pd


def main():
    linkedin_url = "https://www.linkedin.com/in/ivan-pavlovich-363216219/"  # https://www.linkedin.com/in/ivan-pavlovich-363216219/ https://www.linkedin.com/in/yonas-khorsi/ https://www.linkedin.com/in/pavel-fakanov/ https://www.linkedin.com/in/husnain-pasha-66158119b/ https://www.linkedin.com/in/fokinadaria/ https://www.linkedin.com/in/fritz-wierper-6933b6104/
    settings = Settings()
    openai.api_key = settings.OPENAI_API_TOKEN
    parsed_profile = parse_profile(linkedin_url, settings)
    print(json.dumps(parsed_profile, indent=4), "\n")
    summary = get_linkedin_profile_summary(parsed_profile)
    print(summary, "\n")
    marketing_letters = get_marketing_letter(summary)
    print(marketing_letters, "\n")
    json_packaged_marketing_letters = get_json_packaged_marketing_letters(
        marketing_letters
    )
    print(json.dumps(json_packaged_marketing_letters, indent=4), "\n")
    df = pd.DataFrame([json_packaged_marketing_letters])
    df.to_csv("result.csv")


if __name__ == "__main__":
    main()
