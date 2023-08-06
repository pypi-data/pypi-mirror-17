# -*- coding: utf-8 -*-
#
# This file is part of Inspirehep.
# Copyright (C) 2016 CERN.
#
# Inspirehep is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 2 of the
# License, or (at your option) any later version.
#
# Inspirehep is distributed in the hope that it will be
# useful, but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Inspirehep; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330, Boston,
# MA 02111-1307, USA.
#
# In applying this license, CERN does not
# waive the privileges and immunities granted to it by virtue of its status
# as an Intergovernmental Organization or submit itself to any jurisdiction.

from __future__ import absolute_import, print_function

import six

from .comparator import DefaultComparator
from .nothing import NOTHING

FIRST = 'first'


class BeforeNodes(object):

    def __init__(self, head_node=None, update_node=None):
        self.head_node = head_node
        self.update_node = update_node

    def __repr__(self):
        return 'BeforeNodes <head_node: {}, update_node: {}>'.format(
            self.head_node, self.update_node)


class ListMatchStats(object):

    def __init__(self, lst, root):
        self.lst = lst
        self.root = root

        self.in_result_idx = set()
        self.not_in_result_idx = set(range(len(lst)))
        self.not_in_result_root_match_idx = set()
        self.root_matches = {}

    def move_to_result(self, lst_idx):
        self.in_result_idx.add(lst_idx)
        self.not_in_result_idx.remove(lst_idx)

        if lst_idx in self.not_in_result_root_match_idx:
            self.not_in_result_root_match_idx.remove(lst_idx)

    def add_root_match(self, lst_idx, root_idx):
        self.root_matches[lst_idx] = root_idx
        if lst_idx in self.in_result_idx:
            return

        self.not_in_result_root_match_idx.add(lst_idx)

    @property
    def not_in_result_not_root_match_idx(self):
        return self.not_in_result_idx.difference(
            self.not_in_result_root_match_idx)

    @property
    def in_result(self):
        return [self.lst[e] for e in self.in_result_idx]

    @property
    def not_in_result(self):
        return [self.lst[e] for e in self.not_in_result_idx]

    @property
    def not_in_result_root_match(self):
        return [self.lst[e] for e in self.not_in_result_root_match_idx]

    @property
    def not_in_result_not_root_match(self):
        return [self.lst[e] for e in self.not_in_result_not_root_match_idx]

    @property
    def not_in_result_root_match_pairs(self):
        return [(self.lst[e], self.root[self.root_matches[e]])
                for e in self.not_in_result_root_match_idx]

    @property
    def not_matched_root_objects(self):
        matched_root_idx = set(self.root_matches.values())
        return [o for idx, o in enumerate(self.root)
                if idx not in matched_root_idx]


class ListMatchGraphBuilder(object):

    def __init__(self, root, head, update, sources,
                 comparator_cls=DefaultComparator):
        self.root = root
        self.head = head
        self.update = update
        self.sources = sources

        self.root_head_comparator = comparator_cls(self.root, self.head)
        self.root_update_comparator = comparator_cls(self.root, self.update)
        self.head_update_comparator = comparator_cls(self.head, self.update)

        # Keys are (target, source), values are comparator_instance and
        # the source list from which to search.
        self.comparators = {
            ('root', 'head'): (self.root_head_comparator, 'l2'),
            ('head', 'root'): (self.root_head_comparator, 'l1'),
            ('root', 'update'): (self.root_update_comparator, 'l2'),
            ('update', 'root'): (self.root_update_comparator, 'l1'),
            ('head', 'update'): (self.head_update_comparator, 'l2'),
            ('update', 'head'): (self.head_update_comparator, 'l1'),
        }

        self.node_data = {}
        self.graph = {}
        self.head_stats = ListMatchStats(head, root)
        self.update_stats = ListMatchStats(update, root)

        self._node_src_indices = {}
        self._head_idx_to_node = {}
        self._update_idx_to_node = {}
        self._dirty_nodes = set()

        self._next_node_id = 0

        self.multiple_match_choice_idx = set()
        self.multiple_match_choices = []

    def _new_node_id(self):
        node_id = self._next_node_id
        self._next_node_id += 1
        return node_id

    def _push_node(self, root_elem, head_elem, update_elem):
        root_idx, root_obj = root_elem
        head_idx, head_obj = head_elem
        update_idx, update_obj = update_elem

        node_id = self._new_node_id()
        self.node_data[node_id] = (root_obj, head_obj, update_obj)
        self._node_src_indices[node_id] = (root_idx, head_idx, update_idx)

        if head_idx >= 0:
            self._head_idx_to_node[head_idx] = node_id
        if update_idx >= 0:
            self._update_idx_to_node[update_idx] = node_id

    def _get_nodes(self, head_elem, update_elem):
        """Get nodes to which either head_elem or update_elem point to."""
        head_idx, head_obj = head_elem
        update_idx, update_obj = update_elem
        res = set()

        if head_idx in self._head_idx_to_node:
            res.add(self._head_idx_to_node[head_idx])
        if update_idx in self._update_idx_to_node:
            res.add(self._update_idx_to_node[update_idx])

        return res

    def _pop_node(self, node_id):
        """Remove a node from the graph."""
        root_idx, head_idx, update_idx = self._node_src_indices[node_id]
        del self._node_src_indices[node_id]
        del self.node_data[node_id]

        if head_idx in self._head_idx_to_node:
            del self._head_idx_to_node[head_idx]
        if update_idx in self._update_idx_to_node:
            del self._update_idx_to_node[update_idx]

    def _get_matches(self, target, source, source_idx):
        comparator, src_list = self.comparators[(target, source)]
        matches = comparator.get_matches(src_list, source_idx)
        return matches if matches else [(-1, NOTHING)]

    def _add_matches(self, root_elems, head_elems, update_elems):
        matches = [(r, h, u)
                   for r in root_elems
                   for h in head_elems
                   for u in update_elems]
        if len(matches) == 1:
            root_elem, head_elem, update_elem = matches[0]
            node_ids = self._get_nodes(head_elem, update_elem)
            # If this single match overrides a previous node entry we remove
            # add this match as a multiple_match_choice and mark the node
            # for removal. We will later remove the node from the graph so
            # that future collisions with this node will be caught.
            if not node_ids:
                self._push_node(root_elem, head_elem, update_elem)
            else:
                self._dirty_nodes.update(node_ids)
                self.multiple_match_choice_idx.add(
                    (root_elem[0], head_elem[0], update_elem[0]))
        else:
            match_indices = [(r[0], h[0], u[0]) for r, h, u in matches]
            self.multiple_match_choice_idx.update(match_indices)

    def _populate_nodes(self):
        if 'head' in self.sources:
            for head_idx, head_obj in enumerate(self.head):
                head_elems = [(head_idx, head_obj)]
                root_elems = self._get_matches('root', 'head', head_idx)
                update_elems = self._get_matches('update', 'head', head_idx)
                self._add_matches(root_elems, head_elems, update_elems)

        if 'update' in self.sources:
            for update_idx, update_obj in enumerate(self.update):
                # Already added this node in the graph, continue.
                if update_idx in self._update_idx_to_node:
                    continue

                update_elems = [(update_idx, update_obj)]
                root_elems = self._get_matches('root', 'update', update_idx)
                head_elems = self._get_matches('head', 'update', update_idx)
                self._add_matches(root_elems, head_elems, update_elems)

        for node_id in self._dirty_nodes:
            self.multiple_match_choice_idx.add(self._node_src_indices[node_id])
            self._pop_node(node_id)
        for r_idx, h_idx, u_idx in self.multiple_match_choice_idx:
            r_obj = self.root[r_idx] if r_idx >= 0 else None
            h_obj = self.head[h_idx] if h_idx >= 0 else None
            u_obj = self.update[u_idx] if u_idx >= 0 else None
            self.multiple_match_choices.append((r_obj, h_obj, u_obj))

    def _build_stats(self):
        for node_id, indices in self._node_src_indices.items():
            root_idx, head_idx, update_idx = indices

            if head_idx >= 0:
                self.head_stats.move_to_result(head_idx)
            if update_idx >= 0:
                self.update_stats.move_to_result(update_idx)

        for idx in range(len(self.head)):
            matches = self._get_matches('root', 'head', idx)
            # Matches[0][0] is the index in the root list of the first match.
            if len(matches) == 1 and matches[0][0] >= 0:
                self.head_stats.add_root_match(idx, matches[0][0])

        for idx in range(len(self.update)):
            matches = self._get_matches('root', 'update', idx)
            if len(matches) == 1 and matches[0][0] >= 0:
                self.update_stats.add_root_match(idx, matches[0][0])

    def _get_next_node(self, source, indices):
        if source not in self.sources:
            return None
        idx_to_node = {
            'head': self._head_idx_to_node,
            'update': self._update_idx_to_node
        }[source]
        for idx in indices:
            if idx in idx_to_node:
                return idx_to_node[idx]
        return None

    def build_graph(self):
        self._populate_nodes()
        self._build_stats()

        # Link a dummy first node before the first element of the sources
        # lists.
        self.node_data[FIRST] = (NOTHING, NOTHING, NOTHING)
        self.graph[FIRST] = BeforeNodes()

        next_head_node = self._get_next_node('head', range(len(self.head)))
        next_update_node = self._get_next_node('update',
                                               range(len(self.update)))
        self.graph[FIRST].head_node = next_head_node
        self.graph[FIRST].update_node = next_update_node

        # Link any other nodes with the elements that come after them in their
        # source lists.
        for node_id, node_indices in six.iteritems(self._node_src_indices):
            root_idx, head_idx, update_idx = node_indices
            head_next_l = []
            update_next_l = []
            if head_idx >= 0:
                head_next_l = range(head_idx + 1, len(self.head))
            if update_idx >= 0:
                update_next_l = range(update_idx + 1, len(self.update))

            next_head_node = self._get_next_node('head', head_next_l)
            next_update_node = self._get_next_node('update', update_next_l)
            self.graph[node_id] = BeforeNodes(next_head_node, next_update_node)

        return self.graph, self.node_data


def _get_traversal(next_nodes, pick_first):
    if pick_first == 'head':
        return [next_nodes.update_node, next_nodes.head_node]
    else:
        return [next_nodes.head_node, next_nodes.update_node]


def toposort(graph, pick_first='head'):
    """Toplogically sorts a list match graph.

    Tries to perform a topological sort using as tiebreaker the pick_first
    argument. If the graph contains cycles, raise ValueError.
    """
    in_deg = {}
    for node, next_nodes in six.iteritems(graph):
        for next_node in [next_nodes.head_node, next_nodes.update_node]:
            if next_node is None:
                continue
            in_deg[next_node] = in_deg.get(next_node, 0) + 1

    stk = [FIRST]
    ordered = []
    visited = set()
    while stk:
        node = stk.pop()
        visited.add(node)
        if node != FIRST:
            ordered.append(node)
        traversal = _get_traversal(graph.get(node, BeforeNodes()), pick_first)
        for next_node in traversal:
            if next_node is None:
                continue
            if next_node in visited:
                raise ValueError('Graph has a cycle')

            in_deg[next_node] -= 1
            if in_deg[next_node] == 0:
                stk.append(next_node)

    # Nodes may not be walked because they don't reach in degree 0.
    if len(ordered) != len(graph) - 1:
        raise ValueError('Graph has a cycle')
    return ordered


def sort_cyclic_graph_best_effort(graph, pick_first='head'):
    """Fallback for cases in which the graph has cycles."""
    ordered = []
    visited = set()
    # Go first on the pick_first chain then go back again on the others
    # that were not visited. Given the way the graph is built both chains
    # will always contain all the elements.
    if pick_first == 'head':
        fst_attr, snd_attr = ('head_node', 'update_node')
    else:
        fst_attr, snd_attr = ('update_node', 'head_node')

    current = FIRST
    while current is not None:
        visited.add(current)
        current = getattr(graph[current], fst_attr)
        if current not in visited and current is not None:
            ordered.append(current)
    current = FIRST
    while current is not None:
        visited.add(current)
        current = getattr(graph[current], snd_attr)
        if current not in visited and current is not None:
            ordered.append(current)
    return ordered
