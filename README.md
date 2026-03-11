Binomial Tree Option Pricing under the CRR Model

This project implements a **Cox-Ross-Rubinstein (CRR) recombining binomial tree** to price **European and American options** on both **equities** and **foreign exchange (FX)** under a no-arbitrage, risk-neutral valuation framework.

The objective is not only to compute the option price at the initial node, but also to show how the value is built **node by node** through backward induction. The model displays both the **underlying asset price tree** and the **option value tree**, and flags **early exercise** when it is optimal for American options.

---

## Project Objective

The project is designed to connect financial theory with numerical implementation.

It shows how option prices are derived from:

- the dynamics of the underlying asset under a binomial process,
- the no-arbitrage principle,
- risk-neutral valuation,
- and backward induction from maturity to the present.

The framework supports:

- **European call and put options**
- **American call and put options**
- **Equity options** with a continuous dividend yield
- **FX options** with domestic and foreign interest rates
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
## Input Parameters

The script uses a structured input dictionary with the following fields:

- `asset_type`: `"equity"` or `"forex"`
- `option_type`: `"call"` or `"put"`
- `style`: `"european"` or `"american"`
- `S0`: initial underlying price
- `K`: strike price
- `T`: maturity
- `sigma`: volatility
- `N`: number of time steps

For equities:
- `r`: risk-free rate
- `q`: dividend yield

For FX:
- `rd`: domestic rate
- `rf`: foreign rate

---

## Example Input

```python
data = {
    "asset_type": "equity",
    "option_type": "put",
    "style": "european",
    "S0": 50.0,
    "K": 52.0,
    "T": 2.0,
    "sigma": 0.30,
    "N": 10,
    "r": 0.05,
    "q": 0.00,
    "rd": 0.05,
    "rf": 0.02
}
