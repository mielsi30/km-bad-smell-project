import javalang
import rdflib.plugins.sparql as sq
import rdflib
from owlready2 import *
from pathlib import Path
import pytest
import individ_creator
from onto_creator import *



output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output/queries/")

def detect_bad_smells():
    print("Detecting bad smells")

    get_ontology("file://tree2.owl").load()
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
            HAVING (COUNT(?s) >= 20)
        """, g)

    out = open(output_path + "longMethod.txt", "w")
    out.write("Long Methods:\n\n")
    for row in methods:
        print(row)
        out.write("Class: " + row.cn + " Method: " + row.mn + " " + row.tot + " statements\n")

    out.close()
    print("LENGTH = " , len(methods))
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

detect_bad_smells()

# tests not done yet
@pytest.fixture
def setup_ontology():
    onto = owlready2.get_ontology("file://testing.owl").load()
    yield onto


def test_long_method(setup_ontology):
    onto = setup_ontology
    tree = javalang.parse.parse("class A { int f(int x) { x++;x++;x++;x++;x++;x++;x++;x++;x++;x++; x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;}}")
    individ_creator.populate_ontology(onto, tree)
    onto.save(file="testing.owl", format="rdfxml")
    get_ontology("file://testing.owl").load()
    g = default_world.as_rdflib_graph()
    long_methods(g)