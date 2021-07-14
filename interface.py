from flask import request, jsonify, Flask
import pandas as pd
from flask_cors import CORS
app = Flask(__name__)
CORS(app, resources=r'/*',supports_credentials=True)	# 注册CORS, "/*" 允许访问所有api


'''
输入如下所示格式的dataframe
   news_title          news_content
0  四川大学毕业典礼       四川大学毕业典礼盛大举行
1  四川攀枝花旅游旺季     四川攀枝花旅游旺季
2  四川大学留学xxx人     四川大学留学xxx人
返回如下所示格式的dataframe
  result
0     教育
1     旅游
2     国际
'''
def getPrediction(news_info):
    pass

    '''
    news_info这个变量是如上面的注释所示的格式的dataframe，也就是说lz你收到的news的形式会是这样的，然后你针对这个news_info进行预测
    预测结果以list[str]的形式，存放在result_list这个变量里，如下面的result_list所示，然后你我之间的交接就完成了
    '''

    result_list = ['教育','旅游','国际']
    result_pd = pd.DataFrame(result_list)
    result_pd.columns=['result']
    return result_pd

'''
在body内传输json格式的数据，格式如下所示
{"news":
    [
        {"news_title":"四川大学毕业典礼","news_content":"四川大学毕业典礼盛大举行"},
        {"news_title":"四川攀枝花旅游旺季","news_content":"四川攀枝花旅游旺季"},
        {"news_title":"四川大学留学xxx人","news_content":"四川大学留学xxx人"}
    ] 
}
获取到的返回值如下所示：
{"predict_results": 
    [
        {"result":"教育"},
        {"result":"旅游"},
        {"result":"国际"}
    ] 
}
'''
@app.route('/uploadJson', methods=["POST"])
def uploadJson():
    raw_data = request.get_json()  # 获取 JSON 数据
    news_data = pd.DataFrame(raw_data['news'])  # 获取参数并转变为 DataFrame 结构

    # 经过处理之后得到要传回的数据
    res = getPrediction(news_data)

    # 将 DataFrame  数据再次打包为 JSON 并传回
    res = '{{"predict_results": {} }}'.format(res.to_json(orient="records", force_ascii=False))
    return res


'''
在form-data中添加一个叫file的文件csv，里面为:
   news_title          news_content
0  四川大学毕业典礼       四川大学毕业典礼盛大举行
1  四川攀枝花旅游旺季     四川攀枝花旅游旺季
2  四川大学留学xxx人     四川大学留学xxx人
返回的格式为
返回如下所示格式的dataframe
  result
0     教育
1     旅游
2     国际
'''
@app.route('/uploadCsv', methods=['POST'])
def uploadCsv():
    import pandas as pd
    csv_data = pd.read_csv(request.files['file'],index_col=0)
    print(csv_data)
    # 经过处理之后得到要传回的数据
    res = getPrediction(csv_data)

    # 将 DataFrame  数据再次打包为 JSON 并传回
    res = '{{"predict_results": {} }}'.format(res.to_json(orient="records", force_ascii=False))
    return res

if __name__ == '__main__':
    app.run(port=8848)