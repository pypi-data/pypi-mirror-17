# -*- coding: utf-8 -*-
u"""
Created on 2015-7-31

@author: cheng.li
"""

try:
    import Queue as queue
except ImportError:
    import queue

import time
import numpy as np
from PyFin.Env import Settings
from AlgoTrading.Enums import PortfolioType
from AlgoTrading.Execution.OrderBook import OrderBook
from AlgoTrading.Execution.FilledBook import FilledBook
from AlgoTrading.Strategy import Strategy
from AlgoTrading.Assets import XSHGStock
from AlgoTrading.Assets import XSHEStock
from AlgoTrading.Assets import IFFutures
from AlgoTrading.Assets import ICFutures
from AlgoTrading.Assets import IHFutures
from AlgoTrading.Assets import TFFutures
from AlgoTrading.Assets import TFutures
from AlgoTrading.Assets import RUFutures
from AlgoTrading.Assets import RBFutures
from AlgoTrading.Assets import AFutures
from AlgoTrading.Assets import YFutures
from AlgoTrading.Assets import TAFutures
from AlgoTrading.Assets import EXIndex


ASSETS_MAPPING = {
    ('', 'xshg'): XSHGStock,
    ('', 'xshe'): XSHEStock,
    ('', 'zicn'): EXIndex,
    ('if', 'ccfx'): IFFutures,
    ('ic', 'ccfx'): ICFutures,
    ('ih', 'ccfx'): IHFutures,
    ('tf', 'ccfx'): TFFutures,
    ('t', 'ccfx'): TFutures,
    ('ru', 'xsge'): RUFutures,
    ('rb', 'xsge'): RBFutures,
    ('a', 'xdce'): AFutures,
    ('y', 'xdce'): YFutures,
    ('ta', 'xzce'): TAFutures,
}


def setAssetsConfig(symbolList):
    res = {}
    for s in symbolList:
        code_com = s.split('.')
        code = ''.join(filter(str.isalpha, code_com[0]))
        exchange = code_com[-1]
        key = (code, exchange)

        res[s] = ASSETS_MAPPING[key]
    return res


class Backtest(object):

    def __init__(self,
                 initial_capital,
                 heartbeat,
                 data_handler,
                 execution_handler,
                 portfolio,
                 strategy,
                 logger,
                 benchmark=None,
                 refreshRate=1,
                 plot=False,
                 portfolioType=PortfolioType.CashManageable,
                 strategyParameters=()):
        self.initialCapital = initial_capital
        self.heartbeat = heartbeat
        self.dataHandler = data_handler
        self.executionHanlderCls = execution_handler
        self.portfolioCls = portfolio
        self.strategyCls = strategy
        self.strategyParameters = strategyParameters
        self.symbolList = self.dataHandler.whole_symbols
        self.tradable = self.dataHandler.allTradableAssets
        self.assets = setAssetsConfig(self.tradable)
        self.events = queue.Queue()
        self.dataHandler.setEvents(self.events)
        self.signals = 0
        self.num_strats = 1
        self.benchmark = benchmark
        self.refreshRate = refreshRate
        self.counter = 0
        self.plot = plot
        self.logger = logger
        self.portfolioType = portfolioType

        if portfolioType == PortfolioType.FullNotional:
            self.initialCapital = np.inf

        self._generateTradingInstance()

    def _generateTradingInstance(self):
        Settings.defaultSymbolList = self.symbolList
        if isinstance(self.strategyCls, Strategy):
            self.strategy = self.strategyCls
        else:
            self.strategy = self.strategyCls(*self.strategyParameters)
        self.strategy.events = self.events
        self.strategy.bars = self.dataHandler
        self.strategy.symbolList = self.symbolList
        self.strategy.logger = self.logger
        self.portfolio = self.portfolioCls(self.dataHandler,
                                           self.events,
                                           self.dataHandler.getStartDate(),
                                           self.assets,
                                           self.initialCapital,
                                           self.benchmark,
                                           self.portfolioType)
        self.executionHanlder = self.executionHanlderCls(self.events, self.dataHandler, self.portfolio, self.logger)
        self.portfolio.orderBook = OrderBook(self.logger)
        self.filledBook = FilledBook()
        self.portfolio.filledBook = self.filledBook
        self.strategy._port = self.portfolio
        self.strategy._posBook = self.portfolio.positionsBook

    def _runBacktest(self):
        i = 0
        while True:
            i += 1
            if self.dataHandler.continueBacktest:
                self.dataHandler.checkingDayBegin()
                self.strategy.symbolList, self.strategy.tradableAssets = self.dataHandler.updateBars()
            else:
                break

            while True:
                try:
                    event = self.events.get(False)
                except queue.Empty:
                    break
                if event is not None:
                    if event.type == 'MARKET':
                        self.counter += 1
                        self.strategy._updateTime()
                        self.strategy._updateSubscribing()
                        self.portfolio.updateTimeindex()
                        # update still alive orders
                        for order in self.portfolio.orderBook:
                            if order.symbol in self.strategy.tradableAssets:
                                self.executionHanlder.executeOrder(order,
                                                                   self.assets[order.symbol],
                                                                   self.portfolio.orderBook,
                                                                   self.portfolio)
                        if self.counter % self.refreshRate == 0:
                            self.strategy._handle_data()
                    elif event.type == 'SIGNAL':
                        self.signals += 1
                        self.portfolio.updateSignal(event)
                    elif event.type == 'ORDER':
                        self.portfolio.orderBook.updateFromOrderEvent(event)
                        self.executionHanlder.executeOrder(event.to_order(),
                                                           self.assets[event.symbol],
                                                           self.portfolio.orderBook,
                                                           self.portfolio)
                        self.strategy.handle_order(event)
                    elif event.type == 'FILL':
                        self.strategy.handle_fill(event)
                    elif event.type == 'DAYBEGIN':
                        self.strategy.checkingPriceLimit()
                        self.strategy.current_datetime = event.timeIndex
                        self.portfolio.cancelOrders(event.timeIndex, self.strategy._posBook)
                        self.strategy.day_begin()
            time.sleep(self.heartbeat)

    def _outputPerformance(self):

        self.portfolio.createEquityCurveDataframe()
        perf_metric, perf_df, rollingRisk, aggregated_positions, transactions, turnover_rate = \
            self.portfolio.outputSummaryStats(self.portfolio.equityCurve, self.plot)
        return self.portfolio.equityCurve, \
               self.portfolio.orderBook.view(), \
               self.filledBook.view(), \
               perf_metric, perf_df, \
               rollingRisk, \
               aggregated_positions, \
               transactions, \
               turnover_rate, \
               self.strategy.infoView()

    def simulateTrading(self):
        self.logger.info("Start backtesting...")
        self.strategy._subscribe()
        self._runBacktest()
        self.logger.info("Backesting finished!")
        return self._outputPerformance()
