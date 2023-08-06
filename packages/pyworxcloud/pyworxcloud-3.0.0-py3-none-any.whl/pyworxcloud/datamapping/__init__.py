"""Datamapping module."""
from __future__ import annotations

from datetime import datetime

from ..status import ErrorMap, StatusMap
from .maps import MAP, TIMESTAMPS

DATE_FORMATS = [
    "%Y-%m-%d %H:%M:%S",
    "%d-%m-%Y %H:%M:%S",
    "%Y/%m/%d %H:%M:%S",
    "%d/%m/%Y %H:%M:%S",
]


def _recursive(key: str, value: str, parent: dict, debug: bool = False) -> dict:
    """Recursive mapping."""
    ovalue = value

    dataset: dict = {}
    for key, value in ovalue.items():
        if isinstance(value, dict):
            if key in parent["sub"]:
                dataset.update(
                    {
                        parent["sub"][key]["name"]: _recursive(
                            key, value, parent["sub"][key], debug
                        )
                    }
                )
            elif debug:
                dataset.update({key: value})
        else:
            if key in parent["sub"]:
                dataset.update({parent["sub"][key]["name"]: value})
            elif debug:
                dataset.update({key: value})

    return dataset


def DataMap(data: dict, debug: bool = False) -> dict | None:
    """Map data to properties."""
    dataset = {}

    if "last_status" in data:
        last_data = data.pop("last_status")["payload"]
        for key, value in last_data.items():
            if isinstance(value, dict):
                if key in MAP:
                    if key in TIMESTAMPS:
                        value = TimeStringToObject(value)
                    dataset.update(_recursive(key, value, MAP[key]))
                elif debug:
                    dataset.update({key: value})
            else:
                if key in MAP:
                    if key in TIMESTAMPS:
                        value = TimeStringToObject(value)
                    dataset.update({MAP[key]["name"]: value})
                elif debug:
                    dataset.update({key: value})

    for key, value in data.items():
        if isinstance(value, dict):
            if key in MAP:
                if key in TIMESTAMPS:
                    value = TimeStringToObject(value)
                if not "initial" in MAP[key]:
                    dataset.update(_recursive(key, value, MAP[key], debug))
                else:
                    dataset.update({key: value})
            elif debug:
                dataset.update({key: value})
        else:
            if key in MAP:
                if key in TIMESTAMPS:
                    value = TimeStringToObject(value)
                if not "initial" in MAP[key]:
                    dataset.update({MAP[key]["name"]: value})
                else:
                    dataset.update({key: value})
            elif debug:
                dataset.update({key: value})

    dataset.update(
        {
            "last_update": TimeStringToObject(
                f"{dataset.pop('date')} {dataset.pop('time')}"
            )
        }
    )
    dataset.update(
        {
            "status_description": StatusMap[dataset["status_code"]]
            if dataset["status_code"] in StatusMap
            else "Unknown",
            "error_description": ErrorMap[dataset["error_code"]]
            if dataset["error_code"] in ErrorMap
            else "Unknown",
        }
    )
    return dataset


def TimeStringToObject(time: str) -> datetime:
    """Convert a time string to a datetime object."""
    for format in DATE_FORMATS:
        try:
            dt_object = datetime.strptime(time, format)
        except ValueError:
            pass
        except TypeError:
            # Something wasn't right with the provided string, just return it as it was
            dt_object = time

    return dt_object
