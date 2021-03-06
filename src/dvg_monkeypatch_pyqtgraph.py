#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Monkey-patch for pyqtgraph v0.11.0
"""
__author__ = "Dennis van Gils"
__authoremail__ = "vangils.dennis@gmail.com"
__url__ = "https://github.com/Dennis-van-Gils/python-dvg-pyqtgraph-monkeypatch"
__date__ = "20-01-2022"
__version__ = "2.0.0"
# fmt: off

import numpy as np
import pyqtgraph as pg

def PlotCurveItem_paintGL(self, p, opt, widget):
    """
    Edited:
        pyqtgraph/graphicsItems/PlotCurveItem.py
        v0.11.0

    Added missing statement between line 571 and 572:
        gl.glLineWidth(width)
    """
    p.beginNativePainting()
    import OpenGL.GL as gl

    ## set clipping viewport
    view = self.getViewBox()
    if view is not None:
        rect = view.mapRectToItem(self, view.boundingRect())
        #gl.glViewport(int(rect.x()), int(rect.y()), int(rect.width()), int(rect.height()))

        #gl.glTranslate(-rect.x(), -rect.y(), 0)

        gl.glEnable(gl.GL_STENCIL_TEST)
        gl.glColorMask(gl.GL_FALSE, gl.GL_FALSE, gl.GL_FALSE, gl.GL_FALSE) # disable drawing to frame buffer
        gl.glDepthMask(gl.GL_FALSE)  # disable drawing to depth buffer
        gl.glStencilFunc(gl.GL_NEVER, 1, 0xFF)
        gl.glStencilOp(gl.GL_REPLACE, gl.GL_KEEP, gl.GL_KEEP)

        ## draw stencil pattern
        gl.glStencilMask(0xFF)
        gl.glClear(gl.GL_STENCIL_BUFFER_BIT)
        gl.glBegin(gl.GL_TRIANGLES)
        gl.glVertex2f(rect.x(), rect.y())
        gl.glVertex2f(rect.x()+rect.width(), rect.y())
        gl.glVertex2f(rect.x(), rect.y()+rect.height())
        gl.glVertex2f(rect.x()+rect.width(), rect.y()+rect.height())
        gl.glVertex2f(rect.x()+rect.width(), rect.y())
        gl.glVertex2f(rect.x(), rect.y()+rect.height())
        gl.glEnd()

        gl.glColorMask(gl.GL_TRUE, gl.GL_TRUE, gl.GL_TRUE, gl.GL_TRUE)
        gl.glDepthMask(gl.GL_TRUE)
        gl.glStencilMask(0x00)
        gl.glStencilFunc(gl.GL_EQUAL, 1, 0xFF)

    try:
        x, y = self.getData()
        pos = np.empty((len(x), 2))
        pos[:,0] = x
        pos[:,1] = y
        gl.glEnableClientState(gl.GL_VERTEX_ARRAY)
        try:
            gl.glVertexPointerf(pos)
            pen = pg.mkPen(self.opts['pen'])
            color = pen.color()
            gl.glColor4f(color.red()/255., color.green()/255., color.blue()/255., color.alpha()/255.)
            width = pen.width()
            if pen.isCosmetic() and width < 1:
                width = 1
            gl.glPointSize(width)
            gl.glLineWidth(width)
            gl.glEnable(gl.GL_LINE_SMOOTH)
            gl.glEnable(gl.GL_BLEND)
            gl.glBlendFunc(gl.GL_SRC_ALPHA, gl.GL_ONE_MINUS_SRC_ALPHA)
            gl.glHint(gl.GL_LINE_SMOOTH_HINT, gl.GL_NICEST)
            gl.glDrawArrays(gl.GL_LINE_STRIP, 0, int(pos.size / pos.shape[-1]))
        finally:
            gl.glDisableClientState(gl.GL_VERTEX_ARRAY)
    finally:
        p.endNativePainting()

# Monkey-patch errors in pyqtgraph v0.11.0
if pg.__version__ == "0.11.0":
    pg.PlotCurveItem.paintGL = PlotCurveItem_paintGL
