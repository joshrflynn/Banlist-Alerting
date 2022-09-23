import time
import hashlib
from urllib.request import urlopen, Request
from util.etext import send_sms_via_email
from util.users import USERS

SENDER_CREDENTIALS=("banlistalerting@outlook.com", "wktbrrsvbrimkhqz")
 
# set url
#url = Request('https://www.yugioh-card.com/en/limited/', headers={'User-Agent': 'Mozilla/5.0'})
url = Request('https://www.yugioh-card.com/en/limited', headers={'User-Agent': 'Mozilla/5.0'})
# initial load of the page and hashing
response = urlopen(url).read()
currentHash = hashlib.sha224(response).hexdigest()

print("Initial load successful.")

while True:
    try:

        # load the page and create the new hash
        response = urlopen(url).read()
        newHash = hashlib.sha224(response).hexdigest()
        
        # compare hashes
        if newHash == currentHash:
            print("No change detected.")
            continue
 
        else:
            # notify
            print("A change has been detected. Alerting users.")
            currentHash = newHash

            message="Yugioh Ban List site change"
            
            for user in USERS:
                print(user["phone"])
                send_sms_via_email(user["phone"], message, user["provider"], SENDER_CREDENTIALS, subject="Ban List Alert", name=user["name"])

        # wait 5 minutes to check again
        time.sleep(300)

        
    # To handle exceptions
    except Exception as e:
        print(e)
