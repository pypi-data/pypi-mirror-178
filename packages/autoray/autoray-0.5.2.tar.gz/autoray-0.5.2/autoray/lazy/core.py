import operator
import threading
import functools
import itertools
import contextlib
import collections

from ..autoray import (
    get_lib_fn,
    infer_backend,
    register_backend,
    get_dtype_name,
    register_function,
    astype,
    complex_add_re_im,
)


_EMPTY_DICT = {}


class LazyArray:
    """A lazy array representing a shaped node in a computational graph."""

    __slots__ = (
        "_backend",
        "_fn",
        "_args",
        "_kwargs",
        "_shape",
        "_data",
        "_deps",
    )

    def __init__(
        self,
        backend,
        fn,
        args,
        kwargs,
        shape,
        deps=None,
    ):
        # info required to perform the computation
        self._backend = backend
        self._fn = fn
        self._args = args
        if kwargs is None:
            self._kwargs = _EMPTY_DICT
        else:
            self._kwargs = kwargs

        # resulting array information
        self._shape = shape
        self._data = None

        # lazy arrays this ``LazyArray`` depends on
        if deps is None:
            # automatically find them
            self._deps = (*find_lazy(self._args), *find_lazy(self._kwargs))
        else:
            # manually specified (more efficient)
            self._deps = deps

    @classmethod
    def from_data(cls, data):
        """Create a new ``LazyArray`` directly from a concrete array."""
        obj = cls.__new__(cls)
        obj._backend = infer_backend(data)
        obj._fn = obj._args = obj._kwargs = None
        obj._shape = tuple(map(int, data.shape))
        obj._data = data
        obj._deps = ()
        return obj

    @classmethod
    def from_shape(cls, shape, backend="numpy"):
        """Create a new ``LazyArray`` with a given shape."""
        obj = cls.__new__(cls)
        obj._backend = backend
        obj._fn = obj._args = obj._kwargs = None
        obj._shape = tuple(map(int, shape))
        obj._data = "__PLACEHOLDER__"
        obj._deps = ()
        return obj

    def to(
        self,
        fn,
        args=None,
        kwargs=None,
        backend=None,
        shape=None,
        deps=None,
    ):
        """Create a new ``LazyArray``, by default propagating backend, shape,
        and deps from the the current LazyArray.
        """
        return LazyArray(
            fn=fn,
            args=args if args is not None else (self,),
            kwargs=kwargs,
            backend=backend if backend is not None else self._backend,
            shape=shape if shape is not None else self.shape,
            deps=deps if deps is not None else (self,),
        )

    def _materialize(self):
        """Recursively compute all required args and kwargs for this node
        before computing itself and dereferencing dependencies. Note using this
        to materialize a large computation from scratch should be avoided due
        to the recursion limit, use ``x.compute()`` instead.
        """
        if self._data is None:

            # materialize any actual array args
            args = (maybe_materialize(x) for x in self._args)
            kwargs = {k: maybe_materialize(v) for k, v in self._kwargs.items()}

            self._data = self._fn(*args, **kwargs)

            # free any references to deps
            self._fn = self._args = self._kwargs = None
            self._deps = ()

        return self._data

    def __iter__(self):
        """Generate each unique computational node. Use ``ascend`` if you need
        to visit children before parents.
        """
        seen = set()
        queue = [self]
        queue_pop = queue.pop
        queue_extend = queue.extend
        seen_add = seen.add
        while queue:
            node = queue_pop()
            nid = id(node)
            if nid not in seen:
                yield node
                queue_extend(node._deps)
                seen_add(nid)

    def ascend(self):
        """Generate each unique computational node, from leaves to root."""
        seen = set()
        ready = set()
        queue = [self]
        queue_extend = queue.extend
        queue_pop = queue.pop
        ready_add = ready.add
        seen_add = seen.add
        while queue:
            node = queue[-1]
            need_to_visit = [c for c in node._deps if id(c) not in ready]
            if need_to_visit:
                queue_extend(need_to_visit)
            else:
                node = queue_pop()
                nid = id(node)
                ready_add(nid)
                if nid not in seen:
                    yield node
                    seen_add(nid)

    def compute(self):
        """Compute the value of this lazy array.

        Unlike ``self._materialize()`` this avoids deep recursion.
        """
        for node in self.ascend():
            node._materialize()
        return self._data

    def compute_constants(self, variables):
        """Fold constant arrays - everything not dependent on ``variables`` -
        into the graph.
        """
        if isinstance(variables, LazyArray):
            variables = (variables,)
        variables = set(variables)

        # must ascend
        for node in self.ascend():
            if not any(c in variables for c in node._deps):
                # can fold
                node._materialize()
            else:
                # mark as variable
                variables.add(node)

    def as_string(self, params):
        """Create a string which evaluates to the lazy array creation."""
        # name function and store in locals
        fn_name = f"{getattr(self._fn, '__name__', 'fn')}{id(self._fn)}"
        params.setdefault(fn_name, self._fn)

        # string of args and kwargs
        str_call = ", ".join(
            itertools.chain(
                (stringify(x, params) for x in self._args),
                (f"{k}: {stringify(v, params)}" for k, v in self._kwargs.items()),
            )
        )

        # assign function call to new variable
        return f"x{id(self)} = {fn_name}({str_call})"

    def get_source(self, params=None):
        """Write the source code of an unravelled version of the computational
        graph, injecting required runtime objects into ``params``.
        """
        if params is None:
            # locals space mapping LazyArray names to values
            params = {}

        delete_checked = set()
        s = []  # source code lines

        for node in reversed(tuple(self.ascend())):
            # when *descending*, the first encounter of a node is the
            # *last* time it is referenced in forward pass -> delete,
            # need to do this for GC since running in single big function
            for c in node._deps:
                if c not in delete_checked:
                    if c._deps:
                        # is an intermediate - safe to delete
                        s.append(f"del x{id(c)}")
                    delete_checked.add(c)

            if node._data is None:
                # create the array via computation
                s.append(node.as_string(params))
            else:
                # inject the already computed data as constant
                params[f"x{id(node)}"] = node._data

        # reverse (ascend) into source code
        return "\n".join(reversed(s))

    def get_compiled(self, optimize=1):
        """Compile the function into a  code object using ``compile``,
        returning a  wrapper that executes it using ``exec`` and the 'locals'
        dict specifiying inputs which can be modified. It should be called
        like:

            fn, params = x.get_compiled()
            # modify params e.g. inject new arrays here before call
            ...
            fn(params)

        """
        # write source and populate locals mapping that function will run under
        params = {}
        source = self.get_source(params)

        # compile source
        code = compile(source, f"code{id(self)}", "exec", optimize=optimize)
        compiled = functools.partial(_code_exec_fn, code=code, out_name=f"x{id(self)}")

        # need both function and locals mapping to run it with / modify args
        return compiled, params

    def get_function(self, variables, fold_constants=True):
        """Get a compiled function that computes ``fn(arrays)``, with ``fn``
        describing the computational graph of this ``LazyArray`` and ``arrays``
        corresponding to the downstream ``LazyArray`` nodes ``variables``.

        Parameters
        ----------
        variables : sequence of LazyArray
            Input nodes whose data can change between calls.
        fold_constants : bool, optional
            Compute all intermediates which do not depend on ``variables``
            prior to compilation.

        Returns
        -------
        fn : callable
            Function with signature ``fn(arrays)``.
        """
        if fold_constants:
            self.compute_constants(variables=variables)

        var_names = tuple(f"x{id(v)}" for v in variables)
        fn, params = self.get_compiled()

        return functools.partial(_array_fn, var_names=var_names, params=params, fn=fn)

    def history_max_size(self):
        """Get the largest single tensor size appearing in this computation."""
        return max(node.size for node in self)

    def history_size_footprint(self):
        """Get the combined size of intermediates at each step of the
        computation. Note this assumes that intermediates are immediately
        garbage collected when they are no longer required.
        """
        delete_checked = set()
        sizes = []
        for node in reversed(tuple(self.ascend())):
            for c in node._deps:
                if c not in delete_checked:
                    # last time a dependency is seen, subtract the size
                    if c._deps:
                        sizes.append(-c.size)
                    delete_checked.add(c)

            if node._data is None:
                # this is a new intermediate, add the size
                sizes.append(+node.size)

        sizes.reverse()
        return list(itertools.accumulate(sizes))

    def history_peak_size(self):
        """Get the peak combined intermediate size of this computation."""
        return max(self.history_size_footprint())

    def history_total_size(self):
        """The the total size of all unique arrays in the computational graph,
        possibly relevant e.g. for back-propagation algorithms.
        """
        return sum(node.size for node in self)

    def plot_history_size_footprint(
        self,
        log=None,
        figsize=(8, 2),
        color="purple",
        alpha=0.5,
        ax=None,
        return_fig=False,
    ):
        """Plot the memory footprint throughout this computation.

        Parameters
        ----------
        log : None or int, optional
            If not None, display the sizes in base ``log``.
        figsize : tuple, optional
            Size of the figure.
        color : str, optional
            Color of the line.
        alpha : float, optional
            Alpha of the line.
        ax : matplotlib.axes.Axes, optional
            Axes to plot on, will be created if not provided.
        return_fig : bool, optional
            If True, return the figure object, else just show and close it.
        """
        import numpy as np
        import matplotlib.pyplot as plt

        y = np.array(self.history_size_footprint())
        if log:
            y = np.log2(y) / np.log2(log)
            ylabel = f"$\\log_{log}[SIZE]$"
        else:
            ylabel = "SIZE"

        x = np.arange(y.size)

        if ax is None:
            fig, ax = plt.subplots(figsize=figsize)
        else:
            fig = None

        ax.fill_between(x, 0, y, alpha=alpha, color=color)

        if fig is not None:
            ax.grid(True, c=(0.95, 0.95, 0.95), which="both")
            ax.set_axisbelow(True)
            ax.set_xlim(0, np.max(x))
            ax.set_ylim(0, np.max(y))
            ax.set_ylabel(ylabel)

        if return_fig or fig is None:
            return fig
        else:
            plt.show()
            plt.close(fig)

    def to_nx_digraph(
        self,
        variables=None,
        var_color=(0, 0.5, 0.25),
        const_color=(0, 0.5, 1.0),
        root_color=(1, 0, 0.5),
        node_scale=5,
    ):
        """Convert this ``LazyArray`` into a ``networkx.DiGraph``, injecting
        various plotting information as properties.
        """
        import numpy as np
        import networkx as nx

        if variables is not None:
            if isinstance(variables, LazyArray):
                variables = (variables,)
            variables = set(variables)

            def is_variable(node):
                return node in variables

        else:

            def is_variable(_):
                return False

        def extract_props(node, **kwargs):
            v = is_variable(node)
            d = {
                "variable": v,
                "fn": getattr(node._fn, "__name__", "CONST"),
                "size": node_scale * np.log2(node.size) + node_scale,
                "color": var_color if v else const_color,
            }
            d.update(kwargs)
            if not node._deps:
                d["color"] = tuple(x**0.2 for x in d["color"])
            return d

        G = nx.DiGraph()
        for node in self.ascend():
            if any(is_variable(child) for child in node._deps):
                variables.add(node)
            G.add_node(node, **extract_props(node))
            for x in node._deps:
                G.add_edge(x, node)
        G.nodes[self]["color"] = root_color

        return G

    def plot(
        self,
        variables=None,
        initial_layout="spiral",
        iterations=0,
        k=None,
        connectionstyle="arc3,rad=0.2",
        arrowsize=5,
        edge_color=None,
        var_color=(0, 0.5, 0.25),
        const_color=(0, 0.5, 1.0),
        root_color=(1, 0, 0.5),
        node_scale=5,
        node_alpha=1.0,
        show_labels=True,
        label_alpha=0.2,
        label_color=None,
        font_size=8,
        figsize=(6, 6),
        ax=None,
        return_fig=False,
        **layout_opts,
    ):
        """Plot the computational graph of this ``LazyArray``."""
        import matplotlib as mpl
        import matplotlib.pyplot as plt
        from matplotlib.colors import to_rgb
        import networkx as nx

        isdark = sum(to_rgb(mpl.rcParams["figure.facecolor"])) / 3 < 0.5
        if isdark:
            draw_color = (0.75, 0.77, 0.80, 1.0)
        else:
            draw_color = (0.45, 0.47, 0.50, 1.0)

        if edge_color is None:
            edge_color = draw_color

        if label_color is None:
            label_color = mpl.rcParams["axes.labelcolor"]

        created_fig = ax is None
        if created_fig:
            fig, ax = plt.subplots(figsize=figsize, constrained_layout=True)
            ax.axis("off")
            ax.set_aspect("equal")

        G = self.to_nx_digraph(
            variables=variables,
            var_color=var_color,
            const_color=const_color,
            root_color=root_color,
            node_scale=node_scale,
        )

        if initial_layout == "spiral":
            layout_opts.setdefault("equidistant", True)

        pos = getattr(nx, initial_layout + "_layout")(G, **layout_opts)
        if iterations:
            pos = nx.layout.spring_layout(G, pos=pos, k=k, iterations=iterations)

        nx.draw_networkx_edges(
            G,
            pos=pos,
            ax=ax,
            edge_color=draw_color,
            connectionstyle=connectionstyle,
            arrowsize=arrowsize,
            arrows=True,
        )
        nx.draw_networkx_nodes(
            G,
            pos=pos,
            ax=ax,
            node_color=[G.nodes[x]["color"] for x in G.nodes],
            node_size=[G.nodes[x]["size"] for x in G.nodes],
            alpha=node_alpha,
        )
        if show_labels:
            nx.draw_networkx_labels(
                G,
                pos=pos,
                ax=ax,
                labels={x: G.nodes[x]["fn"] for x in G.nodes},
                font_color=label_color,
                font_size=font_size,
                alpha=label_alpha,
                bbox={
                    "color": to_rgb(mpl.rcParams["figure.facecolor"]),
                    "alpha": label_alpha,
                },
            )

        if not created_fig:
            return

        if return_fig:
            return fig
        else:
            plt.show()
            plt.close(fig)

    @property
    def fn(self):
        return self._fn

    @property
    def fn_name(self):
        return getattr(self._fn, "__name__", "None")

    @property
    def args(self):
        return self._args

    @property
    def kwargs(self):
        return self._kwargs

    @property
    def shape(self):
        return self._shape

    @property
    def ndim(self):
        return len(self._shape)

    @property
    def size(self):
        return functools.reduce(operator.mul, self.shape, 1)

    @property
    def backend(self):
        return self._backend

    @property
    def deps(self):
        return self._deps

    def __getitem__(self, key):
        return getitem(self, key)

    # this makes numpy operations delegate to __rmatmul__ etc.
    __array_ufunc__ = None

    def __mul__(self, other):
        return multiply(self, other)

    def __rmul__(self, other):
        return multiply(self, other)

    def __add__(self, other):
        return add(self, other)

    def __radd__(self, other):
        return add(self, other)

    def __sub__(self, other):
        return sub(self, other)

    def __rsub__(self, other):
        return sub(other, self)

    def __floordiv__(self, other):
        return floordivide(self, other)

    def __rfloordiv__(self, other):
        return floordivide(other, self)

    def __truediv__(self, other):
        return truedivide(self, other)

    def __rtruediv__(self, other):
        return truedivide(other, self)

    def __pow__(self, other):
        return pow_(self, other)

    def __rpow__(self, other):
        return pow_(other, self)

    def __matmul__(self, other):
        return matmul(self, other)

    def __rmatmul__(self, other):
        return matmul(other, self)

    def __abs__(self):
        return abs_(self)

    def __neg__(self):
        return self.to(operator.neg)

    @property
    def T(self):
        return transpose(self)

    @property
    def H(self):
        return conj(transpose(self))

    def reshape(self, shape):
        return reshape(self, shape)

    def astype(self, dtype_name):
        return lazy_astype(self, dtype_name)

    @property
    def real(self):
        return real(self)

    @property
    def imag(self):
        return imag(self)

    def __repr__(self):
        return (
            f"<{self.__class__.__name__}("
            f"fn={self.fn_name}, "
            f"shape={self.shape}, "
            f"backend='{self.backend}')>"
        )


register_backend(LazyArray, "autoray.lazy")


def ensure_lazy(array):
    if not isinstance(array, LazyArray):
        return LazyArray.from_data(array)
    return array


def find_lazy(x):
    """Recursively search for ``LazyArray`` instances in pytrees."""
    if isinstance(x, LazyArray):
        yield x
        return

    if isinstance(x, (tuple, list)):
        for subx in x:
            yield from find_lazy(subx)
        return

    if isinstance(x, dict):
        for subx in x.values():
            yield from find_lazy(subx)
        return


# --------------------- recusively evaluating 'pytrees' --------------------- #


def materialize_larray(x):
    return x._materialize()


def materialize_tuple(x):
    return tuple(map(maybe_materialize, x))


def materialize_list(x):
    return list(map(maybe_materialize, x))


def materialize_dict(x):
    return {k: maybe_materialize(v) for k, v in x.items()}


def materialize_identity(x):
    return x


_materialize_dispatch = collections.defaultdict(
    lambda: materialize_identity,
    {
        LazyArray: materialize_larray,
        tuple: materialize_tuple,
        list: materialize_list,
        dict: materialize_dict,
    },
)


def maybe_materialize(x):
    """Recursively evaluate LazyArray instances in tuples, lists and dicts."""
    return _materialize_dispatch[x.__class__](x)


# -------------------- recusively stringifying 'pytrees' -------------------- #


def stringify_larray(x, params):
    name = f"x{id(x)}"
    if x._data is not None:
        params.setdefault(name, x._data)
    return name


def stringify_tuple(x, params):
    if not x:
        return "()"
    return f"({', '.join(stringify(xi, params) for xi in x)},)"


def stringify_list(x, params):
    return f"[{', '.join(stringify(xi, params) for xi in x)}]"


def stringify_dict(x, params):
    entries = (f"{k}: {stringify(v, params)}" for k, v in x.items())
    return f"{{{', '.join(entries)}}}"


def stringify_identity(x, params):
    if isinstance(x, (int, float, complex, bool, slice, range)):
        return f"{x}"
    if isinstance(x, str):
        return f"'{x}'"
    name = f"c{id(x)}"
    params.setdefault(name, x)
    return name


_stringify_dispatch = collections.defaultdict(
    lambda: stringify_identity,
    {
        LazyArray: stringify_larray,
        tuple: stringify_tuple,
        list: stringify_list,
        dict: stringify_dict,
    },
)


def stringify(x, params):
    """Recursively stringify LazyArray instances in tuples, lists and dicts."""
    return _stringify_dispatch[x.__class__](x, params)


def _code_exec_fn(params, code, out_name):
    exec(code, None, params)
    return params[out_name]


def _array_fn(arrays, var_names, fn, params):
    # inject the new arrays
    for name, array in zip(var_names, arrays):
        params[name] = array
    # run the byte-compiled function with the new locals
    return fn(params)


# --------------------------------- caching --------------------------------- #


_SHARING_STACK = collections.defaultdict(list)


def currently_sharing():
    """Check if we are currently sharing a cache -- thread specific."""
    return threading.get_ident() in _SHARING_STACK


def get_sharing_cache():
    """Return the most recent sharing cache -- thread specific."""
    return _SHARING_STACK[threading.get_ident()][-1]


def _add_sharing_cache(cache):
    _SHARING_STACK[threading.get_ident()].append(cache)


def _remove_sharing_cache():
    tid = threading.get_ident()
    _SHARING_STACK[tid].pop()
    if not _SHARING_STACK[tid]:
        del _SHARING_STACK[tid]


@contextlib.contextmanager
def shared_intermediates(cache=None):
    """Context in which contract intermediate results are shared.

    Note that intermediate computations will not be garbage collected until
    1. this context exits, and
    2. the yielded cache is garbage collected (if it was captured).

    Parameters
    ----------
    cache : dict
        If specified, a user-stored dict in which intermediate results will
        be stored. This can be used to interleave sharing contexts.

    Returns
    -------
    cache : dict
        A dictionary in which sharing results are stored. If ignored,
        sharing results will be garbage collected when this context is
        exited. This dict can be passed to another context to resume
        sharing.
    """
    if cache is None:
        cache = {}
    _add_sharing_cache(cache)
    try:
        yield cache
    finally:
        _remove_sharing_cache()


def maybe_id(x):
    if hasattr(x, "shape"):
        return id(x)
    return x


def hash_args_kwargs(fn_name, *args, **kwargs):
    hargs = tuple(map(maybe_id, args))
    if kwargs:
        hkwargs = tuple(sorted((k, maybe_id(v)) for k, v in kwargs.items()))
    else:
        hkwargs = None
    return f"{fn_name}-{hash((hargs, hkwargs))}"


def lazy_cache(fn_name, hasher=None):

    if hasher is None:
        hasher = hash_args_kwargs

    def wrapper(fn):
        @functools.wraps(fn)
        def wrapped(*args, **kwargs):

            if not currently_sharing():
                return fn(*args, **kwargs)

            cache = get_sharing_cache()

            key = hasher(fn_name, *args, **kwargs)
            if key not in cache:
                cache[key] = fn(*args, **kwargs)

            return cache[key]

        return wrapped

    return wrapper


_DTYPES_REAL_EQUIV = {"complex128": "float64", "complex64": "float32"}
_DTYPES_COMPLEX_EQUIV = {"float64": "complex128", "float32": "complex64"}


@functools.lru_cache(None)
def dtype_real_equiv(dtype_name):
    return _DTYPES_REAL_EQUIV.get(dtype_name, dtype_name)


@functools.lru_cache(None)
def dtype_complex_equiv(dtype_name):
    return _DTYPES_COMPLEX_EQUIV.get(dtype_name, dtype_name)


@functools.lru_cache(None)
def _find_common_dtype(array_types, scalar_types):
    import numpy as np

    return np.find_common_type(array_types, scalar_types).name


def find_common_dtype(*xs):
    return _find_common_dtype(tuple(map(get_dtype_name, xs)), ())


def find_common_backend(*xs):
    backend = None

    # prefer inferring from LazyArray
    for x in xs:
        b = getattr(x, "backend", None)
        if b == "autoray.lazy":
            # check if any LazyArray is *itself* backed by LazyArray
            return b

        # else default to first backend seen
        elif (backend is None) and (b is not None):
            backend = b

    # if no LazyArray args, check raw arrays
    if backend is None:
        backend = next(iter(infer_backend(x) for x in xs if hasattr(x, "shape")), None)

    return backend


@functools.lru_cache(1024)
def find_broadcast_shape(xshape, yshape):
    xndim = len(xshape)
    yndim = len(yshape)
    if xndim < yndim:
        xshape = (1,) * (yndim - xndim)
    elif yndim < xndim:
        yshape = (1,) * (xndim - yndim)
    return tuple(max(d1, d2) for d1, d2 in zip(xshape, yshape))


# -------------------------------- interface -------------------------------- #


def Variable(shape, backend=None):
    """Create a ``LazyArray`` from a shape only, representing a leaf node
    in the computational graph. It can only act as a placeholder for data.
    """
    return LazyArray.from_shape(shape, backend=backend)


@lazy_cache("array")
def array(x):
    """Create a ``LazyArray`` from an input array, representing a leaf node
    in the computational graph.
    """
    return LazyArray.from_data(x)


@lazy_cache("transpose")
def transpose(a, axes=None):
    a = ensure_lazy(a)
    fn_transpose = get_lib_fn(a.backend, "transpose")

    if axes is None:
        axes = range(a.ndim)[::-1]
    newshape = tuple(a.shape[i] for i in axes)

    # check for chaining transpositions
    if a._fn is fn_transpose:
        b = a._args[0]
        if isinstance(b, LazyArray):
            axes_prev = a._args[1]
            axes_chained = tuple(axes_prev[k] for k in axes)
            return b.to(fn_transpose, (b, axes_chained), shape=newshape)

    return a.to(fn_transpose, (a, axes), shape=newshape)


@lazy_cache("reshape")
def _reshape_tuple(a, newshape):
    a = ensure_lazy(a)
    fn_reshape = get_lib_fn(a.backend, "reshape")

    # check for redundant reshapes
    if a._fn is fn_reshape:
        b = a._args[0]
        if isinstance(b, LazyArray):
            a = b

    return a.to(fn_reshape, (a, newshape), shape=newshape)


@functools.lru_cache(2**14)
def find_full_reshape(newshape, size):
    try:
        expand = newshape.index(-1)
        before = newshape[:expand]
        after = newshape[expand + 1 :]
        d = size // functools.reduce(operator.mul, itertools.chain(before, after), 1)
        return (*before, d, *after)
    except ValueError:
        return newshape


def reshape(a, newshape):
    newshape = (newshape,) if isinstance(newshape, int) else tuple(newshape)
    newshape = find_full_reshape(newshape, a.size)
    return _reshape_tuple(a, newshape)


def getitem_hasher(_, a, key):
    if not isinstance(key, tuple):
        key = (key,)
    hkey = tuple(
        str(k) if isinstance(k, slice) else id(k) if hasattr(k, "shape") else k
        for k in key
    )
    return f"getitem-{hash((id(a), hkey))}"


@lazy_cache("getitem", hasher=getitem_hasher)
def getitem(a, key):
    a = ensure_lazy(a)

    deps = (a,)

    if not isinstance(key, tuple):
        key = (key,)

    try:
        # expand ellipsis
        expand = key.index(...)
        ndiff = a.ndim - len(key) + 1
        key = key[:expand] + (slice(None),) * ndiff + key[expand + 1 :]
    except ValueError:
        # else pad trailing slices if necessary
        ndiff = a.ndim - len(key)
        if ndiff:
            key = key + (slice(None),) * ndiff

    newshape = []
    for k, d in zip(key, a.shape):
        if isinstance(k, LazyArray):
            newshape.append(k.size)
            deps += (k,)
        elif isinstance(k, slice):
            newshape.append(len(range(d)[k]))
        else:
            try:
                newshape.append(len(k))
            except TypeError:
                pass

    # TODO: np.newaxis == None

    newshape = tuple(newshape)
    return a.to(operator.getitem, (a, key), shape=newshape, deps=deps)


@lazy_cache("tensordot")
def tensordot(a, b, axes=2):

    if isinstance(axes, int):
        axes = (tuple(range(a.ndim - axes, a.ndim)), tuple(range(axes)))

    newshape = tuple(d for i, d in enumerate(a.shape) if i not in axes[0]) + tuple(
        d for i, d in enumerate(b.shape) if i not in axes[1]
    )

    backend = find_common_backend(a, b)
    fn_tensordot = get_lib_fn(backend, "tensordot")

    return LazyArray(
        backend=backend,
        fn=fn_tensordot,
        args=(a, b, axes),
        kwargs=None,
        shape=newshape,
        deps=tuple(x for x in (a, b) if isinstance(x, LazyArray)),
    )


@lazy_cache("einsum")
def einsum(*operands):
    from opt_einsum.parser import parse_einsum_input

    deps, output, larrays = parse_einsum_input(operands)

    size_dict = {}
    for term, op in zip(deps.split(","), larrays):
        for i, char in enumerate(term):
            size_dict[char] = max(size_dict.get(char, 1), op.shape[i])
    eq = deps + "->" + output
    newshape = tuple(size_dict[char] for char in output)

    backend = find_common_backend(*larrays)
    fn_einsum = get_lib_fn(backend, "einsum")

    return LazyArray(
        backend=backend,
        fn=fn_einsum,
        args=(eq, *larrays),
        kwargs=None,
        shape=newshape,
        deps=tuple(x for x in larrays if isinstance(x, LazyArray)),
    )


@lazy_cache("trace")
def trace(a):
    a = ensure_lazy(a)
    return a.to(
        fn=get_lib_fn(a.backend, "trace"),
        args=(a,),
        shape=(),
    )


@lazy_cache("matmul")
def matmul(x1, x2):
    backend = find_common_backend(x1, x2)
    newshape = (*x1.shape[:-1], *x2.shape[1:])
    return LazyArray(
        backend=backend,
        fn=operator.matmul,
        args=(x1, x2),
        kwargs=None,
        shape=newshape,
        deps=tuple(x for x in (x1, x2) if isinstance(x, LazyArray)),
    )


@lazy_cache("kron")
def kron(x1, x2):
    backend = find_common_backend(x1, x2)
    newshape = tuple(d1 * d2 for d1, d2 in zip(x1.shape, x2.shape))
    fn_kron = get_lib_fn(backend, "kron")
    return LazyArray(
        backend=backend,
        fn=fn_kron,
        args=(x1, x2),
        kwargs=None,
        shape=newshape,
        deps=tuple(x for x in (x1, x2) if isinstance(x, LazyArray)),
    )


@lazy_cache("clip")
def clip(a, a_min, a_max):
    a = ensure_lazy(a)
    fn_clip = get_lib_fn(a.backend, "clip")
    return a.to(fn_clip, (a, a_min, a_max))


@lazy_cache("flip")
def flip(a, axis=None):
    a = ensure_lazy(a)
    fn_flip = get_lib_fn(a.backend, "flip")
    return a.to(fn_flip, (a, axis))


@lazy_cache("sort")
def sort(a, axis=-1):
    a = ensure_lazy(a)
    return a.to(get_lib_fn(a.backend, "sort"), (a, axis))


@lazy_cache("argsort")
def argsort(a, axis=-1):
    a = ensure_lazy(a)
    return a.to(
        fn=get_lib_fn(a.backend, "argsort"),
        args=(a, axis),
    )


@lazy_cache("stack")
def stack(arrays, axis=0):
    arrays = tuple(arrays)
    newshape = list(arrays[0].shape)
    newshape.insert(axis if axis >= 0 else axis + 1, len(arrays))

    backend = find_common_backend(*arrays)
    fn = get_lib_fn(backend, "stack")
    return LazyArray(
        backend=backend,
        fn=fn,
        args=(arrays, axis),
        kwargs=None,
        shape=tuple(newshape),
        deps=tuple(x for x in arrays if isinstance(x, LazyArray)),
    )


@lazy_cache("concatenate")
def concatenate(arrays, axis=0):
    arrays = tuple(arrays)
    newshape = list(arrays[0].shape)
    newshape[axis] = sum(a.shape[axis] for a in arrays)

    backend = infer_backend(arrays[0])
    fn = get_lib_fn(backend, "concatenate")
    return LazyArray(
        backend=backend,
        fn=fn,
        args=(arrays, axis),
        kwargs=None,
        shape=tuple(newshape),
        deps=tuple(x for x in arrays if isinstance(x, LazyArray)),
    )


@lazy_cache("split")
def split(ary, indices_or_sections, axis=0):
    ary = ensure_lazy(ary)

    d = ary.shape[axis]
    num_subarrays = len(indices_or_sections) + 1
    div_points = [0] + list(indices_or_sections) + [d]

    sub_arys = []
    selector = [slice(None)] * ary.ndim
    for i in range(num_subarrays):
        st = div_points[i]
        end = div_points[i + 1]
        selector[axis] = slice(st, end)
        sub_arys.append(ary[tuple(selector)])

    return tuple(sub_arys)


def make_binary_func(name, fn):
    @lazy_cache(name)
    def binary_func(x1, x2):
        x1shape = getattr(x1, "shape", ())
        x2shape = getattr(x2, "shape", ())
        newshape = find_broadcast_shape(x1shape, x2shape)
        return LazyArray(
            backend=find_common_backend(x1, x2),
            fn=fn,
            args=(x1, x2),
            kwargs=None,
            shape=newshape,
            deps=tuple(x for x in (x1, x2) if isinstance(x, LazyArray)),
        )

    return binary_func


multiply = make_binary_func("multiply", operator.mul)
add = make_binary_func("add", operator.add)
sub = make_binary_func("sub", operator.sub)
floordivide = make_binary_func("floordivide", operator.floordiv)
truedivide = make_binary_func("truedivide", operator.truediv)
pow_ = make_binary_func("pow", operator.pow)


def complex_(re, im):
    newshape = find_broadcast_shape(re.shape, im.shape)
    backend = find_common_backend(re, im)
    fn_complex = get_lib_fn(backend, "complex")
    return LazyArray(
        backend=backend,
        fn=fn_complex,
        args=(re, im),
        kwargs=None,
        shape=newshape,
        deps=tuple(x for x in (re, im) if isinstance(x, LazyArray)),
    )


def make_unary_func(name, to_real=False):
    @lazy_cache(name)
    def unary_func(x):
        x = ensure_lazy(x)
        return x.to(fn=get_lib_fn(x.backend, name))

    return unary_func


sin = make_unary_func("sin")
cos = make_unary_func("cos")
tan = make_unary_func("tan")
arcsin = make_unary_func("arcsin")
arccos = make_unary_func("arccos")
arctan = make_unary_func("arctan")
sinh = make_unary_func("sinh")
cosh = make_unary_func("cosh")
tanh = make_unary_func("tanh")
arcsinh = make_unary_func("arcsinh")
arccosh = make_unary_func("arccosh")
arctanh = make_unary_func("arctanh")
sqrt = make_unary_func("sqrt")
exp = make_unary_func("exp")
log = make_unary_func("log")
log2 = make_unary_func("log2")
log10 = make_unary_func("log10")
conj = make_unary_func("conj")
sign = make_unary_func("sign")
abs_ = make_unary_func("abs", to_real=True)
angle = make_unary_func("angle", to_real=True)
real = make_unary_func("real", to_real=True)
imag = make_unary_func("imag", to_real=True)


def make_reduction_func(name):
    @lazy_cache(name)
    def reduction_func(a, axis=None):
        a = ensure_lazy(a)
        fn = get_lib_fn(a.backend, name)

        nd = a.ndim
        if axis is None:
            return a.to(
                fn=fn,
                shape=(),
            )
        elif not hasattr(axis, "__len__"):
            axis = (axis,)
        axis = tuple(nd - i if i < 0 else i for i in axis)

        newshape = tuple(d for i, d in enumerate(a.shape) if i not in axis)
        return a.to(fn=fn, args=(a, axis), shape=newshape)

    return reduction_func


sum_ = make_reduction_func("sum")
prod = make_reduction_func("prod")
min_ = make_reduction_func("min")
max_ = make_reduction_func("max")

# # XXX: still missing
# allclose, complex, diag
# dot, vdot, kron, inner, outer
# pad, eye
# squeeze, expand_dims
# to_numpy


# ---------------------------- autoray specials ----------------------------- #


def lazy_get_dtype_name(x):
    return x.dtype


@lazy_cache("astype")
def lazy_astype(x, dtype_name):
    x = ensure_lazy(x)
    return x.to(fn=astype, args=(x, dtype_name))


register_function("autoray.lazy", "get_dtype_name", lazy_get_dtype_name)
register_function("autoray.lazy", "astype", lazy_astype)
