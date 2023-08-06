import unittest
import os
from pathlib import Path
from itertools import groupby, product, islice
from tablemap import Conn


table1 = [
    {'col1': 'a', 'col2': 4},
    {'col1': 'a', 'col2': 5},
    {'col1': 'b', 'col2': 1},
    {'col1': 'c', 'col2': 3},
    {'col1': 'c', 'col2': 4},
    {'col1': 'c', 'col2': 7},
    {'col1': 'd', 'col2': 2},

]

table2 = [
    {'col1': 'd', 'col3': 3},
    {'col1': 'b', 'col3': 1},
    {'col1': 'e', 'col3': 3},
    {'col1': 'e', 'col3': 4},
    {'col1': 'd', 'col3': 2},
]


class TestGeneral(unittest.TestCase):
    def setUp(self):
        self.dbfile = 'test/sample.db'

    def tearDown(self):
        if Path(self.dbfile).is_file():
            os.remove(self.dbfile)

    def test_by(self):
        def sum_by_col1(rs):
            r = {}
            r['col1'] = rs[0]['col1']
            r['col2'] = sum(r['col2'] for r in rs)
            yield r

        conn = Conn(self.dbfile)
        conn['t1'] = table1
        conn['t1_sum'] = conn['t1'].by('col1')\
            .map(sum_by_col1)

        self.assertEqual(list(conn['t1_sum'].iter()),
                         [{'col1': 'a', 'col2': 9},
                          {'col1': 'b', 'col2': 1},
                          {'col1': 'c', 'col2': 14},
                          {'col1': 'd', 'col2': 2}]
                         )
        conn['t1_sum2'] = conn['t1']\
            .by('col1').map(sum_by_col1)

        self.assertEqual(conn['t1_sum'].list(), conn['t1_sum2'].list())

    def test_full_join(self):
        def add_col3(rs1, rs2):
            # inner join
            if rs1 and rs2:
                for r1 in rs1:
                    for r2 in rs2:
                        r1['col3'] = r2['col3']
                        yield r1
            # left join
            elif rs1 and not rs2:
                for r1 in rs1:
                    r1['col3'] = None
                    yield r1
            # right join
            elif not rs1 and rs2:
                for r2 in rs2:
                    r2['col2'] = None
                    yield r2

        conn = Conn(self.dbfile)
        conn['t1'] = table1
        conn['t2'] = table2

        conn['t1_col3'] = conn['t1'].by('col1')\
            .merge(add_col3, conn['t2'].by('col1'))

        self.assertEqual(conn['t1_col3'].list(), [
            {'col1': 'a', 'col2': 4, 'col3': None},
            {'col1': 'a', 'col2': 5, 'col3': None},
            {'col1': 'b', 'col2': 1, 'col3': 1},
            {'col1': 'c', 'col2': 3, 'col3': None},
            {'col1': 'c', 'col2': 4, 'col3': None},
            {'col1': 'c', 'col2': 7, 'col3': None},
            {'col1': 'd', 'col2': 2, 'col3': 3},
            {'col1': 'd', 'col2': 2, 'col3': 2},
            {'col1': 'e', 'col2': None, 'col3': 3},
            {'col1': 'e', 'col2': None, 'col3': 4}]
        )

        table2_1 = sorted(table2, key=lambda r: r['col1'])
        conn['t1_col3_1'] = conn['t1'].by('col1')\
            .merge(add_col3, groupby(table2_1, lambda r: r['col1']))

        self.assertEqual(conn['t1_col3'].list(), conn['t1_col3_1'].list())

    def test_concat(self):
        conn = Conn(self.dbfile)
        conn['t1'] = table1
        conn['t1_double'] = conn['t1'].concat(conn['t1'])
        self.assertEqual(conn['t1'].list() + conn['t1'].list(),
                         conn['t1_double'].list())

        conn['t1_double'] = conn['t1'].concat(table1)
        self.assertEqual(conn['t1'].list() + conn['t1'].list(),
                         conn['t1_double'].list())


class TestBy(unittest.TestCase):
    def setUp(self):
        self.dbfile = 'test/sample.db'
        self.dbfile1 = 'test/sample1.db'

    def tearDown(self):
        if Path(self.dbfile).is_file():
            os.remove(self.dbfile)
        if Path(self.dbfile1).is_file():
            os.remove(self.dbfile1)

    def test_by_after_map(self):
        def sumit(rs):
            tot = sum(r['col2']for r in rs)
            for r in rs:
                r['tot'] = tot
                yield r

        def count(rs):
            n = len(rs)
            for r in rs:
                r['cnt'] = n
                yield r

        conn = Conn(self.dbfile)
        conn['t1'] = table1
        conn['t1_sum'] = conn['t1'].by('col1')\
            .map(sumit).by('tot').map(count)

        # on another db
        conn1 = Conn(self.dbfile1)
        conn1['t1_sum'] = conn['t1'].by('col1').map(sumit).by('tot').map(count)
        conn1['t1_sum2'] = conn['t1'].by('col1').map(sumit)\
            .by('tot').map(count).iter()

        self.assertEqual(conn['t1_sum'].list(), conn1['t1_sum'].list())
        self.assertEqual(conn['t1_sum'].list(), conn1['t1_sum2'].list())

    def test_multiple_by(self):
        def foo(r):
            r['col3'] = 1
            return r

        conn = Conn(self.dbfile)
        conn['t1'] = table1
        conn['t1_1'] = conn['t1'].map(foo).by('col1', 'col3')\
            .map(lambda rs: rs)

        conn['t1_2'] = conn['t1'].map(foo).by('col1').map(lambda rs: rs)
        self.assertEqual(conn['t1_1'].list(), conn['t1_2'].list())

        conn['t1_1_double'] = conn['t1_1']\
            .concat(conn['t1'].map(foo).by('col1', 'col3')
                              .map(lambda rs: rs))
        conn['t1_1_double2'] = conn['t1_1'].concat(conn['t1_1'])

        self.assertEqual(conn['t1_1_double'].list(),
                         conn['t1_1_double2'].list())

    def test_itertools(self):

        conn = Conn(self.dbfile)
        conn['t1'] = table1
        conn['t2'] = table2

        conn['t1_1'] = islice(conn['t1'].iter(), 0, 3)

        self.assertEqual(len(conn['t1_1'].list()), 3)

        xs = conn['t1'].iter()
        ys = conn['t2'].iter()

        conn['t1_2'] = ({**x, **y} for x, y in product(xs, ys))

        n1 = len(conn['t1'].list())
        n2 = len(conn['t2'].list())
        n3 = len(conn['t1_2'].list())

        self.assertEqual(n3, n1 * n2)


class TestDerivs(unittest.TestCase):
    def setUp(self):
        self.dbfile = 'test/sample.db'

    def tearDown(self):
        if Path(self.dbfile).is_file():
            os.remove(self.dbfile)

    def test_filter(self):
        conn = Conn(self.dbfile)

        conn['t1'] = table1
        conn['t1_1'] = conn['t1'].filter(lambda r: r['col2'] > 2)

        self.assertEqual(len(conn['t1_1'].list()), 5)

    def test_update(self):
        conn = Conn(self.dbfile)
        conn['t1'] = table1
        conn['t1_1'] = conn['t1'].update(
            col2=lambda r: r['col2'] + 1,
            col3=lambda r: r['col1'] + str(r['col2'])
        )
        # table is fetched as it's inserted. not sure if it's a feature.
        self.assertEqual(conn['t1_1'].list()[0],
                         {'col1': 'a', 'col2': 5, 'col3': 'a5'})

    def test_select(self):
        conn = Conn(self.dbfile)
        conn['t1'] = table1
        conn['t1_1'] = conn['t1'].update(
            col2=lambda r: r['col2'] + 1,
            col3=lambda r: r['col1'] + str(r['col2'])
        )

        r = next(conn['t1_1'].select('col1', 'col3').iter())
        self.assertEqual(len(r), 2)

    def test_join(self):
        conn = Conn(self.dbfile)
        conn['t1'] = table1
        conn['t2'] = table2

        conn['t1_1'] = conn['t1'].by('col1').join(['col1', 'col2', 'col3'],
                                                  conn['t2'].by('col1'))

        self.assertEqual(len(conn['t1_1'].list()), 3)

        conn['t1_2'] = conn['t1'].by('col1').left_join(['col1', 'col2', 'col3'],
                                                       conn['t2'].by('col1'))

        self.assertEqual(len(conn['t1_2'].list()), 8)

        conn['t1_3'] = conn['t1'].by('col1').right_join(['col1', 'col2', 'col3'],
                                                        conn['t2'].by('col1'))

        self.assertEqual(len(conn['t1_3'].list()), 5)

        conn['t1_4'] = conn['t1'].by('col1').full_join(['col1', 'col2', 'col3'],
                                                        conn['t2'].by('col1'))

        self.assertEqual(len(conn['t1_4'].list()), 10)
