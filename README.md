# Slack Mass Messenger
Provides possibility of messaging multiple Slack users at the same time while "pretending" to be the user that has authorized this process with his/her token.
  
  
    
### Requirements:
- `python3`
- `pip3`
  - In most cases it will be installed already but if not: https://pip.pypa.io/en/stable/installing/
- Requests library
  - Try `pip3 install requests`
  - If above failed `pip3 install --user requests` (do not run this in virtual environment)
  
    
    
### Permissions setup
- A Slack Admin needs to add you to an appropriate Slack application:
  - Toptal Core: https://api.slack.com/apps/A01504E0004
  - Toptal Community: https://api.slack.com/apps/ATENC9MCP

- Afterwards you need to retrieve your Slack authorization token from:
  - Toptal Core: https://api.slack.com/apps/A01504E0004/oauth
  - Toptal Community: https://api.slack.com/apps/ATENC9MCP/oauth

   **\* DO NOT SHARE THIS AUTHORIZATION TOKEN WITH ANYONE \***



### Local application setup
- Get the application in either of two ways:
  - Download and unpack ZIP file: https://github.com/toptal/slack-mass-messenger/archive/master.zip
  - Clone this repository somewhere on your disk `git clone git@github.com:toptal/slack-mass-messenger.git` 
  
  
    
### Usage
- Enter the directory you have extracted/cloned this application into
- Edit `message_slack_users.emails` and `message_slack_users.message` (See: `Getting more help` for more details)
- Run `python3 message_slack_users -t YOUR_AUTH_TOKEN_HERE`
  
    
    
### Getting more help
- Run `python3 message_slack_users.py` - running without parameters will display inbuilt help message
- Contact: Michał Kujawski on Toptal Core
