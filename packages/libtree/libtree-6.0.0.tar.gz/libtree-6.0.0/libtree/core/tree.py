# Copyright (c) 2016 Fabian Kochem


import json
import uuid

from libtree import exceptions
from libtree.core.node_data import NodeData
from libtree.core.positioning import (ensure_free_position,
                                      find_highest_position, shift_positions)
from libtree.core.query import (get_children, get_descendant_ids, get_node,
                                get_root_node)


def print_tree(cur, start_node=None, indent='  ', _level=0):
    """
    Print tree to stdout.

    :param start_node: Starting point for tree output.
                       If ``None``, start at root node.
    :type start_node: int, Node, NodaData or None
    :param str indent: String to print per level (default: '  ')
    """
    if start_node is None:
        start_node = get_root_node(cur)

    print('{}{}'.format(indent * _level, repr(start_node)))  # noqa

    for child in list(get_children(cur, start_node)):
        print_tree(cur, child, indent=indent, _level=_level + 1)


def insert_node(cur, parent, properties=None, position=None,
                auto_position=True, id=None):
    """
    Create a ``Node`` object, insert it into the tree and then return
    it.

    :param parent: Reference to its parent node. If `None`, this will
                   be the root node.
    :type parent: Node or uuid4
    :param dict properties: Inheritable key/value pairs
                            (see :ref:`core-properties`)
    :param int position: Position in between siblings. If 0, the node
                         will be inserted at the beginning of the
                         parents children. If -1, the node will be
                         inserted the the end of the parents children.
                         If `auto_position` is disabled, this is just a
                         value.
    :param bool auto_position: See :ref:`core-positioning`
    :param uuid4 id: Use this ID instead of automatically generating
                     one.
    """
    if id is None:
        id = str(uuid.uuid4())

    parent_id = None
    if parent is not None:
        parent_id = str(parent)

    if properties is None:
        properties = {}

    # Can't run set_position() because the node doesn't exist yet
    if auto_position:
        if isinstance(position, int) and position >= 0:
            ensure_free_position(cur, parent, position)
        else:
            position = find_highest_position(cur, parent) + 1

    sql = """
        INSERT INTO
          nodes
          (id, parent, position, properties)
        VALUES
          (%s, %s, %s, %s);
    """
    cur.execute(sql, (id, parent_id, position, json.dumps(properties)))

    return NodeData(id, parent_id, position, properties)


def delete_node(cur, node, auto_position=True):
    """
    Delete node and its subtree.

    :param node:
    :type node: Node or uuid4
    :param bool auto_position: See :ref:`core-positioning`
    """
    id = str(node)

    # Get Node object if integer (ID) was passed
    if auto_position and not isinstance(node, NodeData):
        node = get_node(cur, id)

    sql = """
        DELETE FROM
          nodes
        WHERE
          id=%s;
    """
    cur.execute(sql, (id, ))

    if auto_position:
        shift_positions(cur, node.parent, node.position, -1)


def change_parent(cur, node, new_parent, position=None, auto_position=True):
    """
    Move node and its subtree from its current to another parent node.
    Return updated ``Node`` object with new parent set. Raise
    ``ValueError`` if ``new_parent`` is inside ``node`` s subtree.

    :param node:
    :type node: Node or uuid4
    :param new_parent: Reference to the new parent node
    :type new_parent: Node or uuid4
    :param int position: Position in between siblings. If 0, the node
                         will be inserted at the beginning of the
                         parents children. If -1, the node will be
                         inserted the the end of the parents children.
                         If `auto_position` is disabled, this is just a
                         value.
    :param bool auto_position: See :ref:`core-positioning`.
    """
    new_parent_id = str(new_parent)
    if new_parent_id in get_descendant_ids(cur, node):
        raise exceptions.CantMoveIntoOwnSubtree()

    # Can't run set_position() here because the node hasn't been moved yet,
    # must do it manually
    if auto_position:
        if isinstance(position, int) and position >= 0:
            ensure_free_position(cur, new_parent_id, position)
        else:
            position = find_highest_position(cur, new_parent_id) + 1

    sql = """
        UPDATE
          nodes
        SET
          parent=%s,
          position=%s
        WHERE
          id=%s;
    """
    cur.execute(sql, (new_parent_id, position, str(node)))

    if isinstance(node, str):
        node = get_node(cur, node)

    kwargs = node.to_dict()
    kwargs['parent'] = new_parent_id
    kwargs['position'] = position
    return NodeData(**kwargs)
