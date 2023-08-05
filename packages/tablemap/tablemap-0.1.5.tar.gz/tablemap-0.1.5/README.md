# About 
'tablemap' is a very simple yet handy Python data wrangling tool hinges on Sqlite3 which
requires no knowledge of SQL or pandas. If only you are familiar with a list of dictionaries, 
you are good to go.

# Installation
Requires only built-in Python libraries.
```
pip install tablemap
```
# Tutorial 

## keep
```python
table1 = [
    {'col1': 'a', 'col2': 4},
    {'col1': 'a', 'col2': 5},
    {'col1': 'b', 'col2': 1},
    {'col1': 'c', 'col2': 3},
    {'col1': 'c', 'col2': 4},
    {'col1': 'c', 'col2': 7},
    {'col1': 'd', 'col2': 2},
]

conn = Conn('sample.db')
```

Let's create a table 't1' in 'sample.db'

```python
conn['t1'] = table1
```
The right hand side of the assignment can be a list of dictionaries, an iterator that yields dictionaries or an object fetched from the connection, for example, conn['t1'] where you can chain up some methods such as 'map', 'by', 'merge' and 'concat'. 

To browse the table,

```python
print(conn['t1'].list())

# to save some memory,
for r in conn['t1'].iter():
    print(r)
```

Softwares like [SQLiteStudio](https://sqlitestudio.pl/) or [DB Browser for SQLite](https://sqlitebrowser.org/) can be a help to browse the dataset graphically.


## map

filter col2 > 2 and add 1 to col2,

```python
def add1(r):
    if r['col2'] > 2:
        r['col2'] += 1 
        return r

conn['t1_1'] = conn['t1'].map(add1)
```

'map' takes a generator that yields dictionaries or an ordinary function that 
returns a dictionary, a list of dictionaries, or None

The function that's passed on map takes a dictionary as an argument,
which of course represents a row in your dataset.


## by
```python
def sum1(rs):
    r0 = rs[0]
    r0['col2_sum'] = sum(r['col2'] for r in rs)
    del r0['col2']
    yield r0

conn['t1_sum_by_col2'] = conn['t1'].by('col2')\
    .map(sum1)
```

'by' takes columns as an argument(comma separated string) for grouping
and the next process(map in this case) takes on each group. (a list of dictionaries) 


CAUTION

'by' loads up the whole iterator on memory, so in case it's worrisome, 
the following code does the same while using much less of it.

```python
conn['t1_sum_by_col2'] = conn['t1', 'col2'].map(sum1)
```

## merge

To merge table1 and table2 by col1

```python
table2 = [
    {'col1': 'd', 'col3': 3},
    {'col1': 'b', 'col3': 1},
    {'col1': 'e', 'col3': 3},
    {'col1': 'e', 'col3': 4},
    {'col1': 'd', 'col3': 2},
]

conn['t2'] = keep(table2)

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
            r2['col2'] = None
            yield r2
```

Sequences must be grouped before you merge them. 

append_col3 takes two list of dictionaries which can be empty on either side when there's no match.

```python
conn['t1_col3'] = conn['t1', 'col1']\
    .merge(append_col3, conn['t2', 'col1'])
```

If interested in cross join, consider passing a lexical closure on map to avoid repetitive table fetching. 

```python
def fn():
    table2 = conn['t2'].list()
    def innerfn(rs):
        ...do some work using table2 
        yield something
    return innerfn

conn['some_table'] = conn['t1', 'col1'].map(fn())
```

## concat

To concatenate tables with the same columns, 
```python
conn['t1_double'] = conn['t1'].concat(conn['t1'])
```
which is the same as
```python
conn['t1_double'] = conn['t1'].concat(table1)
```

That's all there's to know.
<!-- [Documentation]
(https://tablemap.readthedocs.io/en/latest/index.html)
 -->
