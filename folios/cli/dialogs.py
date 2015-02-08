#!/usr/bin/env python3
# encoding: utf-8


def proceed_yes_no(msg):
    while True:
        answer = input(msg + " (yes/no)? ")
        answer = answer.lower()
        if 'yes'.startswith(answer) or 'no'.startswith(answer):
            break
        print("Please answer 'yes' or 'no'.")
    return 'yes'.startswith(answer)
