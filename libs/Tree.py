'''
Tree from:
http://www.quesucede.com/page/show/id/python-3-tree-implementation
'''

from urllib.parse import urlparse
import os

(_ROOT, _DEPTH, _BREADTH) = range(3)


class Node:
    def __init__(self, identifier):
        self.__identifier = identifier
        self.__children = []

    @property
    def identifier(self):
        return self.__identifier

    @property
    def children(self):
        return self.__children

    def add_child(self, identifier):
        self.__children.append(identifier)


class Tree:

    def __init__(self):
        self.__nodes = {}

    @property
    def nodes(self):
        return self.__nodes

    def add_node(self, identifier, parent=None):
        print("identifier: " + identifier + " parent= " + str(parent))
        node = Node(identifier)
        self[identifier] = node

        if parent is not None:
            self[parent].add_child(identifier)

        return node

    def display(self, identifier, depth=_ROOT):
        children = self[identifier].children
        if depth == _ROOT:
            print("{0}".format(identifier))
        else:
            print("\t"*depth, "{0}".format(identifier))

        depth += 1
        for child in children:
            print("\t"*depth, "{0}".format(identifier))
            self.display(child, depth)  # recursive call

    def traverse(self, identifier, mode=_DEPTH):
        yield identifier
        queue = self[identifier].children
        while queue:
            yield queue[0]
            expansion = self[queue[0]].children
            if mode == _DEPTH:
                queue = expansion + queue[1:]  # depth-first
            elif mode == _BREADTH:
                queue = queue[1:] + expansion  # width-first

    def __getitem__(self, key):
        return self.__nodes[key]

    def __setitem__(self, key, item):
        self.__nodes[key] = item
            

'''
tree = Tree()

t = print("{0}".format("palestras"))
tree.add_node("Harry")  # root node
tree.add_node("Jane", t)
tree.add_node("Bill", "Harry")
tree.add_node("Joe", "Jane")
tree.add_node("Diane", "Jane")
tree.add_node("George", "Diane")
tree.add_node("Mary", "Diane")
tree.add_node("Jill", "George")
tree.add_node("Carol", "Jill")
tree.add_node("Grace", "Bill")
tree.add_node("Mark", "Jane")

tree.display("Harry")
print("***** DEPTH-FIRST ITERATION *****")
for node in tree.traverse("Harry"):
    print(node)
print("***** BREADTH-FIRST ITERATION *****")
for node in tree.traverse("Harry", mode=_BREADTH):
    print(node)
'''