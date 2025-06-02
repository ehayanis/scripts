groups = []
if connect.entries and hasattr(connect.entries[0], 'memberOf'):
    for group_dn in connect.entries[0].memberOf.values:
        match = re.search(r'CN=([^,]+)', group_dn, re.IGNORECASE)
        if match:
            groups.append(match.group(1).upper())
