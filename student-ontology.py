from owlready2 import *

onto = get_ontology('http://students-ontology.org')

with onto:
    # definir une classe Person
    class Person(Thing):
        pass


    class Course(Thing):
        pass


    AllDisjoint([Person, Course])


    class teaches(Person >> Course):
        pass


    class Teacher(Thing):
        equivalent_to = [And([Person, teaches.some(Course)])]


    class attends(Person >> Course):
        pass


    class Student(Thing):
        equivalent_to = [And([Person, attends.some(Course)])]


    mary = Person(name='mary')
    cs600 = Course(name='cs600')
    alice = Person(name='alice')

    alice.teaches = [cs600]
    mary.attends = [cs600]

    print(alice.iri)
    print(alice.is_a)
    print(mary)
    print(mary.is_a)

    pass

# sync_reasoner_pellet([onto], infer_property_values=True, infer_data_property_values=True, debug=True,
# keep_tmp_file=True)

print(alice.iri)
print(alice.is_a)
print(mary)
print(mary.is_a)

with onto:
    bob = Person(name='bob')
    cs101 = Course(name='cs101')
    bob.teaches = [cs101]
    bob.attends = [cs600]
    print(f'bob is a {bob.is_a}')
    AllDifferent([bob, alice, mary])

# sync_reasoner_pellet([onto], infer_property_values=True, infer_data_property_values=True, debug=True,
#                      keep_tmp_file=True)

print(f'bob is a {bob.is_a}')

with onto:
    class Man(Person):
        pass


    class Woman(Person):
        pass


    AllDisjoint([Man, Woman])


    class has_sibling(Person >> Person):
        pass


    class has_sister(Person >> bool, FunctionalProperty):
        pass


    bob.is_a.append(Man)
    alice.is_a.append(Woman)
    mary.is_a.append(Woman)
    bob.has_sibling = [mary]
    alice.has_sibling = [mary]

with onto:
    imp = Imp()
    imp.set_as_rule(
        'Person(?x), Person(?y), Person(?z), DifferentFrom(?x, ?y),DifferentFrom(?x, ?z), DifferentFrom(?y, ?z), has_sibling(?x, ?z), has_sibling(?y, ?z) -> has_sibling(?x, ?y)')
    imp = Imp()
    imp.set_as_rule('Person(?x), Woman(?y), DifferentFrom(?x,?y), has_sibling(?x,?y) -> has_sister(?x,true)')

sync_reasoner_pellet([onto], infer_property_values=True, infer_data_property_values=True, debug=True,
                     keep_tmp_file=True)

print(onto.bob.has_sibling)
print(onto.bob.has_sister)

infer = get_ontology('http://infererences/')
print(list(infer.data_properties()))
