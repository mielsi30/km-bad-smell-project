from owlready2 import *
import ast
import types
import sys

file_name = sys.argv[1]
print("Creating ontology: ", file_name)

def main():
    file = open("tree.py", "r")
    text = file.read()
    tree = ast.parse(source=text)

    onto = get_ontology("http://my.onto.org/tree.owl")
    analyzer = Analyzer(onto)
    analyzer.visit(tree)
    onto.save(file = file_name, format="rdfxml")
    print("Ontology %s saved" % file_name)


def buildOntology(self, node):
    onto = self.onto
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

def testOntology():
    onto = get_ontology("file://testing.owl").load()

    cd = onto["ClassDeclaration"]
    assert cd.name == "ClassDeclaration"
    assert len(cd.is_a) == 1
    assert cd.is_a[0].name == "TypeDeclaration"

    constructor_decl = onto["ConstructorDeclaration"]
    assert constructor_decl.name == "ConstructorDeclaration"
    assert len(constructor_decl.is_a) == 2
    assert constructor_decl.is_a[0].name == "Declaration"
    assert constructor_decl.is_a[1].name == "Documented"

    field_decl = onto["FieldDeclaration"]
    assert field_decl.name == "FieldDeclaration"
    assert len(field_decl.is_a) == 2
    assert field_decl.is_a[0].name == "Member"
    assert field_decl.is_a[1].name == "Declaration"

    method_decl = onto["MethodDeclaration"]
    assert method_decl.name == "MethodDeclaration"
    assert len(method_decl.is_a) == 2
    assert method_decl.is_a[0].name == "Member"
    assert method_decl.is_a[1].name == "Declaration"

    if_stmt = onto["IfStatement"]
    assert if_stmt.name == "IfStatement"
    assert len(if_stmt.is_a) == 1
    assert if_stmt.is_a[0].name == "Statement"


class Analyzer(ast.NodeVisitor):

    def __init__(self, onto):
        self.onto = onto

    def generic_visit(self, node):
        ast.NodeVisitor.generic_visit(self, node)
        buildOntology(self, node)


if __name__ == "__main__":
    main()


