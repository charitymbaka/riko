# -*- coding: utf-8 -*-
# vim: sw=4:ts=4:expandtab
"""
    pipe2py.twisted.collections
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Provides methods for creating asynchronous pipe2py pipes
"""

from __future__ import (
    absolute_import, division, print_function, with_statement,
    unicode_literals)

from twisted.internet.defer import inlineCallbacks, returnValue
from pipe2py.modules.pipeforever import asyncPipeForever
from pipe2py.lib.collections import PyPipe


class AsyncPipe(PyPipe):
    """An asynchronous PyPipe object"""
    def __init__(self, name=None, context=None, **kwargs):
        super(AsyncPipe, self).__init__(name, context)
        self.pipe_input = kwargs.pop('input', asyncPipeForever())
        self.pipeline = getattr(self.module, 'asyncPipe%s' % self.name.title())
        self.kwargs = kwargs

    @property
    @inlineCallbacks
    def list(self):
        output = yield self.output
        returnValue(list(output))

    def pipe(self, name, **kwargs):
        return AsyncPipe(name, self.context, input=self.output, **kwargs)

    def loop(self, name, **kwargs):
        async_pipe = AsyncPipe(name, self.context)
        kwargs.update({'setup': async_pipe.setup})
        return self.pipe('loop', embed=async_pipe.pipeline, **kwargs)
