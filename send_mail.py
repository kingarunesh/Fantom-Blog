from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


sender_email = "fantomblog.contact@gmail.com"
sender_email_password = "loggflqbakatmlhj"


# password reset mail
def send_reset_mail(receiver_email, url):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Reset Password"
    message["From"] = sender_email
    message["To"] = receiver_email

    #   HTML part
    html = f"""\
    <!DOCTYPE html>
    <html lang="en">
    <body style="background-color: rgb(247, 247, 247);">
        <div style="width: 80%;margin: auto;padding:1rem 0">
        <div style="background-color: white;padding: 1rem;border: 1px solid rgb(225, 225, 225);border-radius: 0.5rem;width: 50vh;margin: auto;margin-top: 1rem;">
            <div>
            Hi {name}, <br />A password reset for your account was requested.
            </div>
            <div>Please click the link below to change your password.</div>
            <div style="margin: 2rem 0;">
            <a href="{url}" style="background-color: black;padding: 1rem;color: white;font-size: 1.2rem;border-radius: 0.5rem;text-decoration: none;">Change Your Password </a>
            </div>
            <div>If you did not make this request, please ignore.</div>
        </div>
        </div>
    </body>
    </html>
    """
    # convert both parts to MIMEText objects and add them to the MIMEMultipart message
    send_data = MIMEText(html, "html")
    message.attach(send_data)

    with SMTP("smtp.gmail.com", port=587) as server:
        server.starttls()
        server.login(user=sender_email, password=sender_email_password)
        server.sendmail(
            from_addr=sender_email,
            to_addrs=receiver_email,
            msg=message.as_string()
        )


#   
def verification_admin(url):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Reset Password"
    message["From"] = sender_email
    message["To"] = sender_email

    #   HTML part
    html = f"""\
    <!DOCTYPE html>
    <html lang="en">
    <body style="background-color: rgb(247, 247, 247);">
        <div style="width: 80%;margin: auto;padding:1rem 0">
        <div style="background-color: white;padding: 1rem;border: 1px solid rgb(225, 225, 225);border-radius: 0.5rem;width: 50vh;margin: auto;margin-top: 1rem;">
            <h2>
                Hello Fantom Blog, <br />A user has request to you become 'Fantom Blog' admin.
            </h2>
            <div>Please click the link below to make requested user to become admin.</div>
            <div style="margin: 2rem 0;">
            <a href="{url}" style="background-color: black;padding: 1rem;color: white;font-size: 1.2rem;border-radius: 0.5rem;text-decoration: none;">Verified</a>
            </div>
            <div>If you do not want make admin then, please ignore.</div>
        </div>
        </div>
    </body>
    </html>
    """
    # convert both parts to MIMEText objects and add them to the MIMEMultipart message
    send_data = MIMEText(html, "html")
    message.attach(send_data)

    with SMTP("smtp.gmail.com", port=587) as server:
        server.starttls()
        server.login(user=sender_email, password=sender_email_password)
        server.sendmail(
            from_addr=sender_email,
            to_addrs=sender_email,
            msg=message.as_string()
        )
















# def send_reset_mail(receiver_email, message, name):
#     with SMTP("smtp.gmail.com", port=587) as connection:
#         connection.starttls()
#         connection.login(user=sender_email, password=sender_email_password)
#         connection.sendmail(
#             from_addr=sender_email,
#             to_addrs=receiver_email,
#             msg=f"""Subject:Reset Password\n\nHi {name},\nA password reset for your account was requested.\nPlease click the link below to change your password.\n\n{message}"""
#         )