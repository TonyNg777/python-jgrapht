from . import backend
from ._internals._wrappers import (
    _JGraphTLongDoubleMap,
    _JGraphTLongSet,
)


def diameter(graph):
    r"""Compute the `diameter <https://mathworld.wolfram.com/GraphDiameter.html>`_ of a graph. The  
    diameter of a graph is defined as :math:`\max_{v\in V}\epsilon(v)`, where :math:`\epsilon(v)`
    is the eccentricity of vertex :math:`v`. In other words, this method computes the 'longest
    shortest path'. Two special cases exist: (a) if the graph has no vertices, the diameter is 0,
    and (b) if the graph is disconnected, the diameter is positive infinity.

    :param graph: the input graph
    :returns: the graph diameter
    """
    return backend.jgrapht_graph_metrics_diameter(graph.handle)


def radius(graph):
    r"""Compute the `radius <https://mathworld.wolfram.com/GraphRadius.html>`_ of a graph. 

    The radius of a graph is the minimum vertex eccentricity.

    .. note::
    
      If the graph has no vertices, the radius is zero. In case the graph is disconnected, the 
      radius is positive infinity.

    :param graph: the input graph
    :returns: the graph diameter
    """
    return backend.jgrapht_graph_metrics_radius(graph.handle)


def girth(graph):
    r"""Compute the `girth <https://mathworld.wolfram.com/Girth.html>`_ of a graph. 

    The girth is the length of the shortest graph cycle (if any) in a graph. Acyclic graphs
    are considered to have infinite girth. For directed graphs, the length of the shortest 
    directed cycle is returned.

    This method invokes a breadth-first search from every vertex in the graph. Thus, its 
    runtime complexity is :math:`\mathcal{O}(n(m+n)) = \mathcal{O}(m n)`.

    :param graph: the input graph
    :returns: the graph girth
    """
    return backend.jgrapht_graph_metrics_girth(graph.handle)


def count_triangles(graph):
    r"""Count the number of triangles in a graph.

    This is an :math:`\mathcal{O}(m^{3/2})` algorithm for counting the number of 
    triangles in an undirected graph.

    :param graph: the input graph. Must be undirected
    :returns: the number of triangles in the graph 
    :raises IllegalArgumentError: if the graph is not undirected
    """
    return backend.jgrapht_graph_metrics_triangles(graph.handle)


def measure(graph): 
    """Measure the graph. This method executes an all-pairs shortest paths 
    using Floyd-Warshal.

    This method computes: 

     * the graph diameter
     * the graph radius
     * the set of vertices which form the center of the graph
     * the set of vertices which form the periphery of the graph
     * the set of vertices which form the pseudo-periphery of the graph
     * the vertex eccentricity map

    :param graph: the input graph
    :returns: a 6-tuple containing the results.
    """
    ( 
        diameter, 
        radius, 
        center_handle,
        periphery_handle,
        pseudo_periphery_handle,
        vertex_eccentricity_map_handle
    ) = backend.jgrapht_graph_metrics_measure_graph(graph.handle)

    return (
        diameter, 
        radius, 
        _JGraphTLongSet(handle=center_handle),
        _JGraphTLongSet(handle=periphery_handle),
        _JGraphTLongSet(handle=pseudo_periphery_handle),
        _JGraphTLongDoubleMap(handle=vertex_eccentricity_map_handle),
    )
