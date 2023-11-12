import copy
import json
import os

from tqdm import tqdm
from settings import Settings
import openai
from linkedin_parsing import *
from gpt_toolkit import *
import pandas as pd


def get_email_sequence_by_linked_in_profile(
    profile_url: str, company_url: str, settings: Settings, spendings_counter: dict
) -> Optional[dict]:
    parsed_profile = parse_profile(profile_url, settings, spendings_counter)
    parsed_company = parse_company(company_url, settings, spendings_counter)
    print(json.dumps(parsed_profile, indent=4), "\n")
    print(json.dumps(parsed_company, indent=4), "\n")
    profile_summary = get_linkedin_profile_summary(parsed_profile, spendings_counter)
    print(profile_summary, "\n")
    company_summary = get_linkedin_company_summary(parsed_company, spendings_counter)
    print(company_summary, "\n")
    marketing_letters = get_marketing_letter(
        profile_summary, company_summary, spendings_counter
    )
    print(marketing_letters, "\n")
    json_packaged_marketing_letters = get_json_packaged_marketing_letters(
        marketing_letters, spendings_counter
    )
    if json_packaged_marketing_letters is None:
        return None
    print(json.dumps(json_packaged_marketing_letters, indent=4), "\n")
    return json_packaged_marketing_letters


def get_current_state(input_file_name):
    output_file_name = input_file_name + "_enriched.csv"
    input_file_name += ".csv"
    df_v0 = pd.read_csv(input_file_name)
    if os.path.exists(output_file_name):
        df_v1 = pd.read_csv(output_file_name)
    else:
        df_v1 = pd.DataFrame(
            columns=df_v0.columns.tolist()
            + ["subject", "body", "follow_up_1", "follow_up_2"]
        )
    if len(df_v1) > 0:
        for i, row in df_v0.iterrows():
            if row["Email"] == df_v1.iloc[-1]["Email"]:
                df_v0 = df_v0.iloc[i + 1 :]
                break
    with open("spendings_counter.json", "r") as f:
        spendings_counter = json.load(f)
    return df_v0, df_v1, spendings_counter


def save_current_state(input_file_name, df_v1, spendings_counter):
    output_file_name = input_file_name + "_enriched.csv"
    df_v1.to_csv(output_file_name, index=False)
    with open("spendings_counter.json", "w") as f:
        json.dump(spendings_counter, f, indent=4)


def main():
    input_file_name = "apollo-contacts-export"
    settings = Settings()
    openai.api_key = settings.OPENAI_API_TOKEN
    df_v0, df_v1, spendings_counter = get_current_state(input_file_name)
    for _, row in tqdm(df_v0.iterrows(), total=df_v0.shape[0]):
        result = get_email_sequence_by_linked_in_profile(
            row["Person Linkedin Url"],
            row["Company Linkedin Url"],
            settings,
            spendings_counter,
        )
        if result is None:
            continue
        new_row = copy.deepcopy(row)
        new_row["subject"] = result["subject"]
        new_row["body"] = result["body"]
        new_row["follow_up_1"] = result["follow_up_1"]
        new_row["follow_up_2"] = result["follow_up_2"]
        df_v1 = df_v1._append(new_row)
        save_current_state(input_file_name, df_v1, spendings_counter)


if __name__ == "__main__":
    main()
