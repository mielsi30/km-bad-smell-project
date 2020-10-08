import owlready2
import javalang
import os




def populate_ontology(onto, tree):
    process_tree(tree, onto)
    onto.save(format="rdfxml")

def get_files():
    # Gets all Java files from the source directory
    java_files = []
    for path, dirs, files in os.walk('android-chess/app/src/main/java/jwtc/chess/'):
        for f in files:
            if f.endswith(".java"):
                java_files.append(os.path.join(path, f))
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
    method_def = onto['MethodDeclaration']()
    method_def.jname = [member.name]
    cd.body.append(method_def)

def create_field(onto, cd, member):
    for field in member.declarators:
        field_def = onto['FieldDeclaration']()
        field_def.jname = [field.name]
        cd.body.append(field_def)

def testIndividualCreation():
    onto = owlready2.get_ontology("file://tree.owl").load()
    tree = javalang.parse.parse("class A { int x, y; }")
    populate_ontology(onto, tree)
    instances = onto['ClassDeclaration'].instances()

    findingA = [x for x in instances if x.jname[0] == 'A']
    a = findingA[0]

    assert a.body[0].is_a[0].name == 'FieldDeclaration'
    assert a.body[1].is_a[0].name == 'FieldDeclaration'
    assert a.body[0].jname[0] == 'x'
    assert a.body[1].jname[0] == 'y'


onto = owlready2.get_ontology("file://tree.owl").load()
files = get_files()
for file in files:
    tree = read_file(file)
    populate_ontology(onto, tree)

