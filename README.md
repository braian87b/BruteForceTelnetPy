# BruteForceTelnetPy
Brute Force Telnet Login

TL;DR: Some time ago I had an ADSL Modem from Argentinean ISP Company (Telecom ARNET) Model: ADB DA 2210 or DA-2210, and I wanted to recover the telnet password, but in each try the telnet drops a pseudo Captcha made of chars on the screen... so... I writed an script to be able to recognize the digits and doing that be able to brute force the password... It worked just fine so I upload it here! 

Keywords: Recuperar contraseña telnet Modem ARNET ADB 2210

Usage:

    brute_force_telnet_login.py [host] [credentials-file]
    
Sample usage:

    brute_force_telnet_login.py 192.168.0.1 credentials.txt
    
credentials.txt may have pair of user/password or just a list of password (some devices just ask for a password only)
see sample_credentials_only_passwords.txt and sample_credentials_user_password.txt

Why I didn't use THC Hydra?

A basic pseudo OCR-like was implemented in order to bypass Verification code protection found on some device (ADB DA2210)

    ====================================================
       * * * *      *     *      * * * *      * * * *
       *            *     *            *            *
       * * * *      * * * *      * * * *            *
             *            *            *            *
             *            *            *            *
       * * * *            *      * * * *            *
    ====================================================

Digits must be entered just one time each, and will saved for later usage (this allow to diferent format of digits).
digit width may be modified (this one have 13 chars), and delimitation of '==\n' and '\n==' can also be modified.

This script is not intended to be a password cracker, nor any other criminal intention, the main purpose of this script is allow to recover a forgotten password using a password dictionary. (Mainly because of the slowlyness)

The scripts can detect if asked a username/password pair or just password.

A simple resume after process end was implementend (last_index.txt)

A valid output file (for persistence) was implemented (valid_credentials.txt)

Any modification is welcome.

Please if you need some modification and don't know how to do it, I can help, but enable "# tn.debuglevel = 10" and provide the output.

