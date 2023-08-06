from more_polars.more_polars import col 
import polars as pl
from composable import pipeable
from composable.strict import map
from composable.string import join

__all__ = ['contains', 'startswith', 'endswith', 'from_', 'to', 'between']


def contains(substr: str, cols) -> pl.Expr:
    ''' Creates an Expr for select all columns containing substr.
    
    Args:
        - substr: Pattern contained in some/all column names

    Returns: A pl.col expression to be used in the select method to return all
            columns with names containing substr.
    '''
    return pl.col('^.*' + substr + '.*$')


def startswith(substr: str, cols = None) -> pl.Expr:
    ''' Creates an list of columns or Expr for select all columns starting with substr.
    
    Args:
        - substr: Pattern at the start of some/all column names

    Returns: A pl.col expression to be used in the select method to return all
            columns with names starting with substr.
    '''
    return pl.col('^' + substr + '.*$')


def endswith(substr: str, cols=None) -> pl.Expr:
    ''' Creates an Expr for select all columns ending with substr.
    
    Args:
        - substr: Pattern at the end of some/all column names

    Returns: A pl.col expression to be used in the select method to return all
            columns with names ending with substr.
    '''
    return pl.col('^.*' + substr + '$')


@pipeable
def _make_reg_ex(s):
    return '^' + s + '$'


@pipeable
def _make_col_expr(cols):
    return cols >> map(_make_reg_ex) >> join('|') >> col


@pipeable
def from_(first_col, cols):
    ''' Creates an Expr to select all columns starting with and following `first_col`
    
    Args:
        - first_col: Column label (str) to start selection  

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
    return cols[start_idx:] >> _make_col_expr


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
    return cols[:end_idx+1] >> _make_col_expr


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
        return cols[start_idx:end_idx+1] >> _make_col_expr

    else:
        return cols[start_idx+1:end_idx] >> _make_col_expr