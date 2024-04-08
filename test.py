import sys
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content

# sys.argv[0] is the script name, parameters start from sys.argv[1]
if len(sys.argv) > 2:
    link = sys.argv[1]
    email = sys.argv[2]
    print(f"Parameter 1: {link}, Parameter 2: {email}")
    txt_file = open('kek.txt', 'w', newline='')
    txt_file.write(f"Parameter 1: {link}, Parameter 2: {param2}")
    

    sg = sendgrid.SendGridAPIClient(api_key='your_sendgrid_apikey')
    from_email = Email("your_email@example.com")  # Change to your verified sender email
    to_email = To("recipient_email@example.com")  # Change to your recipient
    subject = "Sending with SendGrid is Fun"
    content = Content("text/plain", "and easy to do anywhere, even with Python")
    mail = Mail(from_email, to_email, subject, content)

    response = sg.client.mail.send.post(request_body=mail.get())
    print(response.status_code)
    print(response.body)
    print(response.headers)

else:
    print("Not enough parameters provided.")
    txt_file = open('kek.txt', 'w', newline='')
    txt_file.write('fail')
