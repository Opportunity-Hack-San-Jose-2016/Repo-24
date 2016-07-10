from flask import Flask
from flask import request
from Pandora import dry_run
from cheating import Cheating
from twilio.rest import TwilioRestClient
import json
from indeed import IndeedClient
import redis

class db_formation(object):

    def __init__(self):
        self.r = redis.StrictRedis(host='localhost')

    def insert(self,phone_number,salary,expense,amount,date,item):
        current_set = {"salary":salary,"expenditure":expense,"item_amount":amount,"date":date,"item_name":item,"goal":100,"savings_rate":1,"daily_goal":99,
                       "savings_per_goal":0,"expense_per_day":0,'goal_eta':100}
        print current_set
        self.r.hmset(phone_number,current_set)

    def display(self,phone_number):
        d = (self.r).hgetall(phone_number)
        print d

app = Flask(__name__)

from twilio.rest import TwilioRestClient

indeed_client = IndeedClient('9093816856988990')

account_sid = "ACe8e7416fc2481af951f75f17212de45c" # Your Account SID from www.twilio.com/console
auth_token  = "f15cf79758f1cf0093ecb1d1c15fb14c"  # Your Auth Token from www.twilio.com/console

client = TwilioRestClient(account_sid, auth_token)


@app.route("/")
def hello():
    return "Hello World!"

@app.route("/twitter",methods = ['POST','GET'])
def twitter():
    if request.method=='POST':
        if request.form['tweet']:
            print "TWEET:%s" %(request.form['tweet'])
        else:
            print "no tweet data"
        return "OK"

@app.route("/credit",methods = ['POST','GET'])
def credit():
    if request.method=='POST':
        if request.form['item'] and request.form['value']:
            print request.form['item']
            # got expense
            # check if its below your daily goal, alert user OK
            # if its over goal, adjust the gaoal ETA and alert user
            expense = request.form['value']
            obj = db_formation()
            t=obj.r.hgetall("+19197445728")
            response=""
            t['expense_per_day'] = int(t['expense_per_day'])+int(expense)
            obj.r.hmset("+19197445728",t)
            print "EXPENSE:%s\nEXPENSE_PER_DAY:%s" % (expense,t['expense_per_day'])
            # if(expense+t['todays_expense'] < t['daily_goal']):
            #     # ok
            #     t['todays_expense']+=expense
            #     response+="You're still under your daily goal."
            # else:
            #     overflow=expense+t['todays_expense_so_far'] - t['daily_goal']
            #     t['todays_expense_so_far']+=expense


            # sms(response)
        else:
            print "NOPE"
        return "OK"

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
            params = {
                'q' : "part time",
                'l' : "san jose",
                'userip' : "173.224.162.79",
                'useragent' : "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2)"
            }
            search_response = indeed_client.search(**params)
            # print json.dumps(search_response,indent=4)
            count =1
            for i in search_response['results']:
                print str(count)+" "+i['company']+"-"+i['jobtitle']+'\n'
                resp=resp+str(count)+" "+i['company']+"-"+i['jobtitle']+'\n'
                if count >=3:
                    break
                count+=1
            if len(resp) <=0:
                resp="no results found"
        elif(action=='SAVE'):
            if target=="checkSavingsBuy":
                checkSavingsBuy("car")
            elif target=="checkSavingsStudy":
                checkSavingStudy
                pass
            elif targey=="checkSavingsSpend":
                pass
            else:
                print "invalid target in SAVE action"
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
    obj = db_formation()
    obj.insert("+19197445728",1000,800,12, "12.04.2016", "lunch")
    obj.display("+19197445728")
    app.run(host="0.0.0.0", port=80,debug=True)
