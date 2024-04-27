
# OPTIMIZING RAKE FORECASTING IN FOIS

# Data exploration and Modelling file:
[Google Drive Link](https://drive.google.com/drive/folders/1ncN31YYLWbdVkMxpY8kEjxACpRXvsb77?usp=drive_link) 


## O v e r v i e w
This project focuses on optimizing freight
operations for steel production at BSP,
which involves accurately predicting the
arrival time of incoming rakes carrying
essential raw materials such as iron,
coal, limestone, and dolomite.

## But here comes the question why we need it?
### Important Terminology
Here are some basic
terms we need
understand on which
our project is based
on.

### 1.FOIS
* Government of India's Freight Operations Information System (FOIS).
* Tracks incoming rakes to BSP.
* Provides real-time data.
* Facilitates manual data input.

### 2.Wagon Rake
* Rake: Train consisting of wagons.
* Used to transport bulk materials.
* Carries raw materials like iron, coal, limestone, dolomite.
* Critical for steel production at BSP.

## Project Details
The model serves the purpose to calculate
and present an estimated time of arrival(ETA)
of freight trains that are headed to BSP from
various staions situated throughout India.

The need of this model arises due to the fact
that the train management system used by the
BSP that is provided by Indian Railways called
FOIS shows error in one of its field that is ETA.

The domain of project is ML
and Data Science. The major
work for the project has
been done on platforms like
Google Collab, Jupyter
Notebook for the ML and DS
process . The front-end has
been made using basic html,
css, js and the back-end
includes the django
framework.

 <img src="assets/Screenshot 2024-04-27 at 10.47.44 PM.png" alt="Workflow"/>

### ML Libraries
* Matplotlib
* Numpy
* Pandas
* Sk learn
* Techniques like -
* Linear Regression
* SVM
* Random Forest

###Model Evaluated
* Linear Regressor
* Support Vector Machine
* Random Forest Regressor

 <img src="assets/Screenshot 2024-04-27 at 10.58.07 PM.png" alt="Workflow"/>

Aong these three RandomForestRegressor ensemble methode showed highest accuracy with 93% and mean absolute error of 153 minutes approximately