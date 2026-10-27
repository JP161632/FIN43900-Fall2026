"""Reproduce the instructor's known answer and later-cutoff experiment."""
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import asof


def main():
    rows = asof.load_rows(asof.TABLE)
    panel, naive, funnel = asof.filter_rows(rows, asof.DECISION_DATE)
    assert [[r['row'] for r in removed] for _, removed in funnel] == [[11], [7], [3, 8, 10], [2]]
    assert [r['row'] for r in panel] == [1, 4, 5, 6, 9, 12]
    expected = {'AAA': ('+1.98', '+5.83', '2026-03'),
                'BBB': ('-1.02', '-5.15', '2026-03'),
                'CCC': ('+0.91', '+1.82', '2026-02')}
    actual, comparison = asof.signals(panel), asof.signals(naive)
    for ticker, (point_in_time, hindsight, naive_month) in expected.items():
        assert actual[ticker][0].strftime('%Y-%m') == '2026-02'
        assert f'{actual[ticker][1]:+.2f}' == point_in_time
        assert f'{comparison[ticker][1]:+.2f}' == hindsight
        assert comparison[ticker][0].strftime('%Y-%m') == naive_month
    later, later_naive, _ = asof.filter_rows(rows, '2026-04-15')
    assert asof.signals(later) == asof.signals(later_naive) == comparison
    # Publication-day boundary: April 5 includes CCC's April 5 revision.
    boundary, _, _ = asof.filter_rows(rows, '2026-04-05')
    assert 10 in [r['row'] for r in boundary]
    assert 12 not in [r['row'] for r in boundary]
    # Input ordering must not cause the older vintage to win.
    reversed_panel, _, _ = asof.filter_rows(list(reversed(rows)), asof.DECISION_DATE)
    assert asof.signals(reversed_panel) == actual
    # A missing adjacent calendar month must not become a multi-month signal.
    gap = asof.load_rows('row,ticker,month,published,index\n1,X,2026-01,2026-02-01,100\n2,X,2026-03,2026-04-01,110\n')
    assert asof.signals(gap)['X'][1] is None
    assert asof.DECISION_DATE == '2026-03-31'
    output = StringIO()
    with redirect_stdout(output):
        print('BASELINE: python asof.py')
        asof.report()
        print('\nLATER-CUTOFF EXPERIMENT (in memory; delivered cutoff unchanged)')
        asof.report(decision_date='2026-04-15')
        print('\nPASS: known funnel, panel, six signals and named months.')
        print('PASS: April 15 as-of equals naive for every ticker; March 31 input preserved.')
        print('PASS: inclusive cutoff, reversed row order, missing previous calendar month.')
        print('Partner activities are documented from student reports in the writeup; not authenticated by these software checks.')
    text = output.getvalue()
    Path(__file__).with_name('verification-results.txt').write_text(text, encoding='utf-8')
    print(text, end='')


if __name__ == '__main__':
    main()
