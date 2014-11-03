"""
Module Licence and docstring
"""
from __future__ import absolute_import, division, print_function
from ibeis import constants


# =======================
# Schema Version Current
# =======================


VERSION_CURRENT = '1.0.2'

def update_current(db, ibs=None):
    db.add_table(constants.CHIP_TABLE, (
        ('chip_rowid',                   'INTEGER PRIMARY KEY'),
        ('annot_rowid',                  'INTEGER NOT NULL'),
        ('config_rowid',                 'INTEGER DEFAULT 0'),
        ('chip_uri',                     'TEXT'),
        ('chip_width',                   'INTEGER NOT NULL'),
        ('chip_height',                  'INTEGER NOT NULL'),
    ),
        superkey_colnames=['annot_rowid', 'config_rowid'],
        docstr='''
        Used to store *processed* annots as chips''')

    db.add_table(constants.FEATURE_TABLE, (
        ('feature_rowid',                'INTEGER PRIMARY KEY'),
        ('chip_rowid',                   'INTEGER NOT NULL'),
        ('config_rowid',                 'INTEGER DEFAULT 0'),
        ('feature_num_feats',            'INTEGER NOT NULL'),
        ('feature_keypoints',            'NUMPY'),
        ('feature_vecs',                 'NUMPY'),
        ('feature_forground_weight',     'NUMPY'),
    ),
        superkey_colnames=['chip_rowid', 'config_rowid'],
        docstr='''
        Used to store individual chip features (ellipses)''')

    db.add_table(constants.METADATA_TABLE, (
        ('metadata_rowid',               'INTEGER PRIMARY KEY'),
        ('metadata_key',                 'TEXT'),
        ('metadata_value',               'TEXT'),
    ),
        superkey_colnames=['metadata_key'],
        docstr='''
        The table that stores permanently all of the metadata about the
        database (tables, etc)''')

    db.add_table(constants.RESIDUAL_TABLE, (
        ('residual_rowid',               'INTEGER PRIMARY KEY'),
        ('feature_rowid',                'INTEGER NOT NULL'),
        ('config_rowid',                 'INTEGER DEFAULT 0'),
        ('residual_vector',              'NUMPY'),
    ),
        superkey_colnames=['residual_rowid', 'feature_rowid', 'config_rowid'],
        docstr='''
        Used to store individual SMK/ASMK residual vectors for features''')
