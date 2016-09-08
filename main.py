import datetime
import logging
import sys
import time

import praw

import bot


def main(username, password, subreddit_name):
    # Log into reddit
    session = praw.Reddit(
        user_agent="nix:github.com/brownhead/flair-enforcer:v0 "
                   "(by /u/%s)" % username)
    session.login(username, password, disable_warning=True)

    # Set up super basic logging
    logging.basicConfig(level=logging.DEBUG)

    # Start enforcing!
    enforcer = bot.FlairEnforcer(session, subreddit_name)
    while True:
        try:
            enforcer.run_once(datetime.datetime.utcnow())
        except Exception:
            logging.exception("Exception occurred while running...")

        time.sleep(60)


if __name__ == "__main__":
    main(username=sys.environ["FLAIR_ENFORCER_USERNAME"],
         password=sys.environ["FLAIR_ENFORCER_PASSWORD"],
         subreddit_name=sys.environ["FLAIR_ENFORCER_SUBREDDIT_NAME"])
