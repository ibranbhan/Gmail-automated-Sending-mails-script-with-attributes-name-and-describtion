import pandas as pd
import smtplib
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from dotenv import load_dotenv
import os

load_dotenv()

df = pd.read_csv(r"C:\Users\hemna\Downloads\testing gdsc.csv")
print(df.head())

hostMail = os.getenv('hostMail')
password = os.getenv('password')

def send_message(email, name, certi):
    msg = MIMEMultipart()
    msg["From"] = hostMail
    msg["To"] = email
    msg["Subject"] = "UX Designing Boot Camp - Certificate"

    html_content = """
    <html>
      <head>
        <style>
          body {{
            font-family: Arial, sans-serif;
          }}
          h1 {{
            font-size: 20px;
            font-weight: bold;
            margin-bottom: 3px;
          }}
             .signature {{
            font-weight: bold;
            font-size: 15px;
          }}
           .colo {{
            color: red;
            font-weight: bold;
          }}
        </style>
      </head>
      <body>
        <div class="message-container">
          <h1>Dear: {}</h1>
          <p>Congratulations on completing the UX Design Boot Camp! We are so proud of your hard work and dedication. Your contributions to the program were invaluable, and we are grateful for your participation.</p>
          <p>We are excited to see what you will accomplish in the future. Your skills and knowledge in UX design are in high demand, and we are confident that you will be successful in your career.</p>
          <p>We have attached your certificate of completion to this email. Please keep this certificate as a record of your achievement.</p>
          <p class= "colo"><a href={}>Press here for the Certificate Link</a> </p>
        </div>
        <br>
        <p class="signature">Sincerely,</p>
        <p class="signature">GDSCKFU</p>
        <br>
        <img src="cid:image.jpg">
      </body>
    </html>
    """.format(name, certi)

    html_part = MIMEText(html_content, "html")
    msg.attach(html_part)

    with open(r"C:\Users\hemna\Downloads\logos gdsc.png", "rb") as image_file:
        image_data = image_file.read()

    image_part = MIMEImage(image_data, name="image.jpg")
    image_part.add_header("Content-ID", "<image.jpg>")
    msg.attach(image_part)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
        try:
            server.login(hostMail, password)
            server.sendmail(hostMail, email, msg.as_string())
            print("Email sent to", email)
        except Exception as e:
            print("An error occurred while sending the email:", str(email))
            error_df = pd.DataFrame({'name': [name], 'email': [email]})
            error_df.to_csv('error_log.csv', mode='a', index=False, header=not bool(index))

for index, row in df.iterrows():
    email = row['email']
    name = row['name']
    certi = row['certi']
    send_message(email, name, certi)
