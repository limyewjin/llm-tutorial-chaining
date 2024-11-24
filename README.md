# Prompt Chaining Test

This is a simple test to demonstrate the effectiveness of prompt chaining across multiple LLMs. In this test, we ask models for the list of words ending in "tan", and then chain prompt the same models to self-reflect and improve the list. The framework compares how well different models can enhance their responses when given a chance to review and correct their initial output. Results are saved to CSV files for analysis, tracking both the initial response quality and the improvement achieved through chaining.


## Results

Running for the suffix -ab, and with the cheaper models for each (haiku, flash, mini), below are the results:

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
