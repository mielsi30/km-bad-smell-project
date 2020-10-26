from owlready2 import *
import javalang
import pytest
import os


def populate_ontology(onto, tree):
    process_tree(tree, onto)

def get_files():
    # Gets all Java files from the source directory
    java_files = []
    android_chess = 'android-chess/app/src/main/java/jwtc/chess/'
    for file in os.listdir(android_chess):
            if file.endswith(".java"):
                java_files.append(os.path.join(android_chess, file))
    return java_files

def read_file(file_path):
    # Reads java files and returns a Javalang tree
    content = open(file_path, 'r').read()
    tree = javalang.parse.parse(content)

    return tree

def process_tree(tree, onto):
    for _, node in tree.filter(javalang.tree.ClassDeclaration):
        cd = onto['ClassDeclaration']()
        cd.jname = [node.name]
        for member in node.body:
            create_member(onto, cd, member)


def create_member(onto, cd, member):
    if type(member) == javalang.tree.MethodDeclaration or type(member) == javalang.tree.ConstructorDeclaration:
        create_method(onto, cd, member)

    elif type(member) == javalang.tree.FieldDeclaration:
        create_field(onto, cd, member)


def create_method(onto, cd, member):
    method_def = onto[member.__class__.__name__]()
    method_def.jname = [member.name]
    create_statement(onto, method_def, member)
    create_parameters(onto, method_def, member)
    cd.body.append(method_def)


def create_field(onto, cd, member):
    for field in member.declarators:
        field_def = onto['FieldDeclaration']()
        field_def.jname = [field.name]
        cd.body.append(field_def)

def create_statement(onto, method_def, member):
    for _, statement in member.filter(javalang.tree.Statement):
        if type(statement) != javalang.tree.Statement:
            statement_type = statement.__class__.__name__
            stmt = onto[statement_type]()
            method_def.body.append(stmt)

def create_parameters(onto, method_def, member):
    for _, statement in member.parameters:
        fp = onto['FormalParameter']()
        fp.jname = [statement[0][0].name]
        method_def.parameters.append(fp)


@pytest.fixture
def setup_ontology():
    onto = owlready2.get_ontology("file://tree.owl").load()
    yield onto
    for e in onto['ClassDeclaration'].instances():
        print("deleting", e)
        destroy_entity(e)

    for m in onto['MethodDeclaration'].instances():
        print("deleting", m)
        destroy_entity(m)

    for f in onto['FieldDeclaration'].instances():
        print("deleting", f)
        destroy_entity(f)

    for f in onto['Statement'].instances():
        print("deleting", f)
        destroy_entity(f)

    onto.save(format="rdfxml")


def testIndividualCreation(setup_ontology):
    onto = setup_ontology
    tree = javalang.parse.parse("class A { int x, y; }")
    populate_ontology(onto, tree)
    a = onto['ClassDeclaration'].instances()[0]

    assert a.body[0].is_a[0].name == 'FieldDeclaration'
    assert a.body[1].is_a[0].name == 'FieldDeclaration'
    assert a.body[0].jname[0] == 'x'
    assert a.body[1].jname[0] == 'y'

def testReturnStatement(setup_ontology):
    onto = setup_ontology
    tree = javalang.parse.parse("class A { int f() { return 0; } }")
    populate_ontology(onto, tree)
    a = onto['ClassDeclaration'].instances()[0]

    assert a.body[0].body[0].is_a[0].name == 'ReturnStatement'

def testIfStatement(setup_ontology):
    onto = setup_ontology
    tree = javalang.parse.parse("class A { int f() {"
                                "int i = 0; "
                                "if(i < 0){ int j = 1; }"
                                "} }")
    populate_ontology(onto, tree)
    a = onto['ClassDeclaration'].instances()[0]
    assert a.body[0].body[0].is_a[0].name == 'IfStatement'

def testWhileStatement(setup_ontology):
    onto = setup_ontology
    tree = javalang.parse.parse("class A { int f() {"
                                "int i = 0; int b = 5; "
                                "while(i < b){ i++; }"
                                "} }")
    populate_ontology(onto, tree)
    a = onto['ClassDeclaration'].instances()[0]
    assert a.body[0].body[0].is_a[0].name == 'WhileStatement'

def testMethodParameters(setup_ontology):
    onto = setup_ontology
    tree = javalang.parse.parse("class A { int f(int a, boolean b) {"
                                "return a; "
                                "} }")
    populate_ontology(onto, tree)
    a = onto['ClassDeclaration'].instances()[0]

    assert a.body[0].parameters[0].is_a[0].name == 'FormalParameter'
    assert a.body[0].parameters[1].is_a[0].name == 'FormalParameter'
    assert a.body[0].parameters[0].jname[0] == 'a'
    assert a.body[0].parameters[1].jname[0] == 'b'



onto = owlready2.get_ontology("file://tree.owl").load()
files = get_files()
for file in files:
    tree = read_file(file)
    populate_ontology(onto, tree)
onto.save(format="rdfxml")

