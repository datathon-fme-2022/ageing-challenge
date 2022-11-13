import os
from flask import Flask, request, render_template
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'awatchdata2022@gmail.com'
app.config['MAIL_PASSWORD'] = 'rwxvtlmbzpbpeurv'
app.config['MAIL_USE_TLS'] = False

mail = Mail(app)

geo_position={
    'latitude': 0,
    'longitude': 0
}

@app.route('/emergency', methods=['POST'])
def emergency():
    content = request.json
    msg = Message('New health alert near you!', sender ='awatchdata2022@gmail.com',
        recipients = ['andreu.vallhernandez@gmail.com'])
    print(content)
    msg.html = render_template('message.html', 
                            name=content['name'],
                            latitude=content['lat'],
                            longitude=content['lng'],
                            sentence=content['message'])
    #msg.body = f'{content["name"]}: {content["message"]}\nLocated at coordinates latitude {content["lat"]}º longitude {content["lng"]}º' 
    mail.send(msg)
    return "Message sent!"
