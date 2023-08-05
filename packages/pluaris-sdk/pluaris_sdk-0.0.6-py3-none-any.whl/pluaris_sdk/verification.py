import requests





class Verify:

    def __init__(self):
        pass

    

    ###  VERIFY EMAIL
    
    def verifyEmail(client_id,client_secret,appid,verifier_passphrase,wallet_address):
        payload = {'client_id':client_id,'client_secret':client_secret,'verifier_passphrase':verifier_passphrase,'address':wallet_address,'appid':appid}
        data = requests.post("https://pluaris-sdk.herokuapp.com/verify_apis/verify_email",data=payload)
        return data.json()




    ###  VERIFY MOBILE
    
    def verifyMobile(client_id,client_secret,appid,verifier_passphrase,wallet_address):
        payload = {'client_id':client_id,'client_secret':client_secret,'verifier_passphrase':verifier_passphrase,'address':wallet_address,'appid':appid}
        data = requests.post("https://pluaris-sdk.herokuapp.com/verify_apis/verify_mobile",data=payload)
        return data.json()



    ###  VERIFY POL
    
    def verifyPOL(client_id,client_secret,appid,verifier_passphrase,wallet_address,topic):
        payload = {'client_id':client_id,'client_secret':client_secret,'verifier_passphrase':verifier_passphrase,'address':wallet_address,'appid':appid,'topic':topic}
        data = requests.post("https://pluaris-sdk.herokuapp.com/verify_apis/verify_pol",data=payload)
        return data.json()


    ###  VERIFY POE
    
    def verifyPOE(client_id,client_secret,appid,verifier_passphrase,wallet_address,domain):
        payload = {'client_id':client_id,'client_secret':client_secret,'verifier_passphrase':verifier_passphrase,'address':wallet_address,'appid':appid,'domain':domain}
        data = requests.post("https://pluaris-sdk.herokuapp.com/verify_apis/verify_poe",data=payload)
        return data.json()