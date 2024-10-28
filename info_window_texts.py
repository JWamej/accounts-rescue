tutorial_data = (""
                 "Setup\n"
                 "    1.    In the 'Get Passwords' window, click the 'First Use' button.\n"
                 "    2.    Click the 'Copy key' button.\n"
                 "    3.    Paste the copied data in a safe place.\n"
                 "    4.    Click the 'Copy vector' button.\n"
                 "    5.    Paste the copied data in a safe place.\n"
                 "    6.    Click the 'Select directory' button.\n"
                 "    6.1. Browse directories and select the one where you want the source file to be stored.\n"
                 "    7.    Click 'Confirm' and complete the configuration.\n\n"

                 "Accessing the file\n"
                 "    1.    In the 'Get Passwords' window, paste the key (from Setup 2./3.) into the 'Encryption Key' entry.\n"
                 "    2.    Paste the initialization vector (from Setup 4./5.) into the 'Initialization Vector' entry.\n"
                 "    3.    Click the 'Select file' button.\n"
                 "    3.1. Browse directories and files, and pick the source file (from Setup 6.1.).\n"
                 "    4.    Click the 'Confirm' button.\n\n"

                 "Add account\n"
                 "    1.    In the 'Display' window, click the 'Add E-Mail' button.\n"
                 "    2.    In the 'Add E-Mail' window, fill in the 'E-Mail' and 'Password' fields (both must be filled).\n"
                 "    3.    Click the 'Confirm' button (the new account should appear in the 'Display' window).\n"
                 "    4.    You can then add more emails in the same way or close the 'Add E-Mail' window by clicking the 'Exit' button.\n\n"

                 "Delete account\n"
                 "    1.    In the 'Display' window, click the 'Delete E-Mail' button.\n"
                 "    2.    In the 'Delete E-Mail' window, select an account to delete from the list (only emails are shown).\n"
                 "    3.    Click the 'Delete' button and confirm your choice.\n"
                 "    4.    You can then delete more emails in the same way or close the 'Delete E-Mail' window by clicking the 'Exit' button.\n")



data_handling = (""
                 "How to store the source file, key, and IV?\n"
                 "	The main principle behind this project was to create an application designed to store login credentials for accounts that the user cannot afford to lose. To ensure the complete safety of the necessary data, follow these recommendations:\n"
                 "		1. Store the key and IV on a drive that is entirely disconnected from the main computer (e.g., a dedicated USB drive) and/or in physical form (e.g., a notebook).\n"
                 "		2. Create backups of the source file on separate drives (in case of drive failure) and/or on external drives (in case of ransomware attacks).\n")



faq = (""
       "Is it possible to recover login credentials without the key or IV?\n"
       "    No. The source file is completely encrypted, so unless the AES-256 encryption is compromised, the data is impossible to restore.\n\n"

       "Does using this application ensure security against attacks?\n"
       "    No system can be made completely impenetrable. Not even the best antivirus software or the most expensive password manager can protect against critical user errors.\n\n"

       "Does this application have any anti-keylogger functionality?\n"
       "    The application can only prevent direct access to unencrypted login credentials. It remains vulnerable to spyware attacks.\n\n")

dosdonts = (""
            "Dos and Don'ts:\n"
            "   - Do keep backups of the source file on different, unrelated drives.\n"
            "   - Do store the key and IV on secure drives and/or in physical form.\n"
            "   - Use this application to store accounts that do not require frequent access—there are better alternatives for frequent use.\n"
            "   - Never store the key and IV in the same location as the source file and application.\n")
