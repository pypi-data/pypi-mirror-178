import copy

from ..universe import Universe


class Pipe:

    def __init__(self, definition: str):
        self._definition = definition

        self._model = None
        self._model_node = None
        self._node_type = None
        self._orders = []
        self._filters = []

    def model(self, model_id):
        new_pipe = copy.copy(self)
        new_pipe._model = model_id
        return new_pipe

    def filter(self, path: str, operator: str, value: any):
        new_pipe = copy.copy(self)
        new_pipe._filters.append({
            'path': path,
            'operator': operator,
            'value': value,
        })
        return new_pipe

    def order(self, path: str, asc=True):
        new_pipe = copy.copy(self)
        new_pipe._orders.append({
            'path': path,
            'ascending': asc,
        })
        return new_pipe

    def list_node(self):
        node = {
            'type': 'list',
            'list': {
                'entry': self._model_node,
            }
        }

        for o in self._orders:
            node = {
                'type': 'sort',
                'sort': {
                    'order': {
                        'source': self._path_source(o['path']),
                        'ascending': o['ascending'],
                    },
                    'node': node,
                }
            }

        for f in self._filters:
            node = {
                'type': 'filter',
                'filter': {
                    'filter': {
                        'source': self._path_source(f['path']),
                        'operator': f['operator'],
                        'value': f['value'],
                    },
                    'node': node,
                }
            }

        node = {
            'type': 'context',
            'context': {
                'context': {
                    'value': self._model,
                },
                'node': {
                    'type': 'specials',
                    'specials': {
                        'type': 'list',
                        'direct': True,
                        'indirect': True,
                        'node': node,
                    }
                }
            }
        }

        return node

    def _path_source(self, path: str):
        path_node = self._model_node
        source_node = None
        cur_node = {}
        format = ''
        paths = path.split('.')

        if len(paths) > 0 and paths[0] != '':
            paths.append('')

        def descend_path(node, node_ptr):
            nonlocal source_node, cur_node
            if not source_node:
                source_node = node
                cur_node = node_ptr
            else:
                cur_node = node
                cur_node = node_ptr

        for p in paths:
            if p != '':
                if path_node['type'] == 'map':
                    for e in path_node['map']['entries']:
                        if e['name'] == p:
                            path_node = e['node']
                            break
                    else:
                        raise RuntimeError(f'Entry not found: {p}')
                    continue

            while True:
                path_node_type = path_node['type']

                if path_node_type == 'value':
                    node = copy.copy(path_node)
                    format = path_node['value']['format']
                    descend_path(node, None)
                    break

                if path_node_type == 'relation':
                    node = copy.copy(path_node)
                    path_node = path_node['relation']['node']
                    descend_path(node, node['relation']['node'])
                    continue

                if path_node_type == 'specials':
                    node = copy.copy(path_node)
                    path_node = path_node['specials']['node']
                    descend_path(node, node['specials']['node'])
                    continue

        return {
            'type': 'node',
            'format': format,
            'node': source_node
        }

    def load_pipe(self, universe: Universe) -> None:
        if self._definition.startswith('$'):
            endpoint_node = universe.get_pipe(self._definition[1:])
            if not endpoint_node:
                raise RuntimeError(f'Endpoint not found: {self._definition[1:]}')

            self._model_node = endpoint_node['node']
            self._node_type = endpoint_node['type']

            if endpoint_node['context']['value']:
                self._model = endpoint_node['context']['context']['value']
            elif endpoint_node['context']['environment'].get('model'):
                self._model = endpoint_node['context']['environment']['model']

        else:
            # TODO: Parse VyLang pipe definition
            pass

    def __copy__(self):
        new_pipe = Pipe(self._definition)
        new_pipe._model = self._model
        new_pipe._model_node = copy.deepcopy(self._model_node)
        new_pipe._node_type = self._node_type
        return new_pipe
