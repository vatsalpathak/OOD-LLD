class MessageBuilder:
    def build_message(self,count):
        return f"Dear Alice, you have {count} unread messages."

class EmailSender:
    def send_email(self,message):
        print(message)

msg = MessageBuilder()
message = msg.build_message(3)
email = EmailSender()
send_email = email.send_email(message=message)
