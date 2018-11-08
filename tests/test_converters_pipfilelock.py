import json
from dephell.converters import PIPFileLockConverter
from dephell.models import Requirement


def test_load():
    converter = PIPFileLockConverter()
    # https://github.com/pypa/pipfile/blob/master/examples/Pipfile.lock
    root = converter.load('./tests/requirements/pipfile.lock.json')
    deps = {dep.name: dep for dep in root.dependencies}
    assert 'requests' in deps
    assert 'records' in deps
    assert 'django' in deps
    assert str(deps['records'].constraint) == '==0.5.2'
    assert len(deps['pyyaml'].group.best_release.hashes) == 14


def test_dump():
    converter = PIPFileLockConverter()
    resolver = converter.load_resolver('./tests/requirements/pipfile.lock.json')
    reqs = Requirement.from_graph(graph=resolver.graph, lock=False)
    assert len(reqs) > 2
    content = converter.dumps(reqs=reqs)
    content = json.loads(content)
    assert content['default']['chardet']['version'] == '==3.0.4'