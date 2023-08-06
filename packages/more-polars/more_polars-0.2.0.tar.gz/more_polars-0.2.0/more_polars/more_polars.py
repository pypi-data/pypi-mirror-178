from composable import pipeable
import polars as pl

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
