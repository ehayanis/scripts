from ldap3 import Server, Connection, ALL, NTLM

# 🔧 AD Config
AD_SERVER = 'ldap://your.ad.server'
AD_USER = 'DOMAIN\\your_username'
AD_PASSWORD = 'your_password'
SEARCH_BASE = 'DC=your,DC=domain,DC=com'

# 🔍 The user ID you want to look up
user_id = 'jdoe'  # Replace with the actual sAMAccountName

# 🔌 Connect
server = Server(AD_SERVER, get_info=ALL)
conn = Connection(server, user=AD_USER, password=AD_PASSWORD, authentication=NTLM, auto_bind=True)

# 🔍 Search for the user
search_filter = f'(sAMAccountName={user_id})'

conn.search(
    search_base=SEARCH_BASE,
    search_filter=search_filter,
    attributes=['sAMAccountName', 'objectSid', 'displayName']
)

# 🔄 Output
if conn.entries:
    for entry in conn.entries:
        print(f"User: {entry.sAMAccountName} ({entry.displayName})")
        print(f"SID: {entry.objectSid}")
else:
    print(f"No user found with ID '{user_id}'")

conn.unbind()
