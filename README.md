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
