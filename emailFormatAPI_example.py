from emailFormatAPI import EmailFormatAPI
res = EmailFormatAPI().get('google.com')
print res  # retrieves the results
res = EmailFormatAPI().get('companydoesnotexist')
print res  # does not exist
