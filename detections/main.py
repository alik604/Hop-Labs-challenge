import uvicorn
import pandas as pd

if __name__ == "__main__":
    # # Left here for reference and ease of testing. of couse IRL this would be deleted..

    # df_motion = pd.read_parquet("../44746f8e-c3d6-4cd0-8fbc-dcd03a159a77.motion_data.parquet")
    # df_object = pd.read_parquet("../44746f8e-c3d6-4cd0-8fbc-dcd03a159a77.object_detections.parquet")
    #
    # # convert from unix time to datatime
    # df_motion['time'] = pd.to_datetime(df_motion['time'] - (4 * 3600 * 1000), unit='ms')
    # df_object['time'] = df_object['time'].dt.round('ms')
    #
    # # see how the timeszones are now corrected. And object_detections goes beyond the dataset by 1 datapoint.
    # print(df_motion['time'][-5:])
    # print(df_object['time'][-5:])
    #
    # # merge the above two dfs
    # df = pd.merge(df_motion, df_object, on='time', how='right')
    # print(df.shape)  # missing one. see my note in read me
    # print(df_motion.shape)
    # print(df_object.shape)
    #
    # df_types = pd.read_parquet("../object_types.parquet")
    # mapping = df_types.set_index('object_code').to_dict()['object_type_name']
    #
    # # apply the mapping
    # df['object_type'] = df['object_type'].map(mapping)
    #
    # # convert time to timestamp
    # df['time'] = df['time'].astype('int64') // 10 ** 9
    #
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None):  # more options can be specified also
    #     print(df.head(5))
    #
    # # convert the time column to unix timestamp
    # df['time'] = df['time'].astype('int64') // 10**9

    uvicorn.run("api.app:app", host="0.0.0.0", port=8000) # I had to use Localhost Since my Docker install is broken
