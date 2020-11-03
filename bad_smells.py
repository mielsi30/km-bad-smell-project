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

output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output/")
output_path = output_dir + "log.txt"

def detect_bad_smells(file_name):
    get_ontology("file://" + file_name).load()
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    graph = default_world.as_rdflib_graph()
    long_methods(g=graph)
    long_constructors(g=graph)
    large_classes(g=graph)
    method_with_switch(g=graph)
    constructor_with_switch(g=graph)
    constructor_long_parameter_list(g=graph)
    method_long_parameter_list(g=graph)
    data_class(g=graph)


def long_methods(g):
    print("1. Looking for long methods")
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

    out = open(output_path, "w")
    out.write("Long Methods:\n\n")
    out.write("Total: " + str(len(methods)) + "\n")
    for row in methods:
        out.write("Class: " + row.cn + " Method: " + row.mn + " " + row.tot + " statements\n")
    out.close()

def long_constructors(g):
    print("2. Looking for long constructors")
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

    out = open(output_path, "a")
    out.write("\nLong Constructors:\n\n")
    out.write("Total: " + str(len(constructors)) + "\n")
    for row in constructors:
        out.write("Class: " + row.cn + "  Constructor: " + row.con + row.tot + " statements\n")
    out.close()

def large_classes(g):
    print("3. Looking for large classes")
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

    out = open(output_path, "a")
    out.write("\nLarge Classes:\n\n")
    out.write("Total: " + str(len(classes)) + "\n")
    for row in classes:
        out.write("Class: " + row.cn + " " + row.tot + " methods\n")

    out.close()

def method_with_switch(g):
    print("4. Looking for methods with switch statements")
    methods = run_query(
        """SELECT ?mn ?cn ?sw (COUNT(*)AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:MethodDeclaration .
                ?m tree:jname ?mn .
                ?m tree:body ?s .
                ?sw a tree:SwitchStatement .
            } GROUP BY ?m
            HAVING (COUNT(?sw) >= 1)
        """, g)

    out = open(output_path, "a")
    out.write("\nMethods with Switch:\n\n")
    out.write("Total: " + str(len(methods)) + "\n")
    for row in methods:
        out.write("Method: " + row.mn + " " + row.tot + " statements\n")

    out.close()

def constructor_with_switch(g):
    print("5. Looking for constructors with switch statements")
    methods = run_query(
         """SELECT ?cn ?con ?s (COUNT(*)AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?cd .
                ?cd a tree:ConstructorDeclaration .
                ?cd tree:jname ?con .
                ?cd tree:body ?s .
                ?s a tree:SwitchStatement .
            } GROUP BY ?cd
            HAVING (COUNT(?s) >= 1)
        """, g)

    out = open(output_path, "a")
    out.write("\nConstructors with Switch:\n\n")
    out.write("Total: " + str(len(methods)) + "\n")
    for row in methods:
        out.write("Constructors: " + row.mn + " " + row.tot + " statements\n")

    out.close()

def constructor_long_parameter_list(g):
    print("6. Looking for constructors with long parameter list")
    constructors =  run_query(
        """SELECT ?cn ?con ?fp (COUNT(*)AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:ConstructorDeclaration .
                ?m tree:jname ?con .
                ?m tree:parameters ?fp .
                ?fp a tree:FormalParameter .
            } GROUP BY ?m
            HAVING (COUNT(?fp) >= 5)
        """, g)

    out = open(output_path, "a")
    out.write("\nConstructors with Long Parameter List:\n\n")
    out.write("Total: " + str(len(constructors)) + "\n")
    for row in constructors:
        out.write("Constructors: " + row.mn + " " + row.tot + " parameters\n")

    out.close()

def method_long_parameter_list(g):
    print("7. Looking for methods with long parameter list")
    methods =  run_query(
        """SELECT ?cn ?mn ?fp (COUNT(*)AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:MethodDeclaration .
                ?m tree:jname ?mn .
                ?m tree:parameters ?fp .
                ?fp a tree:FormalParameter .
            } GROUP BY ?m
            HAVING (COUNT(?fp) >= 5)
        """, g)

    out = open(output_path, "a")
    out.write("\nMethods with Long Parameter List:\n\n")
    out.write("Total: " + str(len(methods)) + "\n")
    for row in methods:
        out.write("Method: " + row.mn + " " + row.tot + " parameters\n")

    out.close()



def data_class(g):
    print("7. Looking for data classes")
    class_methods = run_query(
        """SELECT ?mn ?cn (COUNT(*)AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:MethodDeclaration .
                ?m tree:jname ?mn .
            } GROUP BY ?cn
        """, g)

    setters_getters = run_query(
        """SELECT ?mn ?cn (COUNT(*)AS ?tot) WHERE {
                ?c a tree:ClassDeclaration .
                ?c tree:jname ?cn .
                ?c tree:body ?m .
                ?m a tree:MethodDeclaration .
                ?m tree:jname ?mn .
                FILTER (regex(?mn, "get.*") || regex(?mn, "set.*"))
            } GROUP BY ?cn
        """, g)

    out = open(output_path, "a")
    out.write("\nData Classes:\n\n")

    for row in setters_getters:
        for method in class_methods:
            if method.cn == row.cn and row.tot == method.tot:
                out.write("Total: " + row.tot + "\n")
                out.write("Class: " + row.cn)


    out.close()

def run_query(query, g):
    q = sq.prepareQuery(
        query,
        initNs={"tree": "http://my.onto.org/tree.owl#"}
    )
    return g.query(q)


# TODO: finish tests
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
    # first create a test ontology with python3 onto_creator.py testing.owl
    onto = setup_ontology
    tree = javalang.parse.parse("class A { int f(int x) { x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;}}")
    individ_creator.populate_ontology(onto, tree)
    onto.save(file="testing.owl", format="rdfxml")
    get_ontology("file://testing.owl").load()
    graph = default_world.as_rdflib_graph()
    long_methods(g=graph)

if __name__ == "__main__":
    main()