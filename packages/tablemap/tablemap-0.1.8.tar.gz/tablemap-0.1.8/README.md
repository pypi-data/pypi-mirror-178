# About

'tablemap' is a handy little Python data wrangling tool for whom Pandas or SQL feel clunky when problems
touch just one small step further than their routine, ordinary circle.

When a table is simply a list of dictionaries, often times Pandas looks like a long way around. 
It can wait till it's really required.

Some people might be happy if only they can easily chain up some processes they do on tables 
without worrying too much about the memory. Less on stackoverflow.com for arcane pandas spells. This is for those. 

# Installation

Requires only built-in Python libraries.

```
pip install tablemap
```


# Tutorial

## Create a table in the database

Let's create a table 't1' in 'sample.db'. 

```python
from tablemap import Conn

t1 = [
    {'col1': 'a', 'col2': 4},
    {'col1': 'a', 'col2': 5},
    {'col1': 'b', 'col2': 1},
]

conn = Conn('sample.db')
conn['t1'] = t1
```

The right hand side of the assignment can be a list of dictionaries, an iterator that yields dictionaries or an object fetched from the connection, for example, conn['t1'] on which you can chain up some methods such as 'map', 'by', 'merge' and 'concat'

Each dictionary represents a row in a table. For instance {'col1': a, 'col2': 4} is a row with two columns, col1 and col2.

To browse the table,

```python
print(conn['t1'].list())

# or if you want to save some memory,
for r in conn['t1'].iter():
    print(r)
```

If you prefer GUI, you can open up the file 'sample.db' with softwares like [SQLiteStudio](https://sqlitestudio.pl/) or [DB Browser for SQLite](https://sqlitebrowser.org/). 

## map

We'd like to filter rows with col2 > 2 and add 1 to col2 for some reason.

```python
def add1(r):
    if r['col2'] > 2:
        r['col2'] += 1
        return r

conn['t1_1'] = conn['t1'].map(add1)
```

The argument for map is a dictionary-yielding generator or an ordinary function that
returns a dictionary, a list of dictionaries, or None. It takes a single dictionary as an argument 
or a list of dictionaries (multiple rows) when the previous process is 'by'.

## by

To sort and group t1 by 'col1' before summing up 'col2',

```python
def sumup(rs):
    r0 = rs[0]
    r0['col2_sum'] = sum(r['col2'] for r in rs)
    del r0['col2']
    return r0

conn['t1_col2sum_groupby_col1'] = conn['t1'].by('col1')\
    .map(sumup)
```

'by' takes columns as arguments (multiple args for multiple columns) for grouping
and the next process (map in this case) takes on each group (a list of dictionaries).

## merge

To merge t1 and t2 below by col1

```python
t2 = [
    {'col1': 'd', 'col3': 3},
    {'col1': 'b', 'col3': 1},
    {'col1': 'b', 'col3': 4},
]

conn['t2'] = t2

def append_col3(rs1, rs2):
    # inner join, neither rs1 nor rs2 are []
    if rs1 and rs2:
        for r1 in rs1:
            for r2 in rs2:
                r1['col3'] = r2['col3']
                yield r1
    # left join, rs2 is an empty list, []
    elif rs1 and not rs2:
        for r1 in rs1:
            r1['col3'] = None
            yield r1
    # right join, rs1 is an empty list, []
    elif not rs1 and rs2:
        for r2 in rs2:
            # no need to worrry about the order of columns in the dictionary, 
            # as long as they have the same columns (keys)
            r2['col2'] = None
            yield r2

conn['t1_col3'] = conn['t1'].by('col1')\
    .merge(append_col3, conn['t2'].by('col1'))

```

Tables must be grouped before you merge them.

append_col3 takes two list of dictionaries which can be empty on either side when there's no match.

As in the argument for map, merge takes as an argument, a dictionary-yielding generator or an ordinary function that
returns a dictionary, a list of dictionaries, or None. 


To do the cross join, consider passing a (lexical) closure on map to avoid repetitive table fetching.

```python
def fn():
    table2 = conn['t2'].list()
    def innerfn(rs):
        ...do some work using table2
        yield something
    return innerfn

conn['some_table'] = conn['t1'].by('col1').map(fn())
```

## concat

To concatenate t1 with itself,  

```python
conn['t1_double'] = conn['t1'].concat(conn['t1'])
```

which is the same as

```python
conn['t1_double'] = conn['t1'].concat(table1)

```

Tables for concatenation must have the same columns.


<!-- [Documentation]
(https://tablemap.readthedocs.io/en/latest/index.html)
 -->
