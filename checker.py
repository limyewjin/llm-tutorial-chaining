import api
import re

def check_wordlist(wordlist):
  response = api.ask_anthropic(f"""
You will be given a list of words that are supposed to end with "can". Your task is to identify and return a list of words from this list which are not real words or do not end with "can" in the English language.

Here is the list of words:
<word_list>
{wordlist}
</word_list>

Follow these steps to complete the task:

1. Process each word in the list.
2. For each word, determine if it is a real English word that ends with "can".
3. If a word is not a real English word or does not end with "can", include it in your output list.
4. If a word is a real English word and ends with "can", do not include it in your output list.
5. If a word is duplicate, only count it once and list it as a "fake word" in your output list labeled as "(duplicate)".

Provide your answer in the following format:
<fake_words>
- [Word 1]
- [Word 2]
- ...
</fake_words>

If all words in the list are real words ending with "can", output an empty tag:
<fake_words></fake_words>

Examples:
- "American" is a real word ending with "can", so it would not be included in the output list.
- "Fakecan" is not a real word (even though it ends with "can"), so it would be included in the output list.
- "Pelican" is a real word ending with "can", so it would not be included in the output list.
- "Canister" is a real word but doesn't end with "can", so it would be included in the output list.

Note: Be sure to consider case sensitivity. Treat words as case-insensitive when determining if they are real words or if they end with "can".

Process the given list and provide your output as instructed.
""".strip(),
    model='claude-3-5-sonnet-latest')  # Use the better sonnet model for testing

  fake_words = re.search(r'<fake_words>(.*?)</fake_words>', response, re.DOTALL).group(1).strip()
  fake_wordlist = fake_words.split('\n')
  print(f'Number of fake words found: {len(fake_wordlist)}')
  print(fake_words)

  return len(fake_wordlist)
