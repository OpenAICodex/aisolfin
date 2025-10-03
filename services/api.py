"""API client abstractions for the Base44 Streamlit port."""
from __future__ import annotations

import random
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List

import pandas as pd
import streamlit as st

from tokens import THEME


class APIError(RuntimeError):
    """Normalized exception raised when an API request fails."""

    def __init__(self, message: str, status_code: int | None = None):
        super().__init__(message)
        self.status_code = status_code


@dataclass(frozen=True)
class Process:
    id: str
    name: str
    owner: str
    status: str
    throughput: float
    efficiency: float
    updated_at: datetime


@dataclass(frozen=True)
class Metric:
    label: str
    value: float
    unit: str
    trend: float


class ApiClient:
    """Mocked API client with retry/backoff semantics."""

    def __init__(self, max_retries: int = 3, backoff_factor: float = 0.3):
        self.max_retries = max_retries
        self.backoff_factor = backoff_factor

    def _with_retry(self, fn, *args, **kwargs):
        last_error: Exception | None = None
        for attempt in range(self.max_retries):
            try:
                return fn(*args, **kwargs)
            except Exception as exc:  # noqa: BLE001 - normalized below
                last_error = exc
                sleep_time = self.backoff_factor * (2**attempt)
                time.sleep(sleep_time)
        raise APIError(str(last_error) if last_error else "Unknown error")

    def list_processes(self) -> List[Process]:
        return self._with_retry(_generate_processes)

    def list_metrics(self) -> List[Metric]:
        return self._with_retry(_generate_metrics)

    def process_history(self) -> pd.DataFrame:
        return self._with_retry(_generate_history)


def _generate_processes() -> List[Process]:
    now = datetime.utcnow()
    processes: List[Process] = []
    for idx in range(1, 9):
        processes.append(
            Process(
                id=f"PRC-{idx:03d}",
                name=f"Optimization Stream {idx}",
                owner=random.choice(["Amelia", "Noah", "Evelyn", "Kai"]),
                status=random.choice(["Active", "Monitoring", "Paused"]),
                throughput=round(random.uniform(120, 320), 1),
                efficiency=round(random.uniform(0.65, 0.98), 2),
                updated_at=now - timedelta(hours=random.randint(1, 72)),
            )
        )
    return processes


def _generate_metrics() -> List[Metric]:
    return [
        Metric("Daily Throughput", 286.0, "units", +4.2),
        Metric("Yield", 0.82, "ratio", +1.1),
        Metric("Cycle Time", 6.4, "hrs", -0.6),
        Metric("Cost per Unit", 14.3, "USD", -0.9),
    ]


def _generate_history() -> pd.DataFrame:
    now = datetime.utcnow()
    data = {
        "timestamp": [now - timedelta(days=idx) for idx in range(30)][::-1],
        "throughput": [round(random.uniform(180, 320), 1) for _ in range(30)],
    }
    return pd.DataFrame(data)


@st.cache_data(ttl=THEME.cache.ttl_seconds, max_entries=THEME.cache.max_entries)
def fetch_processes(client: ApiClient) -> List[Process]:
    return client.list_processes()


@st.cache_data(ttl=THEME.cache.ttl_seconds, max_entries=THEME.cache.max_entries)
def fetch_metrics(client: ApiClient) -> List[Metric]:
    return client.list_metrics()


@st.cache_data(ttl=THEME.cache.ttl_seconds, max_entries=THEME.cache.max_entries)
def fetch_history(client: ApiClient) -> pd.DataFrame:
    return client.process_history()
