from settings import Settings
import openai
from linkedin_parsing import parse_profile
from gpt_toolkit import get_linkedin_profile_summary


def main():
    linkedin_url = "https://www.linkedin.com/in/pavel-fakanov/"  # https://www.linkedin.com/in/pavel-fakanov/ https://www.linkedin.com/in/husnain-pasha-66158119b/
    settings = Settings()
    openai.api_key = settings.OPENAI_API_TOKEN
    parsed_profile = parse_profile(linkedin_url, settings)
    summary = get_linkedin_profile_summary(parsed_profile)
    print(summary)


if __name__ == "__main__":
    main()
