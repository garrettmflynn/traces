# test s3 path: "s3://aind-open-data/ecephys_661279_2023-03-23_15-31-18/ecephys_compressed/experiment1_Record Node 104#Neuropix-PXI-100.ProbeA.zarr/"

instances = {}

def get_traces(
        s3_url: str, 
        start_time: float, 
        end_time: float, 
        channel_indices=None
    ):

    recording = instances[s3_url] 
    sampling_frequency = recording.get_sampling_frequency()
    if channel_indices is not None:
        channel_ids = recording.channel_ids[channel_indices]
    else:
        channel_ids = None
        
    start_frame = int(start_time * sampling_frequency)
    end_frame  = int(end_time * sampling_frequency)
    traces = recording.get_traces(start_frame=start_frame,
                                  end_frame=end_frame,
                                  channel_ids=channel_ids)
    
    return dict(
        data = traces.T.tolist(),
        timestamps = recording.get_times()[start_frame:end_frame].tolist()
    )


def init_zarr(
    s3_url: str
):
    
    try:
        import spikeinterface as si

        if (instances.get(s3_url)):
            recording = instances[s3_url]

        else: 
            recording = si.read_zarr(s3_url) # Instantiate this once
            instances[s3_url] = recording

        return dict(
            # nFrames = recording.get_num_frames(),
            # nSamples = recording.get_num_samples(),
            nSegments = recording.get_num_segments(),
            samples = recording.get_total_samples(),
            duration = recording.get_total_duration()
        )
    
    except Exception as e:
        return { "error": repr(e) }
