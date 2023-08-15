from flask import *
import requests 
import json

app = Flask(__name__)
#Defind Post Methods
# @app.route('/nso',methods = ['POST'])
# def nso():
#     if request.method == 'POST':
#         url = "https://api.nso.go.th/api/v1.0/branch21/dataset/458?year=2560"
#         payload={}
#         headers = {
#           'Authorize': '91f27382-ca92-4665-8723-f32450bdd914'
#         }
#         response = requests.request("POST", url, headers=headers, data=payload)
#         return json.loads(response.text)
#Get methods
@app.route('/nso/')
def nso2():
      url = "https://api.nso.go.th/api/v1.0/branch21/dataset/458?year=2560"
      payload={}
      headers = {
        'Authorize': '91f27382-ca92-4665-8723-f32450bdd914'
      }
      response = requests.request("POST", url, headers=headers, data=payload)
      return json.loads(response.text)

@app.route('/nso/apikey/admin/')
def nso3():
    url = "https://api.nso.go.th/api/v1.0/branch21/dataset/458?year=2560"
    payload={}
    headers = {
    'Authorize': '91f27382-ca92-4665-8723-f32450bdd914'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    return json.loads(response.text)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
