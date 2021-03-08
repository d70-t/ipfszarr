import itertools
import os
import shutil
import numpy as np
import xarray as xr

from optimize_chunks import optimize_chunk_size

MAX_IPFS_CHUNK_SIZE = 256 * 1024 - 14  # default 256 KiB blocksize - 14 bytes header


def guess_chunks(variable, compression_factor=1.):
    return optimize_chunk_size(variable.dtype.itemsize, variable.shape, MAX_IPFS_CHUNK_SIZE, compression_factor)


def find_compression_factors(ds, encoding, zarrpath):
    factors = {}
    for varname, enc in encoding.items():
        if "chunks" in enc:
            var = ds[varname]
            chunks = enc["chunks"]
            gross_size = var.dtype.itemsize * np.prod(chunks)
            folder = os.path.join(zarrpath, varname)
            n_full_chunks = tuple(s // c for s, c in zip(var.shape, chunks))
            full_chunk_files = [".".join(map(str, cid)) for cid in itertools.product(*map(range, n_full_chunks))]
            if len(full_chunk_files) == 0:
                continue
            sizes = [os.path.getsize(os.path.join(folder, fcf)) for fcf in full_chunk_files]
            net_size = np.mean(sizes)
            factors[varname] = gross_size / net_size

    return factors 


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("infile", help="input netcdf file")
    parser.add_argument("outfile", help="output zarr folder")
    parser.add_argument("-O", "--optimization", default=1, type=int, help="optimization level")
    args = parser.parse_args()

    ds = xr.open_dataset(args.infile, decode_cf=False)

    if args.optimization >= 1:
        encoding = {
            k: {"chunks": guess_chunks(v)}
            for k, v in list(ds.items()) + list(ds.coords.items())
        }
    else:
        encoding = {}

    if os.path.exists(args.outfile):
        shutil.rmtree(args.outfile)

    ds.to_zarr(args.outfile,
               mode="w",
               consolidated=True,
               encoding=encoding)

    if args.optimization >= 2:
        cf = find_compression_factors(ds, encoding, args.outfile)
        encoding = {
            k: {"chunks": guess_chunks(v, cf.get(k, 1))}
            for k, v in list(ds.items()) + list(ds.coords.items())
        }
        shutil.rmtree(args.outfile)
        ds.to_zarr(args.outfile,
                   mode="w",
                   consolidated=True,
                   encoding=encoding)


if __name__ == "__main__":
    main()
