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
pip install praw

# Let's us import properly without having to work for it
export PYTHONPATH="$(pwd)"

# Configure
export FLAIR_ENFORCER_USERNAME=yourusername
export FLAIR_ENFORCER_PASSWORD=yourpassword
export FLAIR_ENFORCER_SUBREDDIT_NAME=yoursubreddit

# Run!
python main.py
```
