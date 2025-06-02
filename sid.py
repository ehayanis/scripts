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

# Search for all users (or use a filter to reduce scope)
conn.search(
    search_base=SEARCH_BASE,
    search_filter='(objectClass=user)',
    attributes=['objectSid', 'sAMAccountName', 'displayName']
)

# Match SIDs
for entry in conn.entries:
    sid_bytes = entry.objectSid.value  # This is in bytes
    if sid_bytes in binary_sid_map:
        print(f"{binary_sid_map[sid_bytes]} => {entry.sAMAccountName} ({entry.displayName})")

conn.unbind()




def binary_sid_to_string(sid_bin):
    revision = sid_bin[0]
    sub_authority_count = sid_bin[1]
    identifier_authority = int.from_bytes(sid_bin[2:8], byteorder='big')
    sub_authorities = [struct.unpack('<I', sid_bin[8 + 4*i:12 + 4*i])[0] for i in range(sub_authority_count)]
    return f"S-{revision}-{identifier_authority}-" + '-'.join(str(sa) for sa in sub_authorities)


for entry in conn.entries:
    sid_bytes = entry.objectSid.value
    if sid_bytes:
        sid_str = binary_sid_to_string(sid_bytes)
        if sid_str in sids:
            print(f"{sid_str} => {entry.sAMAccountName} ({entry.displayName})")
