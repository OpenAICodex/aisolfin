"""AgGrid wrapper matching Base44 behaviour."""
from __future__ import annotations

from typing import Any, Dict, Optional

import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

from tokens import THEME


DEFAULT_PAGE_SIZE = 10


def _base_grid_options(data: pd.DataFrame, enable_sidebar: bool) -> Dict[str, Any]:
    builder = GridOptionsBuilder.from_dataframe(data)
    builder.configure_default_column(
        resizable=True,
        sortable=True,
        filter=True,
        floatingFilter=True,
    )
    builder.configure_grid_options(
        rowHeight=int(THEME.spacing.scale["500"].replace("px", "")),
        headerHeight=int(THEME.spacing.scale["400"].replace("px", "")),
        suppressRowClickSelection=True,
        rowSelection="multiple",
        pagination=True,
        paginationPageSize=DEFAULT_PAGE_SIZE,
        sideBar="columns" if enable_sidebar else False,
    )
    return builder.build()


def data_table(
    data: pd.DataFrame,
    key: str,
    page_size: int = DEFAULT_PAGE_SIZE,
    height: Optional[int] = None,
    enable_sidebar: bool = False,
    grid_options: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Render the data table and return the AgGrid response."""

    if data.empty:
        from .empty_state import empty_state

        empty_state(
            title="No results",
            description="Adjust your filters or add new records to populate the table.",
        )
        return {}

    options = grid_options or _base_grid_options(data, enable_sidebar)
    options["paginationPageSize"] = page_size

    return AgGrid(
        data,
        gridOptions=options,
        height=height,
        key=key,
        enable_enterprise_modules=False,
        theme="streamlit",
        allow_unsafe_jscode=False,
    )
