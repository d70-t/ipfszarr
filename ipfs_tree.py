from sh import ipfs
from cid import make_cid
import json

NODECACHE = {}

def get_node(cid):
    if cid not in NODECACHE:
        NODECACHE[cid] = DAGNode(cid)
    return NODECACHE[cid]


class DAGNode:
    def __init__(self, cid):
        self.cid = make_cid(cid)
        self._content = None
        self._stat = None

    @property
    def content(self):
        if self._content is None:
            self._content = json.loads(ipfs.dag.get(self.cid.encode()).stdout.decode("utf-8"))
        return self._content
    
    @property
    def codec(self):
        return self.cid.codec

    @property
    def stat(self):
        if self._stat is None:
            parts = [p.split(":") for p in ipfs.dag.stat(self.cid.encode()).stdout.decode("utf-8").split(",")]
            self._stat = {k.strip(): int(v.strip()) for k, v in parts}
        return self._stat

    def items(self):
        if self.codec == "dag-pb":
            for link in self.content["links"]:
                yield link["Name"], get_node(link["Cid"]["/"])

    def __str__(self):
        return f"DAGNode({self.cid})"

def format_tree(node, level=0, name=None):
    spacer = "  " * level
    if name:
        yield f"{spacer}{name}: {node.cid} ({node.codec})"
    else:
        yield f"{spacer}{node.cid} ({node.codec})"
    for k, v in node.items():
        yield from format_tree(v, level+1, k)

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("CID")
    args = parser.parse_args()

    root = get_node(args.CID)
    for line in format_tree(root):
        print(line)


if __name__ == "__main__":
    main()
