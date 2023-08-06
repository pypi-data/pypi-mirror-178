from composable import pipeable
import polars as pl
from functools import reduce
from typing import Union, Optional

__all__ = ('get_dtype_dict', 'col', 'recode')

@pipeable
def get_dtype_dict(df):
    ''' Construct a `dict` of column name, dtype pairs.
    
        **Note.** Useful when defining/changing the schema.
        
        Args:
            df - A polars.Dataframe
        
        Returns: A dict of column names: str, and polars.dataypes
    '''
    return  dict(zip(df.columns, df.dtypes))


@pipeable
def col(s: str) -> pl.Expr:
    ''' Pipeable function for creating polars column expressions.
    
    Args:
        - s: A column label
             Can be a regular expression starting with ^ and ending with $
    Returns: A polars column expression.
    '''
    return pl.col(s)

@pipeable
def recode(d: dict[str], col: Union[str, pl.Expr], *, default: Optional[str] = None) -> pl.Expr:
    ''' Create a column expression to recode all labels using the dict d

    Args:
        - d: A translation dictionary with key,value pairs of the form old_lbl, new_lbl
        - col: The name of a column or a column expression
        - default: An optional default value.
    '''
    items = list(d.items())
    if isinstance(col, str):
        col = pl.col(col)
    update_when = lambda acc, tup: acc.when(col == tup[0]).then(tup[1])
    e = reduce(update_when, items, pl)
    if default:
        e = e.otherwise(default)
    return e
