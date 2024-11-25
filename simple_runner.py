
"""
This module interacts with the Gemini API to generate and validate a list of
words that end with a specified suffix. Demonstrates how to do chained
prompting by reusing the response from the initial prompt in a subsequent
prompt.
"""

import api
import checker

response = api.ask_gemini(f"""
Name ten Standard English words that end with "{checker.SUFFIX}".
Do not return uncommon words or spellings.
Return as a list with each word on a new line labeled by 1., 2.,
and so on in <output> tag.

Example with "ing":
<output>
1. singing
2. wing
...
</output>
""".strip())

initial_list = response
print(f"Initial response:\n{initial_list}")
original_count = checker.check_wordlist(initial_list)

response = api.ask_gemini(f"""
Check if each word in this list is a valid standard English word
ending in "{checker.SUFFIX}". For invalid or duplicate words,
replace with valid alternatives. Show your analysis by breaking
down each word's ending.

Input:
<wordlist>
{initial_list}
</wordlist>

<thinking>
Check each word -> [preceding letters]-[last {len(checker.SUFFIX)} letters]:
- Valid word + correct ending: keep
- Invalid word or wrong ending: replace
</thinking>

<output>
1. [final word]
2. [final word]
...
</output>

Example with "ing":
Input: [singing, fakking, wing]
<thinking>
- singing -> sing-ing: valid ✓
- stink -> st-ink: ink != ing, use "sting"
- fakking -> fakk-ing: not real, use "walking"
- wing -> w-ing: valid ✓
</thinking>

<output>
1. singing
2. sting
3. walking
4. wing
</output>
""".strip())

chained_list = response
print(f"Chained response:\n{chained_list}")
chained_count = checker.check_wordlist(chained_list)
