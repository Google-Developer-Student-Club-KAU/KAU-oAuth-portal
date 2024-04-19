import identity
import identity.web
import requests
from flask import session
import os


tenant = os.environ["AZURE_TENANT"]
client_id = os.environ["AZURE_CLIENT_ID"]
client_secret = os.environ["AZURE_CLIENT_SECRET"]


azure_auth = identity.web.Auth(
    session=session,
    authority=tenant,
    client_id=client_id,
    client_credential=client_secret,
)


# retreive user data https://graph.microsoft.com/v1.0/users/<user-id>?$select=accountEnabled,businessPhones,createdDateTime,department,displayName,mail,givenName,imAddresses,identities,surname,mailNickname,mobilePhone,id,onPremisesSamAccountName,onPremisesUserPrincipalName,preferredDataLocation,preferredLanguage,proxyAddresses,signInSessionsValidFromDateTime,usageLocation,userPrincipalName,userType
# search user by mail https://graph.microsoft.com/v1.0/users?$count=true&$search="mail:<user-mail>" \\ could add the $select too!
