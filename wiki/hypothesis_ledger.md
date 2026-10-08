# Hypothesis ledger

One row per idea the bots have tested or carry: every bot, every agent, every Friday tune. Its job is to stop a
failed idea coming back under a new name. Before a new bot, agent or tune is proposed, look for its row here first;
a match means the proposal names what is different and adds a variation, not a new row.

Rules: rows are never deleted or rewritten; a new result appends to `result` and `lesson` with its date. Every Friday
tune adds a row (`T…`) and adds one to `variations` on the row it changes. No backtest, replay or retune starts from
this page (6 Oct rule); it records, it does not decide.

Status: untested · failed · logging · voting · paused · retired. Regime: trend up · trend down · choppy · high vol;
"not split" means the test pooled every regime and says nothing about any one of them.

## Bots and setups

| id | idea | source | symbol | date | version / commit | variations | regime when tested | result | status | lesson |
|---|---|---|---|---|---|---|---|---|---|---|
| H01 | Opening-range breakout, 5m and 15m box, with and without GEX | Ty's plan v2 | 16-symbol list | 2026-10-04 | Phase A grid (`signals.py`) | 12 (2 boxes × 3 expiry groups × GEX on/off) | not split, 2025–2026 | No cell survived 2–5 bps costs; best after real spreads (M1): 15m box, t 1.45 | failed | ORB alone does not beat costs. H15 must show what it adds |
| H02 | 9:30 5-minute candle, break and retest | video test | SPY, QQQ | 2026-10-06 | `video_tests/orb_retest.py` | 2 stop readings | not split, 2024-01-18 to 2026-10-02 | Tight stop −0.49R a trade net; wide stop −0.004R net (2026: −0.10R) | failed | Same family as H01 and H15 |
| H03 | 9 EMA × VWAP cross; 5/9/13 EMA ribbon | Ty's setups | SPY, QQQ | 2026-10-04 | VWAP/EMA backtest | 4 (2 rules × 3m/5m) | not split | All negative after $5.30 a round trip; ADX > 25 the only filter that helped, still under costs | failed | A trend filter helps but does not pay for spread |
| H04 | Sweep V0–V6 | sweep study | SPY, QQQ, TSLA | 2026-10-06 | `sweep/` | 7 | not split | All seven failed their gates | logging (V0 paper forward test, 30 sessions) | V0 is watched on paper only |
| H05 | Bot #1: 3m SuperTrend flip, +30% / −30% / 10 min | Ty's Cockpit | SPY, QQQ, TSLA (v8: SPY, QQQ) | 2026-10-06 | `reference/bot1_st3m.md`; v7, v8 | 1 | 13-week study Jul–Oct 2026; hold-out not split | Study +2.20% a trade (t 3.45, n 1,411). Hold-out 2024-01-18 to 2026-06-30: n 7,629, gross −0.7%, net −1.8% (t −7.0), every year, symbol and direction negative | failed (trades on paper in v8 under the 6 Oct go-live rule) | 13 good weeks are not an edge; the study window was the result |
| H06 | Bot #2: late-day momentum (sign of close-to-10:00, enter 15:30) | Gao et al. 2018 | SPY, QQQ, TSLA (v8: SPY, QQQ) | 2026-10-06 | `bot2_study.py`; v7, v8 | 1 | study Jul–Oct 2026; hold-out not split | Study +6.1% (t 3.3). Hold-out: n 1,650, net −3.5% (t −5.5), every year and symbol negative | failed (trades on paper in v8) | Edge sat in Aug 19 – Oct 2 only |
| H07 | 3m Chandelier exit flip, opening hour | Cockpit | SPY, QQQ, TSLA | 2026-10-06 | `ce_study.py` | 1 | not split | +1.1% (t 0.8, n 324); 75% fired within 10 min of a Bot #1 flip; the other 80 lost −7.0% (t −2.7) | failed | Not a separate signal from H05 |
| H08 | Trend + Timing pullback | Cockpit | SPY, QQQ, TSLA | 2026-10-06 | `tt_study.py` | 1 | not split | Failed its pass bar | failed | — |
| H09 | Gap go / gap fade | study | SPY, QQQ, TSLA | 2026-10-06 | `bot2_study.py` | 2 | not split | Failed | failed | — |
| H10 | QQQ leads TSLA | study | QQQ, TSLA | 2026-10-06 | `bot2_study.py` | 1 | not split | Failed | failed | — |
| H11 | Bot #1 rules on other symbols ("Bot #4" candidate) | study | IWM; NVDA, AAPL, AMZN | 2026-10-06 | `bot4_study.py` | 2 | not split, Jul 1 – Oct 2 2026 | IWM gross −1.9%, net −4.6% (t −2.8, n 257). NVDA/AAPL/AMZN net −4.8% (t −5.9, n 824); every symbol, side and window negative | failed | Warned early that H05 was its 3 symbols in 13 weeks, not the signal |
| H12 | Sweep reclaim ("Bot #3" candidate, 6 Oct) | study | SPY, QQQ, TSLA | 2026-10-06 | `bot3_study.py` | 1 | not split | n 225, gross −1.3%, net −2.8% (t −1.8); near a Bot #1 flip +1.4%, away from one −6.6% | failed | 4th candidate to fail away from H05; Bot #6 (later) must say what differs |
| H13 | Volume rule: signal bar ≥ median of the same slot over 40 sessions | video tests | SPY, QQQ, TSLA | 2026-10-06 | `holdout_study.py` (volume mode) | 2 (fixed median, rolling median) | hold-out, not split | Kept −1.4% vs skipped −2.4%: V1 failed, V2/V3 held | logging | Separates a little, does not make a loser win |
| H14 | Ty's chart entries managed by the bot's exits | TradingView setup study | SPY, QQQ, others | 2026-10-06 | setup study | 20 filters | not split | −0.029R a trade (t −0.38); 0 of 20 filters passed; bot exits cut the study loss by about half | failed (became co-pilot mode, not built) | Closest to zero of anything tested |
| H15 | Bot #3: 15m ORB box on Champ's rules (sweep back inside, or break and retest), graded A+ to B by flow | Champ's videos and live trades | SPY, QQQ | 2026-10-08 | orb-options spec `work/261008-orb-champ-merge` frozen 5d17ebd | 0 | — | Not built; waits for the 3c verdict | untested | Must state what it adds over H01 and H02 (flow grade, sweep-back entry, TP1 at box mid) |

## Agents

| id | idea | source | symbol | date | version / commit | variations | regime when tested | result | status | lesson |
|---|---|---|---|---|---|---|---|---|---|---|
| A01 | Structure agent: Cockpit's own swings on the chart timeframe, CHoCH/BOS | Ty's Cockpit | all v7 symbols | 2026-10-08 | v7 read agent; vote dropped in v8 (4324e85) | 1 | 2 sessions, not split | 10/06–10/07: the only no-vote on 0 skips for SPY/QQQ; read BEAR on 10/07 14:08 while Ty's chart read up | logging (counts in READY, no entry vote) | One misread: unproven, not condemned. v9 rebuilds it on Ty's SMC settings; the vote returns at the first Friday tune after its readings match his chart |
| A02 | Flow agent: signed IBKR option prints, net call/put flow, z vs 20 sessions, flow speed | Champ's call-flow filter | SPY, QQQ | 2026-10-08 | orb-options PR #6 | 0 | — | Built, log only; warm-up needs 20 sessions | logging | Votes only inside H15, and only after warm-up |

## Friday tunes

| id | idea | source | symbol | date | version / commit | variations | regime when tested | result | status | lesson |
|---|---|---|---|---|---|---|---|---|---|---|

None yet. The first tune adds row T01.

Sources: the orb-options study scripts and logs named in each row (private repo); results as recorded there on the
dates shown. (Verified: orb-options study logs, 2026-10-04 to 2026-10-08)
