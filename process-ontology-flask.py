# Fichier site_dynamique.py
from owlready2 import *

onto = get_ontology("process-ontology.owl").load()

from flask import Flask, url_for

app = Flask(__name__)

sync_reasoner_pellet([onto], infer_property_values=True, infer_data_property_values=True, debug=True,
                     keep_tmp_file=True)


@app.route('/')
def page_ontologie():
    html = """<html><body>"""
    html += """<h2>Ontologie '%s'</h2>""" % onto.base_iri
    html += """<h3>Classes racines</h3>"""
    for Class in Thing.subclasses():
        html += """<p><a href="%s">%s</a></p>""" % (url_for("page_classe", iri=Class.iri), Class.name)

    html += """</body></html>"""
    return html


@app.route('/classe/<path:iri>')
def page_classe(iri):
    Class = IRIS[iri]
    html = """<html><body><h2>Classe '%s'</h2>""" % Class.name

    html += """<h3>superclasses</h3>"""
    for SuperClass in Class.is_a:
        if isinstance(SuperClass, ThingClass):
            html += """<p><a href="%s">%s</a></p>""" % (url_for("page_classe", iri=SuperClass.iri), SuperClass.name)
        else:
            html += """<p>%s</p>""" % SuperClass

    html += """<h3>Classes équivalentes</h3>"""
    for EquivClass in Class.equivalent_to:
        html += """<p>%s</p>""" % EquivClass

    html += """<h3>Sous-classes</h3>"""
    for SousClass in Class.subclasses():
        html += """<p><a href="%s">%s</a></p>""" % (url_for("page_classe", iri=SousClass.iri), SousClass.name)

    html += """<h3>Individus</h3>"""
    for individu in Class.instances():
        html += """<p><a href="%s">%s</a></p>""" % (url_for("page_individu", iri=individu.iri), individu.name)

    html += """</body></html>"""
    return html


@app.route('/individu/<path:iri>')
def page_individu(iri):
    individu = IRIS[iri]
    html = """<html><body><h2>Individu '%s'</h2>""" % individu.name

    html += """<h3>Classes</h3>"""
    # TODO: ajouter des liens vers chacune des classes dont l'individu est instance
    classGroupAncestors = []
    for classgroup in individu.is_a:
        print(classgroup)
        classGroupAncestors = list(classgroup.ancestors())
        isProcess = False
        for a in classGroupAncestors:
            if a.name == 'Process':
                isProcess = True
        html += """<p><a href="%s">%s</a></p>""" % (url_for("page_classe", iri=classgroup.iri), classgroup.name)

    html += """<h3>Relations</h3>"""
    # TODO: pour les individus qui sont instances de Process, donner les propriétés
    if isProcess:
        for prop in individu.get_properties():
            for value in prop[individu]:
                print(".%s == %s" % (prop.python_name, value))

                def valueToDisplay(value):
                    try:
                        return value.name
                    except:
                        return value

                html += """<p>.%s == %s</p>""" % (prop.python_name, valueToDisplay(value))
                html += """</body></html>"""
    return html


import werkzeug.serving

werkzeug.serving.run_simple("localhost", 5000, app)
