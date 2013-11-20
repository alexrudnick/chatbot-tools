#!/usr/bin/env python3

import random
import re
import readline
import sys

"""
Python version of ELIZA for b490 NLP at Indiana University!

Based on Peter Norvig's Common Lisp version, available here:
http://www.norvig.com/paip/README.html
"""

ELIZA_RULES = [
    [r".*\bhello\b.*",
     "How do you do.  Please state your problem."],
    [r".*\bI remember (.*)\b",
     "Do you often think of {0}",
     "Does thinking of {0} bring anything else to mind?",
     "What else do you remember",
     "Why do you recall {0} right now?",
     "What in the present situation reminds you of {0}",
     "What is the connection between me and {0}"],
    [r".*\bcomputer\b.*",
     "Do computers worry you?",
     "What do you think about machines?",
     "Why do you mention computers?",
     "What do you think machines have to do with your problem?"],
    [r".*\bname\b.*",
     "I am not interested in names"],
    [r".*\bsorry\b.*",
     "Please don't apologize",
     "Apologies are not necessary",
     "What feelings do you have when you apologize"],
    [r".*\b[Dd]o you remember (.*)\b",
     "Did you think I would forget {0}?",
     "Why do you think I should recall {0} now",
     "What about {0}",
     "You mentioned {0}"],
    [r".*\b[Ii]f (.*)", 
     "Do you really think its likely that {0}",
     "Do you wish that {0}",
     "What do you think about {0}",
     "Really-- if {0}"],
    [r".*\bI dreamt (.*)\b",
     "Really-- {0}",
     "Have you ever fantasized {0} while you were awake?",
     "Have you dreamt {0} before?"],
    [r".* dream about (.*)\b",
     "How do you feel about {0} in reality?"],
    [r".* dream\b.*",    
     "What does this dream suggest to you?",
     "Do you dream often?",
     "What persons appear in your dreams?",
     "Don't you believe that dream has to do with your problem?"],
    [r".*\b[Mm]y mother (.*)\b.*",
     "Who else in your family {0}?",
     "Tell me more about your family"],
    [r".*\b[Mm]y father\b.*",
     "Your father",
     "Does he influence you strongly?",
     "What else comes to mind when you think of your father?"],
    [r".*\bI (.*) you\b.*",
     "Perhaps in your fantasy we {0} each other"],
    [".*",
     "Very interesting",
     "I am not sure I understand you fully",
     "What does that suggest to you?",
     "Please continue",
     "Go on",
     "Do you feel strongly about discussing such things?",
     "oic"]
]

def switch_viewpoint(text):
    """Change I to you and vice versa, and so on."""
    ## TODO(you): Implement this and make sure it gets called in
    ## response_for_rule.
    ## The Common Lisp version looks like:
    ## (sublis '((I . you) (you . I) (me . you) (am . are)) words))
    ## ... if that helps.
    return text

def response_for_rule(text, rule):
    """Given some text, input by the user, and an Eliza rule, see whether the
    text matches the rule. If it does, pick a template from the rule and
    substitute the appropriate text into it. Otherwise return None."""
    try:
        match = re.match(rule[0], text)
    except:
        print("probably error in pattern:", rule[0])
        sys.exit(1)
        
    if not match: return None
    template = random.choice(rule[1:])
    matched_strings = match.groups()

    return template.format(*matched_strings)

def eliza_response(text):
    """Find a rule that matches this text, return an appropriate (?)
    response."""
    for rule in ELIZA_RULES:
        response = response_for_rule(text, rule)
        if response:
            return response

def main():
    print("Hello, how can I help you?")

    ## Eliza main loop!
    while True:
        try:
            user_input = input("> ")
            response = eliza_response(user_input)
            print(response)
        except:
            print()
            break

if __name__ == "__main__": main()
