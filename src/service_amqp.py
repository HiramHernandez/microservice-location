import smtplib, ssl
from email.message import EmailMessage
from nameko.rpc import rpc, RpcProxy


class Mail():
    name = "mail"

    @rpc
    def send(self, to, subject, contents):
        mail_user = 'schiram_9@hotmail.com'
        mail_password = 'mxB3rl1n'

        msg = EmailMessage()
        msg.set_content(contents)
        msg["Subject"] = subject
        msg["From"] = mail_user
        msg["To"] = to
       
        context=ssl.create_default_context()

        try:
            with smtplib.SMTP("smtp-mail.outlook.com", port=587) as smtp:
                smtp.starttls(context=context)
                smtp.login(mail_user, mail_password)
                smtp.send_message(msg)
            print ("Email sent successfully!")
        except Exception as ex:
            print ("Something went wrong….",ex)

class Compute():
    name = "compute"
    mail = RpcProxy('mail')
    @rpc
    def compute(self, operation, value, other, email):
        operations = {'sum': lambda x, y: int(x) + int(y),
                      'mul': lambda x, y: int(x) * int(y),
                      'div': lambda x, y: int(x) / int(y),
                      'sub': lambda x, y: int(x) - int(y)}
        try:
            result = operations[operation](value, other)
        except Exception as e:
            self.mail.send.call_async(email, "An error occurred", str(e))
            raise
        else:
            self.mail.send.call_async(
                email, 
                "Your operation is complete!", 
                "The result is: %s" % result
            )
            return result

    