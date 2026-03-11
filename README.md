## Pricing Logic

The option is priced by **backward induction** under the **risk-neutral measure**.

At maturity, the option value is equal to its payoff.

### Call Option Payoff

\[
f_T = \max(S_T - K, 0)
\]

### Put Option Payoff

\[
f_T = \max(K - S_T, 0)
\]

At each prior node, the option value is equal to the **discounted risk-neutral expected value** of the option in the next period.

### European Option Valuation

In the basic binomial framework, the one-step valuation formula is:

\[
f = e^{-r\Delta t}\left[p f_u + (1-p) f_d\right]
\]

where:

- \(f\) = option value at the current node
- \(f_u\) = option value at the up-state node in the next period
- \(f_d\) = option value at the down-state node in the next period
- \(p\) = risk-neutral probability
- \(r\) = risk-free rate
- \(\Delta t\) = time step length

This is the standard no-arbitrage binomial pricing formula: the current option value is the discounted expected future value under risk-neutral probabilities.

### Risk-Neutral Probability

For the basic no-dividend equity case:

\[
p = \frac{e^{r\Delta t} - d}{u - d}
\]

For equity options with a continuous dividend yield \(q\), the more general formula becomes:

\[
p = \frac{e^{(r-q)\Delta t} - d}{u - d}
\]

For FX options, the foreign interest rate plays the role of a carry term, so the probability becomes:

\[
p = \frac{e^{(r_d-r_f)\Delta t} - d}{u - d}
\]

where:

- \(r_d\) = domestic interest rate
- \(r_f\) = foreign interest rate

### American Option Valuation

For an American option, the model compares:

- the **continuation value**
- the **intrinsic value**

The continuation value is:

\[
f^{cont} = e^{-r\Delta t}\left[p f_u + (1-p) f_d\right]
\]

and the option value is:

\[
f = \max(f^{cont}, \text{intrinsic value})
\]

So the model checks at each node whether it is optimal to continue holding the option or to exercise it immediately.

For a call, the intrinsic value is:

\[
\max(S-K, 0)
\]

For a put, the intrinsic value is:

\[
\max(K-S, 0)
\]

### Interpretation

This means that:

- for a **European option**, the holder can only exercise at maturity, so the value is always the discounted expected continuation value;
- for an **American option**, the holder may exercise before maturity, so the model must compare continuation and immediate exercise at every node.

This backward-induction structure is what makes the binomial tree especially useful for pricing American-style derivatives.
