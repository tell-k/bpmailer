"""
Email backend that writes messages to console instead of sending them.
"""
import sys
import threading

from mailer.backends.base import BaseEmailBackend

class EmailBackend(BaseEmailBackend):
    def __init__(self, *args, **kwargs):
        self.stream = kwargs.pop('stream', sys.stdout)
        self._lock = threading.RLock()
        super(EmailBackend, self).__init__(*args, **kwargs)

    def send_messages(self, email_messages):
        """Write all messages to the stream in a thread-safe way."""
        from mailer.signals import mail_pre_send, mail_post_send

        if not email_messages:
            return
        self._lock.acquire()
        try:
            # The try-except is nested to allow for
            # Python 2.4 support (Refs #12147)
            try:
                stream_created = self.open()
                for message in email_messages:
                    mail_pre_send.send(sender=message, message=message)
                    self.stream.write('%s\n' % message.message().as_string())
                    self.stream.write('-'*79)
                    self.stream.write('\n')
                    self.stream.flush()  # flush after each message
                    mail_post_send.send(sender=message, message=message)
                if stream_created:
                    self.close()
            except:
                if not self.fail_silently:
                    raise
        finally:
            self._lock.release()
        return len(email_messages)
