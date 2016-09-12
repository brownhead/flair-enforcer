# Flair Enforcer

Forces users to flair their posts on Reddit.

## Getting, Installing, Running

```shell
# Grab a copy of the code
git clone https://github.com/brownhead/flair-enforcer.git
cd flair-enforcer

# Then install dependencies
virtualenv env
source env/bin/activate
pip install -r ./requirements.txt

# Let's us import properly without having to work for it
export PYTHONPATH="$(pwd)"

# Configure
export FLAIR_ENFORCER_USERNAME=yourusername
export FLAIR_ENFORCER_PASSWORD=yourpassword
export FLAIR_ENFORCER_SUBREDDIT_NAME=yoursubreddit
export FLAIR_ENFORCER_RECOVERY_FILE=somefilesomewhere.json

# Run!
python main.py
```

## Limitations

This'll only work for subreddits with pretty low volume. If your subreddit receives posts faster than 25 every 10 minutes, this bot will start choking. It'd be trivial to make it work for slightly higher loads (like up to 100 every 10 minutes) but any higher and a more drastic change to how the bot functions would need to be made.

This is a script born out of need, and isn't really meant to be reused by other people. But you're welcome to try to anyways.
