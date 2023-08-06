from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler

from ._encoders import TimeIndexEncoder
from ._group_wise import GroupWiseColumnTransformer
from ._pandas_column_transformer import PandasColumnTransformer
from ._column_selector import ColumnSelector


def _make_step(step_name, transformer):
    """Private function for making a single sklearn :class:`Pipeline` step.
    """
    return step_name, transformer


def _make_column_selector(dtype_include, to_exclude):
    """Private function for instantiating :class:`ColumnSelector`.
    """
    return ColumnSelector(
        dtype_include=dtype_include,
        pattern_exclude=to_exclude
    )


class PreprocessorCreator:
    """Creates a preprocessor in the form of a sklearn :class:`Pipeline`.

    The preprocessor transforms the data into a numerical space suitable
    for the learning algorithm and includes the following steps:

    - Target transformations:
        Transformations defined here will act only in the target variable.

    - Group transformations:
        Transformations defined here will act group by group.

    - Column transformations:
        Transformations defined here will act on the entire data

    Steps are meant to be chained together with other steps (for example,
    with the ones from :meth:`make_default_steps`).

    Parameters
    ----------
    group_ids : list of str.
        Group ids identifying each time series.

    target : str
        Name of target column.
    """

    def __init__(self, group_ids, target):
        self.group_ids = group_ids
        self.target = target

    def create_preprocessor(self, steps):
        """Creates a preprocessor in the form of a sklearn :class:`Pipeline`.

        Parameters
        ----------
        steps : list of tuple
            List of (name, transform) tuples (implementing `fit`/`transform`)
            that are chained in sequential order. See :meth:`make_steps` for
            obtaining a collection of ready to use steps.

        Returns
        -------
        preprocessor : sklearn.pipeline.Pipeline
        """
        return Pipeline(steps)

    def make_target_step(
            self, transformer=MinMaxScaler(), step_name='target_step'
    ):
        """Makes target transformation step.

        Group wise transformation.

        Parameters
        ----------
        transformer : Transformer, default=MinMaxScaler()
            Transformer instance.

        step_name : str, default='target_step'
            Name for identifying the step.

        Returns
        -------
        (step_name, transformer) : tuple
        """
        trans_tuple = [(transformer, [self.target])]
        return self.make_step(step_name, trans_tuple, group_wise=True)

    def make_numerical_step(
            self,
            transformer=MinMaxScaler(),
            to_exclude=None,
            step_name='numerical_step'
    ):
        """Makes numerical transformation step.

        Group wise transformation.

        Parameters
        ----------
        transformer : Transformer, default=MinMaxScaler()
            Transformer instance.

        to_exclude : list of str, default=None
            Column names to exclude from this transformation. By default,
            ``target`` and ``group_ids`` are always excluded from this
            transformation step.

        step_name : str, default='group_wise_step'
            Name for identifying the step.

        Returns
        -------
        (step_name, transformer) : tuple
        """
        if to_exclude is None:
            to_exclude = []

        # Feature/columns to include in the transformation step.
        # Notice only numerical dtypes are included.
        to_exclude += [self.target] + self.group_ids
        col_selector = _make_column_selector(
            dtype_include=['int', 'float'], to_exclude=to_exclude)

        trans_tuple = [(transformer, col_selector)]
        return self.make_step(step_name, trans_tuple, group_wise=True)

    def make_time_index_encoding_step(
            self, timestamp_col, start_idx=0, extra_timestamps=10,
            freq='D', step_name='time_index_encoder'
    ):
        """Creates the step for a time index encoding.

        Group wise transformation.

        Parameters
        ----------
        timestamp_col : str
            Timestamp column.

        start_idx : int, default=0
            Integer (including 0) where the time index will start

        extra_timestamps : int, default=10
            Extra timestamp to include in the encoding.

        freq : str, default='D'
            Frequency of timestamps

        step_name : str, default='time_index_encoder'
            Name for the step.

        Returns
        -------
        (step_name, transformer) : tuple
        """
        encoder = TimeIndexEncoder(start_idx, extra_timestamps, freq)
        trans_tuple = [(encoder, timestamp_col)]
        return self.make_step(step_name, trans_tuple)

    def make_default_steps(self):
        """Makes default steps.

        Returns
        -------
        steps : list of (step_name, transformer) tuples.
        """
        steps = [
            self.make_target_step(),
            self.make_numerical_step(),
        ]
        return steps

    def make_step(self, step_name, transformer_tuples, group_wise=False):

        if group_wise:
            transformer = GroupWiseColumnTransformer(transformer_tuples,
                                                     self.group_ids)
        else:
            transformer = PandasColumnTransformer(transformer_tuples)

        return _make_step(step_name, transformer)
