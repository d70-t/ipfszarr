from ipfs_tree import get_node
import matplotlib.pyplot as plt

def collect_nodes(node):
    yield node
    for k, v in node.items():
        yield from collect_nodes(v)

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("CID")
    args = parser.parse_args()

    root = get_node(args.CID)
    raw_sizes = [node.stat["Size"] for node in collect_nodes(root) if node.codec == "raw"]

    plt.hist(raw_sizes)
    plt.axvline(256 * 1024 - 14, color="red")
    plt.title(args.CID)
    plt.xlabel("size")
    plt.ylabel("count")
    plt.show()


if __name__ == "__main__":
    main()
