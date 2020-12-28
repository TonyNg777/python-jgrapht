from .. import backend as _backend

from .._internals._intgraph._flows import (
    _JGraphTCut,
    _JGraphTIntegerFlow,
    _JGraphTLongFlow,
    _JGraphTIntegerEquivalentFlowTree,
    _JGraphTLongEquivalentFlowTree,
)
from .._internals._intgraph._long_graphs import _is_long_graph
from .._internals._mapgraph._graphs import (
    _is_anyhashable_graph,
    _vertex_anyhashableg_to_g as _vertex_anyhashableg_to_g,
)
from .._internals._mapgraph._flows import (
    _AnyHashableGraphCut,
    _AnyHashableGraphFlow,
    _AnyHashableGraphEquivalentFlowTree,
)
from .._internals._refgraph._graphs import _is_refcount_graph
from .._internals._refgraph._flows import (
    _RefCountGraphCut,
    _RefCountGraphFlow,
    __RefCountGraphEquivalentFlowTree,
)


def _maxflow_alg(name, graph, source, sink, *args):
    if _is_anyhashable_graph(graph):
        alg_method = getattr(_backend, "jgrapht_ii_maxflow_exec_" + name)
        flow_value, flow_handle, cut_source_partition_handle = alg_method(
            graph.handle,
            _vertex_anyhashableg_to_g(graph, source),
            _vertex_anyhashableg_to_g(graph, sink),
            *args
        )
    elif _is_refcount_graph(graph):
        alg_method = getattr(_backend, "jgrapht_ll_maxflow_exec_" + name)
        flow_value, flow_handle, cut_source_partition_handle = alg_method(
            graph.handle,
            id(source),
            id(sink),
            *args
        )
    elif _is_long_graph(graph):
        alg_method = getattr(_backend, "jgrapht_ll_maxflow_exec_" + name)
        flow_value, flow_handle, cut_source_partition_handle = alg_method(
            graph.handle,
            source,
            sink,
            *args
        )
    else:
        alg_method = getattr(_backend, "jgrapht_ii_maxflow_exec_" + name)
        flow_value, flow_handle, cut_source_partition_handle = alg_method(
            graph.handle,
            source,
            sink,
            *args
        )

    if _is_anyhashable_graph(graph):
        flow = _AnyHashableGraphFlow(graph, flow_handle, source, sink, flow_value)
        cut = _AnyHashableGraphCut(graph, flow_value, cut_source_partition_handle)
    elif _is_refcount_graph(graph):
        flow = _RefCountGraphFlow(flow_handle, source, sink, flow_value)
        cut = _RefCountGraphCut(graph, flow_value, cut_source_partition_handle)
    elif _is_long_graph(graph):
        flow = _JGraphTLongFlow(flow_handle, source, sink, flow_value)
        cut = _JGraphTCut(graph, flow_value, cut_source_partition_handle)
    else:
        flow = _JGraphTIntegerFlow(flow_handle, source, sink, flow_value)
        cut = _JGraphTCut(graph, flow_value, cut_source_partition_handle)

    return flow, cut


def dinic(graph, source, sink):
    r"""Compute a maximum flow using Dinic's algorithm with scaling.

    This is a :math:`\mathcal{O}(n^2 m)` algorithm where :math:`n` is the number of vertices
    and :math:`m` the number of edges of the graph.

    The algorithm uses the graph edge weights as the network edge capacities.
    It returns a maximum s-t flow and a minimum s-t cut with the same value.

    :param graph: The input graph. This can be either directed or undirected. Edge capacities
                  are taken from the edge weights.
    :param source: The source vertex
    :param sink: The sink vertex.
    :returns: A tuple (max s-t flow, min s-t cut).
    """
    return _maxflow_alg("dinic", graph, source, sink)


def push_relabel(graph, source, sink):
    r"""Compute a maximum flow using the Push-relabel algorithm.

    This is a :math:`\mathcal{O}(n^3)` algorithm where :math:`n` is the number of vertices
    of the graph. For more details on the algorithm see:

      * Andrew V. Goldberg and Robert Tarjan. A new approach to the maximum flow problem.
        Proceedings of STOC '86.

    The algorithm uses the graph edge weights as the network edge capacities.
    It returns a maximum s-t flow and a minimum s-t cut with the same value.

    :param graph: The input graph. This can be either directed or undirected. Edge capacities
                  are taken from the edge weights.
    :param source: The source vertex
    :param sink: The sink vertex.
    :returns: A tuple (max s-t flow, min s-t cut).
    """
    return _maxflow_alg("push_relabel", graph, source, sink)


def edmonds_karp(graph, source, sink):
    r"""Compute a maximum flow using the Edmonds-Karp variant of the Ford-Fulkerson algorithm.

    This is a :math:`\mathcal{O}(n m^2)` algorithm where :math:`n` is the number of vertices
    and :math:`m` the number of edges of the graph.

    The algorithm uses the graph edge weights as the network edge capacities.
    It returns a maximum s-t flow and a minimum s-t cut with the same value.

    .. note:: This implementation assumes that the graph does not contain self-loops or multiple-edges.

    :param graph: The input graph. This can be either directed or undirected. Edge capacities
                  are taken from the edge weights.
    :param source: The source vertex
    :param sink: The sink vertex.
    :returns: A tuple (max s-t flow, min s-t cut).
    """
    return _maxflow_alg("edmonds_karp", graph, source, sink)


def max_st_flow(graph, source, sink):
    r"""Compute a maximum flow using the Push-relabel algorithm.

    This is a :math:`\mathcal{O}(n^3)` algorithm where :math:`n` is the number of vertices
    of the graph. For more details on the algorithm see:

      * Andrew V. Goldberg and Robert Tarjan. A new approach to the maximum flow problem.
        Proceedings of STOC '86.

    The algorithm uses the graph edge weights as the network edge capacities.

    :param graph: The input graph. This can be either directed or undirected. Edge capacities
                  are taken from the edge weights.
    :param source: The source vertex
    :param sink: The sink vertex.
    :returns: The max s-t flow.
    """
    flow, _ = push_relabel(graph, source, sink)
    return flow


def equivalent_flow_tree_gusfield(graph):
    r"""Computes an Equivalent Flow Tree using Gusfield's algorithm.

    Equivalent flow trees can be used to calculate the maximum flow value between all pairs
    of vertices in an undirected network. It does so by performing :math:`n-1` minimum
    s-t cut computations.

    For more details see:

      * Gusfield, D, Very simple methods for all pairs network flow analysis. SIAM Journal
        on Computing, 19(1), p142-155, 1990

    This implementation uses the push-relabel algorithm for the minimum s-t cut which
    is :math:`\mathcal{O}(n^3)`. The total complexity is, therefore, :math:`\mathcal{O}(n^4)`.

    :param graph: an undirected network
    :returns: an equivalent flow tree as an instance of :py:class:`jgrapht.types.EquivalentFlowTree`
    """
    handle = _backend.jgrapht_xx_equivalentflowtree_exec_gusfield(graph.handle)

    if _is_anyhashable_graph(graph):
        return _AnyHashableGraphEquivalentFlowTree(handle, graph)
    if _is_refcount_graph(graph):
        return __RefCountGraphEquivalentFlowTree(handle, graph)
    elif _is_long_graph(graph):
        return _JGraphTLongEquivalentFlowTree(handle, graph)
    else:
        return _JGraphTIntegerEquivalentFlowTree(handle, graph)
