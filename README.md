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




2025-06-17T10:48:31Z INF IsV2Project: Project cagip-secuv8-dev has APIVersion: ''
2025-06-17T10:48:31Z INF IsV2Project: Project cagip-secuv8-dev is v2: false
2025-06-17T10:48:32Z INF Creation of Repository cagip-secuv8-docker-scratch-intranet successful. service=artifactory
2025-06-17T10:48:32Z ERR Unable to retrieve CN from group :  service=artifactory
Technical error occured when looking at existing group:  GET https://registry-iso-prd.saas.cagip.group.gca/artifactory/api/security/groups: 406 [{Status:406 Message:Not Acceptable}]
2025-06-17T10:48:33Z INF Users cagip_secuv8_intranet_k8s_reader created service=artifactory
2025-06-17T10:48:33Z INF Password created and stored in Vault server for user cagip_secuv8_intranet_jenkins_writer service=artifactory
2025-06-17T10:48:34Z INF Users cagip_secuv8_intranet_jenkins_writer created service=artifactory
2025-06-17T10:48:39Z INF Permission cagip-secuv8-docker-allrepos-intranet-ro created, status code is 201 service=artifactory
2025-06-17T10:48:44Z ERR Technical Error occured during permission creation/update: 'PUT https://registry-iso-prd.saas.cagip.group.gca/artifactory/api/security/permissions/cagip-secuv8-docker-development-intranet-ro: 400 [{Status:400 Message:Group name cannot be empty}]' service=artifactory
2025-06-17T10:48:44Z INF Permission cagip-secuv8-docker-allrepos-intranet-rw created, status code is 201 service=artifactory
2025-06-17T10:48:49Z ERR Technical Error occured during permission creation/update: 'PUT https://registry-iso-prd.saas.cagip.group.gca/artifactory/api/security/permissions/cagip-secuv8-docker-development-intranet-rw: 400 [{Status:400 Message:Group name cannot be empty}]' service=artifactory
2025-06-17T10:48:49Z INF Creating docker config secret: project-registries for namespace: cagip-secuv8-dev service=imagepullsecrets


Best regards,
[Your Name / Team Name]
[Organization or DevOps Team]


2025-06-17T11:13:45Z INF IsV2Project: Project cagip-secuv11-dev has APIVersion: ''
2025-06-17T11:13:45Z INF IsV2Project: Project cagip-secuv11-dev identified as v2 based on missing stages
2025-06-17T11:13:45Z INF IsV2Project: Project cagip-secuv11-dev is v2: true
2025-06-17T11:13:45Z INF Calling external API for tenant: cagip, project: secuv11 service=externalapi
2025-06-17T11:13:45Z ERR API call failed with status: 404 service=externalapi
2025-06-17T11:13:45Z ERR Error calling external API for project cagip-secuv11-dev: API call failed with status: 404
2025-06-17T11:13:45Z ERR Couldn't read Project fields for project {cagip development secuv11  []  }: Spec.Stages empty. service=project
2025-06-17T11:13:45Z ERR Error handling project cagip-secuv11-dev: Spec.Stages empty.


2025-06-17T11:31:10Z INF IsV2Project: Project cagip-secuv12-dev has APIVersion: ''
2025-06-17T11:31:10Z INF IsV2Project: Project cagip-secuv12-dev identified as v2 based on missing stages
2025-06-17T11:31:10Z INF IsV2Project: Project cagip-secuv12-dev is v2: true
2025-06-17T11:31:10Z INF Calling external API for tenant: cagip, project: secuv12 service=externalapi
2025-06-17T11:31:10Z ERR API call failed with status: 404 service=externalapi
2025-06-17T11:31:10Z ERR Error calling external API for project cagip-secuv12-dev: API call failed with status: 404
2025-06-17T11:31:10Z INF IsV2Project: Project cagip-secuv12-dev has APIVersion: ''
2025-06-17T11:31:10Z INF IsV2Project: Project cagip-secuv12-dev identified as v2 based on missing stages
2025-06-17T11:31:10Z INF IsV2Project: Project cagip-secuv12-dev is v2: true
2025-06-17T11:31:10Z INF Setting default stages for v2 project cagip-secuv12-dev service=project
2025-06-17T11:31:10Z INF Creation of Repository cagip-secuv12-docker-stable-intranet successful. service=artifactory
2025-06-17T11:31:11Z ERR Unable to retrieve CN from group :  service=artifactory
Technical error occured when looking at existing group:  GET https://registry-iso-prd.saas.cagip.group.gca/artifactory/api/security/groups: 406 [{Status:406 Message:Not Acceptable}]
2025-06-17T11:31:11Z INF Users cagip_secuv12_intranet_k8s_reader created service=artifactory
2025-06-17T11:31:11Z INF Password created and stored in Vault server for user cagip_secuv12_intranet_jenkins_writer service=artifactory
2025-06-17T11:31:12Z INF Users cagip_secuv12_intranet_jenkins_writer created service=artifactory
2025-06-17T11:31:12Z INF Permission cagip-secuv12-docker-allrepos-intranet-ro created, status code is 201 service=artifactory
2025-06-17T11:31:22Z ERR Technical Error occured during permission creation/update: 'PUT https://registry-iso-prd.saas.cagip.group.gca/artifactory/api/security/permissions/cagip-secuv12-docker-development-intranet-ro: 400 [{Status:400 Message:Group name cannot be empty}]' service=artifactory
2025-06-17T11:31:22Z INF Creating docker config secret: project-registries for namespace: cagip-secuv12-dev service=imagepullsecrets


Objet : Accès aux catalogues d'entités dans PSSIT pour automatisation des souscriptions

Bonjour [Nom du destinataire],

Je viens de mettre à jour l’operator Kubernetes qui gère la création de dépôts dans Artifactory. Désormais, une v2 du CRD est disponible : elle ne crée plus directement les dépôts, mais déclenche une souscription à l’offre "Artifactory Repository" via l’API SOAPI.

L’objectif est d’orchestrer automatiquement cette souscription lorsque quelqu’un active l’offre "Kubernative Namespace". En résumé :
➡️ Une souscription à "Kubernative Namespace" entraîne automatiquement une souscription à "Artifactory Repository".

Cependant, j’ai rencontré une difficulté : dans PSSIT, les offres sont réparties en catalogues par entité (ex : CATS, DSIN, etc.).
Pour que la souscription à "Artifactory Repository" fonctionne correctement, il faut qu’elle se fasse dans le même catalogue que celui de la souscription "Kubernative Namespace".

Je cherche donc à savoir comment accéder à l’ensemble des catalogues d’entités via PSSIT ou un autre moyen, afin de :

Identifier dynamiquement dans quel catalogue se trouve la souscription initiale

Répliquer cette information pour déclencher la souscription à "Artifactory Repository" dans le bon contexte (même entité)







TASK [Pull OnlyOffice image] ***************************************************
task path: /runner/project/ff3.yml:33
<XXXX> ESTABLISH SSH CONNECTION FOR USER: YYY
<XXXX> SSH: EXEC sshpass -d12 ssh -C -o ControlMaster=auto -o ControlPersist=60s -o StrictHostKeyChecking=no -o 'User="YYY"' -o ConnectTimeout=10 -o 'ControlPath="/runner/cp/e7a8233fba"' XXXX '/bin/sh -c '"'"'echo ~YYY && sleep 0'"'"''
<XXXX> (0, b'/home/YYY\\n', b'')
<XXXX> ESTABLISH SSH CONNECTION FOR USER: YYY
<XXXX> SSH: EXEC sshpass -d12 ssh -C -o ControlMaster=auto -o ControlPersist=60s -o StrictHostKeyChecking=no -o 'User="YYY"' -o ConnectTimeout=10 -o 'ControlPath="/runner/cp/e7a8233fba"' XXXX '/bin/sh -c '"'"'( umask 77 && mkdir -p "` echo /var/tmp `"&& mkdir "` echo /var/tmp/ansible-tmp-1753796075.309591-47-53493719016930 `" && echo ansible-tmp-1753796075.309591-47-53493719016930="` echo /var/tmp/ansible-tmp-1753796075.309591-47-53493719016930 `" ) && sleep 0'"'"''
<XXXX> (0, b'ansible-tmp-1753796075.309591-47-53493719016930=/var/tmp/ansible-tmp-1753796075.309591-47-53493719016930\\n', b'')
Using module file /runner/requirements_collections/ansible_collections/containers/podman/plugins/modules/podman_image.py
<XXXX> PUT /runner/.ansible/tmp/ansible-local-17nimhziju/tmpaazvzah2 TO /var/tmp/ansible-tmp-1753796075.309591-47-53493719016930/AnsiballZ_podman_image.py
<XXXX> SSH: EXEC sshpass -d12 sftp -o BatchMode=no -b - -C -o ControlMaster=auto -o ControlPersist=60s -o StrictHostKeyChecking=no -o 'User="YYY"' -o ConnectTimeout=10 -o 'ControlPath="/runner/cp/e7a8233fba"' '[XXXX]'
<XXXX> (0, b'sftp> put /runner/.ansible/tmp/ansible-local-17nimhziju/tmpaazvzah2 /var/tmp/ansible-tmp-1753796075.309591-47-53493719016930/AnsiballZ_podman_image.py\\n', b'')
<XXXX> ESTABLISH SSH CONNECTION FOR USER: YYY
<XXXX> SSH: EXEC sshpass -d12 ssh -C -o ControlMaster=auto -o ControlPersist=60s -o StrictHostKeyChecking=no -o 'User="YYY"' -o ConnectTimeout=10 -o 'ControlPath="/runner/cp/e7a8233fba"' XXXX '/bin/sh -c '"'"'setfacl -m u:docker:r-x /var/tmp/ansible-tmp-1753796075.309591-47-53493719016930/ /var/tmp/ansible-tmp-1753796075.309591-47-53493719016930/AnsiballZ_podman_image.py && sleep 0'"'"''
<XXXX> (0, b'', b'')
<XXXX> ESTABLISH SSH CONNECTION FOR USER: YYY
<XXXX> SSH: EXEC sshpass -d12 ssh -C -o ControlMaster=auto -o ControlPersist=60s -o StrictHostKeyChecking=no -o 'User="YYY"' -o ConnectTimeout=10 -o 'ControlPath="/runner/cp/e7a8233fba"' -tt XXXX '/bin/sh -c '"'"'sudo -H -S -n  -u docker /bin/sh -c '"'"'"'"'"'"'"'"'echo BECOME-SUCCESS-zyjxoynvykglsfyvpvxxvdzwytgubtwg ; /usr/libexec/platform-python /var/tmp/ansible-tmp-1753796075.309591-47-53493719016930/AnsiballZ_podman_image.py'"'"'"'"'"'"'"'"' && sleep 0'"'"''
Escalation succeeded
<XXXX> (1, b'\\r\\n{"failed": true, "msg": "Failed to pull image silca-tools-docker-stable-intranet.registry.saas.cagip.group.gca/fakename:9.0", "invocation": {"module_args": {"name": "silca-tools-docker-stable-intranet.registry.saas.cagip.group.gca/fakename", "tag": "9.0", "pull": true, "push": false, "force": false, "state": "present", "executable": "podman", "build": {"force_rm": false, "format": "oci", "cache": true, "rm": true, "annotation": null, "file": null, "container_file": null, "volume": null, "extra_args": null, "target": null}, "push_args": {"compress": null, "format": null, "remove_signatures": null, "sign_by": null, "dest": null, "extra_args": null, "transport": null}, "arch": null, "pull_extra_args": null, "path": null, "validate_certs": null, "auth_file": null, "username": null, "password": null, "ca_cert_dir": null, "quadlet_dir": null, "quadlet_filename": null, "quadlet_file_mode": null, "quadlet_options": null}}}\\r\\n', b'Shared connection to XXXX closed.\\r\\n')
<XXXX> Failed to connect to the host via ssh: Shared connection to XXXX closed.
<XXXX> ESTABLISH SSH CONNECTION FOR USER: YYY
<XXXX> SSH: EXEC sshpass -d12 ssh -C -o ControlMaster=auto -o ControlPersist=60s -o StrictHostKeyChecking=no -o 'User="YYY"' -o ConnectTimeout=10 -o 'ControlPath="/runner/cp/e7a8233fba"' XXXX '/bin/sh -c '"'"'rm -f -r /var/tmp/ansible-tmp-1753796075.309591-47-53493719016930/ > /dev/null 2>&1 && sleep 0'"'"''
<XXXX> (0, b'', b'')
fatal: [XXXX]: FAILED! => {
    "changed": false,
    "invocation": {
        "module_args": {
            "arch": null,
            "auth_file": null,
            "build": {
                "annotation": null,
                "cache": true,
                "container_file": null,
                "extra_args": null,
                "file": null,
                "force_rm": false,
                "format": "oci",
                "rm": true,
                "target": null,
                "volume": null
            },
            "ca_cert_dir": null,
            "executable": "podman",
            "force": false,
            "name": "silca-tools-docker-stable-intranet.registry.saas.cagip.group.gca/fakename",
            "password": null,
            "path": null,
            "pull": true,
            "pull_extra_args": null,
            "push": false,
            "push_args": {
                "compress": null,
                "dest": null,
                "extra_args": null,
                "format": null,
                "remove_signatures": null,
                "sign_by": null,
                "transport": null
            },
            "quadlet_dir": null,
            "quadlet_file_mode": null,
            "quadlet_filename": null,
            "quadlet_options": null,
            "state": "present",
            "tag": "9.0",
            "username": null,
            "validate_certs": null
        }
    },
    "msg": "Failed to pull image silca-tools-docker-stable-intranet.registry.saas.cagip.group.gca/fakename:9.0"
}

PLAY RECAP *********************************************************************
XXXX : ok=2    changed=0    unreachable=0    failed=1    skipped=0    rescued=0    ignored=0   


Peux-tu m’indiquer s’il existe une API ou un mécanisme pour obtenir cette information ?
Ou éventuellement, à qui je pourrais m’adresser pour y accéder ?

Merci d’avance pour ton aide,
[Ta signature]
