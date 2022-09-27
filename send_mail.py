from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


sender_email = "contact.fantomblog@gmail.com"
sender_email_password = "atoyegyyjeefxcsr"


#   password reset mail
def send_reset_mail(receiver_email, url, name):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Reset Password"
    message["From"] = sender_email
    message["To"] = receiver_email

    #   HTML part
    html = f"""\
   <!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Bootstrap demo</title>

    <style>
      body {{
        background-color: rgb(247, 247, 247);
      }}

      .container {{
        max-width: 50%;
        margin: auto;
      }}

      .card {{
        border: 2px solid rgb(219, 219, 219);
        border-radius: 0.5rem;
        background-color: white;
        padding: 1rem;
      }}

      .btn-container {{
        margin: 2rem;
        text-align: center;
      }}

      .text {{
        margin: 1rem 0;
      }}

      .wish {{
        margin-top: 0.7rem;
      }}

      .btn {{
        background-color: black;
        color: white;
        padding: 1rem 2rem;
        border-radius: 1rem;
        text-decoration: none;
        font-size: 1.2rem;
      }}

      a:link {{
        color: white;
      }}

      @media only screen and (max-width: 600px) {{
        .container {{
          max-width: 90%;
        }}
      }}
    </style>
  </head>
  <body>
    <!--  -->

    <div class="container">
      <div class="card">
        <h1>Hello {name},</h1>
        <div class="text">
          A password reset for your account was requested. If you did request,
          then please click the link below to change your password. If you did
          not make this request, please ignore.
        </div>
        <div class="btn-container">
          <a href="{url}" class="btn btn-dark">Change Your Password</a>
        </div>
        <div class="wish">Thank You 🙏</div>
      </div>
    </div>

    <!--  -->
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


#   send varification mail
def verification_admin(url):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Admin Verification"
    message["From"] = sender_email
    message["To"] = sender_email

    #   HTML part
    html = f"""\
    <!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Bootstrap demo</title>

    <style>
      body {{
        background-color: rgb(247, 247, 247);
      }}

      .container {{
        max-width: 50%;
        margin: auto;
      }}

      .card {{
        border: 2px solid rgb(219, 219, 219);
        border-radius: 0.5rem;
        background-color: white;
        padding: 1rem;
      }}

      .btn-container {{
        margin: 2rem;
        text-align: center;
      }}

      .text {{
        margin: 1rem 0;
      }}

      .wish {{
        margin-top: 0.7rem;
      }}

      .btn {{
        background-color: black;
        color: white;
        padding: 1rem 2rem;
        border-radius: 1rem;
        text-decoration: none;
        font-size: 1.2rem;
      }}

      a:link {{
        color: white;
      }}

      @media only screen and (max-width: 600px) {{
        .container {{
          max-width: 90%;
        }}
      }}
    </style>
  </head>
  <body>
    <!--  -->

    <div class="container">
      <div class="card">
        <h1>Hello Fantom Blog,</h1>
        <div class="text">
          A user has request to you become 'Fantom Blog' admin. Please click the
          link below to make requested user to become admin. If you do not want
          make admin then, please ignore.
        </div>
        <div class="btn-container">
          <a href="{url}" class="btn btn-dark">Change Your Password</a>
        </div>
        <div class="wish">Thank You 🙏</div>
      </div>
    </div>

    <!--  -->
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



#   account verified mail
def account_verified(email, url, name):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Account Verified"
    message["From"] = sender_email
    message["To"] = email

    #   HTML part
    html = f"""\
   <!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Bootstrap demo</title>

    <style>
      body {{
        background-color: rgb(247, 247, 247);
      }}

      .container {{
        max-width: 50%;
        margin: auto;
      }}

      .card {{
        border: 2px solid rgb(219, 219, 219);
        border-radius: 0.5rem;
        background-color: white;
        padding: 1rem;
      }}

      .btn-container {{
        margin: 2rem;
        text-align: center;
      }}

      .text {{
        margin: 1rem 0;
      }}

      .wish {{
        margin-top: 0.7rem;
      }}

      .btn {{
        background-color: black;
        color: white;
        padding: 1rem 2rem;
        border-radius: 1rem;
        text-decoration: none;
        font-size: 1.2rem;
      }}

      a:link {{
        color: white;
      }}

      @media only screen and (max-width: 600px) {{
        .container {{
          max-width: 90%;
        }}
      }}
    </style>
  </head>
  <body>
    <!--  -->

    <div class="container">
      <div class="card">
        <h1>Hello {name},</h1>
        <div class="text">
          Your account had verified as a Admin. Now you are admin of 'Fantom
          Blog', You can post new blog, update, delete and more thing you can do
          now.
        </div>
        <div class="wish">Congratulation 🥳, To become our family part.</div>
        <div class="btn-container">
          <a href="{url}" class="btn btn-dark">Login</a>
        </div>
      </div>
    </div>

    <!--  -->
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
            to_addrs=email,
            msg=message.as_string()
        )




#   send latest post
def send_latest_post(email, url, name, category, title):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Latest Post Update"
    message["From"] = sender_email
    message["To"] = email

    #   HTML part
    html = f"""\
        <!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Bootstrap demo</title>

    <style>
      body {{
        background-color: rgb(247, 247, 247);
      }}

      .container {{
        max-width: 50%;
        margin: auto;
      }}

      .card {{
        border: 2px solid rgb(219, 219, 219);
        border-radius: 0.5rem;
        background-color: white;
        padding: 1rem;
      }}

      .btn-container {{
        margin: 2rem;
        text-align: center;
      }}

      .text {{
        margin: 1rem 0;
      }}

      .wish {{
        margin-top: 0.7rem;
      }}

      .btn {{
        background-color: black;
        color: white;
        padding: 1rem 2rem;
        border-radius: 1rem;
        text-decoration: none;
        font-size: 1.2rem;
      }}

      a:link {{
        color: white;
      }}

      @media only screen and (max-width: 600px) {{
        .container {{
          max-width: 90%;
        }}
      }}
    </style>
  </head>
  <body>
    <!--  -->

    <div class="container">
      <div class="card">
        <h1>Hello {name},</h1>
        <div class="text">
          We have just added new post on related to {category}. <br />
          Post Title is : <h2>{title}</h2>. <br />
          Please click the button to read our latest post.
        </div>
        <div class="btn-container">
          <a href="{url}" class="btn btn-dark">Read Post</a>
        </div>
        <div class="wish">Thank You 🙏</div>
      </div>
    </div>

    <!--  -->
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
            to_addrs=email,
            msg=message.as_string()
        )






#   send latest post
def contact_update_admin(email, name, subject, url):
    message = MIMEMultipart("alternative")
    message["Subject"] = "Contact Update"
    message["From"] = sender_email
    message["To"] = email

    #   HTML part
    html = f"""\
        <!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Bootstrap demo</title>

    <style>
      body {{
        background-color: rgb(247, 247, 247);
      }}

      .container {{
        max-width: 50%;
        margin: auto;
      }}

      .card {{
        border: 2px solid rgb(219, 219, 219);
        border-radius: 0.5rem;
        background-color: white;
        padding: 1rem;
      }}

      .btn-container {{
        margin: 2rem;
        text-align: center;
      }}

      .text {{
        margin: 1rem 0;
      }}

      .wish {{
        margin-top: 0.7rem;
      }}

      .btn {{
        background-color: black;
        color: white;
        padding: 1rem 2rem;
        border-radius: 1rem;
        text-decoration: none;
        font-size: 1.2rem;
      }}

      a:link {{
        color: white;
      }}

      @media only screen and (max-width: 600px) {{
        .container {{
          max-width: 90%;
        }}
      }}
    </style>
  </head>
  <body>
    <!--  -->

    <div class="container">
      <div class="card">
        <h1>Hello {name},</h1>
        <div class="text">
        Fantom user trying to contact with you, <br /> 
         Subject : <h2>'{subject}'.</h2> <br />
         If you like then please check your dashboard, click on login button.
        </div>
        <div class="btn-container">
          <a href="{url}" class="btn btn-dark">Login</a>
        </div>
        <div class="wish">Thank You 🙏</div>
      </div>
    </div>

    <!--  -->
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
            to_addrs=email,
            msg=message.as_string()
        )

