from flask import Flask
from flask import request
from Pandora import dry_run
from cheating import Cheating
from twilio.rest import TwilioRestClient

app = Flask(__name__)

from twilio.rest import TwilioRestClient

account_sid = "ACe8e7416fc2481af951f75f17212de45c" # Your Account SID from www.twilio.com/console
auth_token  = "f15cf79758f1cf0093ecb1d1c15fb14c"  # Your Auth Token from www.twilio.com/console

client = TwilioRestClient(account_sid, auth_token)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/input",methods = ['POST','GET'])
def input():
    if request.method=='POST':
        # print str(request.form)
        response=dry_run(request.form['Body'])
        print "INPUT:%s\nOUTPUT:%s"%(request.form['Body'],response)
        # action & target
        t=response['response'].split(" ")
        action=t[1]
        # 'response': u'DEVALERT: BEST_RATES my doorknob'}
        target= ' '.join(t[2:])
        print "ACTION=%s\nTARGET=%s" % (action,target)
        resp=""
        if(action == 'JOBS'):
            pass
        elif(action=='SAVE'):
            pass
        elif(action=='BEST_RATES'):
            results=Cheating(target).targets()
            count=1
            for i in results:
                print(i.name)
                resp=resp+str(count)+" "+i.name+'\n'
                count+=1
            if len(resp) <=0:
                resp="no results found"
        else:
            print "invalid action"
        try:
            message = client.messages.create(body=resp,
                                             to=request.form['From'],    # Replace with your phone number
                                             from_="+19196799036") # Replace with your Twilio number
        except Exception as e:
            print(e)

        return str(request.form.keys())
    else:
        return "input error"



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80,debug=True)
