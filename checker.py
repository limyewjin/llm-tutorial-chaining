import api
import re

SUFFIX = "ten"

def check_wordlist(wordlist):
  response = api.ask_anthropic(f"""
You will be given a list of words and your task is to identify and return the list of words:

Here is the list of words:
<word_list>
{wordlist}
</word_list>

Return in the format:
<output>
[word 1]
[word 2]
[word 3]
...
</output>

Process the given list and provide your output as instructed.
""".strip(),
    model='claude-3-5-sonnet-latest')  # Use the better sonnet model for testing
  print(f"Checker response:\n{response}")

  output = re.search(r'<output>(.*?)</output>', response, re.DOTALL).group(1).strip()
  words = [word.strip() for word in output.split('\n') if word.strip() != ""]
  incorrect = [word for word in words if not word.endswith(SUFFIX)]
  print(f'==>Number of incorrect words found: {len(incorrect)}')

  return len(incorrect)
