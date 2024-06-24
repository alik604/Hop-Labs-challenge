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


def objects_data_generator():
    df = pd.read_parquet("../44746f8e-c3d6-4cd0-8fbc-dcd03a159a77.object_detections.parquet")
    df['time'] = df['time'].astype('int64') // 10 ** 9
    for _, row in df.iterrows():
        row = dict(row)
        for k, v in row.items():
            if isinstance(v, np.ndarray):
                if isinstance(v[0], np.ndarray):
                    row[k] = [list(bbox) for bbox in v]
                else:
                    row[k] = list(v)
        yield json.dumps(row)


@router.get("/objects")
async def event_object_detections() -> StreamingResponse:
    """
    This returns a stream of json objects.

    Implement this endpoint.

    Each JSON object contains the time, and any detected objects"""
    ...

    gen = objects_data_generator()
    return StreamingResponse(gen)


def objects_motion_data_generator():
    # Don't hard code like this IRL...
    df_motion = pd.read_parquet("../44746f8e-c3d6-4cd0-8fbc-dcd03a159a77.motion_data.parquet")
    df_object = pd.read_parquet("../44746f8e-c3d6-4cd0-8fbc-dcd03a159a77.object_detections.parquet")

    # convert from unix time to datatime. Adjust for 4h timezone diff
    df_motion['time'] = pd.to_datetime(df_motion['time'] - (4 * 3600 * 1000), unit='ms')
    df_object['time'] = df_object['time'].dt.round('ms')

    # merge the above two dfs
    # TODO consider right join to prevent losing an object_detections thats out of scope or eaten up due to rounding (the latter is a edge case expected if in prod, but not seen here. see README)
    df = pd.merge(df_motion, df_object, on='time', how='inner')

    df_types = pd.read_parquet("../object_types.parquet")
    mapping = df_types.set_index('object_code').to_dict()['object_type_name']

    # apply the mapping
    df['object_type'] = df['object_type'].map(mapping)

    # convert time to timestamp
    df['time'] = df['time'].astype('int64') // 10 ** 9

    # might be better to do the above JIT, as that's the point of a generator.
    # compared to opening the parquet, these transformations are not that expensive; Better to do them all at once rather than row by row in the generator.

    for _, row in df.iterrows():
        row = dict(row)
        for k, v in row.items():
            if isinstance(v, np.ndarray):
                if isinstance(v[0], np.ndarray):
                    row[k] = [list(bbox) for bbox in v]
                else:
                    row[k] = list(v)
        yield json.dumps(row)


@router.get("/")
async def event_detections() -> StreamingResponse:
    """
    This returns a stream of json objects.

    Implement this endpoint.

    Each JSON object contains the time, and any detected motion and/or objects
    """
    ...

    gen = objects_motion_data_generator()
    return StreamingResponse(gen)
