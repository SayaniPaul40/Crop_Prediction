import requests

dictToSend = {
'ph':1.0,
'nitrogen':2.0,
'phosphorous':3.0,
'potassium':4.0,
'area':5.0,
'predict_month':'JAN',
'current_crop_month':'FEB',
'current_planted_crop':'MAR',
'crop_season':'Kharif',
'soil_type':'Alluvial',
'lat':'25.594095',
'lng':'85.137566',
'isCurrent':False,
'district':'AURANGABAD',
'state':'Bihar'}

res = requests.post('http://localhost:5000/predict', json=dictToSend)
#print ('response from server:',res.text)
try:   
     dictFromServer = res.json()
     print(dictFromServer)  
#     print ('response from server:',res.json())
except ValueError:
    print("Response content is not valid json")


#print(dictFromServer)

#json_data = json.loads(res.text)

# newHeaders = {'Content-type': 'application/json', 'Accept': 'text/plain'}

# response = requests.post('http://localhost:5000/predict',
#                          data={'area': 1, 'predict_month': 'Jessa'},
#                          headers=newHeaders)

#print("Status code: ", res.status_code)

#response_Json = res.json()
#print("Printing Post JSON data")
#print(response_Json['data'])

# print("Content-Type is ", response_Json['headers']['Content-Type'])
