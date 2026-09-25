# Findings

The selected two-day slice has **12,043,123 User-prefixed account logon events**, including **167,437 failures**. This excludes machine and service accounts and all other Windows event IDs. [Daily totals](results/01_daily_logons.md)

1. **Failure counts stay similar while volume grows.** Day 1 has 5,441,589 logons and 82,414 failures (1.515%). Day 2 has 6,601,534 logons and 85,023 failures (1.288%). [Daily result](results/01_daily_logons.md)
2. **One day of history leaves substantial apparent novelty.** Of 46,370 distinct successful user–destination pairs on day 2, 13,870 (29.91%) are absent on day 1. This measures a short baseline, not confirmed new access to the enterprise. [New pairs](results/11_new_pair_count.md)
3. **Repeated failure windows are a useful review queue.** [Query 08](results/08_user_failure_bursts.md) ranks anonymized user/15-minute windows with at least ten failures. [Query 09](results/09_fail_then_success.md) adds windows where repeated failures precede a later success on the same user–source–destination triple. These are patterns, not validated compromises.
4. **The mirror's local/remote field distinction changes the measured failure rate.** Events with `src = destination` have a 3.604% failure rate, versus 0.931% for `src <> destination`. Because the mirror fills missing fields with `LogHost`, this should be treated as a field-comparison result. [Field comparison](results/05_remote_vs_local.md)

## Limits

The dataset clock is relative, identities are anonymized, and only the first two days were used. There is no attack ground truth in this project slice. The dashboard is for investigation and data exploration; its ranked entries are not maliciousness claims.
