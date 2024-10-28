tutorial_data = (""
                 "Setup\n"
                 "    1.    On the 'Get Passwords' window click the 'First Use' button.\n"
                 "    2.    Click 'Copy key' button.\n"
                 "    3.    Paste copied data into safe place.\n"
                 "    4.    Click 'Copy vector' button.\n"
                 "    5.    Paste copied data into safe place.\n"
                 "    6.    Click the 'Select directory' button.\n"
                 "    6.1. Browse directories and select the one, where you want the source file to be in.\n"
                 "    7.    Click 'Confirm' and then confirm the end of configuration.\n\n"

                 "Accessing the file\n"
                 "    1.    On the 'Get Passwords' window paste the key (from Setup 2./3.) into 'Encryption Key' entry.\n"
                 "    2.    Paste the initialization vector (from Setup 4./5.) into 'Initialization Vector' entry.\n"
                 "    3.    Click the 'Select file' button.\n"
                 "    3.1. Browse directories and files and pick the source file (from Setup 6.1.).\n"
                 "    4.    Click 'Confirm' button.\n\n"

                 "Add account\n"
                 "    1.    On the 'Display' window click 'Add E-Mail' button.\n"
                 "    2.    On the 'Add E-Mail' window fill the 'E-Mail' and 'Password' entries (none of them can be left empty).\n"
                 "    3.    Click 'Confirm' button (new account should appear on the 'Display' window).\n"
                 "    4.    After that you can add more e-mail in the same way or close the 'Add E-Mail' window by clicking 'Exit' button.\n\n"

                 "Delete account\n"
                 "    1.    On the 'Display' window click 'Delete E-Mail' button.\n"
                 "    2.    On the 'Delete E-Mail' window pick an account to delete from the list (list only shows the e-mails).\n"
                 "    3.    Click 'Delete' button and confirm your choice.\n"
                 "    4.    After that you can delete more e-mail in the same way or close the 'Delete E-Mail' window by clicking 'Exit' button.\n")

data_handling = (""
                 "How to go about storing the source file, key and iv?\n"
                 "	The main principle behind this project was to create an application designed to store login credentials to accounts, which the user cannot afford to lose. To ensure the complete safety of the necessary data, it is advised to follow these recommendations:\n"
                 "		1. Store the key and iv on the drive that is, in general, completely disconnected from the main computer (for example a dedicated pendrive) and/or in a physical for (for example in a notebook).\n"
                 "		2. Create backups of the source file on different drives (in case of drive corruption) and/or on external drives (in case of ransomware attack).\n")

faq = (""
       "Is it possible to recover the login credentials without key or iv?\n"
       "    No. The source file is completely encrypted, so until the SAE-256 compromised, the data is impossible to restore.\n\n"

       "Does usage of this application ensure that I am secure in case of attack?\n"
       "    It is impossible to create a system that is unpenetrable. Not even the best AV or most expensive password manager can fix critical user-error.\n\n"

       "Does this application have any anti-keylogger functionalities?\n"
       "    The application can only prevent direct access to the unencrypted login credentials. This means that it is vulnerable to spyware attacks.\n\n")

dosdonts = (""
            "Dos and don'ts:\n"
            "   - have backups of the source file on different, unrelated drives.\n"
            "   - store the key and iv on safe drives and/or in physical form.\n"
            "   - use this application for accounts you do not need to use regularly - there are better alternatives for that.\n"
            "   - never store the key and iv in the same place as the source file and application.\n")
