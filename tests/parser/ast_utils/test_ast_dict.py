from vyper import (
    compiler,
)
from vyper.ast.utils import (
    ast_to_dict,
    dict_to_ast,
    parse_to_ast,
)


def get_node_ids(ast_struct, ids=None):
    if ids is None:
        ids = []

    for k, v in ast_struct.items():
        if isinstance(v, dict):
            ids = get_node_ids(v, ids)
        elif isinstance(v, list):
            for x in v:
                ids = get_node_ids(x, ids)
        elif k == 'node_id':
            ids.append(v)
        elif v is None or isinstance(v, (str, int)):
            continue
        else:
            raise Exception('Unknown ast_struct provided.')
    return ids


def test_ast_to_dict_node_id():
    code = """
@public
def test() -> int128:
    a: uint256 = 100
    return 123
    """
    dict_out = compiler.compile_code(code, ['ast_dict'])
    node_ids = get_node_ids(dict_out)

    assert len(node_ids) == len(set(node_ids))


def test_basic_ast():
    code = """
a: int128
    """
    dict_out = compiler.compile_code(code, ['ast_dict'])
    assert dict_out['ast_dict']['ast'][0] == {
      'annotation': {
        'ast_type': 'Name',
        'col_offset': 3,
        'end_col_offset': 9,
        'end_lineno': 2,
        'id': 'int128',
        'lineno': 2,
        'node_id': 4,
        'src': "4:6:0",
      },
      'ast_type': 'AnnAssign',
      'col_offset': 0,
      'end_col_offset': 9,
      'end_lineno': 2,
      'lineno': 2,
      'node_id': 1,
      'simple': 1,
      'src': '1:9:0',
      'target': {
        'ast_type': 'Name',
        'col_offset': 0,
        'end_col_offset': 1,
        'end_lineno': 2,
        'id': 'a',
        'lineno': 2,
        'node_id': 2,
        'src': '1:1:0',
      },
      'value': None
    }


def test_dict_to_ast():
    code = """
@public
def test() -> int128:
    a: uint256 = 100
    b: int128 = -22
    c: decimal = 3.31337
    d: bytes[11] = b"oh hai mark"
    e: address = 0xdeadbeefdeadbeefdeadbeefdeadbeefdeadbeef
    f: bool = False
    return 123
    """

    original_ast = parse_to_ast(code)
    out_dict = ast_to_dict(original_ast)
    new_ast = dict_to_ast(out_dict)

    assert new_ast == original_ast
