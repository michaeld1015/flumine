from typing import Type
from betfairlightweight import filters
from betfairlightweight.resources import MarketBook, RaceCard, CurrentOrders

from ..streams.marketstream import BaseStream, MarketStream

DEFAULT_MARKET_DATA_FILTER = filters.streaming_market_data_filter(
    fields=[
        "EX_ALL_OFFERS",
        "EX_TRADED",
        "EX_TRADED_VOL",
        "EX_LTP",
        "EX_MARKET_DEF",
        "SP_TRADED",
        "SP_PROJECTED",
    ]
)


class Strategies:
    def __init__(self):
        self._strategies = []

    def __call__(self, strategy):
        self._strategies.append(strategy)
        strategy.start()

    def __iter__(self):
        return iter(self._strategies)

    def __len__(self):
        return len(self._strategies)


class BaseStrategy:
    def __init__(
        self,
        market_filter: dict,
        market_data_filter: dict = None,
        streaming_timeout: float = None,
        conflate_ms: int = None,
        stream_class: Type[BaseStream] = MarketStream,
        name: str = None,
    ):
        self.market_filter = market_filter
        self.market_data_filter = market_data_filter or DEFAULT_MARKET_DATA_FILTER
        self.streaming_timeout = streaming_timeout
        self.conflate_ms = conflate_ms
        self.stream_class = stream_class
        self._name = name

        self.streams = []  # list of streams strategy is subscribed

    def check_market(self, market_book: MarketBook) -> bool:
        if market_book.streaming_unique_id not in self.stream_ids:
            return False  # strategy not subscribed to market stream
        elif self.check_market_book(market_book):
            return True
        else:
            return False

    def start(self) -> None:
        # called when flumine starts e.g. subscribe to extra streams
        return

    def check_market_book(self, market_book: MarketBook) -> bool:
        # process_market_book only executed if this returns True
        return False

    def process_market_book(self, market_book: MarketBook) -> None:
        # process marketBook; place/cancel/replace orders
        return

    def process_raw_data(self, publish_time: int, datum: dict) -> None:
        return

    def process_race_card(self, race_card: RaceCard) -> None:
        # process raceCard object
        return

    def process_orders(self, orders: CurrentOrders) -> None:
        # process currentOrders object
        return

    def finish(self) -> None:
        # called before flumine ends
        return

    @property
    def stream_ids(self) -> list:
        return [stream.stream_id for stream in self.streams]

    @property
    def name(self):
        return self._name or self.__class__.__name__

    def __str__(self):
        return "{0}".format(self.name)
