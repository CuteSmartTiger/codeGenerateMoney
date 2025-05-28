import datetime
import json
import time

from app.real_data.okex import get_index_data,calculate_index_data
from app.strategy.strategy_one import meet_strategy_one

from app.notification.lark import trigger_lark

from app.config import indexIds

class Execution:
    def __init__(self):
        pass

    @staticmethod
    def execute(strategy_name):
        if strategy_name == 'strategy_one':

            try:
                for instId in indexIds:
                    print("循环中", instId)
                    data = get_index_data(instId)
                    df = calculate_index_data(data)
                    if meet_strategy_one(df):
                        msg = "{} {} 有上涨趋势 ".format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), instId)
                        body_data = {'instId': instId,
                                     'bar': '4H',
                                     'timeId': df['beijing'].iloc[0],
                                     'profit': json.loads(df.to_json())['profit'],
                                     'amplitudeRatio': json.loads(df.to_json())['amplitudeRatio'],
                                     'msg': msg
                                     }

                        trigger_lark(body_data)
                    else:
                        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), "{} 没有上涨趋势".format(instId))
                    time.sleep(2)
            except Exception as e:
                print(e)
