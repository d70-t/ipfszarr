# ipfszarr

Utilities to prepare zarr datasets for the use on IPFS.

## reasoning

IPFS features a file system which by defaults stores `256*1024-14` bytes in a raw chunk. This size can be expanded to 1MB, which is a hard technical limit. A file on IPFS may well be larger than one chunk, but in this case, it will be split into multiple chunks, forming a tree structure. Thus as soon as one file grows larger than one chunk, it will turn into at leas three chunks. The reason for limiting the block size is that the integrity of a block can only be checked once it has been received completely. Thus, in order to keep misbehaving nodes from filling you computer's memory, the maximum block size which can be received prior to checking must be limited. In consequence, the smallest object size handled by IPFS is also one IPFS chunk.

zarr also uses chunking in order to speed up access to slices of variables. These chunks factor in the multidimensional structure of the dataset and thus are usually better suited for the application in zarr then the chunking by IPFS would be.

The goal of these tools is to create zarr archives which have their chunk structure aligned to the behavior of IPFS, such that ideally one zarr chunk will map exactly to on IPFS chunk.

## tools

### `nc2zarr.py` -- converts a netCDF file into a zarr archive

```
python nc2zarr.py [-O OPTIMIZATION] infile.nc outfile.zarr
```
The interesting bit is the optimization flag.

* `-O0` will not try to optimize anything
* `-O1` ensures that the uncompressed size of any array chunk is below the default IPFS block size limit
* `-O2` runs `-O1` first, but then retrieves the compression ratio from the previously encoded dataset and re-encodes the dataset with larger blocks, depending on the achieved compression ratio


### `zarr_ipfs_add.sh` -- add zarr archive to IPFS
```
./zarr_ipfs_add.sh outfile.zarr
```
Adds the zarr archive to IPFS. This is basically `ipfs add`, but takes care of recursive adding, hidden files and increases the default block size to cope with the possibility of some chunks becoming larger than others due to variations in compression efficiency.

### other
* `ipfs_tree.py` prints all chunks of an ipfs directory or file
* `ipfs_raw_size_hist.py` displays a histogram of all raw chunks within an IPFS directory or file
