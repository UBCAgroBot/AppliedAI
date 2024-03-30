# best practices, multihreaded backend with stream of batches
# import pycuda.gpuarray

from cuda import cudart

num_aux_streams = engine.num_aux_streams
streams = []
for i in range(num_aux_streams):
    err, stream = cudart.cudaStreamCreate()
    streams.append(stream)
context.set_aux_streams(streams)