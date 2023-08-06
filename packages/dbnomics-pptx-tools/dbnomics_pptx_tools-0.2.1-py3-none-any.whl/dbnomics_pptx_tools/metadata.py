from __future__ import annotations

from enum import Enum
from typing import Literal, TypeAlias

from pydantic import BaseModel, Field

__all__ = ["DataLabelPosition", "PresentationMetadata", "SlideMetadata"]


class DataLabelPosition(Enum):
    LAST_POINT = "last_point"


ChartName: TypeAlias = str
SeriesId: TypeAlias = str
SlideName: TypeAlias = str
TableLocation: TypeAlias = str


class ChartOrTableSeriesSpec(BaseModel):
    id: str
    name: str
    tag: str | None = None

    def has_tag(self, tag: str | None) -> bool:
        return tag == self.tag


class TableSpec(BaseModel):
    series: list[ChartOrTableSeriesSpec]

    def find_series_id_by_name(self, series_name: str, *, tag: str | None = None) -> str | None:
        """Find series ID by its name.

        When tag is None, return the series without a tag (and not any tag).
        """
        for series_spec in self.series:
            if series_spec.name == series_name and series_spec.has_tag(tag):
                return series_spec.id
        return None

    def find_series_spec(self, series_id: str) -> ChartOrTableSeriesSpec | None:
        for series_spec in self.series:
            if series_spec.id == series_id:
                return series_spec
        return None

    def get_series_ids(self) -> set[str]:
        return {series_id_or_spec.id for series_id_or_spec in self.series}


DataLabelPositionT: TypeAlias = Literal["last_point"]


class ChartSpec(TableSpec):
    data_labels: list[DataLabelPositionT] = Field(default_factory=list)


class SlideMetadata(BaseModel):
    charts: dict[ChartName, ChartSpec] = Field(default_factory=dict)
    tables: dict[TableLocation, TableSpec] = Field(default_factory=dict)

    def get_series_ids(self) -> set[str]:
        series_ids = set()
        for chart_spec in self.charts.values():
            series_ids |= set(chart_spec.get_series_ids())
        for table_spec in self.tables.values():
            series_ids |= set(table_spec.get_series_ids())
        return series_ids


class PresentationMetadata(BaseModel):
    slides: dict[SlideName, SlideMetadata]

    def get_slide_series_ids(self) -> set[str]:
        result = set()
        for slide in self.slides.values():
            result |= slide.get_series_ids()
        return result
