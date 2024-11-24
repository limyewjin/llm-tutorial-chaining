import api
import checker

response = api.ask_gemini(f'Name ten words as you can that end with "{checker.SUFFIX}". Return as a list with each word on a new line labeled by 1., 2., and so on.')

initial_list = response
print(f"Initial response:\n{initial_list}")
original_count = checker.check_wordlist(initial_list)

response = api.ask_gemini(f"""
Here are ten words that end with "{checker.SUFFIX}":
{initial_list}

Replace all words that do end with "{checker.SUFFIX}" or are not real words with real words that end with "{checker.SUFFIX}". Place your thinking in <thinking> tag.

Finally, return as a new list with only the replaced words (or original if correct) on a new line labeled by 1., 2., and so on.
""".strip())

chained_list = response
print(f"Chained response:\n{chained_list}")
chained_count = checker.check_wordlist(chained_list)
