# Copyright (c) 2017 Civic Knowledge. This file is licensed under the terms of the
# MIT License, included in this distribution as LICENSE
"""

"""

from pandas import DataFrame, Series
import numpy as np
from six import string_types
import numpy as np
from six import string_types


class CensusSeries(Series):

    _metadata = ['schema', 'parent_frame']

    @property
    def _constructor(self):
        return CensusSeries

    @property
    def _constructor_expanddim(self):
        from .dataframe import CensusDataFrame
        return CensusDataFrame

    @property
    def census_code(self):
        return self.schema['code']

    @property
    def census_index(self):
        return self.schema['index']

    @property
    def census_title(self):
        return self.schema['title']


    def __init__(self, data=None, index=None, dtype=None, name=None, copy=False, fastpath=False):
        super(CensusSeries, self).__init__(data, index, dtype, name, copy, fastpath)


    @property
    def m90(self):
        if self.census_code.endswith('_m90'):
            return self
        else:
            return self.parent_frame[self.census_code+'_m90'].astype('float')

    @property
    def value(self):
        """Return the float value for an error column"""
        if self.census_code.endswith('_m90'):
            return self.parent_frame[self.census_code.replace('_m90','')].astype('float')
        else:
            return self

    @property
    def se(self):
        """Return a standard error series, computed from the 90% margins"""
        return self.m90 / 1.645

    @property
    def rse(self):
        """Return the relative standard error for a column"""

        return self.se / self.value() * 100

    @property
    def m95(self):
        """Return a standard error series, computed from the 90% margins"""
        return self.se * 1.96

    @property
    def m99(self):
        """Return a standard error series, computed from the 90% margins"""
        return self.se * 2.575
