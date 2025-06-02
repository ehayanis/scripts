def get_user_groups_via_tokenGroups(connect, username: str, search_base: str):
    # Step 1: Find the user by sAMAccountName (you can adjust to use UPN if needed)
    user_filter = f'(sAMAccountName={username})'
    if not connect.search(
        search_base=search_base,
        search_filter=user_filter,
        search_scope='SUBTREE',
        attributes=['tokenGroups']
    ) or not connect.entries:
        raise HTTPException(status_code=404, detail=f"User '{username}' not found in LDAP")

    user_entry = connect.entries[0]
    
    # Step 2: Extract binary SIDs from tokenGroups
    try:
        sids = user_entry['tokenGroups'].raw_values
    except KeyError:
        raise HTTPException(status_code=403, detail="User has no group information (tokenGroups not available)")

    groups = []
    
    # Step 3: Resolve each SID to CN
    for sid in sids:
        if connect.search(
            search_base=search_base,
            search_filter=f'(objectSid={sid})',
            search_scope='SUBTREE',
            attributes=['cn']
        ) and connect.entries:
            cn = connect.entries[0]['cn'].value
            groups.append(cn.upper())

    if not groups:
        raise HTTPException(status_code=403, detail="User has no resolved groups")

    return groups
