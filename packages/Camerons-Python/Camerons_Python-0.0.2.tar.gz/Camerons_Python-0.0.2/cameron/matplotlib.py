import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np


__all__ = ["save_all", "named_bar_chart", "named_bar_chart_points"]


def save_all(filename, tight=False, **infodict):
    kwargs = {}
    if tight:
        kwargs['bbox_inches'] = "tight"
    with PdfPages(filename) as pdf:
        for fig in plt.get_fignums():
            pdf.savefig(fig, **kwargs)
        d = pdf.infodict()
        d.update(infodict)


def bar_chart_spacing(num_labels, num_sets, width_factor, offset_factor):
    max_width = 1 / num_sets
    width = max_width * width_factor * offset_factor
    x = np.arange(0, num_labels)
    offsets = offset_factor * np.arange(-0.5 + max_width / 2, 0.5, max_width)
    return width, x, offsets


def named_bar_chart(
    labels,
    data,
    *args,
    width_factor=1,
    offset_factor=1,
    per_set_args=None,
    per_set_kwargs=None,
    tick_kwargs={},
    **kwargs
):
    if not isinstance(data, np.ndarray):
        data = np.array(data)
    if data.ndim == 1:
        data = data.reshape(-1, data.size)
    num_labels = len(labels)
    num_sets = data.shape[0]
    assert num_labels == data.shape[1]
    width, x, offsets = bar_chart_spacing(
        num_labels, num_sets, width_factor, offset_factor
    )
    output = []
    for i, row in enumerate(data):
        set_args = list(args)
        if per_set_args is not None:
            assert len(per_set_args) == num_sets
            set_args.extend(per_set_args[i])
        set_kwargs = dict(kwargs)
        if per_set_kwargs is not None:
            assert len(per_set_kwargs) == num_sets
            set_kwargs.update(per_set_kwargs[i])
        output.append(
            plt.bar(x + offsets[i], row, width=width, *set_args, **set_kwargs)
        )
    output.extend(plt.xticks(x, labels, **tick_kwargs))
    return output


def named_bar_chart_points(data, *args, width_factor=1, offset_factor=1, **kwargs):
    if not isinstance(data, np.ndarray):
        data = np.array(data)
    num_sets = data.shape[0]
    num_labels = data.shape[1]
    width, x, offsets = bar_chart_spacing(
        num_labels, num_sets, width_factor, offset_factor
    )
    for i, row in enumerate(data):
        plt.plot(
            np.zeros_like(row) + x.reshape(num_labels, -1) + offsets[i],
            row,
            *args,
            **kwargs
        )
