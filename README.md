# scripts


(&
  (memberof=CN=DL_CONFLUENCE,OU=CONFLUENCE,OU=DevOps,OU=Applications,OU=Groupes,O=CA)
  (!(memberof=CN=DL_CONFLUENCE_DISABLED,OU=CONFLUENCE,OU=DevOps,OU=Applications,OU=Groupes,O=CA))
)


SELECT u.user_name, u.display_name
FROM cwd_user u
WHERE u.active = 'T'
  AND NOT EXISTS (
    SELECT 1 FROM cwd_user_attribute a
    WHERE a.user_id = u.id AND a.attribute_name = 'lastAuthenticated'
  );


curl -u admin:your_password \
  -X PUT \
  -H "Content-Type: application/json" \
  -d '{"active": false}' \
  "https://your-confluence-url/rest/api/user?username=username_to_disable"
  



from ldap3 import Server, Connection, ALL, NTLM
import base64

# 🔧 AD connection settings
AD_SERVER = 'your.ad.domain.com'         # e.g. 'ldap://dc01.domain.local'
AD_USER = 'DOMAIN\\your_username'        # Format: DOMAIN\\username
AD_PASSWORD = 'your_password'
SEARCH_BASE = 'DC=domain,DC=com'         # Adjust based on your AD domain

# 🔍 List of SIDs to resolve
sids = [
    "S-1-5-21-309284222-728865996-3343784714-6488",
    "S-1-5-21-3584301268-2236452263-9056116576-17629",
    # Add more SIDs here
]

def sid_to_binary(sid_string):
    import win32security
    return win32security.ConvertStringSidToSid(sid_string)

def sid_to_base64(sid_string):
    # For use in LDAP filters (objectSid)
    import win32security
    binary_sid = win32security.ConvertStringSidToSid(sid_string)
    return binary_sid

# Connect to AD
server = Server(AD_SERVER, get_info=ALL)
conn = Connection(server, user=AD_USER, password=AD_PASSWORD, authentication=NTLM, auto_bind=True)

# Perform lookup
for sid in sids:
    try:
        binary_sid = sid_to_base64(sid)
        base64_sid = base64.b64encode(binary_sid).decode('utf-8')
        search_filter = f'(objectSid={binary_sid})'

        conn.search(
            search_base=SEARCH_BASE,
            search_filter=search_filter,
            attributes=['sAMAccountName', 'displayName', 'distinguishedName']
        )

        if conn.entries:
            for entry in conn.entries:
                print(f"{sid} => {entry.sAMAccountName} ({entry.displayName})")
        else:
            print(f"{sid} => No match found.")

    except Exception as e:
        print(f"Error resolving SID {sid}: {e}")

conn.unbind()




Body:

Dear [User First Name or Team],

We are reaching out to inform you that your current API key used with JFrog Artifactory is set to expire in 10 days, as part of JFrog's platform-wide deprecation of API keys.

To ensure uninterrupted access to Artifactory, you must transition to using Identity Tokens instead of API keys.

🔄 Why the change?
JFrog is deprecating API keys in favor of Identity Tokens, which offer improved security, manageability, and compliance with modern authentication standards.

🧭 What you need to do:
Please follow these simple steps to generate and use an Identity Token:

Log in to your JFrog account

Generate an Identity Token

Replace the API key usage in your tools/scripts

Detailed instructions can be found in this guide:
👉 How to Get an Identity Token in 3 Steps

⏳ Deadline:
Your current API key will expire on [Insert Date: 10 days from now].
Please complete the transition before this date to avoid disruptions.

If you have any questions or need assistance, feel free to reach out to [your support team/contact info].

Thank you for your attention to this important update.

Best regards,
[Your Name / Team Name]
[Organization or DevOps Team]

