from more_polars.more_polars import col 
import polars as pl
from composable import pipeable
from composable.strict import map
from composable.string import join
from operator import add
from functools import reduce

__all__ = ['contains', 'startswith', 'endswith', 'from_', 'to', 'between']


@pipeable
def remove_duplicates(cols, *, sort=True, key=None, reverse=False):
    ''' Removes duplicate column names from a list of column names.

    Args:
        - Cols: A list of column names (str)
        - sort: Whether or not the results are sorted
        - key: A custom key function used to determine order.
        - reverse: Whether the results are in descending order

    Returns: A list of unique column names, sorted by default.
    '''
    unique_cols = list({c for c in cols})
    if sort:
        return sorted(unique_cols, key=key, reverse=reverse)
    else:
        return unique_cols


@pipeable
def keep_if(funcs, cols, *, sort=True, key=None, reverse=False):
    ''' Apply each column helper and return the unique list of resulting columns.

    Args:
        - funcs: A list of column helper pipeable functions
        - sort: Whether or not the results are sorted
        - key: A custom key function used to determine order.
        - reverse: Whether the results are in descending order

    Returns: A list of unique column names, sorted by default.
    >>> import polars as pl
    >>> df = pl.DataFrame({l + str(i):range(3) for l in ['a', 'b', 'c'] for i in range(2)}) 
    >>> df
    shape: (3, 6)
    ┌─────┬─────┬─────┬─────┬─────┬─────┐
    │ a0  ┆ a1  ┆ b0  ┆ b1  ┆ c0  ┆ c1  │
    │ --- ┆ --- ┆ --- ┆ --- ┆ --- ┆ --- │
    │ i64 ┆ i64 ┆ i64 ┆ i64 ┆ i64 ┆ i64 │
    ╞═════╪═════╪═════╪═════╪═════╪═════╡
    │ 0   ┆ 0   ┆ 0   ┆ 0   ┆ 0   ┆ 0   │
    ├╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┤
    │ 1   ┆ 1   ┆ 1   ┆ 1   ┆ 1   ┆ 1   │
    ├╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┤
    │ 2   ┆ 2   ┆ 2   ┆ 2   ┆ 2   ┆ 2   │
    └─────┴─────┴─────┴─────┴─────┴─────┘
    >>> from more_polars import cols
    >>> df.columns >> cols.keep_if([cols.startswith('a'), cols.endswith('1')])
    ['a0', 'a1', 'b1', 'c1']
    '''
    combined_results = [c for f in funcs for c in f(cols)]
    return  remove_duplicates(combined_results,sort=sort, key=key, reverse=reverse)


@pipeable
def contains(substr: str, cols) -> pl.Expr:
    ''' Creates an list of column names for select all columns containing substr.
    
    Args:
        - substr: Pattern contained in some/all column names

    Returns: A list of column names to be used in the select method to return all
            columns with names containing substr.
    '''
    return [c for c in cols if substr in c]


@pipeable
def startswith(substr: str, cols) -> pl.Expr:
    ''' Creates an list of columns for select all columns starting with substr.
    
    Args:
        - substr: Pattern at the start of some/all column names

    Returns: A list of columns names to be used in the select method to return all
            columns with names starting with substr.
    '''
    return [c for c in cols if c.startswith(substr)]


@pipeable
def endswith(substr: str, cols) -> pl.Expr:
    ''' Creates a list of column names for select all columns ending with substr.
    
    Args:
        - substr: Pattern at the end of some/all column names

    Returns: A pl.col expression to be used in the select method to return all
            columns with names ending with substr.
    '''
    return [c for c in cols if c.endswith(substr)]


@pipeable
def from_(first_col, cols):
    ''' Creates list of column names to select all columns starting with and following `first_col`
    
    Args:
        - first_col: Column label (str) to start selection  

    Returns: A list of column names for use in the select or drop methods

    Example:

    >>> import polars as pl
    >>> import more_polars.column_helpers as cols
    >>> df = pl.DataFrame({'c' + str(i):range(3) for i in range(5)}) 
    >>> df
    shape: (3, 5)
    ┌─────┬─────┬─────┬─────┬─────┐
    │ c0  ┆ c1  ┆ c2  ┆ c3  ┆ c4  │
    │ --- ┆ --- ┆ --- ┆ --- ┆ --- │
    │ i64 ┆ i64 ┆ i64 ┆ i64 ┆ i64 │
    ╞═════╪═════╪═════╪═════╪═════╡
    │ 0   ┆ 0   ┆ 0   ┆ 0   ┆ 0   │
    ├╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┤
    │ 1   ┆ 1   ┆ 1   ┆ 1   ┆ 1   │
    ├╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┤
    │ 2   ┆ 2   ┆ 2   ┆ 2   ┆ 2   │
    └─────┴─────┴─────┴─────┴─────┘
    >>> df.select(df.columns >> cols.from_('c2'))
    shape: (3, 3)
    ┌─────┬─────┬─────┐
    │ c2  ┆ c3  ┆ c4  │
    │ --- ┆ --- ┆ --- │
    │ i64 ┆ i64 ┆ i64 │
    ╞═════╪═════╪═════╡
    │ 0   ┆ 0   ┆ 0   │
    ├╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┤
    │ 1   ┆ 1   ┆ 1   │
    ├╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┤
    │ 2   ┆ 2   ┆ 2   │
    └─────┴─────┴─────┘
    '''
    start_idx = cols.index(first_col)
    return cols[start_idx:]


@pipeable
def to(last_col, cols):
    ''' Creates an Expr to select all columns from the first until `end_col`
    
    Args:
        - last_col: Column label (str) to end selection  

    Returns: A pl.col expression for use in the select or drop methods

    Example:

    >>> import polars as pl
    >>> import more_polars.column_helpers as cols
    >>> df = pl.DataFrame({'c' + str(i):range(3) for i in range(5)}) 
    >>> df
    shape: (3, 5)
    ┌─────┬─────┬─────┬─────┬─────┐
    │ c0  ┆ c1  ┆ c2  ┆ c3  ┆ c4  │
    │ --- ┆ --- ┆ --- ┆ --- ┆ --- │
    │ i64 ┆ i64 ┆ i64 ┆ i64 ┆ i64 │
    ╞═════╪═════╪═════╪═════╪═════╡
    │ 0   ┆ 0   ┆ 0   ┆ 0   ┆ 0   │
    ├╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┤
    │ 1   ┆ 1   ┆ 1   ┆ 1   ┆ 1   │
    ├╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┤
    │ 2   ┆ 2   ┆ 2   ┆ 2   ┆ 2   │
    └─────┴─────┴─────┴─────┴─────┘
    >>> df.select(df.columns >> cols.to('c2'))
    shape: (3, 3)
    ┌─────┬─────┬─────┐
    │ c0  ┆ c1  ┆ c2  │
    │ --- ┆ --- ┆ --- │
    │ i64 ┆ i64 ┆ i64 │
    ╞═════╪═════╪═════╡
    │ 0   ┆ 0   ┆ 0   │
    ├╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┤
    │ 1   ┆ 1   ┆ 1   │
    ├╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┤
    │ 2   ┆ 2   ┆ 2   │
    └─────┴─────┴─────┘
    '''
    end_idx = cols.index(last_col)
    return cols[:end_idx+1]


@pipeable
def between(first_col, last_col, cols, *, inclusive=True):
    ''' Creates an Expr to select all columns from the `first_col` until `last_col`
    
    Args:
        - last_col: Column label (str) to end selection  
        - inclusive: whether or not the bounding columns are included

    Returns: A pl.col expression for use in the select or drop methods
    
    Example:

    >>> import polars as pl
    >>> import more_polars.column_helpers as cols
    >>> df = pl.DataFrame({'c' + str(i):range(3) for i in range(5)}) 
    >>> df
    shape: (3, 5)
    ┌─────┬─────┬─────┬─────┬─────┐
    │ c0  ┆ c1  ┆ c2  ┆ c3  ┆ c4  │
    │ --- ┆ --- ┆ --- ┆ --- ┆ --- │
    │ i64 ┆ i64 ┆ i64 ┆ i64 ┆ i64 │
    ╞═════╪═════╪═════╪═════╪═════╡
    │ 0   ┆ 0   ┆ 0   ┆ 0   ┆ 0   │
    ├╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┤
    │ 1   ┆ 1   ┆ 1   ┆ 1   ┆ 1   │
    ├╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┼╌╌╌╌╌┤
    │ 2   ┆ 2   ┆ 2   ┆ 2   ┆ 2   │
    └─────┴─────┴─────┴─────┴─────┘
    >>> df.select(df.columns >> cols.between('c2', 'c3'))
    shape: (3, 2)
    ┌─────┬─────┐
    │ c2  ┆ c3  │
    │ --- ┆ --- │
    │ i64 ┆ i64 │
    ╞═════╪═════╡
    │ 0   ┆ 0   │
    ├╌╌╌╌╌┼╌╌╌╌╌┤
    │ 1   ┆ 1   │
    ├╌╌╌╌╌┼╌╌╌╌╌┤
    │ 2   ┆ 2   │
    └─────┴─────┘
    '''
    start_idx = cols.index(first_col)
    end_idx = cols.index(last_col)
    assert start_idx <= end_idx, 'End column must follow the start column'
    if inclusive:
        return cols[start_idx:end_idx+1]

    else:
        return cols[start_idx+1:end_idx]