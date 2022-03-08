from flask import Flask, render_template
from flask import request
from flask import jsonify
# import joblib
import csv
import requests
import json
import pickle
import geopy
from geopy.geocoders import Nominatim
from Models.crop_class import *
from Models.production_class import *
import numpy as np
app = Flask(__name__)

scale_val = 0.1

month_dict = {
    'JAN': 0,
    'FEB': 1,
    'MAR': 2,
    'APR': 3,
    'MAY': 4,
    'JUN': 5,
    'JUL': 6,
    'AUG': 7,
    'SEP': 8,
    'OCT': 9,
    'NOV': 10,
    'DEC': 11
}


def get_avg(temps, predict_month):
#    print("Temp:==>>>",temps,"predict_month:=>>>>",predict_month)
    temp_arr = []
    idx_num = month_dict[predict_month]
    temp_arr.append(float(temps[idx_num]))
    for i in range (0, 5, 1):
        idx_num += 1
        idx_num = idx_num % 12
        temp_arr.append(float(temps[idx_num]))
    return np.average(temp_arr, axis=0)

def get_ground_water(ground_water, predict_month, district):
    temp_arr=[]
    gwater = list(ground_water[district].values())
    idx_num = month_dict[predict_month]
    temp_arr.append(gwater[idx_num])
    for i in range(0, 5, 1):
        idx_num += 1
        idx_num = idx_num % 12
        temp_arr.append(gwater[idx_num])
    print("gwater:  ", temp_arr)
    return np.average(temp_arr, axis=0)

def get_soil(soil_type):
    soil_arr=[]
    if(soil_type == 'Alluvial'):
        soil_arr.append(1)
    else:
        soil_arr.append(0)

    if(soil_type == 'Black'):
        soil_arr.append(1)
    else:
        soil_arr.append(0)

    if(soil_type == 'Loam'):
        soil_arr.append(1)
    else:
        soil_arr.append(0)

    if(soil_type == 'Red'):
        soil_arr.append(1)
    else:
        soil_arr.append(0)

    return soil_arr
    
def get_rain(latitude, longitude):
    data=pd.read_csv('pr_climatology_annual-monthly_cmip5_rcp26_climatology_ensemble_2020-2039_median_IND.csv')
    geolocator = Nominatim(user_agent="CropPredictor_v1")
    location = geolocator.reverse(latitude+","+longitude)

    address = location.raw['address']
    state = address.get('state', '')
    print(type(data))
    info_data=data.query('State_Name == @state')
    rainfall= np.array(info_data.loc[:,'Jan':'Dec'])
    rainfall=rainfall.flatten()
    print(rainfall)
    return rainfall        

def get_tem(latitude, longitude):
    data=pd.read_csv('tas_climatology_annual-monthly_cmip5_rcp26_climatology_ensemble_2020-2039_median_IND.csv')
    geolocator = Nominatim(user_agent="CropPredictor_v1")
    location = geolocator.reverse(latitude+","+longitude)

    address = location.raw['address']
    state = address.get('state', '')
    print(type(data))
    info_data=data.query('State_Name == @state')
    temps= np.array(info_data.loc[:,'Jan':'Dec'])
    temps=temps.flatten()
    print(temps)
    return temps      

# AI/ML parameteres default
nn_weight_path = 'Models\weights\kharif_crops_final.pth'
production_weight_path = 'Models\weights\production_weights.sav'

@app.route('/', methods=['GET'])
def index():
    return "Default Route"


                                                            ##########
@app.route('/result', methods=['GET', 'POST'])
def rootpage():
    name=''
    area =''
    potassium=''
    nitrogen=''
    phosphorus=''
    ph=''
    crop_season=''
    current_planted_crop=''
    current_crop_month=''
    predict_month=''
    isCurrent=''
    soil_type=''
    lat=''
    lng=''
    district=''
    state=''
    if request.method == 'POST' and 'username' in request.form: 
        name= request.form.get('username')
        area= request.form.get('area')
        potassium= request.form.get('potassium')
        nitrogen= request.form.get('nitrogen')
        phosphorus= request.form.get('phosphorus')
        ph=request.form.get('ph')
        crop_season=request.form.get('crop_season')
        current_planted_crop=request.form.get('current_planted_crop')
        current_crop_month=request.form.get('current_crop_month')
        predict_month=request.form.get('predict_month')
        isCurrent=request.form.get(' isCurrent')
        soil_type=request.form.get('soil_type')
        lat=request.form.get('lat')
        lng=request.form.get('lng')
        district=request.form.get('district')
        state=request.form.get('state')
    return render_template("index.html", 
                            name=name, 
                            area=area, 
                            potassium=potassium, 
                            nitrogen=nitrogen,
                            phosphorus=phosphorus,
                            ph=ph, 
                            crop_season=crop_season, 
                            current_planted_crop=current_planted_crop,
                            current_crop_month=current_crop_month,
                            predict_month=predict_month,
                            isCurrent=isCurrent,
                            soil_type=soil_type,
                            lat=lat,
                            lng=lng,
                            district=district,
                            state=state)   
app.run()

                                                            ############


@app.route('/predict', methods=['POST'])
def predict():
    data=request.get_json()
    # area = request.form.get('area')
    # potassium = request.form.get('potassium')
    # nitrogen = request.form.get('nitrogen')
    # phosphorous = request.form.get('phosphorous')
    # ph = request.form.get('ph')
    # crop_season = request.form.get('crop_season')
    # current_crop = request.form.get('current_planted_crop')
    # predict_month = request.form.get('predict_month')
    # is_current = request.form.get('is_current')
    # soil_type = request.form.get('soil_type')

    area = data['area']
    potassium = data['potassium']
    nitrogen = data['nitrogen']
    phosphorous = data['phosphorous']
    ph = data['ph']
    crop_season = data['crop_season']
    current_crop = data['current_planted_crop']
    predict_month = data['predict_month']
    is_current =  False
    soil_type = data['soil_type']

    print(predict_month,area)

    # Use this API for finding data using latitudes and Longitudes
    # https://climateknowledgeportal.worldbank.org/api/data/get-download-data/projection/mavg/tas/rcp26/2020_2039/21.1458$cckp$79.0882/21.1458$cckp$79.0882
    # temps stores the predicted temperature
    latitude = str(data['lat'])
    longitude = str(data['lng'])
    district = (data['district'])
    state = (data['state'])
    
    rainfall= get_rain(latitude, longitude)
    temps= get_tem(latitude, longitude)
    # param = "tas"
    # URL = "https://climateknowledgeportal.worldbank.org/api/data/get-download-data/projection/mavg/"+ param +"/rcp26/2020_2039/" + \
    #     latitude+"$cckp$"+longitude + "/"+latitude + "$cckp$"+longitude + ""
    
    
    # resp = requests.get(url=URL)
    # decoded = resp.content.decode("utf-8")
    # cr = csv.reader(decoded.splitlines(), delimiter=',')
    # my_list = list(cr)
    # temps = [25]
    # for index, row in enumerate(my_list):
    #     if index == 0:
    #         continue
    #     if index > 13:
    #         break
    #     temps.append(row[0])

#    temps = [25,25.9,26.7,28.6,24.8,24.8,23.8]
#    rainfall=[60.84085845,64.75894582,61.57342478,63.76179014,61.35097976,62.52861242,63.20089868,60.35717585,60.19734241,64.99821489,64.80653128,60.57510887,60.11306945
#]

    # param = "pr"
    # resp = requests.get(url=URL)
    # decoded = resp.content.decode("utf-8")
    # cr = csv.reader(decoded.splitlines(), delimiter=',')
    # my_list = list(cr)
    # rainfall = []
    # for index, row in enumerate(my_list):
    #     if index == 0:
    #         continue
    #     if index > 13:
    #         break
    #     rainfall.append(row[0])

    # Getting the current temperature (if Current=true in Input)
    current_weather_url = "http://api.openweathermap.org/data/2.5/weather?lat="+latitude +"&lon="+longitude +"&appid=b9bb7acaa4566f8f7de584f90c2b12c2"
    resp = requests.get(current_weather_url)
    decoded = resp.content.decode("utf-8")
    resp = json.loads(decoded)
    #print(current_temp)
    current_temp = resp["main"]["temp"]


    # Do the prediction here using Classifier clf.
    print(crop_season)
    if(crop_season == 'Kharif'):
        nn_weight_path = 'Models\weights\kharif_crops_final.pth'
    elif(crop_season == 'Rabi'):
        nn_weight_path = 'Models\weights\rabi_crops_final.pth'
    elif(crop_season == 'Zaid'):
        nn_weight_path = 'Models\weights\zaid_crops_final.pth'
    
    production_weight_path = 'Models\weights\production_weights.sav'

    # get avg values
    temp_avg = get_avg(temps, predict_month)
    rain_avg = get_avg(rainfall, predict_month)

    # gwater calculations
    ground_water_avg = get_ground_water(ground_water, predict_month, district)
    max_area_dist = int(max_area[district])
    # print("gwater avg: {}  max_area_dist:  {}  area:  {}".format(type(ground_water_avg), type(max_area_dist), type(area)))
    gwater_available = scale_val * (float(ground_water_avg) * float(area) ) / float(max_area_dist)
    total_water = rain_avg + gwater_available

    # sow_temp
    if(is_current):
        sow_temp = current_temp
    else:
        sow_temp = temps[month_dict[predict_month]]

    # harvest temp
    harvest_temp = temps[(month_dict[predict_month]+5)%12]

    # soil paramteres
    soil = get_soil(soil_type)

    # Create parameter list
    parameteres = [[temp_avg, ph, total_water, sow_temp, harvest_temp, nitrogen, potassium, phosphorous, soil[0], soil[1], soil[2], soil[3]]]

    # create model instance
    nn_model = crop_model(crop_season)
    #load weights
    nn_model.load_weights(nn_weight_path)
    #get predictions
    pred = nn_model.get_predictions(parameteres)
    pred = pred.detach().numpy()

    # get top_3 predictions
    nn_model.get_top_n_predictions(pred, 3)

    print(nn_model.max_pred_array)

    # Crop Price Prediction
    crop = [str(nn_model.max_pred_array[0][1]), str(nn_model.max_pred_array[1][1]), str(nn_model.max_pred_array[2][1])]
    price_model = Production(crop, int(area), production_weight_path)

    #calculate the production and price and also display
    price_model.calculate_production_price() 

    print(price_model.prod_arr)



    # Making the response message
    response = {
        "predict": [
            {
                "crop": nn_model.max_pred_array[0][1],
                "yield_percent": nn_model.max_pred_array[0][0],
                "production": price_model.prod_arr[0][0],
                "price": price_model.prod_arr[0][1]
            },
            {
                "crop": nn_model.max_pred_array[1][1],
                "yield_percent": nn_model.max_pred_array[1][0],
                "production": price_model.prod_arr[1][0],
                "price": price_model.prod_arr[1][1]
            },
            {
                "crop": nn_model.max_pred_array[2][1],
                "yield_percent": nn_model.max_pred_array[2][0],
                "production": price_model.prod_arr[2][0],
                "price": price_model.prod_arr[2][1]
            }
        ]
    }
    return jsonify(response) # send to app


if __name__ == '__main__':

    f = open('../dataset/ground_water_dic.pkl','rb')
    ground_water = pickle.load(f)
    f.close()
    
    f = open('../dataset/max_area_groundwater.pkl','rb')
    max_area = pickle.load(f)
    f.close()
    
    app.run()