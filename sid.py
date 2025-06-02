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

# 🔄 Convert SID string to binary (works on Linux)
def sid_string_to_binary(sid_str):
    parts = sid_str.strip().split('-')
    revision = int(parts[1])
    sub_authorities = list(map(int, parts[3:]))
    identifier_authority = int(parts[2])

    # SID header: revision (1 byte) + count (1 byte)
    sid_bin = struct.pack('B', revision) + struct.pack('B', len(sub_authorities))

    # Identifier Authority is 6 bytes, big-endian
    sid_bin += struct.pack('>Q', identifier_authority)[2:]

    # Each sub-authority is 4 bytes, little-endian
    for sub_auth in sub_authorities:
        sid_bin += struct.pack('<I', sub_auth)

    return sid_bin

# 🔌 Connect to LDAP
server = Server(AD_SERVER, get_info=ALL)
conn = Connection(server, user=AD_USER, password=AD_PASSWORD, authentication=NTLM, auto_bind=True)

# 🔍 Search each SID
for sid in sids:
    try:
        binary_sid = sid_string_to_binary(sid)
        # Encode for LDAP filter: base64 format
        b64_sid = base64.b64encode(binary_sid).decode('utf-8')
        search_filter = f'(objectSid:: {b64_sid})'

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
