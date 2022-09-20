import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

sender_email = "fantomblog.contact@gmail.com"
sender_email_password = "loggflqbakatmlhj"
receiver_email = "aruneshkumar.king@gmail.com"


message = MIMEMultipart("alternative")
message["Subject"] = "Reset Password"
message["From"] = sender_email
message["To"] = receiver_email


# write the HTML part
html = """\
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Document</title>
    <style>
      body {
        background-color: rgb(247, 247, 247);
      }

      .container {
        width: 80%;
        margin: auto;
      }

      .card {
        background-color: white;
        padding: 1rem;
        border: 1px solid rgb(225, 225, 225);
        border-radius: 0.5rem;
        width: 50vh;
        margin: auto;
        margin-top: 1rem;
      }

      .btn {
        background-color: black;
        padding: 1rem;
        color: white;
        font-size: 1.2rem;
        border-radius: 0.5rem;
        text-decoration: none;
      }

      .link {
        margin: 2rem 0;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <div class="card">
        <div>
          Hi Arunesh, <br />A password reset for your account was requested.
        </div>
        <div>Please click the link below to change your password.</div>
        <div class="link">
          <a href="#" class="btn">Change Your Password </a>
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

# send your email
with smtplib.SMTP("smtp.gmail.com", port=587) as server:
    server.starttls()
    server.login(sender_email, sender_email_password)
    server.sendmail(
        from_addr=sender_email, to_addrs=receiver_email, msg=message.as_string()
    )

print('Sent') 