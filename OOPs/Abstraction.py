from abc import ABC, abstractmethod

class Notification(ABC):
    @abstractmethod
    def send_message(self, recipient: str):
        pass

class EmailNotification(Notification):
    def send_message(self, recipient):
        print(f"Sending email to {recipient}")

class SMSNotification(Notification):
    def send_message(self,recipient):
        print(f"Sending SMS to {recipient}")

class PushNotification(Notification):
    def send_message(self, recipient):
        print(f"Sending PUSH notification to {recipient}")

class Notifier:
    def __init__(self,notifier:Notification):
        self.notifier = notifier
    def send_notification(self,recipient):
        self.notifier.send_message(recipient)

#email
print("\n email\n")
email_notifier = Notifier(EmailNotification())
email_notifier.send_notification("user@example.com")

#sms
print("\n sms\n")
sms_notifier = Notifier(SMSNotification())
sms_notifier.send_notification("+1234567890")

#push
print("\n push \n")
push_notifier = Notifier(PushNotification())
push_notifier.send_notification("user123")