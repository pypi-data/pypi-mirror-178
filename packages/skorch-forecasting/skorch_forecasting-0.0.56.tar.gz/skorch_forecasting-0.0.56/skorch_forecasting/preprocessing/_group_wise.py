import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted

from ._pandas_column_transformer import PandasColumnTransformer
from ..utils.data import loc_group
from ..utils.validation import check_group_ids


class GroupWiseColumnTransformer(BaseEstimator, TransformerMixin):
    """Transformer that transforms by groups.

    For each group, a :class:`PandasColumnTransformer` is fitted and
    applied.

    Notes
    -----
    The order of the columns in the transformed feature matrix follows the
    order of how the columns are specified in the transformers list. Since the
    passthrough kwarg is set, columns not specified in the transformers list
    are added at the right to the output.

    Parameters
    ----------
    *transformers : tuples
        Tuples of the form (transformer, columns) specifying the
        transformer objects to be applied to subsets of the data.

        transformer : {'drop', 'passthrough'} or estimator
            Estimator must support :term:`fit` and :term:`transform`.
            Special-cased strings 'drop' and 'passthrough' are accepted as
            well, to indicate to drop the columns or to pass them through
            untransformed, respectively.
        columns : str,  array-like of str, int, array-like of int, slice, \
                array-like of bool or callable
            Indexes the data on its second axis. Integers are interpreted as
            positional columns, while strings can reference DataFrame columns
            by name. A scalar string or int should be used where
            ``transformer`` expects X to be a 1d array-like (vector),
            otherwise a 2d array will be passed to the transformer.
            A callable is passed the input data `X` and can return any of the
            above. To select multiple columns by name or dtype, you can use
            :obj:`make_column_selector`.


    Attributes
    ----------
    mapping_ : dict, str -> ColumnTransformer object
        Dictionary mapping from group_id to its corresponding fitted
        ColumnTransformer object
    """

    def __init__(self, transformers, group_ids):
        self.transformers = transformers
        self.group_ids = group_ids

    def fit(self, X, y=None):
        """Fits a sklearn ColumnTransformer object to each group inside ``X``.

        In other words, each group in ``X`` gets assigned its own
        :class:`PandasColumnTransformer` instance which is then fitted to the
        data inside such group.

        Parameters
        ----------
        X : pd.DataFrame
            Dataframe having __init__ ``group_ids`` column(s).

        y : None
            This param exists for compatibility purposes with sklearn.

        Returns
        -------
        self (object): Fitted transformer.
        """
        check_group_ids(X, self.group_ids)

        # Mapping from group_id to ColumnTransformer object.
        self.mapping_ = {}

        groups = X.groupby(self.group_ids).groups
        for i, group_id in enumerate(groups):
            pandas_ct = PandasColumnTransformer(self.transformers)
            group = loc_group(X, self.group_ids, group_id)
            pandas_ct.fit(group)
            self.mapping_[group_id] = pandas_ct

        self.pandas_column_transformer_ = next(iter(self.mapping_.values()))
        return self

    def transform(self, X):
        """Transforms every group in X using its corresponding
        :class:`ColumnTransformer`.

        Parameters
        ----------
        X : pd.DataFrame
            Dataframe having __init__ ``group_ids`` column(s).

        Returns
        -------
        X_out : pd.DataFrame.
            Transformed dataframe
        """
        check_is_fitted(self)
        check_group_ids(X, self.group_ids)

        transformed_dataframes = []
        for group_id, column_transformer in self.mapping_.items():
            group = loc_group(X, self.group_ids, group_id)
            if not group.empty:
                transformed_group = column_transformer.transform(group)
                transformed_dataframes.append(transformed_group)

        return pd.concat(transformed_dataframes).reset_index(drop=True)

    def inverse_transform(self, X):
        """Inverse transformation.

        Notes
        -----
        Transformed columns whose corresponding transformer does not have
        implemented an :meth:`inverse_transform` method will not appear after
        calling this inverse transformation. This causes that the resulting
        DataFrame ``X_out`` might not be equal to the original X, that is, the
        expression X = f-1(f(X)) wont be satisfied.

        Parameters
        ----------
        X : pd.DataFrame
            Dataframe to be inverse transformed.

        Returns
        -------
        X_inv : pd.DataFrame
            Inverse transformed dataframe
        """
        check_is_fitted(self)
        check_group_ids(X, self.group_ids)

        inverse_transforms = []
        for group_id, pandas_column_transformer in self.mapping_.items():
            group = loc_group(X, self.group_ids, group_id)
            if not group.empty:
                inv = pandas_column_transformer.inverse_transform(group)
                inverse_transforms.append(inv)

        return pd.concat(inverse_transforms)

    def iter(self, fitted=True, replace_strings=False,
             column_as_strings=True):
        return self.pandas_column_transformer_.iter(
            fitted, replace_strings, column_as_strings)

    @property
    def feature_names_in_(self):
        return self.pandas_column_transformer_ \
            .column_transformer_ \
            .feature_names_in_

    def get_feature_names_out(self, input_features=None):
        return self.pandas_column_transformer_ \
            .column_transformer_ \
            .get_feature_names_out(input_features)
