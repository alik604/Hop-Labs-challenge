from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import json
import numpy as np
import pandas as pd

router = APIRouter()


def motion_data_generator():
    df = pd.read_parquet("../44746f8e-c3d6-4cd0-8fbc-dcd03a159a77.motion_data.parquet")
    for _, row in df.iterrows():
        row = dict(row)
        for k, v in row.items():
            if isinstance(v, np.ndarray):
                if isinstance(v[0], np.ndarray):
                    row[k] = [list(bbox) for bbox in v]
                else:
                    row[k] = list(v)
        yield json.dumps(row)


@router.get("/motion")
async def event_motion_detections() -> StreamingResponse:
    """
    This returns a stream of json objects.

    Each JSON object contains the time, and any detected motion"""
    gen = motion_data_generator()
    return StreamingResponse(gen)


@router.get("/objects")
async def event_object_detections() -> StreamingResponse:
    """
    This returns a stream of json objects.

    Implement this endpoint.

    Each JSON object contains the time, and any detected objects"""
    ...


@router.get("/")
async def event_detections() -> StreamingResponse:
    """
    This returns a stream of json objects.

    Implement this endpoint.

    Each JSON object contains the time, and any detected motion and/or objects
    """
    ...
