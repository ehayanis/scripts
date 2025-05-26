import pandas as pd
from ldap3 import Server, Connection, ALL
import requests
from datetime import datetime, timedelta
import yagmail

# === CONFIGURATION ===

CSV_FILE = 'users.csv'

# LDAP
LDAP_SERVER = 'ldap://your-ad-server.com'
LDAP_USER = 'your_bind_user@domain.com'
LDAP_PASSWORD = 'your_password'
LDAP_SEARCH_BASE = 'DC=your,DC=domain,DC=com'

# JFrog
JFROG_BASE_URL = 'https://your-jfrog-domain/artifactory'
JFROG_API_USER = 'your_jfrog_user'
JFROG_API_PASSWORD = 'your_jfrog_password'

# Email
EMAIL_SENDER = 'your_email@example.com'
EMAIL_PASSWORD = 'your_email_password'  # or use app password
EMAIL_SUBJECT = 'Active JFrog User Alert'
EMAIL_BODY_TEMPLATE = """Hello {username},

Your account is still active in JFrog and was recently used (last login: {last_login}).

Regards,
Admin Team
"""

# === FUNCTIONS ===

def check_user_in_ldap(username):
    server = Server(LDAP_SERVER, get_info=ALL)
    conn = Connection(server, LDAP_USER, LDAP_PASSWORD, auto_bind=True)
    search_filter = f'(|(uid={username})(cn={username})(mail={username}))'
    conn.search(LDAP_SEARCH_BASE, search_filter, attributes=['cn'])
    return len(conn.entries) > 0

def get_jfrog_last_login(username):
    url = f'{JFROG_BASE_URL}/api/security/users/{username}'
    response = requests.get(url, auth=(JFROG_API_USER, JFROG_API_PASSWORD))
    if response.status_code == 200:
        data = response.json()
        last_login = data.get('lastLoggedIn')
        if last_login:
            return datetime.fromtimestamp(last_login / 1000)  # JFrog uses milliseconds
    return None

def disable_jfrog_user(username):
    url = f'{JFROG_BASE_URL}/api/security/users/{username}'
    payload = {'disabled': True}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, auth=(JFROG_API_USER, JFROG_API_PASSWORD), json=payload, headers=headers)
    return response.status_code in (200, 204)

def send_email_notification(to_email, username, last_login):
    yag = yagmail.SMTP(EMAIL_SENDER, EMAIL_PASSWORD)
    body = EMAIL_BODY_TEMPLATE.format(username=username, last_login=last_login.strftime('%Y-%m-%d'))
    yag.send(to=to_email, subject=EMAIL_SUBJECT, contents=body)
    print(f"Email sent to {to_email} for user {username}.")

# === MAIN ===

def main():
    df = pd.read_csv(CSV_FILE)
    one_year_ago = datetime.now() - timedelta(days=365)

    for _, row in df.iterrows():
        username = row['username']
        email = row['email']

        print(f'Checking {username} ({email})...')

        if check_user_in_ldap(username):
            last_login = get_jfrog_last_login(username)
            if last_login:
                if last_login > one_year_ago:
                    print(f'User {username} is active, last login {last_login}. Sending email.')
                    send_email_notification(email, username, last_login)
                else:
                    print(f'User {username} last logged in over a year ago.')
            else:
                print(f'User {username} has no recorded login.')
        else:
            print(f'User {username} not found in AD. Disabling in JFrog...')
            if disable_jfrog_user(username):
                print(f'User {username} disabled successfully.')
            else:
                print(f'Failed to disable user {username}.')

if __name__ == '__main__':
    main()
