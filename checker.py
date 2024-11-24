import api
import re

SUFFIX = "tan"

def check_wordlist(wordlist):
  response = api.ask_anthropic(f"""
You will be given a list of words that are supposed to end with "{SUFFIX}". Your task is to identify and return a list of words from this list which are not real words or do not end with "{SUFFIX}" in the English language.

Here is the list of words:
<word_list>
{wordlist}
</word_list>

Follow these steps to complete the task:

1. Process each word in the list.
2. For each word, determine if it is a real English word that ends with "{SUFFIX}".
3. If a word is not a real English word or does not end with "{SUFFIX}", include it in your output list.
4. If a word is a real English word and ends with "{SUFFIX}", do not include it in your output list.
5. If a word is duplicate, only count it once and list it as a "fake word" in your output list labeled as "(duplicate)".
6. Do some thinking for each word by separating the last three letters from each word and reflect if it's "{SUFFIX}". (Example using "ing": "singing" -> "sing-ing")
7. Note that if "{SUFFIX}" is a real English word then the word "{SUFFIX}" itself is allowed.

Provide your answer in the following format:
<thinking>
1. Word 1 -> prefix-suffix
2. Word 2 -> prefix-suffix
...
</thinking>
<fake_words>
- [Word 1]
- [Word 2]
- ...
</fake_words>

If all words in the list are real words ending with "{SUFFIX}", output an empty tag:
<fake_words></fake_words>

Examples using "can" as a suffix:
<examples>
- "American" is a real word ending with "can", so it would not be included in the output list.
- "Fakecan" is not a real word (even though it ends with "can"), so it would be included in the output list.
- "Pelican" is a real word ending with "can", so it would not be included in the output list.
- "Canister" is a real word but doesn't end with "can", so it would be included in the output list.
</examples>

Note: Be sure to consider case sensitivity. Treat words as case-insensitive when determining if they are real words or if they end with "{SUFFIX}".

Process the given list and provide your output as instructed.
""".strip(),
    model='claude-3-5-sonnet-latest')  # Use the better sonnet model for testing
  print(f"Checker response:\n{response}")

  fake_words = re.search(r'<fake_words>(.*?)</fake_words>', response, re.DOTALL).group(1).strip()
  fake_wordlist = [word.strip() for word in fake_words.split('\n') if word.strip() != ""]
  print(f'==>Number of fake words found: {len(fake_wordlist)}')

  return len(fake_wordlist)
