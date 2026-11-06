# FREQ-GAN Strategy Lab

Rule: rank by IS win rate; qualify only if trades>=100, profit>0, profit factor>1, max DD<=35%; OOS shown for validation (min 25 trades)

| # | Strategy | TF | IS trades | IS win% | IS profit% | IS PF | IS maxDD% | OK | OOS trades | OOS win% | OOS profit% | OOS PF | OOS maxDD% |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | GanTrendEma4h (hyperopt) | 4h | 121 | 83.47 | 70.53 | 2.203 | 7.36 | yes | 20 | 75.0 | 2.55 | 1.161 | 3.85 |
| 2 | GanTrendEma4h | 4h | 112 | 62.5 | 128.81 | 1.568 | 23.63 | yes | 19 | 57.89 | 11.64 | 1.374 | 11.49 |
| 3 | SampleStrategy | 5m | 1156 | 86.51 | -63.61 | 0.83 | 75.79 | no | 105 | 86.67 | -5.6 | 0.848 | 17.48 |
| 4 | GanMtfTrendRsi | 15m | 1109 | 71.24 | -64.85 | 0.85 | 71.86 | no | 160 | 68.12 | -9.28 | 0.85 | 18.27 |
| 5 | GanConnorsRsi2_4h | 4h | 909 | 63.26 | -17.6 | 0.966 | 42.96 | no | 107 | 61.68 | 3.56 | 1.091 | 17.98 |
| 6 | GanRsiBbMeanRev | 15m | 3183 | 61.95 | -92.28 | 0.831 | 94.43 | no | 446 | 57.85 | -41.75 | 0.634 | 41.84 |
| 7 | GanConnorsRsi2 | 1h | 3304 | 58.38 | -92.55 | 0.853 | 95.43 | no | 477 | 54.3 | -38.6 | 0.633 | 39.99 |
| 8 | GanDonchianBreakout | 1h | 2075 | 48.63 | -86.01 | 0.89 | 88.04 | no | 259 | 44.79 | -9.43 | 0.946 | 40.76 |
| 9 | GanSupertrend | 1h | 962 | 44.28 | -84.19 | 0.791 | 87.74 | no | 145 | 46.21 | 31.3 | 1.285 | 17.65 |
| 10 | GanMacdRsi | 15m | 4481 | 41.6 | -98.6 | 0.764 | 98.65 | no | 636 | 39.94 | -42.99 | 0.68 | 49.6 |
| 11 | GanEmaPullbackAdx | 1h | 1100 | 37.91 | -89.18 | 0.645 | 89.76 | no | 128 | 35.16 | -0.82 | 0.982 | 13.77 |

## Pattern study (in-sample trades, all strategies)

### by pair (top 8 by win rate)
| key | n | win% | profit USDT |
|---|---|---|---|
| SOL/USDT:USDT | 3295 | 57.4 | -1150.71 |
| DOGE/USDT:USDT | 2785 | 57.1 | -626.12 |
| ETH/USDT:USDT | 3156 | 56.6 | -1255.49 |
| XRP/USDT:USDT | 3128 | 55.7 | -694.1 |
| BNB/USDT:USDT | 2821 | 51.4 | -634.31 |
| BTC/USDT:USDT | 3327 | 50.9 | -534.48 |

### by side (top 8 by win rate)
| key | n | win% | profit USDT |
|---|---|---|---|
| long | 9432 | 56.3 | -3015.12 |
| short | 9080 | 53.3 | -1880.09 |

### by hour_utc (top 8 by win rate)
| key | n | win% | profit USDT |
|---|---|---|---|
| 22 | 556 | 58.3 | -152.91 |
| 20 | 866 | 58.3 | -57.86 |
| 0 | 783 | 57.9 | 49.36 |
| 12 | 876 | 57.9 | -25.69 |
| 10 | 680 | 57.4 | -231.19 |
| 8 | 897 | 56.9 | -1.47 |
| 16 | 1186 | 56.8 | 513.43 |
| 3 | 587 | 56.0 | -172.21 |

### by weekday (top 8 by win rate)
| key | n | win% | profit USDT |
|---|---|---|---|
| Saturday | 2075 | 56.8 | 152.83 |
| Wednesday | 2559 | 55.7 | -645.13 |
| Friday | 2669 | 55.6 | 66.39 |
| Thursday | 2640 | 54.7 | -503.52 |
| Sunday | 2857 | 54.6 | -485.75 |
| Monday | 2984 | 54.1 | -1845.79 |
| Tuesday | 2728 | 53.1 | -1634.25 |

### by tag (top 8 by win rate)
| key | n | win% | profit USDT |
|---|---|---|---|
| SampleStrategy ·  | 1156 | 86.5 | -636.07 |
| GanTrendEma4h (hyperopt) · ema_cross_dn | 69 | 84.1 | 334.19 |
| GanTrendEma4h (hyperopt) · ema_cross_up | 52 | 82.7 | 371.13 |
| GanMtfTrendRsi · mtf_dn_rsi_pop | 556 | 71.8 | -303.57 |
| GanMtfTrendRsi · mtf_up_rsi_dip | 553 | 70.7 | -344.94 |
| GanConnorsRsi2_4h · rsi2_pop_downtrend | 508 | 65.2 | 330.35 |
| GanRsiBbMeanRev · bb_rsi_low | 1528 | 63.5 | -304.11 |
| GanTrendEma4h · ema_cross_dn | 65 | 63.1 | 812.5 |

### by strategy_side (top 8 by win rate)
| key | n | win% | profit USDT |
|---|---|---|---|
| SampleStrategy · long | 1156 | 86.5 | -636.07 |
| GanTrendEma4h (hyperopt) · short | 69 | 84.1 | 334.19 |
| GanTrendEma4h (hyperopt) · long | 52 | 82.7 | 371.13 |
| GanMtfTrendRsi · short | 556 | 71.8 | -303.57 |
| GanMtfTrendRsi · long | 553 | 70.7 | -344.94 |
| GanConnorsRsi2_4h · short | 508 | 65.2 | 330.35 |
| GanRsiBbMeanRev · long | 1528 | 63.5 | -304.11 |
| GanTrendEma4h · short | 65 | 63.1 | 812.5 |

### by strategy_pair (top 8 by win rate)
| key | n | win% | profit USDT |
|---|---|---|---|
| SampleStrategy · SOL/USDT:USDT | 224 | 87.5 | -224.48 |
| SampleStrategy · ETH/USDT:USDT | 208 | 87.0 | -58.61 |
| SampleStrategy · DOGE/USDT:USDT | 171 | 86.5 | -128.89 |
| SampleStrategy · BTC/USDT:USDT | 191 | 86.4 | -102.82 |
| SampleStrategy · XRP/USDT:USDT | 212 | 85.8 | -73.05 |
| SampleStrategy · BNB/USDT:USDT | 150 | 85.3 | -48.22 |
| GanMtfTrendRsi · SOL/USDT:USDT | 198 | 74.7 | -88.27 |
| GanMtfTrendRsi · BTC/USDT:USDT | 183 | 74.3 | 156.62 |

### by exit_reason (top 8 by win rate)
| key | n | win% | profit USDT |
|---|---|---|---|
| roi | 4154 | 99.9 | 16653.62 |
| trailing_stop_loss | 1597 | 99.9 | 13786.56 |
| below_sma5 | 2103 | 63.3 | 2106.57 |
| above_sma5 | 1817 | 61.7 | 1890.11 |
| bb_mid | 2034 | 53.4 | -512.37 |
| mtf_exit | 220 | 33.6 | -719.95 |
| macd_rsi_exit | 3220 | 21.1 | -3024.78 |
| exit_signal | 33 | 9.1 | -180.56 |
