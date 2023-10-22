import copy
import json

from tqdm import tqdm
from settings import Settings
import openai
from linkedin_parsing import parse_profile
from gpt_toolkit import *
import pandas as pd


def get_email_sequence_by_linked_in_profile(
    linkedin_url: str, settings: Settings, spendings_counter: dict
) -> Optional[dict]:
    parsed_profile = parse_profile(linkedin_url, settings, spendings_counter)
    print(json.dumps(parsed_profile, indent=4), "\n")
    summary = get_linkedin_profile_summary(parsed_profile, spendings_counter)
    print(summary, "\n")
    marketing_letters = get_marketing_letter(summary, spendings_counter)
    print(marketing_letters, "\n")
    json_packaged_marketing_letters = get_json_packaged_marketing_letters(
        marketing_letters, spendings_counter
    )
    if json_packaged_marketing_letters is None:
        return None
    print(json.dumps(json_packaged_marketing_letters, indent=4), "\n")
    return json_packaged_marketing_letters


def main():
    input_file_name = "leads_v0.csv"
    output_file_name = "leads_v1.csv"
    settings = Settings()
    openai.api_key = settings.OPENAI_API_TOKEN
    with open("spendings_counter.json", "r") as f:
        spendings_counter = json.load(f)
    df_v0 = pd.read_csv(input_file_name, index_col=0)
    df_v1 = pd.DataFrame(
        columns=df_v0.columns.tolist()
        + ["subject", "body", "follow_up_1", "follow_up_2"]
    )
    for _, row in tqdm(df_v0.iterrows(), len(df_v0)):
        result = get_email_sequence_by_linked_in_profile(
            row["linkedin_url"], settings, spendings_counter
        )
        if result is None:
            continue
        new_row = copy.deepcopy(row)
        new_row["subject"] = result["subject"]
        new_row["body"] = result["body"]
        new_row["follow_up_1"] = result["follow_up_1"]
        new_row["follow_up_2"] = result["follow_up_2"]
        df_v1 = df_v1._append(new_row)
    df_v1.to_csv(output_file_name, index=False)


if __name__ == "__main__":
    main()
