---
theme: ../theme
class: text-center
lineNumbers: false
colorSchema: light
aspectRatio: '16/9'
canvasWidth: 800
transition: slide-left
title: "Zillionare近期更新及路线"
subtitle: "60天搭建量化知识体系"
slogan: "The Pilgrim's Progress to Zillionare"
layout: cover
---

---
clicks: 1
---
## 性能优化 - prefetch_stocks

<show at="0">

```python
class SMAStrategy(BaseStrategy):
    async def predict(
        self, frame: Frame, frame_type: FrameType, i: int, barss, **kwargs
    ):
        if barss is None:
            raise ValueError("please specify `prefetch_stocks` and `min_bars`")

        bars: Union[BarsArray, None] = barss.get(self._sec)
        if bars is None:
            raise ValueError(f"{self._sec} not found in `prefetch_stocks`")
        
        # other stuff here
        ...
```
</show>

<show at="1">

```python
# notebook
from omicron.strategy.sma import SMAStrategy
sma = SMAStrategy(
    url="", # the url of either backtest server, or trade server
    is_backtest=True,
    start=datetime.date(2023, 2, 3),
    end=datetime.date(2023, 4, 28),
    frame_type=FrameType.DAY,
)

await sma.backtest(prefetch_stocks=["600000.XSHG", min_bars=20])
```
</show>

---
---

## Lifecycle 优化

![25%](https://images.jieyu.ai/images/2023/11/strategy_life_cycle.png)

---
---
## 绘制自定义指标功能

![](https://images.jieyu.ai/images/2023/05/20230508160012.png?2)


---
---
## 回测日志

![75%](https://images.jieyu.ai/images/2023/10/zillionare-backtest-log.png)


---
---
## 层次化异常及可串行化

### TradeError
#### entrust.*
#### client.*
#### server.*

---
---
# Roadmap

## Release 2.0 with

* Omega/jq-daptor (数据本地化)
* Omicron        (行情数据读取，策略框架，绘图，回测报告，技术库,...)
* Backtesting    （回测服务）
* Trade-client   （交易客户端）
* gm-adaptor      （东财交易接口）


---
---
# Roadmap
## Release 2.1 with

* QMT 行情集成
* QMT 交易接口集成
