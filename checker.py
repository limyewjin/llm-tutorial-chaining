import api
import re

SUFFIX = "cat"

def check_wordlist(wordlist):
  response = api.ask_anthropic(f"""
You will be given a list of words and your task is to identify and return the list of correctly and incorrectly spelled words:

Here is the list of words:
<word_list>
{wordlist}
</word_list>

Return in the format:
<explanation>
[Explanation of choices]
</explanation>
<correct>
[correctly spelled word 1]
[correctly spelled word 2]
...
</correct>
<incorrect>
[incorrectly spelled word 1]
[incorrectly spelled word 2]
...
</incorrect>

Process the given list and provide your output as instructed.
""".strip(),
    model='claude-3-5-sonnet-latest')  # Use the better sonnet model for testing
  print(f"Checker response:\n{response}")

  correct = re.search(r'<correct>(.*?)</correct>', response, re.DOTALL).group(1).strip()
  correct_words = [word.strip() for word in correct.split('\n') if word.strip() != ""]
  incorrect = re.search(r'<incorrect>(.*?)</incorrect>', response, re.DOTALL).group(1).strip()
  incorrect_words = [word.strip() for word in incorrect.split('\n') if word.strip() != ""]

  incorrect_list = [word for word in correct_words if not word.lower().endswith(SUFFIX.lower())] + [incorrect_words]
  print(f'==>Number of incorrect words found: {len(incorrect_list)}')

  return len(incorrect_list)
