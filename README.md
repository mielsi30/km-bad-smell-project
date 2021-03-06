## Project 1: Bad Smells
### Course: Knowledge Analysis and Management
Brenda Ruiz

#### Instructions to run and test the project
1. To create an ontology:
``$ python3 onto_creator.py <name_of_file>``

2. To test the ontology created:
    - First create a test ontology by running: 
    ````$ python3 onto_creator.py testing.owl ```` <br />
     This ontology will be used by the other tests.
    - Then run the tests with: 
``$ pytest onto_creator.py``

3. To create individuals in the ontology:
``$ python3 individ_creator.py <name_of_file>``

4. To test the individuals creation:
``$ pytest -s individ_creator.py``

5. To detect bad smells:
``$ python3 bad_smells.py <name_of_file>``

6. To test the bad smells detection:
``$ pytest -s bad_smells.py``
