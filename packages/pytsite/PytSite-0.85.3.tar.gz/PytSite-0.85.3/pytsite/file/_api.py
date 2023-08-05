"""File manager.
"""
import re as _re
import os as _os
import shutil as _shutil
import magic as _magic
from typing import Union as _Union
from mimetypes import guess_extension as _guess_extension
from urllib.request import urlopen as _urlopen
from urllib.parse import urlparse as _urlparse
from bson.dbref import DBRef as _DBRef
from pytsite import reg as _reg, util as _util, odm as _odm, validation as _validation, auth as _auth
from . import _model, _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def _build_store_path(mime: str, model: str = 'file', propose: str = None) -> str:
    """Build unique path to store file on the filesystem.
    """
    storage_dir = _os.path.join(_reg.get('paths.storage'), model)
    store_path = ''
    rnd_str = _util.random_str

    # Determine extension for the file in the storage
    extension = _guess_extension(mime)
    if extension == '.jpe':
        extension = '.jpg'

    # Possible (but not final) path
    possible_target_path = _os.path.join(storage_dir, rnd_str(2), rnd_str(2), rnd_str()) + extension

    # Check if the proposed path suits the requirements
    if propose:
        m = _re.match('(\w{2})/(\w{2})/(\w{16})(\.\w+)$', propose)
        if m:
            extension = m.group(4)
            possible_target_path = _os.path.join(storage_dir, m.group(1), m.group(2), m.group(3)) + extension

    # Finding path which doesn't exist on the filesystem
    while True:
        if not _os.path.exists(possible_target_path):
            store_path = possible_target_path
            break
        else:
            possible_target_path = _os.path.join(storage_dir, rnd_str(2), rnd_str(2), rnd_str()) + extension

    return store_path


def create(source_path: str, name: str = None, description: str = None, model: str = 'file',
           remove_source: bool = False, propose_store_path: str = None, owner: _auth.model.AbstractUser = None,
           attached_to: _odm.model.Entity = None) -> _model.File:
    """Create a file from path or URL.
    """
    if not owner:
        owner = _auth.get_current_user()

    # Store remote file to the local if URL was specified
    try:
        _validation.rule.Url(source_path).validate()

        # Copying remote file to the temporary local file
        with _urlopen(_util.url_quote(source_path, safe='/:?&%')) as src:
            data = src.read()

        tmp_file_fd, tmp_file_path = _util.mk_tmp_file()
        _os.write(tmp_file_fd, data)
        _os.close(tmp_file_fd)

        if not name:
            name = _urlparse(source_path).path.split('/')[-1]
        if not description:
            description = 'Downloaded from ' + source_path

        remove_source = True
        source_path = tmp_file_path
    except _validation.error.RuleError:
        pass

    # Validation file size (in megabytes)
    file_size = _os.stat(source_path).st_size
    max_file_size_mb = float(_reg.get('file.upload_max_size', '10'))
    if file_size > (max_file_size_mb * 1048576):
        raise RuntimeError('File size exceeds {} MB'.format(max_file_size_mb))

    # Determining file's MIME type
    mime = _magic.from_file(source_path, True)

    # Generating unique file path in storage
    abs_target_path = _build_store_path(mime, model, propose_store_path)

    # Make sure that directory in storage exists
    target_dir = _os.path.dirname(abs_target_path)
    if not _os.path.exists(target_dir):
        _os.makedirs(target_dir, 0o755, True)

    # Copy file to the storage
    _shutil.copy(source_path, abs_target_path)

    # Setting file's ODM entity name
    if not name:
        name = _os.path.basename(source_path)

    # Setting file's ODM entity description
    if not description:
        description = 'Created from local file ' + source_path

    # Remove source file
    if remove_source:
        _os.unlink(source_path)

    # Create File ODM entity
    storage_dir = _reg.get('paths.storage')
    file_entity = _odm.dispense(model)
    if not isinstance(file_entity, _model.File):
        raise TypeError('Entity does not extend pytsite.file.model.File.')
    file_entity.f_set('path', abs_target_path.replace(storage_dir + '/', ''))
    file_entity.f_set('name', name)
    file_entity.f_set('description', description)
    file_entity.f_set('mime', mime)
    file_entity.f_set('length', file_size)
    file_entity.f_set('attached_to', attached_to)

    if not owner.is_anonymous and not owner.is_system:
        file_entity.f_set('owner', owner)

    return file_entity.save()


def get(uid: str = None, rel_path: str = None, model: str = 'file') -> _model.File:
    """Get file by UID or relative path.
    """
    if uid:
        entity = _odm.find(model).where('_id', '=', uid).first()
    elif rel_path:
        entity = _odm.find(model).where('path', '=', rel_path).first()
    else:
        raise RuntimeError('File UID or relative path should be specified')

    if not entity:
        raise _error.EntityNotFound('File entity is not found for {}.'.format({
            'uid': uid,
            'rel_path': rel_path,
            'model': model,
        }))

    return entity


def get_by_ref(ref: _Union[str, _DBRef]) -> _model.File:
    """Get file by reference.
    """
    entity = _odm.get_by_ref(ref)
    if not entity:
        raise _error.EntityNotFound('File entity is not found for ref {}.'.format(ref))

    if not isinstance(entity, _model.File):
        raise TypeError('Entity does not extend pytsite.file.model.File.')

    return entity
