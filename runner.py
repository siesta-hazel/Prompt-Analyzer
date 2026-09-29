import os
import json
from dotenv import load_dotenv
from groq import Groq
from evaluator import EvaluationResult, JUDGE_SYSTEM_PROMPT

load_dotenv()

client = Groq()

DEFAULT_MODEL = "openai/gpt-oss-120b"

def execute_prompt(system_prompt: str, user_input: str) -> str:
    """Executes the candidate prompt on Groq."""
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ],
        max_tokens=300
    )
    return response.choices[0].message.content

def run_single_eval(user_input: str, system_prompt: str, candidate_output: str) -> EvaluationResult:
    """Evaluates output quality using Groq with structured JSON output."""
    judge_input = f"USER INPUT: {user_input}\n\nCANDIDATE OUTPUT: {candidate_output}"
    
    response = client.chat.completions.create(
        model=DEFAULT_MODEL,
        messages=[
            {"role": "system", "content": JUDGE_SYSTEM_PROMPT + "\nOutput MUST be raw JSON adhering strictly to the schema."},
            {"role": "user", "content": judge_input}
        ],
        response_format={"type": "json_object"}
    )
    
    raw_json = response.choices[0].message.content
    parsed_data = json.loads(raw_json)
    return EvaluationResult(**parsed_data)