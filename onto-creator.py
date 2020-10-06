from owlready2 import *
import ast
import types

def main():


    file = open("tree.py", "r")
    text = file.read()
    tree = ast.parse(source=text)

    analyzer = Analyzer()
    analyzer.visit(tree)


def buildOntology(self, node):

    onto = get_ontology("file://tree.owl")

    with onto:
        if type(node) == ast.ClassDef:
            for base in node.bases:
                base_id = base.id
                if base_id == "Node":
                    types.new_class(node.name, (Thing,))
                else:
                    types.new_class(node.name, (onto[base_id],))

        elif type(node) == ast.Assign:
            for element in node.value.elts:
                if element.s == "body" or element.s == "parameters":
                    types.new_class(element.s, (ObjectProperty, ))
                elif element.s == "name":
                    types.new_class("jname", (DataProperty, ))
                else:
                    types.new_class(element.s, (DataProperty,))

    onto.save()

class Analyzer(ast.NodeVisitor):

    def generic_visit(self, node):
        ast.NodeVisitor.generic_visit(self, node)
        buildOntology(self, node)


if __name__ == "__main__":
    main()