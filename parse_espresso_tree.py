from __future__ import annotations  # crazy feature i learned today
from dataclasses import dataclass

class Literal:
    def __init__(self, left: str, right: str, swap=False) -> None:
        if swap:
            left, right = right, left

        self.left = left
        self.right = right

    def __str__(self) -> str:
        return f"{self.left}<{self.right}"
    
    # used for changing notation
    def substitute(self, subfunc):
        return Literal(subfunc(self.left), subfunc(self.right))
    

@dataclass
class AndNode:
    children: list[Node]

    def __str__(self) -> str:
        return "("+" & ".join(str(child) for child in self.children)+")"
    

@dataclass
class OrNode:
    children: list[Node]

    def __str__(self) -> str:
        return "("+" or ".join(str(child) for child in self.children)+")"

Node = Literal | AndNode | OrNode
    



# input espresso_tts(...)[0].to_ast()
# 'pairs' is to convert boolean algebra indices to permutations
def parse_tree(ast_node, pairs: list[tuple[int, int]]) -> Node:
    match ast_node:
        case ('const', v):
            raise ValueError(f"Tree has constant value {v}")
        
        case ('lit', id):
            is_negated = (id < 0)
            left, right = pairs[abs(id)-1]
            return Literal(str(left), str(right), is_negated)

        case ('or', *terms):
            children = [parse_tree(subtree, pairs) for subtree in terms]
            return OrNode(children)
        
        case ('and', *terms):
            children = [parse_tree(subtree, pairs) for subtree in terms]
            return AndNode(children)
        
        case _:
            raise Exception(f"Unknown node {type(ast_node)}")
        


# apply a substitution function to nodes in the tree
# does this bottom up (so the substitution function should assume that all children have been transformed)
def tree_substitute(tree: Node, subfunc):
    match tree:
        case Literal():
            return subfunc(tree)
        
        case OrNode(children=children):
            new_children = [tree_substitute(child, subfunc) for child in children]
            return subfunc(OrNode(children=new_children))
        
        case AndNode(children=children):
            new_children = [tree_substitute(child, subfunc) for child in children]
            return subfunc(AndNode(children=new_children))

