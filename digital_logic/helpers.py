import importlib
import os
import pkgutil

from flask import Blueprint


def register_blueprints(app, package_name, package_path):  # pragma: no cover
    """
    Register all Blueprint instances on the specified Flask application found
    in all modules for any found package

    :param app: the Flask application
    :param package_name: the package name
    :param package_path: the package path
    :return:
    """
    rv = []
    base_dir = package_path[0]
    for _, pkgname, ispkg in pkgutil.walk_packages([base_dir]):
        for _, modname, ismod in pkgutil.iter_modules(
                [os.path.join(base_dir, pkgname)]):
            m = importlib.import_module(
                '{0}.{1}.{2}'.format(package_name, pkgname, modname))
            for item in dir(m):
                item = getattr(m, item)
                if isinstance(item, Blueprint):
                    app.register_blueprint(item)
                rv.append(item)

    return rv


def parse_user_agent(raw):
    from ua_parser import user_agent_parser

    def make_version_string(dct):
        parts = []
        parts.append(dct['major'] or '0')
        parts.append(dct['minor'] or '0')
        if dct['patch'] is not None:
            parts.append(dct['patch'])
        res = ".".join(parts)
        if 'patch_minor' in dct and dct['patch_minor'] is not None:
            res += '-' + dct['patch_minor']
        return res

    parsed = user_agent_parser.Parse(raw)
    result = dict()
    result['ua_raw'] = raw
    result['ua_browser'] = parsed['user_agent']['family']
    result['ua_browser_version'] = make_version_string(parsed['user_agent'])
    result['ua_device'] = parsed['device']['family']
    result['ua_os'] = parsed['os']['family']
    result['ua_os_version'] = make_version_string(parsed['os'])

    return result


def make_external_id(worker_id, assignment_id, hit_id):
    import hashlib
    hash = hashlib.md5()
    hash.update(worker_id.encode('utf-8'))
    hash.update(assignment_id.encode('utf-8'))
    hash.update(hit_id.encode('utf-8'))

    return hash.hexdigest()
