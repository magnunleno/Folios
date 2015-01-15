#!/usr/bin/env python3
# encoding: utf-8


def proceed_yes_no(msg):
    while True:
        answer = input(msg + " (yes/no)? ")
        if answer in ('yes', 'no') or answer in ('y', 'n'):
            break
        print("Please answer 'yes' or 'no'.")
    return answer == 'yes'
