import numpy as np

def optimize_chunk_size(itemsize, shape, target_size, compression_factor=1., target_shape_ratios=None):
    if len(shape) == 0:
        return ()
    factor = (target_size*compression_factor/(np.prod(shape)*itemsize))**(1/len(shape))
    return tuple(int(factor * s) for s in shape)
