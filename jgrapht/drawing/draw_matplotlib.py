
from ..algorithms.drawing import (
    circular_layout_2d,
    random_layout_2d,
    fruchterman_reingold_layout_2d,
    fruchterman_reingold_indexed_layout_2d
)


def draw(g, positions=None, ax=None, **kwds):
    """Draw a graph using Matplotlib.

    Draws the graph as a simple representation with no node labels or edge labels
    and using the full Matplotlib figure area and no axis labels by default.
    See draw_jgrapht() for more full-featured drawing that allows title, axis labels etc.

    :param g: graph
    :param positions: vertices positions
    :param kwargs: additional arguments to pass through
    :param ax: draw the graph in the specified Matplotlib axes
    :type positions: dictionary, optional
    :type ax: Matplotlib Axes object, optional
    :type kwargs: optional keywords

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> g = jgrapht.create_graph(directed=False, weighted=True)
    >>> for i in range(0,5):g.add_vertex()
    >>> e1 = g.add_edge(0, 1)
    >>> e2 = g.add_edge(0, 2)
    >>> e3 = g.add_edge(0, 3)
    >>> e4 = g.add_edge(0, 4)
    >>> drawing.draw(g, positions=drawing.layout(g, name="random"))
    >>> plt.show()

    See Also
    --------
    draw_jgrapht()
    draw_jgrapht_vertices()
    draw_jgrapht_edges()
    draw_jgrapht_vertex_labels()
    draw_jgrapht_edge_labels()
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError as e:
        raise ImportError("Matplotlib required for draw()") from e
    except RuntimeError:
        print("Matplotlib unable to open display")
        raise

    cf = plt.gcf() if ax is None else ax.get_figure()
    cf.set_facecolor("w")

    if ax is None:
        if cf._axstack() is None:
            ax = cf.add_axes((0, 0, 1, 1))
        else:
            ax = cf.gca()

    if positions is None:
        positions = layout(g)

    draw_jgrapht(g, positions=positions, ax=ax, **kwds)
    ax.set_axis_off()
    plt.draw_if_interactive()


def draw_jgrapht(
    g,
    positions=None,
    arrow=False,
    node_label=True,
    edge_label=False,
    axis=True,
    **kwargs
):
    """Draw the graph g using Matplotlib.

    Draw the graph with Matplotlib with options for node positions, labeling, titles, and many
    other drawing features. See draw() for simple drawing without labels or axes.

    :param g: graph
    :param axis: Draw the axes
    :param node_label: whether to draw node labels
    :param positions: vertices positions
    :param edge_label: whether to draw edge labels
    :param arrow: whether to draw arrowheads
    :param kwargs: additional arguments to pass through
    :type positions: dictionary, optional
    :type arrow: bool, optional (default=True)
    :type axis: bool, optional (default=True)
    :type node_label: bool, optional (default=False)
    :type edge_label: bool, optional (default=False)
    :type kwargs: optional keywords

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> g = jgrapht.create_graph(directed=False, weighted=True)
    >>> for i in range(0,5):g.add_vertex()
    >>> e1 = g.add_edge(0, 1)
    >>> e2 = g.add_edge(0, 2)
    >>> e3 = g.add_edge(0, 3)
    >>> e4 = g.add_edge(0, 4)
    >>> drawing.draw_jgrapht(g, positions=drawing.layout(g, name="random"))
    >>> plt.show()

    See Also
    --------
    draw()
    draw_jgrapht_vertices()
    draw_jgrapht_edges()
    draw_jgrapht_vertex_labels()
    draw_jgrapht_edge_labels()
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError as e:
        raise ImportError("Matplotlib required for draw()") from e
    except RuntimeError:
        print("Matplotlib unable to open display")
        raise
    show = 0

    if positions is None:
        positions = layout(g)

    draw_jgrapht_vertices(
        g, positions, node_label=node_label, axis=axis, show=show, **kwargs
    )

    draw_jgrapht_edges(
        g,
        positions=positions,
        arrow=arrow,
        edge_label=edge_label,
        node_label=node_label,
        axis=axis,
        show=show,
        **kwargs,
    )

    if node_label is True:
        draw_jgrapht_vertex_labels(g, positions=positions, axis=axis, **kwargs)

    if edge_label is True:
        draw_jgrapht_edge_labels(g, positions=positions, axis=axis, **kwargs)

    plt.draw_if_interactive()


def draw_jgrapht_vertices(
    g,
    positions,
    axis=False,
    node_linewidths=1.0,
    node_title=None,
    node_size=450,
    node_color="green",
    node_cmap=None,
    vmin=None,
    vmax=None,
    node_shape="o",
    node_edge_color="face",
    node_list=None,
    alpha=1,
    node_label=False,
    ax=None,
    **kwargs
):
    """Draw the nodes of the graph g.

    This method draws only the nodes of the graph g.

    :param g: graph
    :param positions: vertices positions
    :param axis: Draw the axes
    :param node_linewidths: Line width of symbol border
    :param node_title: Label for graph legend
    :param node_size: Size of nodes
    :param node_color: Node color
    :param node_cmap: Colormap for mapping intensities of nodes
    :param vmin: Minimum for node colormap scaling
    :param vmax: Maximum for node colormap scaling positions
    :param node_shape: The shape of the node
    :param node_edge_color: color the edge of node
    :param node_list: Draw only the nodes in this list
    :param node_label: whether to draw node labels
    :param alpha: The node transparency
    :param ax: Draw the graph in the specified Matplotlib axes
    :param kwargs: Additional arguments to pass through
    :type positions: dictionary, optional
    :type axis: bool, optional (default=False)
    :type node_linewidths: float,(default:1.0)
    :type node_title: list, optional  (default:None)
    :type node_size: scalar or array, optional (default=500)
    :type node_color: color or array of colors (default='green')
    :type node_cmap: Matplotlib colormap, optional (default=None | example:node_cmap=plt.cm.Greens)
    :type vmin: float, optional (default=None)
    :type vmax: float, optional (default=None)
    :type node_shape: string, optional (default='o')
    :type node_edge_color: string, optional (default='face')
    :type node_list: list, optional (default: node_list=None)
    :type alpha: float, optional (default=1.0)
    :type node_label: bool, optional (default=False)
    :type ax: Matplotlib Axes object, optional
    :type kwargs: optional keywords

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> g = jgrapht.create_graph(directed=False, weighted=True)
    >>> for i in range(0,5):g.add_vertex()
    >>> e1 = g.add_edge(0, 1)
    >>> e2 = g.add_edge(0, 2)
    >>> e3 = g.add_edge(0, 3)
    >>> e4 = g.add_edge(0, 4)
    >>> drawing.draw_jgrapht_vertices(g, positions=drawing.layout(g, name="random"))
    >>> plt.show()

    See Also
    --------
    draw()
    draw_jgrapht()
    draw_jgrapht_edges()
    draw_jgrapht_vertex_labels()
    draw_jgrapht_edge_labels()
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError as e:
        raise ImportError("Matplotlib required for draw()") from e
    except RuntimeError:
        print("Matplotlib unable to open display")
        raise

    if ax is None:
        ax = plt.gca()

    # Hide axis values
    ax.get_yaxis().set_visible(False)
    ax.get_xaxis().set_visible(False)

    if axis is False:
        ax.set_axis_off()

    if node_list is not None:
        x, y = zip(*[positions[v] for v in node_list])
    else:
        x, y = zip(*positions)

    # Draw nodes
    ax.scatter(
        x,
        y,
        c=node_color,
        alpha=alpha,
        linewidth=node_linewidths,
        s=node_size,
        cmap=node_cmap,
        vmin=vmin,
        vmax=vmax,
        marker=node_shape,
        edgecolors=node_edge_color,
        zorder=2.5,
        label=node_title,
    )

    if node_title is not None:
        # Draw Legend graph for the nodes
        handles, labels = ax.get_legend_handles_labels()
        unique = [
            (h, l)
            for i, (h, l) in enumerate(zip(handles, labels))
            if l not in labels[:i]
        ]
        ax.legend(
            *zip(*unique),
            loc="upper center",
            fancybox=True,
            framealpha=1,
            shadow=True,
            borderpad=0.3,
            markerscale=0.5,
            markerfirst=True,
            ncol=3,
            bbox_to_anchor=(0.5, 1.15),
        )

    show = kwargs.get("show")  # check if the user called only the function of nodes
    if show is None and node_label is True:
        draw_jgrapht_vertex_labels(g, positions, axis=axis, **kwargs)


def draw_jgrapht_edges(
    g,
    positions,
    edge_color="black",
    edge_cmap=None,
    edge_linewidth=1.3,
    line_style="solid",
    arrow=False,
    arrow_size=1,
    arrow_style="-|>",
    arrow_color="black",
    arrow_line="-",
    arrow_head=20,
    edge_list=None,
    alpha=1,
    axis=False,
    edge_title=None,
    edge_label=False,
    connection_style=None,
    bbox=dict(boxstyle="round,pad=0.03", ec="white", fc="white"),
    ax=None,
    **kwargs
):
    """Draw the edges of the graph g.

    This draws only the edges of the graph g.

    :param g: graph
    :param positions: vertices positions
    :param edge_color: Edge color
    :param edge_cmap: Colormap for mapping intensities of edges
    :param edge_linewidth: Line width of edges
    :param line_style: Edge line style (solid|dashed|dotted|dashdot)
    :param arrow: draw arrowheads
    :param arrow_size: size of arrow
    :param arrow_style: choose the style of the arrowsheads.(Fancy|Simple|Wedge etc)
    :param arrow_color: arrow color
    :param arrow_line: Edge line style (solid|dashed|dotted|dashdot)
    :param arrow_head: size of arrowhead
    :param edge_list: Draw only specified edges
    :param alpha: edge transparency
    :param axis: Draw the axes
    :param edge_title: Label for graph legend
    :param edge_label: draw labels on the edges.
    :param connection_style: Pass the connection_style parameter to create curved arc of rounding radius rad
    :param bbox: Matplotlib bbox,specify text box shape and colors.
    :param ax: Draw the graph in the specified Matplotlib axes
    :param kwargs: See draw_jgrapht
    :type positions: dictionary, optional
    :type edge_color: color or array of colors (default='black')
    :type edge_cmap: list, optional (default:edge_cmap=None | example: edge_cmap =plt.cm.Greens(np.linspace(edge_vmin,edge_vmax,len(g.edges))))
    :type axis: bool, optional (default=False)
    :type edge_linewidth: float, optional (default=1.3)
    :type line_style: string, optional (default='solid')
    :type arrow: bool, optional (default=True)
    :type arrow_size: int, optional (default=1)
    :type arrow_style: str, optional (default='-|>')
    :type arrow_color: color or array of colors (default='black')
    :type arrow_line: string, optional (default='solid')
    :type arrow_head: int, optional (default=20)
    :type edge_list: list, optional (default: edge_list=None)
    :type alpha: float, optional (default=1.0)
    :type edge_title: list, optional  (default:None)
    :type edge_label: bool, optional (default=False)
    :type connection_style: str, optional (default=None | example: connection_style="arc3,rad=-0.3")
    :type ax: Matplotlib Axes object, optional
    :type kwargs: optional keywords

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> g = jgrapht.create_graph(directed=False, weighted=True)
    >>> for i in range(0,5):g.add_vertex()
    >>> e1 = g.add_edge(0, 1)
    >>> e2 = g.add_edge(0, 2)
    >>> e3 = g.add_edge(0, 3)
    >>> e4 = g.add_edge(0, 4)
    >>> drawing.draw_jgrapht_edges(g, positions=drawing.layout(g, name="random"), arrow=True)
    >>> plt.show()

    See Also
    --------
    draw()
    draw_jgrapht()
    draw_jgrapht_vertices()
    draw_jgrapht_vertex_labels()
    draw_jgrapht_edge_labels()
    -----
    """

    try:
        import matplotlib.pyplot as plt
        import numpy as np
        import matplotlib as mpl
        from matplotlib.patches import FancyArrowPatch
    except ImportError as e:
        raise ImportError("Matplotlib required for draw()") from e
    except RuntimeError:
        print("Matplotlib unable to open display")
        raise

    if len(g.edges) == 0:
        return

    if ax is None:
        ax = plt.gca()

    # Hide axis values
    ax.get_yaxis().set_visible(False)
    ax.get_xaxis().set_visible(False)

    if axis is False:
        ax.set_axis_off()

    show = kwargs.get("show")  # check if the user called only the function of edges

    if edge_cmap is not None:  # if the user wants color map for the edges
        plt.close()
        plt.rcParams["axes.prop_cycle"] = plt.cycler("color", edge_cmap)
        ax = plt.gca()
        if show is None:  # if  the user called only this function
            draw_jgrapht_edges(
                g,
                positions=positions,
                edge_label=edge_label,
                edge_cmap=None,
                edge_color="",
                edge_linewidth=edge_linewidth,
                line_style=line_style,
                arrow=arrow,
                arrow_size=arrow_size,
                arrows_tyle=arrow_style,
                arrow_color=arrow_color,
                edge_list=edge_list,
                alpha=alpha,
                axis=axis,
                edge_title=edge_title,
                connection_style=connection_style,
                bbox=bbox,
                ax=ax,
                arrow_head=arrow_head,
                arrow_line=arrow_line,
                **kwargs,
            )
        else:
            kwargs.pop("show")  # delete from kwargs the parameter show
            draw_jgrapht(
                g,
                positions=positions,
                edge_cmap=None,
                edge_color="",
                edge_linewidth=edge_linewidth,
                edge_list=edge_list,
                line_style=line_style,
                arrow=arrow,
                arrow_size=arrow_size,
                arrow_style=arrow_style,
                arrow_color=arrow_color,
                alpha=alpha,
                axis=axis,
                ax=ax,
                edge_title=edge_title,
                connection_style=connection_style,
                edge_label=edge_label,
                bbox=bbox,
                arrow_head=arrow_head,
                arrow_line=arrow_line,
                **kwargs,
            )
        return

    # draw edges
    for e in g.edges:
        v1 = g.edge_source(e)
        v2 = g.edge_target(e)
        x1, y1 = positions[v1]
        x2, y2 = positions[v2]

        if edge_list is None:
            edge_list = []
            for e in g.edges:
                edge_list.append(e)

        for l, edge in enumerate(edge_list):
            if edge_list[l] == e:
                if arrow is True:  # Draw  arrows
                    a = FancyArrowPatch(
                        (x1, y1),
                        (x2, y2),
                        arrowstyle=arrow_style,
                        shrinkA=9.5,
                        shrinkB=9.5,
                        mutation_scale=arrow_head,
                        alpha=alpha,
                        ls=arrow_line,
                        lw=arrow_size,
                        connectionstyle=connection_style,
                        color=arrow_color,
                        label=edge_title,
                    )
                    ax.add_patch(a)
                    ax.autoscale_view()
                else:
                    # Draw  edges
                    ax.plot(
                        (x1, x2),
                        (y1, y2),
                        edge_color,
                        alpha=alpha,
                        linewidth=edge_linewidth,
                        linestyle=line_style,
                        label=edge_title,
                    )

                if edge_title is not None:  # legend title for the specific edges
                    handles, labels = ax.get_legend_handles_labels()
                    unique = [
                        (h, l)
                        for i, (h, l) in enumerate(zip(handles, labels))
                        if l not in labels[:i]
                    ]
                    ax.legend(
                        *zip(*unique),
                        loc="upper center",
                        fancybox=True,
                        framealpha=1,
                        shadow=True,
                        borderpad=0.3,
                        markerscale=0.5,
                        markerfirst=True,
                        ncol=3,
                        bbox_to_anchor=(0.5, 1.15),
                    )

    if show is None and edge_label is True:
        draw_jgrapht_edge_labels(g, positions, axis=axis, **kwargs)


def draw_jgrapht_vertex_labels(
    g,
    positions,
    labels=None,
    node_fontsize=12,
    node_font_color="black",
    node_font_weight="normal",
    node_font_family="sans-serif",
    horizontalalignment="center",
    verticalalignment="center",
    alpha=1,
    axis=False,
    bbox=dict(boxstyle="round,pad=0.03", ec="white", fc="white"),
    ax=None,
    **kwargs
):
    """Draw node labels on the graph g.

    This method draws only the nodes labels of the graph g.

    :param g: graph
    :param positions: vertices positions
    :param labels: vertices labels
    :param node_fontsize: Font size for text labels
    :param node_font_color: Font color string
    :param node_font_weight: Font weight ( 'normal' | 'bold' | 'heavy' | 'light' | 'ultralight')
    :param node_font_family: Font family ('cursive', 'fantasy', 'monospace', 'sans', 'sans serif', 'sans-serif', 'serif')
    :param verticalalignment: Vertical alignment (default='center')
    :param horizontalalignment: Horizontal alignment (default='center')
    :param alpha: label transparency
    :param axis: Draw the axes
    :param ax: Draw the graph in the specified Matplotlib axes
    :param bbox: Matplotlib bbox,specify text box shape and colors.
    :param kwargs: See draw_jgrapht
    :type positions: dictionary, optional
    :type labels: list, optional
    :type node_fontsize: int, optional (default=12)
    :type node_font_color: string, optional (default='black')
    :type node_font_weight: string, optional (default='normal')
    :type node_font_family: string, optional (default='sans-serif')
    :type verticalalignment: {'center', 'top', 'bottom', 'baseline', 'center_baseline'}
    :type horizontalalignment: {'center', 'right', 'left'}
    :type alpha: float, optional (default=1.0)
    :type axis: bool, optional (default=False)
    :type ax: Matplotlib Axes object, optional
    :type kwargs: optional keywords

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> g = jgrapht.create_graph(directed=False, weighted=True)
    >>> for i in range(0,5):g.add_vertex()
    >>> e1 = g.add_edge(0, 1)
    >>> e2 = g.add_edge(0, 2)
    >>> e3 = g.add_edge(0, 3)
    >>> e4 = g.add_edge(0, 4)
    >>> drawing.draw_jgrapht_vertex_labels(g, positions=drawing.layout(g, name="random"))
    >>> plt.show()

    See Also
    --------
    draw()
    draw_jgrapht()
    draw_jgrapht_vertices()
    draw_jgrapht_edges()
    draw_jgrapht_edge_labels()
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError as e:
        raise ImportError("Matplotlib required for draw()") from e
    except RuntimeError:
        print("Matplotlib unable to open display")
        raise

    if ax is None:
        ax = plt.gca()

    # Hide axis values
    ax.get_yaxis().set_visible(False)
    ax.get_xaxis().set_visible(False)

    if not axis:
        ax.set_axis_off()

    if labels is None:
        labels = {}
        for v in g.vertices:
            labels.update({v: str(v)})

    # Draw the labels
    for v, label in labels.items():
        x, y = positions[v]
        ax.text(
            x,
            y,
            label,
            fontsize=node_fontsize,
            horizontalalignment=horizontalalignment,
            verticalalignment=verticalalignment,
            alpha=alpha,
            color=node_font_color,
            weight=node_font_weight,
            family=node_font_family,
            transform=ax.transData,
        )
        ax.plot(x, y)


def draw_jgrapht_edge_labels(
    g,
    positions,
    labels=None,
    draw_edge_weights=False,
    horizontalalignment="center",
    verticalalignment="center",
    edge_fontsize=12,
    edge_font_color="black",
    edge_font_weight="normal",
    edge_font_family="sans-serif",
    alpha=1,
    axis=False,
    bbox=dict(boxstyle="round,pad=0.03", ec="white", fc="white"),
    ax=None,
    **kwargs
):
    """Draw edge labels on the graph g.

    This method draws only the edge labels of the graph g.

    :param g: graph
    :param positions: vertices positions
    :param labels: edge labels
    :param draw_edge_weights: whether to use edge weights as edge labels
    :param edge_fontsize: Font size for text labels
    :param edge_font_color: Font color string
    :param edge_font_weight: Font weight ( 'normal' | 'bold' | 'heavy' | 'light' | 'ultralight')
    :param edge_font_family: Font family ('cursive', 'fantasy', 'monospace', 'sans', 'sans serif', 'sans-serif', 'serif')
    :param verticalalignment: Vertical alignment (default='center')
    :param horizontalalignment: Horizontal alignment (default='center')
    :param alpha: label transparency
    :param bbox: Matplotlib bbox,specify text box shape and colors.
    :param ax: Draw the graph in the specified Matplotlib axes
    :param axis: Draw the axes
    :param kwargs: See draw_jgrapht
    :type positions: dictionary, optional
    :type labels: list, optional
    :type draw_edge_weights: bool, optional (default=False)
    :type edge_fontsize: int, optional (default=12)
    :type edge_font_color: string, optional (default='black')
    :type edge_font_weight: string, optional (default='normal')
    :type alpha: float, optional (default=1.0)
    :type axis: bool, optional (default=False)
    :type ax: Matplotlib Axes object, optional
    :type edge_font_family: string, optional (default='sans-serif')
    :type verticalalignment: {'center', 'top', 'bottom', 'baseline', 'center_baseline'}
    :type horizontalalignment: {'center', 'right', 'left'}
    :type kwargs: optional keywords

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> g = jgrapht.create_graph(directed=False, weighted=True)
    >>> for i in range(0,5):g.add_vertex()
    >>> e1 = g.add_edge(0, 1)
    >>> e2 = g.add_edge(0, 2)
    >>> e3 = g.add_edge(0, 3)
    >>> e4 = g.add_edge(0, 4)
    >>> drawing.draw_jgrapht_edge_labels(g, position=drawing.layout(g, name="random")) 
    >>> plt.show()
    See Also
    --------
    draw()
    draw_jgrapht()
    draw_jgrapht_vertices()
    draw_jgrapht_edges()
    draw_jgrapht_vertex_labels()
    --------
    """
    try:
        import matplotlib.pyplot as plt
    except ImportError as e:
        raise ImportError("Matplotlib required for draw()") from e
    except RuntimeError:
        print("Matplotlib unable to open display")
        raise

    if len(g.edges) == 0:
        return

    if ax is None:
        ax = plt.gca()

    # Hide axis values
    ax.get_yaxis().set_visible(False)
    ax.get_xaxis().set_visible(False)

    if not axis:
        ax.set_axis_off()

    if labels is None:
        labels = {}
        if draw_edge_weights is True:
            for e in g.edges:
                labels.update({e: g.get_edge_weight(e)})
        else:
            for e in g.edges:
                labels.update({e: str(e)})

    # Draw the labels
    for e, label in labels.items():
        v = g.edge_source(e)
        u = g.edge_target(e)
        x1, y1 = positions[v]
        x2, y2 = positions[u]

        ax.text(
            (x1 + x2) / 2,
            (y1 + y2) / 2,
            label,
            fontsize=edge_fontsize,
            horizontalalignment=horizontalalignment,
            verticalalignment=verticalalignment,
            alpha=alpha,
            color=edge_font_color,
            weight=edge_font_weight,
            family=edge_font_family,
            transform=ax.transData,
            bbox=bbox,
            zorder=2,
        )
        ax.plot((x1 + x2) / 2, (y1 + y2) / 2)


def layout(
    g,
    name=None,
    area=(0, 0, 10, 10),
    **kwargs
):
    """Compute the positions of vertices for a particular layout.

    :param g: the graph to draw
    :param name: circular|random|fruchterman_reingold|fruchterman_reingold_indexed
    :param area: the two dimensional area as a tuple (minx, miny, width, height)
    :param kwargs: additional arguments passed through
    :type name: name of the layout
    :type kwargs: optional keywords

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> g = jgrapht.create_graph(directed=False, weighted=True)
    >>> for i in range(0,5):g.add_vertex()
    >>> e1 = g.add_edge(0, 1)
    >>> e2 = g.add_edge(0, 2)
    >>> e3 = g.add_edge(0, 3)
    >>> e4 = g.add_edge(0, 4)
    >>> position = drawing.layout(g, seed=10, name="random")
    >>> drawing.draw_jgrapht(g, position=position)
    >>> plt.show()
    """
    positions = []
    
    if name == 'random':
        alg = random_layout_2d
        args = {
            'seed': kwargs.get('seed')
        }
    elif name == 'fruchterman_reingold': 
        alg = fruchterman_reingold_layout_2d
        args = {
            'iterations': kwargs.get('iterations', 100),
            'normalization_factor': kwargs.get('normalization_factor', 0.5),
            'seed': kwargs.get('seed')
        }
    elif name == 'fruchterman_reingold_indexed': 
        alg = fruchterman_reingold_indexed_layout_2d
        args = {
            'iterations': kwargs.get('iterations', 100),
            'normalization_factor': kwargs.get('normalization_factor', 0.5),
            'seed': kwargs.get('seed'),
            'theta': kwargs.get('theta', 0.5),
            'tolerance': kwargs.get('tolerance'),
        }
    else: 
        alg = circular_layout_2d
        args = {
            'radius': kwargs.get('radius', 5),
            'vertex_comparator_cb': kwargs.get('vertex_comparator_cb', None)
        }

    result = alg(g, area, **args)
    for i, vertex in enumerate(g.vertices):
        x, y = result.get_vertex_location(i)
        positions.append((x, y))

    return positions


def draw_circular(
    g, area=(0, 0, 10, 10), radius=5, vertex_comparator_cb=None, axis=True, **kwargs
):
    """Draw the graph g with a circular layout

    :param g: graph
    :param area: the two dimensional area as a tuple (minx, miny, width, height)
    :param axis: whether to draw the axes
    :param radius: radius of the circle
    :param vertex_comparator_cb: a vertex comparator. Should be a function which accepts two vertices
           v1, v2 and returns -1, 0, 1 depending of whether v1 < v2, v1 == v2, or v1 > v2 in the ordering
    :param kwargs: additional arguments passed through
    :type axis: bool, optional (default=True)
    :type kwargs: optional keywords

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> g = jgrapht.create_graph(directed=False, weighted=True)
    >>> for i in range(0,5):g.add_vertex()
    >>> e1 = g.add_edge(0, 1)
    >>> e2 = g.add_edge(0, 2)
    >>> e3 = g.add_edge(0, 3)
    >>> e4 = g.add_edge(0, 4)
    >>> drawing.draw_circular(g)
    >>> plt.show()
    """
    draw_jgrapht(
        g,
        layout(
            g,
            area=area,
            name="circular",
            radius=radius,
            vertex_comparator_cb=vertex_comparator_cb,
        ),
        axis=axis,
        **kwargs,
    )


def draw_random(g, area=(0, 0, 10, 10), seed=None, axis=True, **kwargs):
    """Draw the graph g with a random layout.

    :param g: graph
    :param area: the two dimensional area as a tuple (minx, miny, width, height)
    :param seed: seed for the random number generator. If None the system time is used
    :param axis: whether to draw the axes
    :param kwargs: additional arguments passed through
    :type axis: bool, optional (default=True)
    :type kwargs: optional keywords

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> g = jgrapht.create_graph(directed=False, weighted=True)
    >>> for i in range(0,5):g.add_vertex()
    >>> e1 = g.add_edge(0, 1)
    >>> e2 = g.add_edge(0, 2)
    >>> e3 = g.add_edge(0, 3)
    >>> e4 = g.add_edge(0, 4)
    >>> drawing.draw_random(g)
    >>> plt.show()
    """
    draw_jgrapht(
        g,
        layout(g, area=area, name="random", seed=seed),
        axis=axis,
        **kwargs,
    )


def draw_fruchterman_reingold(
    g,
    area=(0, 0, 10, 10),
    iterations=100,
    normalization_factor=0.5,
    seed=None,
    theta=0.5,
    tolerance=None,
    indexed=False,
    axis=True,
    **kwargs
):
    """Draw the graph g with a Fruchterman-Reingold layout.

    :param g: graph
    :param area: the two dimensional area as a tuple (minx, miny, width, height)
    :param iterations: number of iterations
    :param normalization_factor: normalization factor when calculating optimal distance
    :param seed: seed for the random number generator. If None the system time is used
    :param theta: parameter for approximation using the Barnes-Hut technique
    :param indexed: whether to use the Barnes-Hut approximation
    :param axis: whether to draw the axes
    :param tolerance: tolerance used when comparing floating point values
    :param kwargs: additional arguments passed through
    :type indexed: bool, optional (default=False)
    :type axis: bool, optional (default=True)
    :type kwargs: optional keywords

    Examples
    --------
    >>> import matplotlib.pyplot as plt
    >>> g = jgrapht.create_graph(directed=False, weighted=True)
    >>> for i in range(0,5):g.add_vertex()
    >>> e1 = g.add_edge(0, 1)
    >>> e2 = g.add_edge(0, 2)
    >>> e3 = g.add_edge(0, 3)
    >>> e4 = g.add_edge(0, 4)
    >>> drawing.draw_fruchterman_reingold(g)
    >>> plt.show()
    """
    extra_args = {
        'area':area,
        'name':'fruchterman_reingold',
        'iterations':iterations,
        'normalization_factor':normalization_factor,
        'seed':seed
    }
    if indexed: 
        extra_args.update({
            'name':'fruchterman_reingold_indexed',
            'theta':theta,
            'tolerance':tolerance
        })

    draw_jgrapht(
            g,
            layout(
                g,
                **extra_args
            ),
            axis=axis,
            **kwargs,
        )
