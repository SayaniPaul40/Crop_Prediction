# Lets_HackIT  

This repo is maintained for the purpose of **Gov-Techthon 2020** by Team : **Lets_HackIT**  
The problem statement focuses on promoting crop recomendation/rotating to help farmers overcome the obtacles and difficulties encountered during farming .So we have tried to come up with the best possible solution from our side to overcome this problem statement by making use of modern technologies.  


## Workflow of the entire solution  
![](https://github.com/shan515/Lets_HackIT/blob/images/assets/process-2.png)  
                           
## The solution is divided into 5 major aspects  
  - [Front end](#front-end)
  - [Data analysis and generation](#data-analysis-and-generation)
  - [AI/ML](#aiml)
  - [App Deployment](#deployement-backend)
  - [Outputs](#output)
  - [To DO](#to-do)
  - [Contributers](#made-with-heart-by)
  
### Front End  
- User Friendly  
  -  SELECT THE MONTH/SEASON 
  -  TYPE OF SOIL
  -  AREA OF FARM 
  -  BILINGUAL SUPPORT IN ENGLISH AND HINDI.  
 - Location  
   - GPS TO GET LATITUDE AND LONGITUDE AUTOMATICALLY  
 - IOT Sensor  
   - N,P,K  
   - Soil pH  
 - Prediction  
   - crop + Prediction  
   - Yield  
   - PDF containing the information of predicted crop  
 - Connect  
   - Agricultural agencies  
   - Agricultural resources/links  
 - History  
   - List and information of previously grown crops   
   
 <img src="assets/input_page.jpeg" width="325"/>      <img src="assets/iot_page.jpeg" width="325"/>   
 
   
   
 ### Data Analysis and Generation  
 - The data required for this model was a combination of data from:  
   - Kaggle : State Name, District Name, Season of cropping , Area, Production, Crop.  
   - Synthetic Data : Teperature range, Sowing temperature, Harvesting Temperature, pH, Nitrogen-Phosphorous-Potassium, Soil type , Water resource.  
   - Forecast Data : Weather/rainfall forecast data , Ground water and Irrigation.  
   ![](https://github.com/shan515/Lets_HackIT/blob/images/assets/sns.png)  
  
 
### AI/ML 
  NEURAL NETWORK PROVIDES A MORE ACCURATE WAY OF DEALING WITH DATASETS WHERE THERE ARE MANY INTERSECTIONS LIKE THE ONE ON WHICH WE ARE WORKING ON.  
  - The Neural Network consists of  
    - 12 input parameteres  
    - 2 Hidden layers each having 64 units  
    - Softmax function at the output  
    - The model attained an accuracy of ariund 99.3% as shown below:  
    
    ![](https://github.com/shan515/Lets_HackIT/blob/images/assets/WhatsApp%20Image%202020-11-01%20at%207.24.56%20AM.jpeg)





### Deployement (Backend)    
- Python Flask Server  

- Exposes a route for Predictions (/predict)  

- External API calls for - Current/Forecasted Weather and Rainfall  

- Returns a JSON for predicted crop with probability.   


## Output

### Postman Test
<img src="assets/postman.png" width="625"/> 

### App Output
<img src="assets/output_app.jpeg" width="425"/> 

### Additional Output (Auto-Genereated)  
![PDF File of Output](https://github.com/shan515/Lets_HackIT/blob/images/assets/Arhar_Tur_eng.pdf)


## To Do
- We have deployed the app on Oracle cloud. There are sme minor issues which have to be fixed. 
- Add disease recognition using computer vision
- Find nearest crop mandal for farmer

## Made with :heart: by:
- [Sravan Chittupalli](https://github.com/SravanChittupalli) :smile:
- [Shantanu Pande](https://github.com/shan515)  :smiley:
- [Twisha Shah](https://github.com/high-functioning-sociopath) :innocent:
- [Prithvi Shirke](https://github.com/prithvi1809)  :sunglasses:
- [Khushal Shah](https://github.com/KhushalPShah) :raised_hands:

  
      
      
 
