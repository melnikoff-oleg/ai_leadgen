import json
from settings import Settings
import openai
from linkedin_parsing import parse_profile
from gpt_toolkit import get_linkedin_profile_summary, get_marketing_letter


def main():
    linkedin_url = "https://www.linkedin.com/in/yonas-khorsi/"  # https://www.linkedin.com/in/yonas-khorsi/ https://www.linkedin.com/in/pavel-fakanov/ https://www.linkedin.com/in/husnain-pasha-66158119b/ https://www.linkedin.com/in/fokinadaria/ https://www.linkedin.com/in/fritz-wierper-6933b6104/
    settings = Settings()
    openai.api_key = settings.OPENAI_API_TOKEN
    parsed_profile = parse_profile(linkedin_url, settings)
    print(json.dumps(parsed_profile, indent=4), "\n")
    summary = get_linkedin_profile_summary(parsed_profile)
    print(summary, "\n")
    marketing_letter = get_marketing_letter(summary)
    print(marketing_letter, "\n")


if __name__ == "__main__":
    main()
