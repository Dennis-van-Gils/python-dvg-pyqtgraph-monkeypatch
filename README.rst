.. image:: https://img.shields.io/pypi/v/dvg-pyqtgraph-monkeypatch
    :target: https://pypi.org/project/dvg-pyqtgraph-monkeypatch
.. image:: https://img.shields.io/badge/License-MIT-purple.svg
    :target: https://github.com/Dennis-van-Gils/python-dvg-pyqtgraph-monkeypatch/blob/master/LICENSE.txt

DvG_PyQtGraph_Monkeypatch
=========================
*Monkeypatch for pyqtgraph==0.11.0 resulting in superior OpenGL performance in contrast to more recent 0.11.1 to 0.12.3*

This monkeypatch is safe to import and will only get applied when it detects the
correct PyQtGraph version `pyqtgraph == 0.11.0`. For other versions it will
not affect anything at all. Also, when not using OpenGL in experimental mode,
nothing changes. 

- Github: https://github.com/Dennis-van-Gils/python-dvg-pyqtgraph-monkeypatch
- PyPI: https://pypi.org/project/dvg-pyqtgraph-monkeypatch

Installation::

    pip install dvg-pyqtgraph-monkeypatch

Reason for monkeypatch
======================

This patch is intended for PyQtGraph with OpenGL acceleration enabled as such: ::

    import pyqtgraph as pg
    import OpenGL.GL as gl  # pylint: disable=unused-import
    pg.setConfigOptions(useOpenGL=True)
    pg.setConfigOptions(enableExperimental=True)
    pg.setConfigOptions(antialias=True)
    
Above code will enable OpenGL acceleration within PyQtGraph and adds
anti-aliasing to the chart curves. However, from versions `0.11.0` to `0.12.2`
it will not draw the linewidth of the curves correctly and they remain at 1
pixel width, regardless of the set linewidth. This patch fixes the linewidth
issue.

Why do I fix the PyQtgraph version for this monkeypatch to `0.11.0`? Several
reasons:

    - `0.11.0` draws the axis tick labels at the borders of the
      `pyqtgraph.PlotWidget` nicely, without cutting them off mid-way of the
      label itself. From `0.11.1` and up the tick labels will be cut off when
      they are at the border. That can be very confusing when reading the graph.
 
    - The most recent version at time of writing (`0.12.3`) actually has fixed
      the linewidth issue. However, the previous problem on the tick labels still
      applies.
    
    - It appears that `0.11.0` has superior plotting performance in frames per
      second / CPU load in contrast to `0.12.0` and up. This was confirmed and
      tested in another of my projects https://github.com/Dennis-van-Gils/DvG_Arduino_lock-in_amp.
      There is a different method used to render the graphs in OpenGL in these
      more recent PyQtGraph versions.

Usage
=====

You only have to import the module into your Python code after you have imported
PyQtGraph. That's all. The patch will then be applied automatically. ::

    import dvg_monkeypatch_pyqtgraph  # pylint: disable=unused-import
