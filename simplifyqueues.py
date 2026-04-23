import argparse
from core import perms_to_dnf_tree
from parse_espresso_tree import *
from collections import defaultdict

def main():
    parser = argparse.ArgumentParser(description="Simplify queues")
    parser.add_argument("-i", default="testinput.txt", help="Input file")
    parser.add_argument("-s", default="\n", help="Input separator (default newline)")
    parser.add_argument("-o", help="Output file (leave blank to print to stdout)")
    
    args = parser.parse_args()

    if args.s == "\\n":
        args.s = "\n"

    with open(args.i, 'r') as f:
        queue_input = f.read()
        
    queues = queue_input.strip().split(args.s)

    validate_input(queues)

    # generate mapping from letters to numbers to convert tetris queue input to normal permutation input e.g. TSZ|TZS -> (1,2,3),(1,3,2)
    representative = queues[0]
    num_to_piece = {i: piece for i, piece in enumerate(representative,start=1)}
    piece_to_num: dict[str, int] = {piece: i for i, piece in enumerate(representative,start=1)}

    def queue_to_perm(queue):
        return tuple(piece_to_num[piece] for piece in queue)

    perms = list(map(queue_to_perm, queues))


    tree = perms_to_dnf_tree(perms, n=len(representative))

    
    def to_original_notation(node: Node) -> Node:
        if not isinstance(node, Literal):
            return node
        
        return node.substitute(lambda n: num_to_piece[int(n)])
    
    tree = tree_substitute(tree, to_original_notation)

    tree = tree_substitute(tree, collapse_relations)

    tree = tree_substitute(tree, remove_redundant_nodes)

    if args.o:
        with open(args.o, 'w') as f:
            f.write(str(tree))
            f.write("\n")
    else:
        print(tree)




# require: nonempty input, all queues same length, no duplicates in any queue, all queues have the same set of letters
# returns None if valid and str otherwise
def validate_input(queues: list[str]):
    if len(queues) == 0:
        raise ValueError("Empty Input")
    
    representative = queues[0]
    req_len = len(representative)
    req_chars = set(representative)

    for queue in queues:
        if len(queue) != req_len:
            # TODO it is possible to deal with an input like this but would require a refactor
            raise ValueError(f"Input permutations {representative} and {queue} differ in length")
        chars = set(queue)
        if len(chars) != len(queue):
            raise ValueError(f"Input permutation {queue} has duplicate characters")
        if chars != req_chars:
            raise ValueError(f"Input permutations {representative} and {queue} differ in characters")


# converts A<B & A<C to A<BC and likewise for other side
def collapse_relations(node: Node) -> Node:
    if not isinstance(node, AndNode):
        return node

    nonworking_set = []
    working_set: list[Literal] = []
    for child in node.children:
        if isinstance(child,Literal):
            working_set.append(child)
        else:
            nonworking_set.append(child)

    left_associations: dict[str, list[str]] = defaultdict(list)
    for lit in working_set:
        left_associations[lit.left].append(lit.right)


    working_set = [
        Literal(left=l, right="".join(map(str,rs)))
        for l, rs in left_associations.items()
    ]

    right_associations: dict[str, list[str]] = defaultdict(list)
    for lit in working_set:
        right_associations[lit.right].append(lit.left)

    working_set = [
        Literal(left="".join(map(str,ls)), right=r)
        for r, ls in right_associations.items()
    ]

    return AndNode(children=nonworking_set + working_set)


# for any node that is an OrNode/AndNode and only has one child
# replace it with its child
def remove_redundant_nodes(node: Node) -> Node:
    if isinstance(node, (AndNode, OrNode)) and len(node.children) == 1:
        return node.children[0]
    return node


main()