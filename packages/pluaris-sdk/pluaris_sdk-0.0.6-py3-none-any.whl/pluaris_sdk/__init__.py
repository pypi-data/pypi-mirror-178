import requests
 
from .verification import Verify
from .log import FetchData
 
 

class PluarisSDK:

    def __init__(self):
        pass


    ### EMPLOYEE / MANAGER / SC_OWNER LOGIN


    def login(client_id,client_secret,appid,passphrase):
        payload = {'client_id':client_id,'client_secret':client_secret,'appid':appid,'passphrase':passphrase}
        data = requests.post("https://pluaris-sdk.herokuapp.com/fetch_apis/login",data=payload)
        return data.json()



    
    ###  SDK INIT
    
    def sdkInit(email):
        payload = {'email':email}
        data = requests.post("https://pluaris-sdk.herokuapp.com/sdk_apis/sdk_init",data=payload)
        return data.json()





    ###  DEPLOY SMART CONTRACT 
    
    def deploySmartContract(client_id,client_secret,owner_passphrase,org_name,org_email):
        payload = {'client_id':client_id,'client_secret':client_secret,'owner_passphrase':owner_passphrase,'org_name':org_name,'org_email':org_email}
        data = requests.post("https://pluaris-sdk.herokuapp.com/sdk_apis/deploy_sc",data=payload)
        return data.json()




    ###  CREATE WALLET

    def createWallet(client_id,client_secret,appid,passphrase, name,email,mobile,designation,manager):
        payload = {'client_id':client_id,'appid':appid,'passphrase':passphrase,'client_secret':client_secret,'name':name,'email':email,'mobile':mobile,'desig':designation,'manager':manager}
        data = requests.post("https://pluaris-sdk.herokuapp.com/sdk_apis/create_wallet",data=payload)
        return data.json()



    ###  ATTENDENCE CHECKIN
    
    def checkIn(client_id,client_secret,appid,emp_passphrase):
        payload = {'client_id':client_id,'client_secret':client_secret,'emp_passphrase':emp_passphrase,'appid':appid}
        data = requests.post("https://pluaris-sdk.herokuapp.com/sdk_apis/emp_checkin",data=payload)
        return data.json()




    ###  ATTENDENCE CHECKOUT
    
    def checkOut(client_id,client_secret,appid,emp_passphrase):
        payload = {'client_id':client_id,'client_secret':client_secret,'emp_passphrase':emp_passphrase,'appid':appid}
        data = requests.post("https://pluaris-sdk.herokuapp.com/sdk_apis/emp_checkout",data=payload)
        return data.json()


    ###  LEAVE REQUEST
    
    def leaveRequest(client_id,client_secret,appid,emp_passphrase,reason,from_date,duration):
        payload = {'client_id':client_id,'client_secret':client_secret,'emp_passphrase':emp_passphrase,'appid':appid,'reason':reason,'from_date':from_date,'duration':duration}
        data = requests.post("https://pluaris-sdk.herokuapp.com/sdk_apis/leave_request",data=payload)
        return data.json()


    ###  LEAVE APPROVE
    
    def leaveApprove(client_id,client_secret,appid,manager_passphrase,emp_address,reason,from_date,duration,status):
        payload = {'client_id':client_id,'client_secret':client_secret,'manager_passphrase':manager_passphrase,'emp_address':emp_address,'appid':appid,'reason':reason,'from_date':from_date,'duration':duration,'status':status}
        data = requests.post("https://pluaris-sdk.herokuapp.com/sdk_apis/leave_approve",data=payload)
        return data.json()



    ###  POL REQUEST
    
    def proofOfLearningRequest(client_id,client_secret,appid,emp_passphrase,topic,url):
        payload = {'client_id':client_id,'client_secret':client_secret,'emp_passphrase':emp_passphrase,'topic':topic,'url':url,'appid':appid}
        data = requests.post("https://pluaris-sdk.herokuapp.com/sdk_apis/pol_request",data=payload)
        return data.json()



    ###  POL APPROVE
    
    def proofOfLearningApproval(client_id,client_secret,appid,owner_passphrase,emp_address,topic,url,status):
        payload = {'client_id':client_id,'client_secret':client_secret,'owner_passphrase':owner_passphrase,'appid':appid,'emp_address':emp_address,'topic':topic,'url':url,'status':status}
        data = requests.post("https://pluaris-sdk.herokuapp.com/sdk_apis/pol_approve",data=payload)
        return data.json()



    ###  POE REQUEST
    
    def proofOfExperienceRequest(client_id,client_secret,appid,emp_passphrase,org,domain,exp,leaving_date):
        payload = {'client_id':client_id,'client_secret':client_secret,'emp_passphrase':emp_passphrase,'org':org,'domain':domain,'appid':appid,'exp':exp,'leaving_date':leaving_date}
        data = requests.post("https://pluaris-sdk.herokuapp.com/sdk_apis/poe_request",data=payload)
        return data.json()



    ###  POE APPROVE
    
    def proofOfExperienceApproval(client_id,client_secret,appid,owner_passphrase,emp_address,org,domain,exp,leaving_date,status):
        payload = {'client_id':client_id,'client_secret':client_secret,'owner_passphrase':owner_passphrase,'appid':appid,'emp_address':emp_address,'exp':exp,'leaving_date':leaving_date,'status':status,'org':org,'domain':domain}
        data = requests.post("https://pluaris-sdk.herokuapp.com/sdk_apis/poe_approve",data=payload)
        return data.json()
    
    
 
