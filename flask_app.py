#import a liberary
from flask import Flask,render_template,request
import joblib
import pandas as pd

#instance of an app
app=Flask(__name__)

#loading the model

#global attr

model=joblib.load("AC_model.pkl")



@app.route('/' )
def hello():
    return render_template("form.html")
@app.route('/submit', methods=["POST"])
def form_data():

    
    dd=request.form.get('date')
    tt=int(request.form.get('temp'))
    rr=int(request.form.get('rain'))
    hh=request.form.get('holiday')

    out_para=['AC 1', 'AC 2', 'AC 3', 'AC 4', 'AC 5', 'AC 6', 'AC 7', 'AC 8', 'AC 9',
       'AC 10', 'AC 11', 'AC 12', 'AC 13', 'AC 14', 'AC 15', 'AC 16', 'AC 17',
       'AC 18']
    dd=pd.Timestamp(dd)
    mf=pd.DataFrame(range(1440),columns=["time"])
    mf["time_block"]=pd.date_range(start=dd,periods=1440,freq="T")
    if (hh=="yes"):
        mf["holiday"]=1
    else:
        mf["holiday"]=0
    mf["weekday"]=mf["time_block"].dt.weekday
    mf.set_index('time_block', inplace=True)
    mf["temp"]=tt
    mf["rain"]=rr
    mf=mf[["weekday","time","holiday","rain","temp"]]
    res={}

    for i in out_para:
        res[i]=model[i].predict(mf)
    res=pd.DataFrame(res,index=mf.index)

    
    

    return render_template("index.html",tables=[res.to_html(classes="data")],titles=res.columns.values)



#run the app
if __name__=="__main__":
    app.run(debug=True)
