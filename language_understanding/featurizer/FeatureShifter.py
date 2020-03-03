#!/usr/bin/env python
import os
import argparse

class FeatureShifter(object):
    def __init__(self, shift):
        self._shift = shift

    def FitTransform(self, input):
        return self.Transform(input)

    def Transform(self, input):
        output = []
        for s,e,fid in input:
            output.append((s + self._shift, e + self._shift, fid))
        return output

