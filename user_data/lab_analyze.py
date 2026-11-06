"""FREQ-GAN STRATEGY LAB analysis: leaderboard (IS vs OOS) + pattern study from freqtrade backtest exports."""
import json, sys, time
from pathlib import Path
import pandas as pd
from freqtrade.data.btanalysis import load_backtest_stats, load_backtest_data, get_latest_backtest_filename

BT = Path('/freqtrade/user_data/backtest_results')
MIN_TRADES = 100
OUT_JSON = BT / 'strategy_lab.json'
OUT_MD = BT / 'strategy_lab.md'


IS_START = int(pd.Timestamp('2024-10-01', tz='UTC').timestamp())
IS_END = int(pd.Timestamp('2026-08-01', tz='UTC').timestamp())
OOS_START = int(pd.Timestamp('2026-08-01', tz='UTC').timestamp())


def find(strategy, period, tf=None, before=None, after=None):
    """latest export for strategy+period, identified via the .meta.json (strategy, start ts, timeframe)"""
    want = IS_START if period == 'IS' else OOS_START
    best = None
    for m in BT.glob('*.meta.json'):
        meta = json.loads(m.read_text())
        if list(meta) != [strategy]:
            continue
        v = meta[strategy]
        ok = (v.get('backtest_end_ts') == IS_END and v.get('backtest_start_ts', 0) >= IS_START) if period == 'IS' \
            else (v.get('backtest_start_ts') == OOS_START)
        if not ok or (tf and v.get('timeframe') != tf):
            continue
        if before and v['backtest_start_time'] >= before:
            continue
        if after and v['backtest_start_time'] < after:
            continue
        if best is None or v['backtest_start_time'] > best[0]:
            best = (v['backtest_start_time'], m.with_name(m.name.replace('.meta.json', '.zip')))
    return best[1] if best and best[1].exists() else None


def summarize(f):
    st = load_backtest_stats(f)
    name, s = next(iter(st['strategy'].items()))
    tr = load_backtest_data(f, name)
    wins = tr[tr['profit_abs'] > 0]['profit_abs'].sum()
    loss = -tr[tr['profit_abs'] < 0]['profit_abs'].sum()
    pf = (wins / loss) if loss > 0 else None
    long_ = tr[~tr['is_short']]; short = tr[tr['is_short']]
    return name, tr, {
        'strategy': name, 'timeframe': s.get('timeframe'), 'timerange': s.get('timerange'), 'start': str(s.get('backtest_start')), 'end': str(s.get('backtest_end')),
        'trades': int(s['total_trades']), 'winrate': round(100 * s['wins'] / s['total_trades'], 2) if s['total_trades'] else 0,
        'profit_pct': round(100 * s['profit_total'], 2), 'profit_abs': round(s['profit_total_abs'], 2),
        'profit_factor': round(pf, 3) if pf else None, 'max_dd_pct': round(100 * s.get('max_drawdown_account', 0), 2),
        'sharpe': round(s.get('sharpe', 0) or 0, 2), 'avg_duration': s.get('holding_avg'),
        'long_trades': len(long_), 'long_winrate': round(100 * (long_['profit_abs'] > 0).mean(), 1) if len(long_) else None,
        'short_trades': len(short), 'short_winrate': round(100 * (short['profit_abs'] > 0).mean(), 1) if len(short) else None,
        'funding_fees': round(float(tr['funding_fees'].sum()), 4) if 'funding_fees' in tr else None,
    }


def qualifies(r):
    return (r['trades'] >= MIN_TRADES and r['profit_pct'] > 0 and (r['profit_factor'] or 0) > 1.0
            and r['max_dd_pct'] <= 35)


def groups(tr, col, min_n):
    g = tr.groupby(col).agg(n=('profit_abs', 'size'), winrate=('profit_abs', lambda x: round(100 * (x > 0).mean(), 1)),
                            profit=('profit_abs', 'sum'))
    g = g[g['n'] >= min_n].sort_values('winrate', ascending=False)
    return [{'key': str(k), 'n': int(v.n), 'winrate': float(v.winrate), 'profit_abs': round(float(v.profit), 2)}
            for k, v in g.iterrows()]


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument('strategies')
    ap.add_argument('--hyp', default='', help='S:ts,... base=before ts, hyperopt variant=after ts')
    ap.add_argument('--deployed', default='')
    a = ap.parse_args()
    hyp = dict(x.split(':') for x in a.hyp.split(',') if x)
    jobs = []
    for st in a.strategies.split(','):
        if st in hyp:
            jobs += [(st, st, {'before': int(hyp[st])}, 'base params'), (st + ' (hyperopt)', st, {'after': int(hyp[st])}, 'hyperopt IS-only')]
        else:
            jobs.append((st, st, {}, ''))
    rows, is_trades = [], []
    for label, st, kw, note in jobs:
        row = {'strategy': label, 'note': note}
        for per in ('IS', 'OOS'):
            f = find(st, per, **kw)
            if not f:
                continue
            name, tr, summ = summarize(f)
            row[per] = summ
            row[per]['file'] = f.name
            if per == 'IS':
                tr = tr.copy(); tr['strategy'] = label; is_trades.append(tr)
        if 'IS' in row:
            row['IS']['qualifies'] = qualifies(row['IS'])
        if 'OOS' in row:
            row['OOS']['qualifies'] = qualifies({**row['OOS'], 'trades': max(row['OOS']['trades'], MIN_TRADES) if row['OOS']['trades'] >= 25 else 0})
        rows.append(row)
    # ranking: qualified (IS) first, by IS winrate; non-qualified after
    rows.sort(key=lambda r: (not r.get('IS', {}).get('qualifies', False), -r.get('IS', {}).get('winrate', 0)))
    allt = pd.concat(is_trades, ignore_index=True)
    allt['side'] = allt['is_short'].map({True: 'short', False: 'long'})
    od = pd.to_datetime(allt['open_date'], utc=True)
    allt['hour_utc'] = od.dt.hour
    allt['weekday'] = od.dt.day_name()
    allt['strategy_side'] = allt['strategy'] + ' · ' + allt['side']
    allt['strategy_pair'] = allt['strategy'] + ' · ' + allt['pair']
    allt['tag'] = allt['strategy'] + ' · ' + allt['enter_tag'].fillna('-')
    patterns = {c: groups(allt, c, mn) for c, mn in (('pair', 50), ('side', 50), ('hour_utc', 50), ('weekday', 50),
                                                       ('tag', 30), ('strategy_side', 30), ('strategy_pair', 30), ('exit_reason', 30))}
    out = {'deployed': a.deployed, 'generated': time.time(), 'min_trades': MIN_TRADES, 'rule': 'rank by IS win rate; qualify only if trades>=100, '
           'profit>0, profit factor>1, max DD<=35%; OOS shown for validation (min 25 trades)', 'leaderboard': rows,
           'patterns': patterns, 'is_trades_total': int(len(allt))}
    txt = json.dumps(out, indent=1, default=lambda o: float(o) if hasattr(o, "__float__") else str(o))
    OUT_JSON.write_text(txt)
    LAB = Path('/freqtrade/user_data/strategy_lab'); LAB.mkdir(exist_ok=True)
    (LAB / 'strategy_lab.json').write_text(txt)
    L = ['# FREQ-GAN Strategy Lab', '', f"Rule: {out['rule']}", '',
         '| # | Strategy | TF | IS trades | IS win% | IS profit% | IS PF | IS maxDD% | OK | OOS trades | OOS win% | OOS profit% | OOS PF | OOS maxDD% |',
         '|---|---|---|---|---|---|---|---|---|---|---|---|---|---|']
    for i, r in enumerate(rows, 1):
        a, b = r.get('IS', {}), r.get('OOS', {})
        L.append(f"| {i} | {r['strategy']} | {a.get('timeframe')} | {a.get('trades')} | {a.get('winrate')} | {a.get('profit_pct')} | "
                 f"{a.get('profit_factor')} | {a.get('max_dd_pct')} | {'yes' if a.get('qualifies') else 'no'} | {b.get('trades')} | "
                 f"{b.get('winrate')} | {b.get('profit_pct')} | {b.get('profit_factor')} | {b.get('max_dd_pct')} |")
    L += ['', '## Pattern study (in-sample trades, all strategies)']
    for c, g in patterns.items():
        L.append(f"\n### by {c} (top 8 by win rate)\n| key | n | win% | profit USDT |\n|---|---|---|---|")
        L += [f"| {x['key']} | {x['n']} | {x['winrate']} | {x['profit_abs']} |" for x in g[:8]]
    OUT_MD.write_text('\n'.join(L) + '\n')
    print('\n'.join(L[:6 + len(rows)]))


main()
