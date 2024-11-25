"""
This module checks a wordlist for correctly and incorrectly spelled words using an external API.
"""

import re
import api

SUFFIX = "ab"


def check_wordlist(wordlist):
    """
    Processes a given word list to identify correctly and incorrectly spelled words.

    The function performs the following steps:
    1. Extracts the word list from the input string using a regular expression.
    2. Sends the extracted word list to an external API for spelling check.
    3. Parses the API response to separate correctly and incorrectly spelled words.
    4. Identifies duplicate words in the correctly spelled words list.
    5. Combines the incorrectly spelled words with the duplicates from the correctly
       spelled words list.
    6. Generates a final list of incorrect words, including words that do not end with
       a specified suffix.
    7. Prints the number of incorrect words found and returns this count.

    Args:
      wordlist (str): A string containing the word list to be checked.

    Returns:
      int: The number of incorrect words found in the word list.
    """
    output_wordlist = (
        re.search(r"<output>(.*?)</output>", wordlist, re.DOTALL).group(1).strip()
    )
    response = api.ask_anthropic(
        f"""
You will be given a list of words and your task is:
  - Identify and return the list of correctly and incorrectly spelled words in the final
    list of words provided (if multiple were given)
  - Duplicate words should be repeated like in the original list given
  - Allow compound words if writing it as a single word is known
  - Do not be concerned about any other pattern in the words

Here is the list of words:
<word_list>
{output_wordlist}
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

If the correct or incorrect list is empty, just return the empty tag
(i.e., <correct></correct> or <incorrect></incorrect>)

Process the given list and provide your output as instructed.
""".strip(),
        model="claude-3-5-sonnet-latest",
    )  # Use the better sonnet model for testing
    print(f"Checker response:\n{response}")

    correct = re.search(r"<correct>(.*?)</correct>", response, re.DOTALL)
    correct_words = []
    if correct:
        correct_words = [
            word.strip()
            for word in correct.group(1).strip().split("\n")
            if word.strip() != ""
        ]

    incorrect = re.search(r"<incorrect>(.*?)</incorrect>", response, re.DOTALL)
    incorrect_words = []
    if incorrect:
        incorrect_words = [
            word.strip()
            for word in incorrect.group(1).strip().split("\n")
            if word.strip() != ""
        ]

    seen = set()
    duplicates = []
    for word in correct_words:
        if word in seen:
            duplicates.append(word)
        seen.add(word)
    updated_incorrect_words = incorrect_words + duplicates

    incorrect_list = [
        word for word in set(correct_words) if not word.lower().endswith(SUFFIX.lower())
    ] + updated_incorrect_words
    print(f"==>Number of incorrect words found: {len(incorrect_list)}")

    return len(incorrect_list)
