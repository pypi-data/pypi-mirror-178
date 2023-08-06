"""
The :mod:`skorch_forecasting.preprocessing` module includes tools for
performing sklearn transformations to pandas DataFrames for general
applications (not only time series). It also includes a group wise column
transformer, i.e., :class:`GroupWiseColumnTransformer`, that makes it possible
to fit and transform each DataFrame group individually.
"""

from ._preprocessor_creator import PreprocessorCreator
from ._data import ColumnDuplicator, IdentityTransformer
from ._encoders import (
    CyclicalDatesEncoder,
    MultiColumnLabelEncoder,
    TimeIndexEncoder
)
from ._group_wise import GroupWiseColumnTransformer
from ._pandas_column_transformer import PandasColumnTransformer
from ._sliding_window import SlidingWindow, inverse_transform_sliding_window

__all__ = [
    'PreprocessorCreator',
    'GroupWiseColumnTransformer',
    'MultiColumnLabelEncoder',
    'PandasColumnTransformer',
    'CyclicalDatesEncoder',
    'SlidingWindow',
    'TimeIndexEncoder',
    'ColumnDuplicator',
    'IdentityTransformer',
    'inverse_transform_sliding_window'
]
