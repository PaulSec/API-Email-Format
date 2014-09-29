from emailFormatAPI import EmailFormatAPI
res = EmailFormatAPI({'verbose': True}).get('sensepost.com')
print res  # retrieves the results
res = EmailFormatAPI().get('companydoesnotexist')
print res  # does not exist
