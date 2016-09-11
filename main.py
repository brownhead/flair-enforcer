import datetime
import json
import logging
import os
import signal
import time

import atomicfile
import praw

import bot


def main(username, password, subreddit_name, recovery_file):
    # Log into reddit
    session = praw.Reddit(
        user_agent="nix:github.com/brownhead/flair-enforcer:v0 "
                   "(by /u/%s)" % username)
    session.login(username, password, disable_warning=True)

    # Set up super basic logging
    logging.basicConfig(level=logging.DEBUG)

    # Create an enforcer from the recovery file if possible, otherwise create
    # a fresh one.
    try:
        enforcer = bot.FlairEnforcer.from_json(
            session, subreddit_name,
            json.load(open(recovery_file, "rb")))
    except IOError:
        logging.info("Could not read from recovery file at %r. Continuing.",
                     recovery_file, exc_info=True)
        enforcer = bot.FlairEnforcer(session, subreddit_name)

    # Start handling the hangup signal
    def handle_hangup(signum, frame):
        logging.info("Hangup signal captured.")
        handle_hangup.hangup_captured = True

    signal.signal(signal.SIGHUP, handle_hangup)

    # Start enforcing!
    while not getattr(handle_hangup, "hangup_captured", False):
        try:
            enforcer.run_once(datetime.datetime.utcnow())
        except Exception:
            logging.exception("Exception occurred while running...")

        with atomicfile.AtomicFile(recovery_file, "wb") as f:
            f.write(enforcer.as_json())

        time.sleep(60)


if __name__ == "__main__":
    main(username=os.environ["FLAIR_ENFORCER_USERNAME"],
         password=os.environ["FLAIR_ENFORCER_PASSWORD"],
         subreddit_name=os.environ["FLAIR_ENFORCER_SUBREDDIT_NAME"],
         recovery_file=os.environ["FLAIR_ENFORCER_RECOVERY_FILE"])
