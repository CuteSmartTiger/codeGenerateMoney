# codeGenerateMoney
1. 调研 https://www.okx.com/docs-v5/zh/#public-data-websocket-index-candlesticks-channel
2. 使用 websocket 的方式，不需要api key，较为安全
3. 一个进程实时订阅消息，并存储记录 K线
4. 一个进程，从本地 DB 读取数据，进行策略判断，将信号推送到飞书


实盘交易 实盘API交易地址如下： • REST：https://www.okx.com
 • WebSocket公共频道：wss://ws.okx.com:8443/ws/v5/public
 • WebSocket私有频道：wss://ws.okx.com:8443/ws/v5/private • WebSocket业务频道：wss://ws.okx.com:8443/ws/v5/business  模拟盘交易 目前可以进行V5 API的模拟盘交易，部分功能不支持如提币、充值、申购赎回等。 模拟盘API交易地址如下： • REST：https://www.okx.com • WebSocket公共频道：wss://wspap.okx.com:8443/ws/v5/public
 • WebSocket私有频道：wss://wspap.okx.com:8443/ws/v5/private • WebSocket业务频道：wss://wspap.okx.com:8443/ws/v5/business


# 服务启动
uvicorn app.main:app --host 0.0.0.0 --port 8000 --loop asyncio