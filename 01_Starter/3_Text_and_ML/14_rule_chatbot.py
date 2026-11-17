"""
14 - A chatbot WITHOUT AI (rules only)
--------------------------------------
This chatbot only knows the keywords we give it.
Compare it with project 15 and CampusBot (04_CampusBot), which use a real AI model:
  - here: fast, predictable, but it understands NOTHING outside its rules
  - with an AI model: understands any sentence, but can make things up

Run:  python 14_rule_chatbot.py      (type "bye" to quit)
Try:  ask "what is your name?" and then "how are you called?" - why does only one work?
"""

import random

# keyword -> possible answers
RULES = {
    "hello": ["Hello!", "Hi there!"],
    "name": ["I'm RuleBot, a very simple chatbot."],
    "python": ["Python is a programming language, named after Monty Python!"],
    "weather": ["I can't see outside, sorry!"],
    "joke": ["Why do programmers prefer dark mode? Because light attracts bugs."],
}

print("RuleBot: Hello! Type 'bye' to quit.")
while True:
    message = input("You: ").lower()
    if "bye" in message:
        print("RuleBot: Goodbye!")
        break
    for keyword, answers in RULES.items():
        if keyword in message:                    # the first keyword found wins
            print("RuleBot:", random.choice(answers))
            break
    else:                                         # "for ... else": runs if no 'break' happened
        print("RuleBot: Sorry, I don't understand.")
