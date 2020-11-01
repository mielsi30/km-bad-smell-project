import javalang
import rdflib.plugins.sparql as sq
from owlready2 import *
from pathlib import Path
import pytest
import individ_creator


def main():
    file_name = sys.argv[1]
    print("Detecting bad smells for ontology %s" % file_name)
    detect_bad_smells(file_name)

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output/queries/")

def detect_bad_smells(file_name):
    get_ontology("file://" + file_name).load()
    Path(output_path).mkdir(parents=True, exist_ok=True)
    graph = default_world.as_rdflib_graph()
    long_methods(g=graph)
    long_constructors(g=graph)


def long_methods(g):
    methods = run_query(
        """SELECT ?cn ?mn ?s (COUNT(*)AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:MethodDeclaration .
                ?m tree:jname ?mn .
                ?m tree:body ?s .
                ?s a/rdfs:subClassOf* tree:Statement .
            } GROUP BY ?m
            HAVING (COUNT(?s) >= 10)
        """, g)

    out = open(output_path + "longMethod.txt", "w")
    out.write("Long Methods:\n\n")

    for row in methods:
        print(row)
        out.write("Class: " + row.cn + " Method: " + row.mn + " " + row.tot + " statements\n")

    out.close()
    print("Length = " , len(methods))
    return methods

def long_constructors(g):
    constructors = run_query(
        """SELECT ?cn ?con ?s (COUNT(*)AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?cd .
                ?cd a tree:ConstructorDeclaration .
                ?cd tree:jname ?con .
                ?cd tree:body ?s .
                ?s a/rdfs:subClassOf* tree:Statement .
            } GROUP BY ?cd
            HAVING (COUNT(?s) >= 20)
        """, g)

    out = open(output_path + "longConstructor.txt", "w")
    out.write("Long Constructors:\n\n")
    for row in constructors:
        print(row)
        out.write("Class: " + row.cn + "  Constructor: " + row.con + row.tot + " statements\n")

    out.close()

def large_classes(g):
    classes = run_query(
        """SELECT ?mn ?cn (COUNT(*)AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:MethodDeclaration .
                ?m tree:jname ?mn .
            } GROUP BY ?cn
            HAVING (COUNT(?m) >= 10)
        """, g)

    out = open(output_path + "largeClasses.txt", "w")
    out.write("Large Classes:\n\n")
    for row in classes:
        print(row)
        out.write("Class: " + row.cn + row.tot + " methods\n")

    out.close()

def run_query(query, g):
    q = sq.prepareQuery(
        query,
        initNs={"tree": "http://my.onto.org/tree.owl#"}
    )
    return g.query(q)

# tests not done yet
@pytest.fixture
def setup_ontology():
    onto = owlready2.get_ontology("file://testing.owl").load()
    yield onto
    for e in onto['ClassDeclaration'].instances():
        print("deleting", e)
        destroy_entity(e)

    for m in onto['Declaration'].instances():
        print("deleting", m)
        destroy_entity(m)

    for f in onto['Statement'].instances():
        print("deleting", f)
        destroy_entity(f)

    onto.save(format="rdfxml")


def test_long_method(setup_ontology):
    # first create a test ontology with  python3 onto_creator.py "testing.owl"
    onto = setup_ontology
    tree = javalang.parse.parse("class A { int f(int x) { x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;}}")
    individ_creator.populate_ontology(onto, tree)
    onto.save(file="testing.owl", format="rdfxml")
    get_ontology("file://testing.owl").load()
    graph = default_world.as_rdflib_graph()
    long_methods(g=graph)

if __name__ == "__main__":
    main()