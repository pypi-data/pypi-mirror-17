# Copyright (c) 2016 Fabian Kochem


from libtree import exceptions
from libtree.core.node_data import NodeData
from libtree.utils import vectorize_nodes


def get_tree_size(cur):
    """
    Return the total amount of tree nodes.
    """
    sql = """
      SELECT
        COUNT(*)
      FROM
        nodes;
    """
    cur.execute(sql)
    result = cur.fetchone()
    return result['count']


def get_root_node(cur):
    """
    Return root node. Raise ``ValueError`` if root node doesn't exist.
    """
    sql = """
        SELECT
          *
        FROM
          nodes
        WHERE
          parent IS NULL;
    """
    cur.execute(sql)
    result = cur.fetchone()

    if result is None:
        raise exceptions.NoRootNode()
    else:
        return NodeData(**result)


def get_node(cur, id):
    """
    Return ``NodeData`` object for given ``id``. Raises ``ValueError``
    if ID doesn't exist.

    :param uuid4 id: Database ID
    """
    sql = """
        SELECT
          *
        FROM
          nodes
        WHERE
          id = %s;
    """
    if not isinstance(id, str):
        raise TypeError('ID must be type string (UUID4).')

    cur.execute(sql, (id, ))
    result = cur.fetchone()

    if result is None:
        raise exceptions.NodeNotFound(id)
    else:
        return NodeData(**result)


def get_node_at_position(cur, node, position):
    """
    Return node at ``position`` in the children of ``node``.

    :param node:
    :type node: Node or uuid4
    :param int position:
    """
    sql = """
      SELECT
        *
      FROM
        nodes
      WHERE
        parent=%s
      AND
        position=%s
    """

    cur.execute(sql, (str(node), position))
    result = cur.fetchone()

    if result is None:
        raise ValueError('Node does not exist.')
    else:
        return NodeData(**result)


def get_children(cur, node):
    """
    Return an iterator that yields a ``NodeData`` object of every
    immediate child.

    :param node:
    :type node: Node or uuid4
    """
    sql = """
        SELECT
          *
        FROM
          nodes
        WHERE
          parent=%s
        ORDER BY
          position;
    """
    cur.execute(sql, (str(node), ))
    for result in cur:
        yield NodeData(**result)


def get_child_ids(cur, node):
    """
    Return an iterator that yields the ID of every immediate child.

    :param node:
    :type node: Node or uuid4
    """
    sql = """
        SELECT
          id
        FROM
          nodes
        WHERE
          parent=%s
        ORDER BY
          position;
    """
    cur.execute(sql, (str(node), ))
    for result in cur:
        yield str(result['id'])


def get_children_count(cur, node):
    """
    Get amount of immediate children.

    :param node: Node
    :type node: Node or uuid4
    """
    sql = """
      SELECT
        COUNT(*)
      FROM
        nodes
      WHERE
        parent=%s;
    """
    cur.execute(sql, (str(node), ))
    result = cur.fetchone()
    return result['count']


def get_ancestors(cur, node, sort=True):
    """
    Return an iterator which yields a ``NodeData`` object for every
    node in the hierarchy chain from ``node`` to root node.

    :param node:
    :type node: Node or uuid4
    :param bool sort: Start with closest node and end with root node.
                      (default: True). Set to False if order is
                      unimportant.
    """
    # TODO: benchmark if vectorize_nodes() or WITH RECURSIVE is faster
    sql = """
        SELECT
          nodes.*
        FROM
          ancestors
        INNER JOIN
          nodes
        ON
          ancestors.ancestor=nodes.id
        WHERE
          ancestors.node=%s;
    """
    cur.execute(sql, (str(node), ))

    if sort:
        make_node = lambda r: NodeData(**r)
        for node in vectorize_nodes(map(make_node, cur))[::-1]:
            yield node
    else:
        for result in cur:
            yield NodeData(**result)


def get_ancestor_ids(cur, node):
    """
    Return an iterator that yields the ID of every element while
    traversing from ``node`` to the root node.

    :param node:
    :type node: Node or uuid4
    """
    # TODO: add sort parameter
    sql = """
        SELECT
          ancestor
        FROM
          ancestors
        WHERE
          node=%s;
    """
    cur.execute(sql, (str(node), ))
    for result in cur:
        yield str(result['ancestor'])


def get_descendants(cur, node):
    """
    Return an iterator that yields the ID of every element while
    traversing from ``node`` to the root node.

    :param node:
    :type node: Node or uuid4
    """
    sql = """
        SELECT
          nodes.*
        FROM
          ancestors
        INNER JOIN
          nodes
        ON
          ancestors.node=nodes.id
        WHERE
          ancestors.ancestor=%s;
    """
    cur.execute(sql, (str(node), ))
    for result in cur:
        yield NodeData(**result)


def get_descendant_ids(cur, node):
    """
    Return an iterator that yields a ``NodeData`` object of each element
    in the nodes subtree. Be careful when converting this iterator to an
    iterable (like list or set) because it could contain billions of
    objects.

    :param node:
    :type node: Node or uuid4
    """
    sql = """
        SELECT
          node
        FROM
          ancestors
        WHERE
          ancestor=%s;
    """
    cur.execute(sql, (str(node), ))
    for result in cur:
        yield str(result['node'])
