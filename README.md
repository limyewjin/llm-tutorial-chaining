# Prompt Chaining Test

This is a simple test to demonstrate the effectiveness of prompt chaining across multiple LLMs. In this test, we ask models for the list of words ending in "can", and then chain prompt the same models to self-reflect and improve the list. The framework compares how well different models can enhance their responses when given a chance to review and correct their initial output. Results are saved to CSV files for analysis, tracking both the initial response quality and the improvement achieved through chaining.

## Requirements

Python 3.x
Access to Gemini, Anthropic, and OpenAI APIs
Required Python packages: datetime, csv, statistics, typing

## Note

Ensure you have proper API credentials configured in your environment before running the tests.
