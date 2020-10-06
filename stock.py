from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import getstockdata
import genforecast
#import df2c3
import json
import datetime
from datetime import date


app=Flask(__name__)

#global variable
global currtick
currtick='AMZN'

#connect to db
#following line is to connect to local database
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:Postg#123@localhost/stockdb'
#following line is to connect to heroku's postgres database - copied from var settings on heroku
app.config['SQLALCHEMY_DATABASE_URI']='postgres://vbiziaiwqvfwwa:6d3ffc8b46ee383ffadf643246b843ef0540c7e0fc06c865d9000b28a157eb5f@ec2-54-165-164-38.compute-1.amazonaws.com:5432/d9iu3fcgvh8tc6'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
class stocktickercom(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    ticker=db.Column(db.String(10))
    feedback=db.Column(db.String(2000))

@app.route('/')
def index():
    #result=stocktickercom.query.all()
    result=stocktickercom.query.order_by(func.random())
    tick=result[0].ticker
    stockdt,success=getstockdata.getstockdata(tick)
    if success==0:
        tick='AMZN'
    #viz_data=df2c3.df2c3(stockdt)
    numrows=len(stockdt.index)
    #to list conversion
    #reset index to include date as first column
    re_stockdt=stockdt.reset_index()
    sh=re_stockdt.shape
    dateext=re_stockdt.Date.to_list()
    datelist=[]
    datestr=""
    for i in range(sh[0]):
        datelist.append(dateext[i].strftime("%Y-%m-%d"))
        datestr=datestr+dateext[i].strftime("%Y-%m-%d")
        if i < sh[0]-1:
            datestr=datestr+','
        #datelist.append(dateext[i].strftime("%Y-%m-%d").replace("'","\\'"))
    highlist=re_stockdt.High.to_list()
    closelist=stockdt.Close.to_list()
    openlist=stockdt.Open.to_list()
    lowlist=stockdt.Open.to_list()
    vollist=stockdt.Volume.to_list()
    global currtick
    currtick=tick
    return render_template('index.html',success=success, tick=tick, stockdt=stockdt, lowlist=lowlist, vollist=vollist, datestr=datestr, openlist=openlist, numrows=numrows, datelist=json.dumps(datelist), closelist=closelist, highlist=highlist)

@app.route('/runticker', methods = ['POST'])
def runticker():
    tick = request.form['tickername']
    if (not(tick and tick.strip())):
        return redirect(url_for('index'))
    else:
        stockdt,success=getstockdata.getstockdata(tick)
        if success==0:
            tick='AMZN'
        
        if success==1:
            #add the ticker into db for random pick next time
            t = request.form['tickername']
            tickdata=stocktickercom(ticker=t)
            db.session.add(tickdata)
            db.session.commit()

        numrows=len(stockdt.index)
        #to list conversion
        #reset index to include date as first column
        re_stockdt=stockdt.reset_index()
        sh=re_stockdt.shape
        dateext=re_stockdt.Date.to_list()
        #dateext=re_stockdt.Date
        datelist=[]
        datestr=""
        for i in range(sh[0]):
            datelist.append(dateext[i].strftime("%Y-%m-%d"))
            datestr=datestr+dateext[i].strftime("%Y-%m-%d")
            if i < sh[0]-1:
                datestr=datestr+','
                #datelist.append(dateext[i].strftime("%Y-%m-%d").replace("'","\\'"))
        highlist=re_stockdt.High.to_list()
        closelist=stockdt.Close.to_list()
        openlist=stockdt.Open.to_list()
        lowlist=stockdt.Open.to_list()
        vollist=stockdt.Volume.to_list()
        global currtick
        currtick=tick
        return render_template('index.html',success=success, tick=tick, stockdt=stockdt, lowlist=lowlist, vollist=vollist, datestr=datestr, openlist=openlist, numrows=numrows, datelist=datelist, closelist=closelist, highlist=highlist)
    


@app.route('/forecast', methods = ['POST'])
def forecast():
    #this is when the user presses forecast button - generates some stat and forecast 
    #tick2 = request.form['tickername']
    #tick='ORCL'
    tick=currtick
    if (not(tick and tick.strip())):
        return redirect(url_for('index'))
    else:
        stockdt,success=getstockdata.getstockdata(tick)
        if success==0:
            tick='AMZN'

        closeval=stockdt.Close
        closer=closeval.reset_index()
        sh=closer.shape
        closedata=closer.Close 
        min_naive, max_naive, min_poly, max_poly, min_ensem, max_ensem, min_redreg, max_redreg, y_test, testct, y_pred_naive, naive_acc, y_pred_poly, poly_acc, y_pred_ensem, ensem_acc, y_pred_redreg, redreg_acc=genforecast.genforecast(closedata) 
        # convert test data, date, each forecast - naive, trend, ensemble with exponential smoothing, reduced regression into list for charting
        #do charting in fc.html
        dateext=closer.Date.to_list()
        y_test_list=y_test.to_list()
        y_pred_naive_list= y_pred_naive.to_list()
        y_pred_poly_list=y_pred_poly.to_list()
        y_pred_ensem_list=y_pred_ensem.to_list()
        y_pred_redreg_list=y_pred_redreg.to_list()
        datelist=[]
        stpt=sh[0]-(testct)
        for i in range(stpt,sh[0]):
            datelist.append(dateext[i].strftime("%Y-%m-%d"))
        return render_template('forecast.html',min_naive=min_naive, max_naive=max_naive, min_poly=min_poly, max_poly=max_poly, min_ensem=min_ensem, max_ensem=max_ensem, min_redreg=min_redreg, max_redreg=max_redreg, tick=tick, datelist=datelist,y_test_list=y_test_list,y_pred_naive_list=y_pred_naive_list,y_pred_poly_list=y_pred_poly_list,y_pred_ensem_list=y_pred_ensem_list,y_pred_redreg_list=y_pred_redreg_list,naive_acc=naive_acc,poly_acc=poly_acc,ensem_acc=ensem_acc,redreg_acc=redreg_acc)

@app.route('/homesite', methods = ['POST'])
def homesite():
    return redirect(url_for('index'))
