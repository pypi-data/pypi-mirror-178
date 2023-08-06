from dataclasses import dataclass
from datetime import datetime
from typing import List, Literal, Optional


@dataclass
class WicaStreamProperties:
    hbflux: Optional[
        int
    ] = None  # Defines the interval in milliseconds between successive SSE 'ev-wica-server-heartbeat' messages.
    metaflux: Optional[
        int
    ] = None  # Defines the interval in milliseconds between successive SSE 'ev-wica-channel-metadata' messages.
    monflux: Optional[
        int
    ] = None  # Defines the interval in milliseconds between successive SSE 'ev-wica-channel-value' monitor value messages.
    pollflux: Optional[
        int
    ] = None  # Defines the interval in milliseconds between successive SSE 'ev-wica-channel-value' polled value messages.
    daqmode: Optional[
        Literal["poll", "monitor", "poll-monitor", "poll-and-monitor"]
    ] = None
    pollint: Optional[int] = None
    fields: Optional[List[str]] = None
    numeric_precision: Optional[int] = None
    filter: Optional[
        Literal[
            "ALL_VALUE",
            "AVERAGER",
            "CHANGE_DETECTOR",
            "LAST_N",
            "ONE_IN_M",
            "RATE_LIMITER",
        ]
    ] = None
    n: Optional[int] = None
    m: Optional[int] = None
    x: Optional[int] = None
    interval: Optional[int] = None
    deadband: Optional[float] = None


@dataclass
class WicaChannelProperties:
    daqmode: Optional[
        Literal["poll", "monitor", "poll-monitor", "poll-and-monitor"]
    ] = None
    pollint: Optional[int] = None
    fields: Optional[List[str]] = None
    filter: Optional[
        Literal[
            "ALL_VALUE",
            "AVERAGER",
            "CHANGE_DETECTOR",
            "LAST_N",
            "ONE_IN_M",
            "RATE_LIMITER",
        ]
    ] = None
    n: Optional[int] = None
    m: Optional[int] = None
    x: Optional[int] = None
    interval: Optional[int] = None
    deadband: Optional[float] = None


@dataclass
class WicaChannel:
    name: str
    properties: WicaChannelProperties = None


@dataclass
class WicaMessage(object):
    stream_id: int = None
    event: Optional[Literal["heartbeat", "metadata", "value"]] = None
    value_type: Optional[Literal["polled", "monitored"]] = None
    data: Optional[dict] = None
    time: Optional[datetime] = None
