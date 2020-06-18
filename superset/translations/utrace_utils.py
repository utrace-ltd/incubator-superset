#!/usr/bin/env python

from flask.cli import with_appcontext
from superset import db

from superset.app import create_app
app = create_app()

"""
    1. Run this for datasource_translate.pot generation.
        to run this in PyCharm (on Windows):
        module name: flask 
        parameters: extract_cols
        ENV: FLASK_APP=superset\\translations\\utrace_utils.py
    2. Init or update lang pack
        pybabel init -i superset\\translations\\datasource_translate.pot -d superset\\translations -D datasource_translate -l ru
        pybabel update -i superset\\translations\\datasource_translate.pot -d superset\\translations -D datasource_translate -l ru
    3. Translate *.po    
    4. Compile (during deploy)
        flask fab babel-compile --target superset/translations 
    
"""

@app.cli.command('extract_cols')
@with_appcontext
def extract_cols():
    from babel.messages import Catalog
    catalog = Catalog(domain = 'datasource_translate')

    from superset.connectors.sqla.models import SqlaTable
    for ds in db.session.query(SqlaTable).all():
        for o in ds.columns:
            catalog.add(o.verbose_name, context = ds.name)
        for o in ds.metrics:
            catalog.add(o.verbose_name, context = ds.name)

    from babel.messages.pofile import write_po
    with open('superset/translations/datasource_translate.pot', 'w+b') as pot_file:
        write_po(pot_file, catalog, omit_header = True)