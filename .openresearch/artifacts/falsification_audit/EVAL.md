# Assumption-satisfying falsification audit

This route searches exact admissible boundaries and exits nonzero unless its
off-contract controls trigger. A failed counterexample search is never reported
as verification.

It found no contradiction to the fixed-parameter statements. It did find two
important scope corrections:

1. Lemma 2's context constant cannot be uniform over all `A,eta` while depending
   only on `Omega`; the appendix correctly derives dependence on `A` and `eta`.
2. Lemma 6 permits its context constant to depend on depth. Only the query
   constant is depth-independent.
