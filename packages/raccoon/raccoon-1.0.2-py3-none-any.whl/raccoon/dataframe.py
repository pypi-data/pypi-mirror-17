"""
DataFrame class
"""

from itertools import compress
from collections import OrderedDict, namedtuple
from tabulate import tabulate
from blist import blist


class DataFrame(object):
    """
    DataFrame class. The raccoon DataFrame implements a simplified version of the pandas DataFrame with the key
    objective difference that the raccoon DataFrame is meant for use cases where the size of the DataFrame rows is
    expanding frequently. This is known to be slow with Pandas due to the use of numpy as the underlying data structure.
    Raccoon uses BList as the underlying data structure which is quick to expand and grow the size.
    """
    def __init__(self, data=None, columns=None, index=None, index_name='index', use_blist=True):
        """
        :param data: (optional) dictionary of lists. The keys of the dictionary will be used for the column names and\
        the lists will be used for the column data.
        :param columns: (optional) list of column names that will define the order
        :param index: (optional) list of index values. If None then the index will be integers starting with zero
        :param index_name: (optional) name for the index. Default is "index"
        :param use_blist: if True then use blist() as the underlying data structure, if False use standard list()
        """
        # quality checks
        if (index is not None) and (not isinstance(index, (list, blist))):
            raise TypeError('index must be a list.')
        if (columns is not None) and (not isinstance(columns, (list, blist))):
            raise TypeError('columns must be a list.')

        # standard variable setup
        self._index = None
        self._index_name = index_name
        self._columns = None
        self._blist = use_blist

        # define from dictionary
        if data is None:
            self._data = blist() if self._blist else list()
            if columns:
                # expand to the number of columns
                self._data = blist([blist() for x in range(len(columns))]) if self._blist \
                    else [[] for x in range(len(columns))]
                self.columns = blist(columns)
            else:
                self.columns = blist()
            if index:
                if not columns:
                    raise ValueError('cannot initialize with index but no columns')
                # pad out to the number of rows
                self._pad_data(max_len=len(index))
                self.index = blist(index)
            else:
                self.index = blist()
        elif isinstance(data, dict):
            # set data from dict values. If dict value is not a list, wrap it to make a single element list
            self._data = blist([blist(x) if isinstance(x, (list, blist)) else blist([x]) for x in data.values()]) if \
                self._blist else \
                [x if isinstance(x, (list, blist)) else [x] for x in data.values()]
            # setup columns from directory keys
            self.columns = blist(data.keys())
            # pad the data
            self._pad_data()
            # setup index
            if index:
                self.index = blist(index)
            else:
                self.index = blist(range(len(self._data[0])))

        # sort by columns if provided
        if columns:
            self._sort_columns(columns)

    def __repr__(self):
        return 'object id: %s\ncolumns:\n%s\ndata:\n%s\nindex:\n%s\n' % (id(self), self._columns,
                                                                         self._data, self._index)

    def __str__(self):
        return self._make_table()

    def _make_table(self, index=True, **kwargs):
        kwargs['headers'] = 'keys' if 'headers' not in kwargs.keys() else kwargs['headers']
        return tabulate(self.to_dict(ordered=True, index=index), **kwargs)

    def print(self, index=True, **kwargs):
        """
        Print the contents of the DataFrame. This method uses the tabulate function from the tabulate package. Use the
        kwargs to pass along any arguments to the tabulate function.

        :param index: If True then include the indexes as a column in the output, if False ignore the index
        :param kwargs: Parameters to pass along to the tabulate function
        :return: output of the tabulate function
        """
        print(self._make_table(index=index, **kwargs))

    def _sort_columns(self, columns_list):
        """
        Given a list of column names will sort the DataFrame columns to match the given order

        :param columns_list: list of column names. Must include all column names
        :return: nothing
        """
        if not (all([x in columns_list for x in self._columns]) and all([x in self._columns for x in columns_list])):
            raise ValueError(
                'columns_list must be all in current columns, and all current columns must be in columns_list')
        new_sort = [self._columns.index(x) for x in columns_list]
        self._data = blist([self._data[x] for x in new_sort]) if self._blist else [self._data[x] for x in new_sort]
        self._columns = blist([self._columns[x] for x in new_sort])

    def _pad_data(self, max_len=None):
        """
        Pad the data in DataFrame with [None} to ensure that all columns have the same length.

        :param max_len: If provided will extend all columns to this length, if not then will use the longest column
        :return: nothing
        """
        if not max_len:
            max_len = max([len(x) for x in self._data])
        for i, col in enumerate(self._data):
            col.extend([None] * (max_len - len(col)))

    def __len__(self):
        return len(self._index)

    @property
    def data(self):
        return self._data.copy()

    @property
    def columns(self):
        return self._columns.copy()

    @columns.setter
    def columns(self, columns_list):
        self._validate_columns(columns_list)
        self._columns = blist(columns_list)

    @property
    def index(self):
        return self._index.copy()

    @index.setter
    def index(self, index_list):
        self._validate_index(index_list)
        self._index = blist(index_list)

    @property
    def index_name(self):
        return self._index_name

    @index_name.setter
    def index_name(self, name):
        self._index_name = name

    def select_index(self, compare, result='boolean'):
        """
        Finds the elements in the index that match the compare parameter and returns either a list of the values that
        match, of a boolean list the length of the index with True to each index that matches. If the indexes are
        tuples then the compare is a tuple where None in any field of the tuple will be treated as "*" and match all
        values.

        :param compare: value to compare as a singleton or tuple
        :param result: 'boolean' = returns a list of booleans, 'value' = returns a list of index values that match
        :return: list of booleans or values
        """
        if isinstance(compare, tuple):
            # this crazy list comprehension will match all the tuples in the list with None being an * wildcard
            booleans = [all([(compare[i] == w if compare[i] is not None else True) for i, w in enumerate(v)]) for x, v in
                        enumerate(self._index)]
        else:
            booleans = [False] * len(self._index)
            booleans[self._index.index(compare)] = True
        if result == 'boolean':
            return booleans
        elif result == 'value':
            return list(compress(self._index, booleans))
        else:
            raise ValueError('only valid values for result parameter are: boolean or value.')

    def get(self, indexes=None, columns=None, as_list=False):
        """
        Given indexes and columns will return a sub-set of the DataFrame. This method will direct to the below methods
        based on what types are passed in for the indexes and columns. The type of the return is determined by the
        types of the parameters.

        :param indexes: index value, list of index values, or a list of booleans. If None then all indexes are used
        :param columns: column name or list of column names. If None then all columns are used
        :param as_list: if True then return the values as a list, if False return a DataFrame. This is only used if\
        the get is for a single column
        :return: either DataFrame, list or single value. The return is a shallow copy
        """
        if indexes is None:
            indexes = [True] * len(self._index)
        if columns is None:
            columns = [True] * len(self._columns)
        # singe index and column
        if isinstance(indexes, (list, blist)) and isinstance(columns, (list, blist)):
            return self.get_matrix(indexes, columns)
        elif isinstance(indexes, (list, blist)) and (not isinstance(columns, (list, blist))):
            return self.get_rows(indexes, columns, as_list)
        elif (not isinstance(indexes, (list, blist))) and isinstance(columns, (list, blist)):
            return self.get_columns(indexes, columns)
        else:
            return self.get_cell(indexes, columns)

    def get_cell(self, index, column):
        """
        For a single index and column value return the value of the cell

        :param index: index value
        :param column: column name
        :return: value
        """
        i = self._index.index(index)
        c = self._columns.index(column)
        return self._data[c][i]

    def get_rows(self, indexes, column, as_list=False):
        """
        For a list of indexes and a single column name return the values of the indexes in that column.

        :param indexes: either a list of index values or a list of booleans with same length as all indexes
        :param column: single column name
        :param as_list: if True return a list, if False return DataFrame
        :return: DataFrame is as_list if False, a list if as_list is True
        """
        if len(indexes) != (indexes.count(True) + indexes.count(False)):  # index list
            bool_indexes = [False] * len(self._index)
            for i in indexes:
                bool_indexes[self._index.index(i)] = True
            indexes = bool_indexes
        c = self._columns.index(column)
        if all(indexes):  # the entire column
            data = self._data[c]
            index = self._index
        else:
            data = list(compress(self._data[c], indexes))
            index = list(compress(self._index, indexes))
        return data if as_list else DataFrame(data={column: data}, index=index, index_name=self._index_name)

    def get_columns(self, index, columns):
        """
        For a single index and list of column names return a DataFrame of the values in that index

        :param index: single index value
        :param columns: list of column names
        :return: DataFrame
        """
        data = dict()
        if len(columns) == (columns.count(True) + columns.count(False)):
            columns = list(compress(self._columns, columns))
        i = self._index.index(index)
        for column in columns:
            c = self._columns.index(column)
            data[column] = [self._data[c][i]]
        return DataFrame(data=data, index=[index], columns=columns, index_name=self._index_name)

    def get_matrix(self, indexes, columns):
        """
        For a list of indexes and list of columns return a DataFrame of the values.

        :param indexes: either a list of index values or a list of booleans with same length as all indexes
        :param columns: list of column names
        :return: DataFrame
        """
        if len(indexes) == (indexes.count(True) + indexes.count(False)):  # boolean list
            i = indexes
            indexes = list(compress(self._index, indexes))
        else:  # index list
            i = [False] * len(self._index)
            for x in indexes:
                i[self._index.index(x)] = True

        if len(columns) == (columns.count(True) + columns.count(False)):  # boolean list
            c = columns
            columns = list(compress(self._columns, columns))
        else:  # name list
            c = [x in columns for x in self._columns]

        data_dict = dict()
        data = list(compress(self._data, c))
        for x, column in enumerate(columns):
            data_dict[column] = list(compress(data[x], i))

        return DataFrame(data=data_dict, index=indexes, columns=columns, index_name=self._index_name)

    def _add_row(self, index):
        """
        Add a new row to the DataFrame

        :param index: index of the new row
        :return: nothing
        """
        self._index.append(index)
        for c, col in enumerate(self._columns):
            self._data[c].append(None)

    def _add_missing_rows(self, indexes):
        """
        Given a list of indexes, find all the indexes that are not currently in the DataFrame and make a new row for
        that index

        :param indexes: list of indexes
        :return: nothing
        """
        new_indexes = [x for x in indexes if x not in self._index]
        for x in new_indexes:
            self._add_row(x)

    def _add_column(self, column):
        """
        Add a new column to the DataFrame

        :param column: column name
        :return: nothing
        """
        self._columns.append(column)
        if self._blist:
            self._data.append(blist([None] * len(self._index)))
        else:
            self._data.append([None] * len(self._index))

    def set(self, indexes=None, columns=None, values=None):
        """
        Given indexes and columns will set a sub-set of the DataFrame to the values provided. This method will direct
        to the below methods based on what types are passed in for the indexes and columns. If the indexes or columns
        contains values not in the DataFrame then new rows or columns will be added.

        :param indexes: indexes value, list of indexes values, or a list of booleans. If None then all indexes are used
        :param columns: columns name, if None then all columns are used. Currently can only handle a single column or\
        all columns
        :param values: value or list of values to set (index, column) to. If setting just a single row, then must be a\
        dict where the keys are the column names. If a list then must be the same length as the indexes parameter, if\
        indexes=None, then must be the same and length of DataFrame
        :return: nothing
        """
        if (indexes is not None) and (columns is not None):
            if isinstance(indexes, (list, blist)):
                self.set_column(indexes, columns, values)
            else:
                self.set_cell(indexes, columns, values)
        elif (indexes is not None) and (columns is None):
            self.set_row(indexes, values)
        elif (indexes is None) and (columns is not None):
            self.set_column(indexes, columns, values)
        else:
            raise ValueError('either or both of indexes or columns must be provided')

    def set_cell(self, index, column, value):
        """
        Sets the value of a single cell. If the index and/or column is not in the current index/columns then a new
        index and/or column will be created.

        :param index: index value
        :param column: column name
        :param value: value to set
        :return: nothing
        """
        try:
            i = self._index.index(index)
        except ValueError:
            i = len(self._index)
            self._add_row(index)
        try:
            c = self._columns.index(column)
        except ValueError:
            c = len(self._columns)
            self._add_column(column)
        self._data[c][i] = value

    def set_row(self, index, values):
        """
        Sets the values of the columns in a single row.

        :param index: index value
        :param values: dict with the keys as the column names and the values what to set that column to
        :return: nothing
        """
        try:
            i = self._index.index(index)
        except ValueError:  # new row
            i = len(self._index)
            self._add_row(index)
        if isinstance(values, dict):
            if not (set(values.keys()).issubset(self._columns)):
                raise ValueError('keys of values are not all in existing columns')
            for c, column in enumerate(self._columns):
                self._data[c][i] = values.get(column, self._data[c][i])
        else:
            raise TypeError('cannot handle values of this type.')

    def set_column(self, index=None, column=None, values=None):
        """
        Set a column to a single value or list of values. If any of the index values are not in the current indexes
        then a new row will be created.

        :param index: list of index values or list of booleans. If a list of booleans then the list must be the same\
        length as the DataFrame
        :param column: column name
        :param values: either a single value or a list. The list must be the same length as the index list if the index\
        list is values, or the length of the True values in the index list if the index list is booleans
        :return: nothing
        """
        try:
            c = self._columns.index(column)
        except ValueError:  # new column
            c = len(self.columns)
            self._add_column(column)
        if index:  # index was provided
            if len(index) == (index.count(True) + index.count(False)):  # boolean list
                if not isinstance(values, (list, blist)):  # single value provided, not a list, so turn values into list
                    values = [values for x in index if x]
                if len(index) != len(self._index):
                    raise ValueError('boolean index list must be same size of existing index')
                if len(values) != index.count(True):
                    raise ValueError('length of values list must equal number of True entries in index list')
                indexes = [i for i, x in enumerate(index) if x]
                for x, i in enumerate(indexes):
                    self._data[c][i] = values[x]
            else:  # list of index
                if not isinstance(values, (list, blist)):  # single value provided, not a list, so turn values into list
                    values = [values for x in index]
                if len(values) != len(index):
                    raise ValueError('length of values and index must be the same.')
                try:  # all index in current index
                    indexes = [self._index.index(x) for x in index]
                except ValueError:  # new rows need to be added
                    self._add_missing_rows(index)
                    indexes = [self._index.index(x) for x in index]
                for x, i in enumerate(indexes):
                    self._data[c][i] = values[x]
        else:  # no index, only values
            if not isinstance(values, (list, blist)):  # values not a list, turn into one of length same as index
                values = blist([values for x in self._index]) if self._blist else [values for x in self._index]
            if len(values) != len(self._index):
                raise ValueError('values list must be at same length as current index length.')
            else:
                self._data[c] = blist(values) if self._blist else values

    def _slice_index(self, slicer):
        try:
            start_index = self._index.index(slicer.start)
        except ValueError:
            raise IndexError('start of slice not in the index')
        try:
            end_index = self._index.index(slicer.stop)
        except ValueError:
            raise IndexError('end of slice not in the index')
        if end_index < start_index:
            raise IndexError('end of slice is before start of slice')

        pre_list = [False] * start_index
        mid_list = [True] * (end_index - start_index + 1)
        post_list = [False] * (len(self._index) - 1 - end_index)

        pre_list.extend(mid_list)
        pre_list.extend(post_list)
        return pre_list

    def __getitem__(self, index):
        """
        Convenience wrapper around the get() method for using df[]
        Usage...
        df['a'] -- get column
        df[['a','b',c']] -- get columns
        df[5, 'b']  -- get cell at index=5, column='b'
        df[[4, 5], 'c'] -- get indexes=[4, 5], column='b'
        df[[4, 5,], ['a', 'b']]  -- get indexes=[4, 5], columns=['a', 'b']
        can also use a boolean list for anything

        :param index: any of the parameters above
        :return: DataFrame of the subset slice
        """
        if isinstance(index, tuple):  # index and column
            indexes = self._slice_index(index[0]) if isinstance(index[0], slice) else index[0]
            return self.get(indexes=indexes, columns=index[1])
        if isinstance(index, slice):  # just a slice of index
            return self.get(indexes=self._slice_index(index))
        else:  # just the columns
            return self.get(columns=index)

    def __setitem__(self, index, value):
        """
        Convenience wrapper around the set() method for using df[] = X
        Usage...

        df[1, 'a'] -- set cell at index=1, column=a
        df[[0, 3], 'b'] -- set index=[0, 3], column=b
        df[1:2, 'b'] -- set index slice 1:2, column=b

        :param index: any of the parameter examples above
        :param value: single value or list of values
        :return: nothing
        """
        if isinstance(index, tuple):  # index and column
            indexes = self._slice_index(index[0]) if isinstance(index[0], slice) else index[0]
            return self.set(indexes=indexes, columns=index[1], values=value)
        if isinstance(index, slice):  # just a slice of index
            return self.set(indexes=self._slice_index(index), columns=None, values=value)
        else:  # just the columns
            return self.set(indexes=None, columns=index, values=value)

    def to_list(self):
        """
        For a single column DataFrame returns a list of the values. Raises error if more then one column.

        :return: list
        """
        if len(self._columns) > 1:
            raise TypeError('tolist() only works with a single column DataFrame')
        return self._data[0]

    def to_dict(self, index=True, ordered=False):
        """
        Returns a dict where the keys are the column names and the values are lists of the values for that column.

        :param index: If True then include the index in the dict with the index_name as the key
        :param ordered: If True then return an OrderedDict() to perserve the order of the columns in the DataFrame
        :return: dict or OrderedDict()
        """
        result = OrderedDict() if ordered else dict()
        if index:
            result.update({self._index_name: self._index})
        if ordered:
            data_dict = [(column, self._data[i]) for i, column in enumerate(self._columns)]
        else:
            data_dict = {column: self._data[i] for i, column in enumerate(self._columns)}
        result.update(data_dict)
        return result

    def rename_columns(self, rename_dict):
        """
        Reanmes the columns

        :param rename_dict: dict where the keys are the current column names and the values are the new names
        :return: nothing
        """
        if not all([x in self._columns for x in rename_dict.keys()]):
            raise ValueError('all dictionary keys must be in current columns')
        for current in rename_dict.keys():
            self._columns[self._columns.index(current)] = rename_dict[current]

    def head(self, rows):
        """
        Return a DataFrame of the first N rows

        :param rows: number of rows
        :return: DataFrame
        """
        rows_bool = [True] * min(rows, len(self._index))
        rows_bool.extend([False] * max(0, len(self._index) - rows))
        return self.get(indexes=rows_bool)

    def tail(self, rows):
        """
        Return a DataFrame of the last N rows

        :param rows: number of rows
        :return: DataFrame
        """
        rows_bool = [False] * max(0, len(self._index) - rows)
        rows_bool.extend([True] * min(rows, len(self._index)))
        return self.get(indexes=rows_bool)

    def delete_rows(self, indexes):
        """
        Delete rows from the DataFrame

        :param indexes: either a list of values or list of booleans for the rows to delete
        :return: nothing
        """
        indexes = [indexes] if not isinstance(indexes, (list, blist)) else indexes
        if len(indexes) == (indexes.count(True) + indexes.count(False)):  # boolean list
            if len(indexes) != len(self._index):
                raise ValueError('boolean indexes list must be same size of existing indexes')
            indexes = [i for i, x in enumerate(indexes) if x]
        else:
            indexes = [self._index.index(x) for x in indexes]
        indexes = sorted(indexes, reverse=True)  # need to sort and reverse list so deleting works
        for c, column in enumerate(self._columns):
            for i in indexes:
                del self._data[c][i]
        # now remove from index
        for i in indexes:
            del self._index[i]

    def delete_columns(self, columns):
        """
        Delete columns from the DataFrame

        :param columns: list of columns to delete
        :return: nothing
        """
        columns = [columns] if not isinstance(columns, (list, blist)) else columns
        if not all([x in self._columns for x in columns]):
            raise ValueError('all columns must be in current columns')
        for column in columns:
            c = self._columns.index(column)
            del self._data[c]
            del self._columns[c]
        if not len(self._data):  # if all the columns have been deleted, remove index
            self._index = blist()

    @staticmethod
    def _sorted_list_indexes(list_to_sort):
        return sorted(range(len(list_to_sort)), key=list_to_sort.__getitem__)

    def sort_index(self):
        """
        Sort the DataFrame by the index. The sort modifies the DataFrame inplace

        :return: nothing
        """
        sort = self._sorted_list_indexes(self._index)
        # sort index
        self._index = blist([self._index[x] for x in sort])
        # each column
        for c in range(len(self._data)):
            self._data[c] = blist([self._data[c][i] for i in sort]) if self._blist else [self._data[c][i] for i in sort]

    def sort_columns(self, column):
        """
        Sort the DataFrame by one of the columns. The sort modifies the DataFrame inplace

        :param column: column name to use for the sort
        :return: nothing
        """
        if isinstance(column, (list, blist)):
            raise TypeError('Can only sort by a single column  ')
        sort = self._sorted_list_indexes(self._data[self._columns.index(column)])
        # sort index
        self._index = blist([self._index[x] for x in sort])
        # each column
        for c in range(len(self._data)):
            self._data[c] = blist([self._data[c][i] for i in sort]) if self._blist else [self._data[c][i] for i in sort]

    def _validate_index(self, indexes):
        if len(indexes) != len(set(indexes)):
            raise ValueError('index contains duplicates')
        if self._data:
            if len(indexes) != len(self._data[0]):
                raise ValueError('index length does not match data length')

    def _validate_columns(self, columns):
        if len(columns) != len(set(columns)):
            raise ValueError('columns contains duplicates')
        if self._data:
            if len(columns) != len(self._data):
                raise ValueError('number of column names does not match number of data columns')

    def _validate_data(self):
        if self._data:
            max_rows = max([len(x) for x in self._data])
            same_lens = all([len(x) == max_rows for x in self._data])
            if not same_lens:
                raise ValueError('data is corrupted, each column not all same length')

    def validate_integrity(self):
        """
        Validate the integrity of the DataFrame. This checks that the indexes, column names and internal data are not
        corrupted. Will raise an error if there is a problem.

        :return: nothing
        """
        self._validate_columns(self._columns)
        self._validate_index(self._index)
        self._validate_data()

    def append(self, data_frame):
        """
        Append another DataFrame to this DataFrame. If the new data_frame has columns that are not in the current
        DataFrame then new columns will be created. All of the indexes in the data_frame must be different from the
        current indexes or will raise an error.

        :param data_frame: DataFrame to append
        :return: nothing
        """
        combined_index = self._index + data_frame.index
        if len(set(combined_index)) != len(combined_index):
            raise ValueError('duplicate indexes in DataFrames')

        for c, column in enumerate(data_frame.columns):
            self.set(indexes=data_frame.index, columns=column, values=data_frame.data[c].copy())

    def equality(self, column, indexes=None, value=None):
        """
        Math helper method. Given a column and optional indexes will return a list of booleans on the equality of the
        value for that index in the DataFrame to the value parameter.

        :param column: column name to compare
        :param indexes: list of index values or list of booleans. If a list of booleans then the list must be the same\
        length as the DataFrame
        :param value: value to compare
        :return: list of booleans
        """
        indexes = [] if indexes is None else indexes
        compare_list = self.get_rows(indexes, column, as_list=True)
        return [x == value for x in compare_list]

    def _get_lists(self, left_column, right_column, indexes):
        indexes = [] if indexes is None else indexes
        left_list = self.get_rows(indexes, left_column, as_list=True)
        right_list = self.get_rows(indexes, right_column, as_list=True)
        return left_list, right_list

    def add(self, left_column, right_column, indexes=None):
        """
        Math helper method that adds element-wise two columns. If indexes are not None then will only perform the math
        on that sub-set of the columns.

        :param left_column: first column name
        :param right_column: second column name
        :param indexes: list of index values or list of booleans. If a list of booleans then the list must be the same\
        length as the DataFrame
        :return: list
        """
        left_list, right_list = self._get_lists(left_column, right_column, indexes)
        return [l + r for l, r in zip(left_list, right_list)]

    def subtract(self, left_column, right_column, indexes=None):
        """
        Math helper method that subtracts element-wise two columns. If indexes are not None then will only perform the
        math on that sub-set of the columns.

        :param left_column: first column name
        :param right_column: name of column to subtract from the left_column
        :param indexes: list of index values or list of booleans. If a list of booleans then the list must be the same\
        length as the DataFrame
        :return: list
        """
        left_list, right_list = self._get_lists(left_column, right_column, indexes)
        return [l - r for l, r in zip(left_list, right_list)]

    def multiply(self, left_column, right_column, indexes=None):
        """
        Math helper method that multiplies element-wise two columns. If indexes are not None then will only perform the
        math on that sub-set of the columns.

        :param left_column: first column name
        :param right_column: second column name
        :param indexes: list of index values or list of booleans. If a list of booleans then the list must be the same\
        length as the DataFrame
        :return: list
        """
        left_list, right_list = self._get_lists(left_column, right_column, indexes)
        return [l * r for l, r in zip(left_list, right_list)]

    def divide(self, left_column, right_column, indexes=None):
        """
        Math helper method that divides element-wise two columns. If indexes are not None then will only perform the
        math on that sub-set of the columns.

        :param left_column: column name of dividend
        :param right_column: column name of divisor
        :param indexes: list of index values or list of booleans. If a list of booleans then the list must be the same\
        length as the DataFrame
        :return: list
        """
        left_list, right_list = self._get_lists(left_column, right_column, indexes)
        return [l / r for l, r in zip(left_list, right_list)]

    def isin(self, column, compare_list):
        """
        Returns a boolean list where each elements is whether that element in the column is in the compare_list.

        :param column: single column name, does not work for multiple columns
        :param compare_list: list of items to compare to
        :return: list of booleans
        """
        return [x in compare_list for x in self._data[self._columns.index(column)]]

    def iterrows(self):
        """
        Iterates over DataFrame rows as dictionary of the values. The index will be included.

        :return: dictionary
        """
        for i in range(len(self._index)):
            row = {self._index_name: self._index[i]}
            for c, col in enumerate(self._columns):
                row[col] = self._data[c][i]
            yield row

    def itertuples(self, name='Raccoon'):
        """
        Iterates over DataFrame rows as tuple of the values.

        :param name: name of the namedtuple
        :return: namedtuple
        """
        fields = [self._index_name]
        fields.extend(self._columns)
        row_tuple = namedtuple(name, fields)
        for i in range(len(self._index)):
            row = {self._index_name: self._index[i]}
            for c, col in enumerate(self._columns):
                row[col] = self._data[c][i]
            yield row_tuple(**row)
