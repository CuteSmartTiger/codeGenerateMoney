import time

from app.execution.execution import Execution



if __name__ == '__main__':
    while True:
        execution = Execution()
        execution.execute('strategy_one')
        time.sleep(60*20)