from stock import db, stocktickercom
res=db.session.query(stocktickercom)
#this code is for checking the tickers folks have tried on the app. 70 tickers as of wednesday. run this on terminal with python3 <filename>
for row in res:
    #print(row) #to see count as last print
    print(row,row.ticker)