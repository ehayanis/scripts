from ldap3 import Server, Connection, ALL, NTLM
import struct
import base64

# 🛠️ AD Settings
AD_SERVER = 'ldap://your.ad.server'        # e.g., ldap://dc01.domain.local
AD_USER = 'DOMAIN\\your_username'          # NTLM format
AD_PASSWORD = 'your_password'
SEARCH_BASE = 'DC=your,DC=domain,DC=com'   # Set to your domain DN

# 🔍 List of SIDs to resolve
sids = [
    "S-1-5-21-309284222-728865996-3343784714-6488",
    "S-1-5-21-3584301268-2236452263-9056116576-17629",
    # Add more as needed
]

# Convert SID string to binary
def sid_string_to_binary(sid_str):
    parts = sid_str.strip().split('-')
    revision = int(parts[1])
    sub_authorities = list(map(int, parts[3:]))
    identifier_authority = int(parts[2])

    sid_bin = struct.pack('B', revision) + struct.pack('B', len(sub_authorities))
    sid_bin += struct.pack('>Q', identifier_authority)[2:]
    for sub_auth in sub_authorities:
        sid_bin += struct.pack('<I', sub_auth)

    return sid_bin

# Create a lookup of binary SID → SID string
binary_sid_map = {sid_string_to_binary(sid): sid for sid in sids}

# Connect
server = Server(AD_SERVER, get_info=ALL)
conn = Connection(server, user=AD_USER, password=AD_PASSWORD, authentication=NTLM, auto_bind=True)

entries = conn.extend.standard.paged_search(
    search_base=SEARCH_BASE,
    search_filter='(&(objectClass=user)(objectCategory=person))',
    search_scope=SUBTREE,
    attributes=['sAMAccountName', 'displayName', 'objectSid'],
    paged_size=1000,
    generator=False  # return as list
)

# 🔄 Match by SID
for entry in entries:
    attr = entry.get('attributes', {})
    sid = attr.get('objectSid')
    if sid in sids:
        print(f"{sid} => {attr.get('sAMAccountName')} ({attr.get('displayName')})")
conn.unbind()


ef get_user_sid_by_id(ad_server, ad_user, ad_password, search_base, user_id):
    """
    Lookup a user's SID from Active Directory using their sAMAccountName.

    :param ad_server: LDAP server URI (e.g. 'ldap://dc01.domain.local')
    :param ad_user: AD bind user in 'DOMAIN\\username' format
    :param ad_password: Password for AD user
    :param search_base: LDAP search base (e.g. 'DC=your,DC=domain,DC=com')
    :param user_id: The sAMAccountName (username) to search for
    :return: Dictionary with user info if found, else None
    """
    try:
        server = Server(ad_server, get_info=ALL)
        conn = Connection(server, user=ad_user, password=ad_password, authentication=NTLM, auto_bind=True)

        search_filter = f'(sAMAccountName={user_id})'

        conn.search(
            search_base=search_base,
            search_filter=search_filter,
            attributes=['sAMAccountName', 'objectSid', 'displayName']
        )

        if conn.entries:
            entry = conn.entries[0]
            result = {
                "sAMAccountName": str(entry.sAMAccountName),
                "displayName": str(entry.displayName),
                "objectSid": str(entry.objectSid)
            }
            conn.unbind()
            return result
        else:
            conn.unbind()
            print(f"No user found with ID '{user_id}'")
            return None

    except Exception as e:
        print(f"Error during LDAP lookup: {e}")
        return None
