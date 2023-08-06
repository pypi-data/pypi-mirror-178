from typing import List, Union, Dict

import inspect
import itertools
import pandas
import pandas as pd
import pandera.dtypes
from pandera.schema_components import Index, MultiIndex, Column
from pandas import DataFrame, Series
from typing import Union, Any
from typing_extensions import TypeAlias
from typing import get_origin
from constellate.thirdparty.pandas.validation.validation import (
    PanderaSchema,
    pandera_schema_from_pydantic_schema,
)


def fillnone(df: DataFrame = None, column_names: List[str] = None) -> None:
    """Convert pandas.NA into None

    :param df: DataFrame:  (Default value = None)
    :param column_names: List[str]:  (Default value = None)

    """

    def _to_none(x):
        return None if isinstance(x, type(pandas.NA)) else x

    for col_name in column_names:
        # Turn nan/NaN/NAType into None
        # pandas v1.3.4: Works
        # pandas v1.4.0: Not Works
        # chunk[col_name] = chunk[col_name].replace({pandas.NA, None})

        # pandas v1.3.4: Untested
        # pandas v1.4.0: Works
        df[col_name] = df[col_name].apply(_to_none)


PandasData: TypeAlias = Union[DataFrame, Series]


def fill_nan_from_schema(
        schema: [PanderaSchema] = None, data: PandasData = None
) -> PandasData:
    """Convert None into NaN or equivalent

    :param schema: [PanderaSchema]:  (Default value = None)
    :param data: Union[DataFrame,Series]:  (Default value = None)

    """

    def _apply_dtype_dataframe(data: pd.DataFrame = None, col_name: str = None, dtype: Any = None) -> pd.DataFrame:
        data[col_name] = data[col_name].astype(col_type.type)
        return data

    def _apply_dtype_series(data: pd.Series = None, col_name: str = None, dtype: Any = None) -> pd.Series:
        data = data.astype(col_type.type)
        return data

    def _apply_dtype(data: PandasData = None, col_name: str = None, dtype: Any = None) -> PandasData:
        if isinstance(data, pd.DataFrame):
            return _apply_dtype_dataframe(data=data, col_name=col_name, dtype=dtype)
        elif isinstance(data, pd.Series):
            return _apply_dtype_series(data=data, col_name=col_name, dtype=dtype)
        else:
            raise NotImplementedError()

    def _to_numeric(data: PandasData = None, col_name: str = None) -> PandasData:
        if isinstance(data, pd.DataFrame):
            data[col_name] = pandas.to_numeric(data[col_name], errors="coerce", downcast=None)
            return data
        elif isinstance(data, pd.Series):
            data = pandas.to_numeric(data, errors="coerce", downcast=None)
            return data
        else:
            raise NotImplementedError()

    def _to_datetime(data: PandasData = None, col_name: str = None) -> PandasData:
        if isinstance(data, pd.DataFrame):
            data[col_name] = pandas.to_datetime(data[col_name], errors="coerce")
            return data
        elif isinstance(data, pd.Series):
            data = pandas.to_datetime(data, errors="coerce")
            return data
        else:
            raise NotImplementedError()

    def _to_timedelta(data: PandasData = None, col_name: str = None) -> PandasData:
        if isinstance(data, pd.DataFrame):
            data[col_name] = pandas.to_timedelta(data[col_name], errors="coerce")
            return data
        elif isinstance(data, pd.Series):
            data = pandas.to_timedelta(data, errors="coerce")
            return data
        else:
            raise NotImplementedError()

    schema2 = pandera_schema_from_pydantic_schema(schema=schema)

    #
    # Fill indexes, if any
    #
    index = schema2.index
    multi_indexed = isinstance(index, MultiIndex)

    # Get index names
    indexes = dict()
    if index is not None:
        if multi_indexed:
            indexes = index.columns
        else:
            if index.name is not None :
                indexes = index.name
            else:
                indexes = next(iter(get_index_columns(schema=schema)), Column(dtype=index.dtype))

    # Fill column based on type
    for col_name, col_info in itertools.chain(indexes.items(), schema2.columns.items()):
        col_type = col_info.dtype

        if pandera.dtypes.is_float(col_type):
            data = _to_numeric(data=data, col_name=col_name)
            # accepts pandas.NA since pandas v1.0.0
            data = _apply_dtype(data=data, col_name=col_name, dtype=col_type.type)
        elif pandera.dtypes.is_int(col_type):
            data = _to_numeric(data=data, col_name=col_name)
            # accepts pandas.NA since pandas v1.0.0
            data = _apply_dtype(data=data, col_name=col_name, dtype=col_type.type)
        elif pandera.dtypes.is_uint(col_type):
            data = _to_numeric(data=data, col_name=col_name)
            # accepts pandas.NA since pandas v1.0.0
            data = _apply_dtype(data=data, col_name=col_name, dtype=col_type.type)
        elif pandera.dtypes.is_bool(col_type):
            # accepts pandas.NA since pandas v1.0.0
            data = _apply_dtype(data=data, col_name=col_name, dtype=col_type.type)
        elif pandera.dtypes.is_string(col_type):
            # accepts pandas.NA since pandas v1.0.0
            data = _apply_dtype(data=data, col_name=col_name, dtype=col_type.type)
        elif pandera.dtypes.is_datetime(col_type):
            data = _to_datetime(data=data, col_name=col_name)
            data = _apply_dtype(data=data, col_name=col_name, dtype=col_type.type)
        elif pandera.dtypes.is_timedelta(col_type):
            data = _to_timedelta(data=data, col_name=col_name)
            data = _apply_dtype(data=data, col_name=col_name, dtype=col_type.type)

    return data

def enum_to_value(data: Union[DataFrame, Series] = None, dtypes: Dict = {}) -> None:
    _enum_value = lambda e: e.value
    for col_name in list(data.columns):
        if col_name not in dtypes:
            continue

        data[col_name] = data[col_name].apply(_enum_value)


def get_index_columns(schema: PanderaSchema = None) -> List[str]:
    schema2 = pandera_schema_from_pydantic_schema(schema=schema)
    if isinstance(schema2.index, pandera.schema_components.MultiIndex):
        return list(schema2.index.columns.keys())
    elif isinstance(schema2.index, pandera.schema_components.Index):
        annotations = next(iter(filter(lambda m: m[0] == '__annotations__', inspect.getmembers(schema))), ('__annotations__', {}))[1]
        index_name = next(iter([k for k, v in annotations.items() if get_origin(v) == pandera.typing.pandas.Index]), None)
        return [index_name]
    raise NotImplementedError()
