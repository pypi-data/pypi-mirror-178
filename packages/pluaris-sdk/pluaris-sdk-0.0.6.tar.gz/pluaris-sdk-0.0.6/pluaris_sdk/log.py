import requests

class FetchData:

    def __init__(self):
        pass
 

    

    ###  GET ALL EMPLOYEES
    
    def getAllEmployees(client_id,client_secret,appid,owner_passphrase):
        payload = {'client_id':client_id,'client_secret':client_secret,'appid':appid,'owner_passphrase':owner_passphrase}
        data = requests.post("https://pluaris-sdk.herokuapp.com/fetch_apis/get_all_emps",data=payload)
        return data.json()




    ###  GET ALL MANAGER
    
    def getAllManager(client_id,client_secret,appid,owner_passphrase):
        payload = {'client_id':client_id,'client_secret':client_secret,'appid':appid,'owner_passphrase':owner_passphrase}
        data = requests.post("https://pluaris-sdk.herokuapp.com/fetch_apis/get_all_managers",data=payload)
        return data.json()





    ###  GET ALL EMPLOYEES UNDER A MANAGER
    
    def getAllEmpsUnderManager(client_id,client_secret,appid,manager_passphrase):
        payload = {'client_id':client_id,'client_secret':client_secret,'appid':appid,'manager_passphrase':manager_passphrase}
        data = requests.post("https://pluaris-sdk.herokuapp.com/fetch_apis/employess_under_manager",data=payload)
        return data.json()



    ###  GET ALL EMPLOYEES LEAVE DATA 
    
    def getAllEmpsLeaveData(client_id,client_secret,appid,emp_passphrase):
        payload = {'client_id':client_id,'client_secret':client_secret,'appid':appid,'emp_passphrase':emp_passphrase}
        data = requests.post("https://pluaris-sdk.herokuapp.com/fetch_apis/emp_leave_data",data=payload)
        return data.json()


 


    ###  GET ALL EMPLOYEES LEAVE DATA UNDER MANAGER
    
    def getAllEmpsLeaveDataUnderManager(client_id,client_secret,appid,manager_passphrase):
        payload = {'client_id':client_id,'client_secret':client_secret,'appid':appid,'manager_passphrase':manager_passphrase}
        data = requests.post("https://pluaris-sdk.herokuapp.com/fetch_apis/emp_leave_data_managers",data=payload)
        return data.json()



    ### GET ALL POEs

    def getAllPOEs(client_id,client_secret,appid,passphrase):
        payload = {'client_id':client_id,'client_secret':client_secret,'appid':appid,'passphrase':passphrase}
        data = requests.post("https://pluaris-sdk.herokuapp.com/fetch_apis/emp_all_poes",data=payload)
        return data.json()



    ### GET ALL POLs

    def getAllPOLs(client_id,client_secret,appid,passphrase):
        payload = {'client_id':client_id,'client_secret':client_secret,'appid':appid,'passphrase':passphrase}
        data = requests.post("https://pluaris-sdk.herokuapp.com/fetch_apis/emp_all_pols",data=payload)
        return data.json()

 


