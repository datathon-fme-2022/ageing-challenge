import os
from flask import Flask, request, render_template
from flask_mail import Mail, Message
from flask_googlemaps import GoogleMaps, Map

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'awatchdata2022@gmail.com'
app.config['MAIL_PASSWORD'] = 'rwxvtlmbzpbpeurv'
app.config['MAIL_USE_TLS'] = False

GoogleMaps(app)

mail = Mail(app)

geo_position={
    'latitude': 0,
    'longitude': 0
}

@app.route('/emergency', methods=['POST'])
def emergency():
    content = request.json
    msg = Message('Hello from the other side!', sender ='awatchdata2022@gmail.com',
        recipients = ['andreu.vallhernandez@gmail.com'])
    print(content)
    msg.body = 'GAYYYY'
    mail.send(msg)
    return "Message sent!"

@app.route('/map')
def public_map():
    return render_template('embedded_map.html')

@app.route("/")
def mapview():
    # creating a map in the view
    mymap = Map(
        identifier="view-side",
        lat=37.4419,
        lng=-122.1419,
        markers=[(37.4419, -122.1419)]
    )
    sndmap = Map(
        identifier="sndmap",
        lat=37.4419,
        lng=-122.1419,
        markers=[
          {
             'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
             'lat': 37.4419,
             'lng': -122.1419,
             'infobox': "<b>Hello World</b>"
          },
          {
             'icon': 'http://maps.google.com/mapfiles/ms/icons/blue-dot.png',
             'lat': 37.4300,
             'lng': -122.1400,
             'infobox': "<b>Hello World from other place</b>"
          }
        ]
    )
    return render_template('example.html', mymap=mymap, sndmap=sndmap)
