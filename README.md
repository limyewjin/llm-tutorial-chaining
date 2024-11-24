# Prompt Chaining Test

This is a simple test to demonstrate the effectiveness of prompt chaining across multiple LLMs. In this test, we ask models for the list of words ending in "ab", and then chain prompt the same models to self-reflect and improve the list. The framework compares how well different models can enhance their responses when given a chance to review and correct their initial output. Results are saved to CSV files for analysis, tracking both the initial response quality and the improvement achieved through chaining.

## Results

Like any prompt engineering technique, results vary based on the task complexity and model capability. I tested this with base-tier models across OpenAI, Anthropic, and Google for the "simple" suffix -ab - while the improvement wasn't dramatic, the models were able to identify errors from their initial responses without introducing new ones during the chaining step.

Especially for the lower-tier models, asking for more complex suffices results in poor performance, and combined with poor instruction following - they often make this chained prompting worse! Always test your prompting strategies!

```
ANTHROPIC:
  count: 10
  avg_initial: 0
  avg_chained: 0
  avg_improvement: 0
  median_improvement: 0.00
  std_improvement: 0.00

GEMINI:
  count: 10
  avg_initial: 1.50
  avg_chained: 1.10
  avg_improvement: -0.40
  median_improvement: 0.00
  std_improvement: 0.52

OPENAI:
  count: 10
  avg_initial: 1
  avg_chained: 0.80
  avg_improvement: -0.20
  median_improvement: 0.00
  std_improvement: 0.42
```

## Requirements

- Python 3.x
- Access to Gemini, Anthropic, and OpenAI APIs
- Required Python packages: datetime, csv, statistics, typing

## Note

Ensure you have proper API credentials configured in your environment before running the tests.
