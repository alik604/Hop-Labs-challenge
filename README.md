# Machine Learning Engineer Technical Assessment

You have just started a client project and are inheriting a repository that was
recently created by the client's research team. This challenge is intended to
simulate working with clients. Treat the existing code as a rough draft by
someone who may or may not have a rigorous background in software engineering,
feel free to suggest or implement improvements as you see fit, as well as
identify any important questions that we may need to resolve with the client.

## Scenario

This system supports downstream consumers of computer vision models. We have two
computer vision models that generate predictions based on sensor data. One
produces object detections from a camera, meaning it predicts where an object is
within the camera's field of view and also what type of object it is detecting.
The other model detects motion: where moving objects are and in what direction
they are moving.

This repository contains a FastAPI application that will read data output from
these models and stream it to downstream consumers.

We want these data to be consumable both as separate streams, but also as a
single stream via three API endpoints (one for each model separately, and one
for the combination of the two). Toward that, we have been asked to develop an
iterator that returns a sequence containing the combination of the two data
sources. We need the data stream to be self contained so the object detection
types will need to be self-evident in the stream (without consulting the object
type lookup table as described below).

Even though the signals produced by the models are produced at different
frequencies (the motion data is produced at 100Hz and the object detection data
is produced at an irregular frequency), we need to consume the data at a fixed
time frequency, 10Hz. By this we mean the timestamps in the data should be
1/10th of a second apart. Note that this is independent of how quickly the API
streams the results. Decide on a good strategy for doing this and explain your
choice and it's implications.

### Data

For the purposes of this exercise, the data samples provided are purely
synthetic. The values isn't meaningful, their structure is what we care about.

#### Object Detections

This data contains bounding boxes, as two coordinate-pairs `(x, y)`for the top
left and bottom right of the bounding box, respectively. It also contains a
numerical code for the type of object detected as described by the following
table as well a timestamp for when the object was detected.

There is a sample of this data in the repository:
[44746f8e-c3d6-4cd0-8fbc-dcd03a159a77.object_detections.parquet](./44746f8e-c3d6-4cd0-8fbc-dcd03a159a77.object_detections.parquet)

The object types are described in a another file:
[object_types.parquet](./object_types.parquet)

#### Motion Detections

This data contains position and velocity data for detected motion. Specifically
it contains two coordinate-pairs for the bounding box as above and a velocity
vector encoded as two floating point numbers representing the `(x, y)`
components of the direction of motion. This data is timestamped with millisecond
precision.

There is a sample of this data in the repository:
[44746f8e-c3d6-4cd0-8fbc-dcd03a159a77.motion_data.parquet](./44746f8e-c3d6-4cd0-8fbc-dcd03a159a77.motion_data.parquet).

## Objective and Instructions

Your objective is to implement additional API endpoints and support future
development by adding tests. Specifically, implement the remaining endpoints in
the [detections](./detections/api/routes/detections.py) module.

Add your code to the repository as if you were going to submit a pull
request to the main branch in the repository. Then send the whole repository
back to us as a zip archive, similar to how it was sent to you.

You are provided with a runnable container image that can exercise the existing
endpoints. Again, feel free to suggest or make improvements to the development
environment as long as the container still runs and the scenario is satisfied as
described above. Be sure to tell us how to run your code and tests; do so
somewhere in the repository itself.

In summary, your deliverables are:

1. Implement the endpoints in [detections.py](./detections/api/routes/detections.py)
2. Add unit tests
3. Make any suggestions or improvements to existing code or the development
   environment; this could include identifying any important questions that you
   would ask of the client
4. Explain how you reconciled the frequency of the different data sources

## Dev notes

1. Seems like there is a 4 hour timezone diff.

2. Motion_data ends at 2024-03-14 09:00:09.999
   object_detections end at 2024-03-14 09:00:10.031
   This is why my join has 397 rather than 398.

3. Used `df_object['time'].dt.round('ms')` to reconcile the frequency of the different data sources.
   I didn't go deep into confirming if everything is correct (capping project at 3 hours... Docker issues).
   Looks like it's working.

4. Not seen here, but I'm worried about the edge case that
    * data points with time 1234.999 and 1235.000 will be rounded to the same time
    * get merged into `df_motion`
    * Only 1 data point survives get lost.

   To deal with this my first step would be to consider a right join.
    * a good side effect is it'll prevent the issue is #2 above

5. Import statement in app.py seems to be wrong. I am not sure why it was this way to begin with. need to dive deeper
6. Given a 2h time constright, not able to firegure out unit testing in Python
    * i've never done it before, let alone have to deal with a webserver
    * `GET http://testserver/motion "HTTP/1.1 404 Not Found"` suspect host name is the issue. 

