"""
Database of interaction models for classical molecular dynamics
and Monte Carlo simulations
"""

import os
import glob
import json
from copy import deepcopy
from . import _schemas

_root = os.path.dirname(__file__)
_samples = os.path.join(_root, 'samples')
_database = {1: {}, 2: {}}  # singleton
schemas = {1: _schemas.m1, 2: _schemas.m2}
default_schema_version = 1


def _validate_model(model, version=None):
    from jsonschema import validate
    if version is None:
        version = default_schema_version
    validate(instance=model, schema=schemas[version])

def _validate_sample(sample):
    assert 'path' in sample
    
def _version(model):
    """
    Return the schema version of the model
    """
    from jsonschema import ValidationError
    
    # Validate model against either version
    valid = []
    for schema_version in [1, 2]:
        try:
            _validate_model(model, schema_version)
            valid.append(schema_version)
        except ValidationError:
            pass
    # Return the schema id
    if len(valid) == 0:
        raise ValidationError(f'invalid model {model}')
    elif len(valid) == 1:
        return valid[0]
    else:
        raise InternalError(f'model {model} is valid for multiple schemas, this should not happen')
    
def _convert(model, version):
    """
    Convert model to schema `version`. Do nothing is schema version is already the requested one
    """
    from .helpers import _upgrade_1_to_2
    if _version(model) == version:
        return model
    elif _version(model) == 1 and version == 2:
        return _upgrade_1_to_2(model)
    else:
        raise ValueError('cannot handle this conversion')

def model(entry, version=None):
    """Get a model from database"""
    if version is None:
        version = default_schema_version
    if entry in _database[version]:
        return deepcopy(_database[version][entry])
    else:
        raise KeyError(f'Model {entry} with schema {version} not available')

# Alias
get = model

def models(version=None):
    """Return all models at schema `version`"""
    if version is None:
        version = default_schema_version
    return deepcopy(_database[version])

# Alias
available = models

def samples():
    """Return all samples"""
    db = {}
    with open(os.path.join(_root, 'samples', '_db.json')) as fh:
        data = json.load(fh)
    for sample in data:
       db[sample["path"]] = sample
    return db #data

def copy(path_or_dict, output_path=None):
    """Get a copy of `path` in the samples database and return the path to it"""
    import tempfile
    import shutil
    from .helpers import _wget
    
    if hasattr(path_or_dict, 'get'):
        path = path_or_dict.get('path')
    else:
        path = path_or_dict
    
    if output_path is None:
        tmpdir = tempfile.mkdtemp()
        basename = os.path.basename(path)
        output_path = os.path.join(tmpdir, basename)

    if path.startswith('http'):
        _wget(path, tmpdir)
    else:
        # Assume they are under samples/
        shutil.copy(os.path.join(_root, 'samples', path), output_path)
    return output_path

# Alias
sample = copy

def read(file_json):
    """Read a single json model file and return the entry as a dict"""
    with open(file_json) as fh:
        try:
            model = json.load(fh)
        except (ValueError, json.decoder.JSONDecodeError):
            print('Error reading file {}'.format(file_json))
            raise
    return model
        
def add(path):
    """
    If `path` is a directory, add all json files in there to the
    global `database`. If `path` ends with `json`, it will be assumed
    to be match one or multiple json files (ex. `*.json`).
    """
    if path.endswith('json'):
        search_path = glob.glob(path)
    else:
        search_path = glob.glob('{}/*.json'.format(path))
    for _path in search_path:
        # Model name is file basename
        # This may overwrite existing models in database
        name = os.path.basename(_path)[:-5]
        model = read(_path)
        # Store model in database according to its version
        _database[_version(model)][name] = model
        
# By default, load all json files in module path
add(os.path.join(_root, '_v1'))
add(os.path.join(_root, '_v2'))
