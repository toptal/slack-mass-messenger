# Slack Mass Messenger
Allows the user to send personalized message to multiple Slack users so it appears on Slack as sent by the user themselves.
  
    
    
### Requirements:
- Python3
- Requests (`pip3 install requests`)
  
    
    
### Setup
- Clone this repository somewhere on your disk `git clone git@github.com:toptal/slack-mass-messenger.git`
  
    
    
### Sending messages
- Enter the directory you have cloned this repo into
- Edit `message_slack_users.emails` and `message_slack_users.message` (more info about that available in app's native help)
- Run `python3 message_slack_users -t AUTH_TOKEN`
  
    
    
### Getting more help
- Run `python3 message_slack_users.py` - running without parameters will display inbuilt help message
- Contact: Michał Kujawski on Toptal Core
