# Copyright (c) 2016 Fabian Kochem


import json

from libtree.core.node_data import NodeData
from libtree.core.query import get_ancestors, get_node
from libtree.utils import recursive_dict_merge


def get_nodes_by_property_dict(cur, query):
    """
    Return an iterator that yields a ``NodeData`` object of every node
    which contains all key/value pairs of ``query`` in its property
    dictionary. Inherited keys are not considered.

    :param dict query: The dictionary to search for
    """
    sql = """
        SELECT
          *
        FROM
          nodes
        WHERE
          properties @> %s;
    """
    cur.execute(sql, (json.dumps(query), ))
    for result in cur:
        yield NodeData(**result)


def get_nodes_by_property_key(cur, key):
    """
    Return an iterator that yields a ``NodeData`` object of every node
    which contains ``key`` in its property dictionary. Inherited keys
    are not considered.

    :param str key: The key to search for
    """
    sql = """
        SELECT
          *
        FROM
          nodes
        WHERE
          properties ? %s;
    """
    cur.execute(sql, (key, ))
    for result in cur:
        yield NodeData(**result)


def get_nodes_by_property_value(cur, key, value):
    """
    Return an iterator that yields a ``NodeData`` object of every node
    which has ``key`` exactly set to ``value`` in its property
    dictionary. Inherited keys are not considered.

    :param str key: The key to search for
    :param object value: The exact value to sarch for
    """
    query = {key: value}
    for node in get_nodes_by_property_dict(cur, query):
        yield node


def get_inherited_properties(cur, node):
    """
    Get the entire inherited property dictionary.

    To calculate this, the trees path from root node till ``node`` will
    be traversed. For each level, the property dictionary will be merged
    into the previous one. This is a simple merge, only the first level
    of keys will be combined.

    :param node:
    :type node: Node or uuid4
    :rtype: dict
    """
    ret = {}
    id = str(node)
    if isinstance(node, str):
        node = get_node(cur, id)

    ancestors = list(get_ancestors(cur, id))

    for ancestor in ancestors[::-1]:  # Go top down
        ret.update(ancestor.properties)

    ret.update(node.properties)

    return ret


def get_inherited_property_value(cur, node, key):
    """
    Get the inherited value for a single property key.

    :param node:
    :type node: Node or uuid4
    :param key: str
    """
    return get_inherited_properties(cur, node)[key]


def get_recursive_properties(cur, node):
    """
    Get the entire inherited and recursively merged property dictionary.

    To calculate this, the trees path from root node till ``node`` will
    be traversed. For each level, the property dictionary will be merged
    into the previous one. This is a recursive merge, so all dictionary
    levels will be combined.

    :param node:
    :type node: Node or uuid4
    :rtype: dict
    """
    ret = {}
    id = str(node)
    if isinstance(node, str):
        node = get_node(cur, id)

    ancestors = list(get_ancestors(cur, id))

    for ancestor in ancestors[::-1]:  # Go top down
        recursive_dict_merge(ret, ancestor.properties, create_copy=False)

    recursive_dict_merge(ret, node.properties, create_copy=False)

    return ret


def set_properties(cur, node, new_properties):
    """
    Set the property dictionary to ``new_properties``.
    Return ``NodeData`` object with updated properties.

    :param node:
    :type node: Node or uuid4
    :param new_properties: dict
    """
    if not isinstance(new_properties, dict):
        raise TypeError('Only dictionaries are supported.')

    id = str(node)
    if isinstance(node, str):
        node = get_node(cur, id)

    sql = """
        UPDATE
          nodes
        SET
          properties=%s
        WHERE
          id=%s;
    """
    cur.execute(sql, (json.dumps(new_properties), str(node)))

    kwargs = node.to_dict()
    kwargs['properties'] = new_properties
    return NodeData(**kwargs)


def update_properties(cur, node, new_properties):
    """
    Update existing property dictionary with another dictionary.
    Return ``NodeData`` object with updated properties.

    :param node:
    :type node: Node or uuid4
    :param new_properties: dict
    """
    if not isinstance(new_properties, dict):
        raise TypeError('Only dictionaries are supported.')

    id = str(node)
    if isinstance(node, str):
        node = get_node(cur, id)

    properties = node.properties.copy()
    properties.update(new_properties)
    return set_properties(cur, node, properties)


def set_property_value(cur, node, key, value):
    """
    Set the value for a single property key.
    Return ``NodeData`` object with updated properties.

    :param node:
    :type node: Node or uuid4
    :param key: str
    :param value: object
    """
    id = str(node)
    if isinstance(node, str):
        node = get_node(cur, id)

    properties = node.properties.copy()
    properties[key] = value
    set_properties(cur, node, properties)

    kwargs = node.to_dict()
    kwargs['properties'] = properties
    return NodeData(**kwargs)
