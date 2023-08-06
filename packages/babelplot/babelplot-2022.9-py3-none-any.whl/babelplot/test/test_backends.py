# Copyright CNRS/Inria/UCA
# Contributor(s): Eric Debreuve (since 2022)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import numpy as nmpy
import plotly.graph_objects as plly  # noqa

from babelplot import NewBabelPlotFigure, ShowAllFigures, plot_e
from babelplot.type.dimension import dim_e


figure_1 = NewBabelPlotFigure(pbe="bokeh")
frame = figure_1.AddFrame(plot_width=400, plot_height=200)
frame.AddPlot("hbar", y=[2, 4, 6], height=1, left=0, right=[1, 2, 3], color="Cyan")


figure_2 = NewBabelPlotFigure(title="Plotly Figure", pbe="plotly")
frame = figure_2.AddFrame(title="Plotly Frame")
frame.AddPlot(
    plly.Surface,
    contours={
        "x": {"show": True, "start": 1.5, "end": 2, "size": 0.04, "color": "white"},
        "z": {"show": True, "start": 0.5, "end": 0.8, "size": 0.05},
    },
    x=[1, 2, 3, 4, 5],
    y=[1, 2, 3, 4, 5],
    z=[
        [0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0],
        [1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0],
    ],
    name="Surface",
)


figure_3 = NewBabelPlotFigure(pbe="bokeh")
frame = figure_3.AddFrame(plot_width=400, plot_height=200)
frame.AddPlot(plot_e.SCATTER, [1, 2, 3], [2, 4, 6])


x, y, z = nmpy.ogrid[-10:10:20j, -10:10:20j, -10:10:20j]
s = nmpy.sin(x * y * z) / (x * y * z)

figure_4 = NewBabelPlotFigure(pbe="vedo")
frame = figure_4.AddFrame(dim=dim_e.XYZ)
frame.AddPlot(plot_e.ISOSET, s, s.min() + 0.1 * s.ptp())
print("!!! VEDO OPENS THE FIGURE AND CRASHES IMMEDIATELY !!!")


ShowAllFigures()
