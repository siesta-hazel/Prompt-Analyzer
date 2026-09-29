from pydantic import BaseModel, Field

class EvaluationResult(BaseModel):
    chain_of_thought: str = Field(
        ..., 
        description="Step-by-step reasoning behind why these scores were assigned."
    )
    accuracy_score: int = Field(
        ..., 
        description="Score from 1 to 5 based on factual correctness and accuracy."
    )
    relevance_score: int = Field(
        ..., 
        description="Score from 1 to 5 based on how directly it addresses the user prompt."
    )
    formatting_score: int = Field(
        ..., 
        description="Score from 1 to 5 based on compliance with requested formatting."
    )
    final_verdict: str = Field(
        ..., 
        description="A concise summary verdict of the candidate response quality."
    )

JUDGE_SYSTEM_PROMPT = """
You are an expert AI Benchmark Judge. Evaluate the candidate output against the original user input.
Assign numerical scores from 1 to 5 for Accuracy, Relevance, and Formatting Compliance.

CRITICAL INSTRUCTIONS:
1. First, explain your step-by-step reasoning inside the 'chain_of_thought' field.
2. Return ONLY a valid JSON object strictly matching this schema:
{
  "chain_of_thought": "string",
  "accuracy_score": integer,
  "relevance_score": integer,
  "formatting_score": integer,
  "final_verdict": "string"
}
"""