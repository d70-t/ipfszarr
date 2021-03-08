from optimize_chunks import optimize_chunk_size
import numpy as np


MAX_IPFS_CHUNK_SIZE = 256 * 1024 - 14  # default 256 KiB blocksize - 14 bytes header


def test_optimize_is_below_max():
    itemsize = 4
    cshape = optimize_chunk_size(itemsize, (231, 153), MAX_IPFS_CHUNK_SIZE)
    assert np.prod(cshape) * itemsize <= MAX_IPFS_CHUNK_SIZE

