import requests
from flask import Flask,render_template,request
from twilio.rest import Client
import requests_cache
import os
from dotenv import load_dotenv

load_dotenv()

account_sid = os.getenv("account_sid")
auth_token = os.getenv("auth_token")


client = Client(account_sid,auth_token)
app = Flask(__name__,static_url_path = '/static')

@app.route('/')
def registration_form():
    return render_template('Registration.html')

@app.route('/Acknowledgement',methods=['POST'])
def login_registration_dtls():
    first_name = request.form['fname']
    last_name = request.form['lname']
    email_id = request.form['email']
    source_st = request.form['source_state']
    source_dt = request.form['source']
    destination_st = request.form['dest-state']
    destination_dt = request.form['destination']
    phoneNumber = request.form['phoneNumber']
    id_proof = request.form['idcard']
    date = request.form['trip']
    
    if(first_name=="" or last_name =="" or source_dt=="" or source_st =="" or destination_dt =="" or destination_st=="" or phoneNumber=="" or date ==""):
        return render_template('Registration.html')
        
    full_name = first_name +" "+ last_name
    r = requests.get('https://api.covid19india.org/v4/data.json')
    json_date = r.json()
    cnt = json_date[destination_st]['districts'][destination_dt]['total']['confirmed']
    pop = json_date[destination_st]['districts'][destination_dt]['meta']['population']
    travel_pass = ((cnt/pop)*100)
    if travel_pass<30 and request.method == 'POST':
        status = 'CONFIRMED'
        apply=''
    else:
        status = 'Not CONFIRMED'
        apply=' Apply Later' 
    client.messages.create(to=" + 91"+phoneNumber,
                            from_=os.getenv("PhoneNumber"),
                            body = "Hello "+ " "+ full_name + "  Your TRAVEL FROM  "+source_dt + "  TO  "+ destination_dt +"  HAS  "+status +" ON "+date +" "+apply)

    return render_template('Acknowledgement.html', var=full_name ,var1=email_id, var2 = id_proof,
                            var3 = source_st, var4 = source_dt , var5 = destination_st ,var6 = destination_dt,
                            var7 = phoneNumber ,var8 = date,var9 = status)

if __name__ == "__main__":
    app.run(port=9001, debug=True)


        


