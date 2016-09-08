import datetime
import logging
import math


class FlairEnforcer(object):
    TIME_TO_INITIAL_WARNING = datetime.timedelta(minutes=3)
    TIME_TO_PERMANENT_REMOVAL = datetime.timedelta(minutes=10)

    WARNING_MESSAGE_TEMPLATE = {
        "subject": "You have not yet added flair to your post",
        "body":
            "[Your recent post]({post_url}) does not have any flair to "
            "designate its language. Please add flair to your post."
            "\n\n"
            "If you do not add flair to your post, it will be automatically "
            "removed in about {minutes_remaining} minutes, and you will have "
            "to resubmit."
    }

    REMOVAL_MESSAGE_TEMPLATE = {
        "subject": "Your post has been automatically removed",
        "body": 
            "[Your recent post]({post_url}) still does not have any flair to "
            "designate its language, so it has been automatically removed."
            "\n\n"
            "You are welcome to resubmit your post."
    }

    def __init__(self, session, subreddit_name):
        super(FlairEnforcer, self).__init__()
        self.session = session
        self.subreddit = session.get_subreddit(subreddit_name)

        self._warned_submission_ids = set()

    @staticmethod
    def has_flair(submission):
        """Return True iff submission is "flaired"."""
        return bool(submission.link_flair_css_class or
                    submission.link_flair_text)

    def get_unflaired_content(self):
        return (submission for submission in self.subreddit.get_new(limit=25)
                if not self.has_flair(submission))

    def run_once(self, utcnow):
        # Keep track of all of the unflaired posts we see so we can clean up
        # out list of warned submissions at the end.
        unflaired_ids = set()

        for submission in self.get_unflaired_content():
            unflaired_ids.add(submission.id)

            # Figure out the age of the submission
            created = datetime.datetime.utcfromtimestamp(
                submission.created_utc)
            lifespan = utcnow - created

            if lifespan > self.TIME_TO_PERMANENT_REMOVAL:
                logging.info("Removing submission at %s",
                             submission.short_link)

                submission.remove()

                self.session.send_message(
                    submission.author,
                    self.REMOVAL_MESSAGE_TEMPLATE["subject"],
                    self.REMOVAL_MESSAGE_TEMPLATE["body"].format(
                        post_url=submission.short_link))

                self._warned_submission_ids.discard(submission.id)
            elif (lifespan > self.TIME_TO_INITIAL_WARNING and
                    submission.id not in self._warned_submission_ids):
                logging.info("Sending warning for submission at %s",
                             submission.short_link)

                time_remaining = self.TIME_TO_PERMANENT_REMOVAL - lifespan
                self.session.send_message(
                    submission.author,
                    self.WARNING_MESSAGE_TEMPLATE["subject"],
                    self.WARNING_MESSAGE_TEMPLATE["body"].format(
                        post_url=submission.short_link,
                        minutes_remaining=time_remaining.seconds // 60))

                self._warned_submission_ids.add(submission.id)

        # Remove any flaired submissions from our list of warned submissions
        self._warned_submission_ids = (
            self._warned_submission_ids.intersection(unflaired_ids))
        logging.debug("Found %s unflaired submissions. (size of warned "
                      "submission IDs is %s)", len(unflaired_ids),
                      len(self._warned_submission_ids))
