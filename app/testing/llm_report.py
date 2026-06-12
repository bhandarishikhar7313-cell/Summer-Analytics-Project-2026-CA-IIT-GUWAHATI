import json
import requests

from testing.business_predictor import (
    predict_business_profile
)

# OLLAMA SETTINGS
OLLAMA_URL = (
    "http://localhost:11434/api/generate"
)

MODEL_NAME = "qwen3:8b"

# PROMPT
def build_prompt(profile):

    prompt = f"""
You are a senior airline retention analyst.

Analyze this customer and provide a business-focused assessment.

Customer Segment:
{profile["cluster_name"]}

Segment Description:
{profile["profile_segment_description"]}

Model Confidence:
{profile["confidence"]}%

Customer Value:
{profile["customer_value"]}

Value Score:
{profile["value_score"]}

Priority:
{profile["priority"]}

Churn Probability:
{profile["churn_probability"]}

Future Flights:
{profile["future_flights"]}

Future Distance:
{profile["future_distance"]}

Future Points:
{profile["future_points"]}

Customer Lifetime Value:
{profile["clv"]}

Salary:
{profile["salary"]}

Loyalty Card:
{profile["loyalty_card"]}

Estimated Revenue Loss:
{profile["estimated_loss"]}

Recommended Actions:
{", ".join(profile["recommended_actions"])}

Generate ONLY valid JSON.

Format:

{{
    "executive_summary":"",
    "risk_analysis":"",
    "retention_strategy":"",
    "business_impact":"",
    "customer_message":"",
    "manager_recommendation":""
}}

Requirements:

- Explain WHY the customer received this risk level.
- Explain WHY the recommended actions were chosen.
- Mention customer value and future activity.
- Mention model confidence.
- Keep executive summary under 100 words.
- Keep customer message professional and friendly.
- Return valid JSON only.

No markdown.
No explanations.
No code blocks.
Return JSON only.
"""

    return prompt

# CALL OLLAMA
def generate_llm_report(profile):

    prompt = build_prompt(
        profile
    )

    payload = {

        "model": MODEL_NAME,

        "prompt": prompt,

        "stream": False,

        "options": {
            "temperature": 0.3
        }

    }

    print("\nGenerating LLM Analysis...")

    response = requests.post(

        OLLAMA_URL,

        json=payload,

        timeout=300

    )

    response.raise_for_status()

    result = response.json()

    text = result["response"]

    try:

        report = json.loads(
            text
        )

        print(
            "\nLLM JSON Parsed Successfully"
        )

        return report

    except Exception:

        print(
            "\nWARNING:"
            " JSON Parse Failed"
        )

        return {

            "raw_response":
            text

        }


# FULL PIPELINE
def run_pipeline(

    loyalty_number=None,

    csv_file=None,
    
    dataframe=None

):

    print("\n" + "=" * 60)

    print("RUNNING FULL PIPELINE")

    print("=" * 60)

    business_profile = (

        predict_business_profile(

            loyalty_number=loyalty_number,

            csv_file=csv_file,

            dataframe=dataframe

        )

    )

    llm_report = (

        generate_llm_report(

            business_profile

        )

    )

    final_output = {

        "business_profile":
        business_profile,

        "llm_analysis":
        llm_report

    }

    return final_output


# SAVE REPORT
def save_report(

    result,

    output_file="report.json"

):

    with open(

        output_file,

        "w",

        encoding="utf-8"

    ) as f:

        json.dump(

            result,

            f,

            indent=4,

            ensure_ascii=False

        )

    print(
        f"\nSaved Report:"
        f" {output_file}"
    )


# TEST
if __name__ == "__main__":

    result = run_pipeline(

        loyalty_number=100018

    )

    print("\n")

    print(
        json.dumps(

            result,

            indent=4,

            ensure_ascii=False

        )
    )

    save_report(

        result,

        "customer_report.json"

    )