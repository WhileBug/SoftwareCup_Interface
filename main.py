from flask import Flask
from flask import request
import pandas as pd
from flask_csv import send_csv
app = Flask(__name__)

def getQueryInfo(queryStr):
    if(' and ' in queryStr):
        return queryStr.split(' and '), 'and'
    elif(' or ' in queryStr):
        return queryStr.split(' or '), 'or'
    else:
        return [], 'error'

def getCsv():
    databasePd = pd.read_csv("database.csv", index_col=0)
    return databasePd

def judgeExpression(query, database):
    if('==' in query):
        queryObjects = query.split("==")
        varName = queryObjects[0]
        varVal = eval(queryObjects[1])
        return set(database[database[varName] == varVal].index.tolist())
    if ('!=' in query):
        queryObjects = query.split("!=")
        varName = queryObjects[0]
        varVal = eval(queryObjects[1])
        return set(database[database[varName] != varVal].index.tolist())
    if ('$=' in query):
        queryObjects = query.split("$=")
        print(queryObjects)
        varName = queryObjects[0]
        varVal = eval(queryObjects[1])
        tempIndex = []
        for i in database.index:
            if(database.loc[i,varName].lower()==varVal.lower()):
                tempIndex.append(i)
        return set(tempIndex)
    if ('&=' in query):
        queryObjects = query.split("&=")
        varName = queryObjects[0]
        varVal = eval(queryObjects[1])
        tempIndex = []
        for i in database.index:
            if (varVal in database.loc[i, varName].lower()):
                tempIndex.append(i)
        return set(tempIndex)
    return set()

def judgeAnd(queryList, database):
    tempIndex = set(database.index.tolist())
    for query in queryList:
        tempIndex = tempIndex.intersection(judgeExpression(query, database))
    return tempIndex

def judgeOr(queryList, database):
    tempIndex = set()
    for query in queryList:
        tempIndex = tempIndex | judgeExpression(query, database)
    return tempIndex

@app.route('/', methods=['GET', 'POST'])
def query():
    # get the query args
    queryStr = request.args.get("query")
    # get the content of csv file
    database = getCsv()
    # split the query args into list
    queryList, tip = getQueryInfo(queryStr)
    print(queryList)
    if(tip=='error'):
        return "Error in parse the quey"
    if(tip=='and'):
        resIndex = judgeAnd(queryList, database)
    if(tip=='or'):
        resIndex = judgeOr(queryList, database)
    resultPd = database.loc[list(resIndex),database.columns]
    resutlList = resultPd.to_dict(orient="records")
    return send_csv(resutlList, "{}.csv".format("result"), database.columns)

if __name__ == '__main__':
    app.run(port=8848)