from .routes import detections

import unittest
import json
from fastapi.testclient import TestClient
from fastapi import FastAPI


app = FastAPI(title="challenge", docs_url="/")
app.include_router(detections.router, prefix="/detections")
app.host("0.0.0.0", "api.app:app")

client = TestClient(app)

def test_event_motion_detections():
    response = client.get("/motion")
    assert response.status_code == 200
    first_item = next(response.iter_lines())
    first_json = json.loads(first_item)
    assert 'time' in first_json
    assert 'velocity' in first_json

def test_event_object_detections():
    response = client.get("/objects")
    assert response.status_code == 200
    first_item = next(response.iter_lines())
    first_json = json.loads(first_item)
    assert 'time' in first_json
    assert 'object_type' in first_json

def test_event_detections():
    response = client.get("/")
    assert response.status_code == 200
    first_item = next(response.iter_lines())
    first_json = json.loads(first_item)
    assert 'time' in first_json
    assert 'velocity' in first_json and 'object_type' in first_json


if __name__ == '__main__':
    unittest.main()
