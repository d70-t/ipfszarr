import xarray as xr
from sh import python3
import os

nc2zarr = python3.bake("nc2zarr.py", O=2)

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("outfolder")
    parser.add_argument("infiles", nargs="+")
    args = parser.parse_args()

    os.makedirs(args.outfolder)

    for filename in args.infiles:
        ds = xr.open_dataset(filename)
        sonde_id = ds.sonde_id.values

        print(filename, sonde_id)
        nc2zarr(filename, os.path.join(args.outfolder, str(sonde_id)))

if __name__ == "__main__":
    main()
