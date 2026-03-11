# Binomial Tree Option Pricing under the CRR Model

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

---

## Model Framework

The underlying asset is modeled with a **recombining binomial tree**.

At each time step, the asset price can:

- move **up** by a factor \( u \),
- or move **down** by a factor \( d \).

The time step is:

\[
\Delta t = \frac{T}{N}
\]

where:

- \( S_0 \) = initial asset price
- \( K \) = strike price
- \( T \) = maturity
- \( N \) = number of time steps
- \( \sigma \) = volatility

Under the **CRR specification**:

\[
u = e^{\sigma \sqrt{\Delta t}}
\]

\[
d = e^{-\sigma \sqrt{\Delta t}}
\]

This choice ensures a recombining lattice and provides a standard discrete-time approximation to continuous-time option pricing.

---

## No-Arbitrage and Risk-Neutral Valuation

The pricing logic is based on the principle of **absence of arbitrage**.

Under the risk-neutral measure, the option value at each node is equal to the **discounted expected value of the option in the next period**.

### Equity Options

For equity options with a **continuous dividend yield** \( q \), the risk-neutral probability is:

\[
p = \frac{e^{(r-q)\Delta t} - d}{u - d}
\]

where:

- \( r \) = risk-free interest rate
- \( q \) = continuous dividend yield

The discount factor is:

\[
e^{-r \Delta t}
\]

### FX Options

For foreign exchange options, the model uses:

\[
p = \frac{e^{(r_d-r_f)\Delta t} - d}{u - d}
\]

where:

- \( r_d \) = domestic risk-free rate
- \( r_f \) = foreign risk-free rate

In the FX setting, the foreign interest rate plays the role of a **continuous carry term**, analogous to a dividend yield in the equity case.

The discount factor is:

\[
e^{-r_d \Delta t}
\]

---

## Payoff Structure

At maturity, the option value is equal to its intrinsic payoff.

### Call Option

\[
\text{Payoff} = \max(S-K, 0)
\]

### Put Option

\[
\text{Payoff} = \max(K-S, 0)
\]

---

## Pricing Logic

The option is priced by **backward induction**.

### European Option

For a European option, the value at each node is:

\[
V = e^{-r\Delta t} \left( p V_{\text{up}} + (1-p)V_{\text{down}} \right)
\]

or, in the FX case, discounted at the domestic rate.

### American Option

For an American option, the model compares:

- the **continuation value**
- the **intrinsic value**

and takes:

\[
V = \max(\text{continuation value}, \text{intrinsic value})
\]

This means the code checks at each node whether **early exercise** is optimal.

---

## Important Financial Note

For an **American call on a non-dividend-paying stock**, early exercise is generally not optimal, so the American and European values should coincide in that case.

However, for:

- **puts**,
- **dividend-paying equities**,
- and some **FX settings**,

early exercise may become optimal, which makes the binomial framework particularly useful.

---

## Key Features

- Pricing of **European call and put options**
- Pricing of **American call and put options**
- **Equity option pricing** with risk-free rate and continuous dividend yield
- **FX option pricing** with domestic and foreign rates
- **Node-by-node valuation**
- **Early exercise detection** for American options
- **Root delta** calculation
- Combined graphical tree with:
  - underlying asset prices
  - option values
  - early exercise markers

---

## Code Logic

The implementation follows these main steps:

1. Define the option and market inputs
2. Compute:
   - \( \Delta t \)
   - up factor \( u \)
   - down factor \( d \)
   - risk-neutral probability \( p \)
3. Build the **underlying price tree**
4. Compute the **payoff at maturity**
5. Apply **backward induction**
6. For American options, compare continuation and intrinsic value at each node
7. Compute the **root delta**
8. Produce:
   - a summary table
   - a combined graphical binomial tree

---

## Input Parameters

The script accepts the following inputs:

- `asset_type`: `"equity"` or `"forex"`
- `option_type`: `"call"` or `"put"`
- `style`: `"european"` or `"american"`
- `S0`: initial asset price
- `K`: strike price
- `T`: maturity
- `sigma`: volatility
- `N`: number of steps

For equities:
- `r`: risk-free rate
- `q`: dividend yield

For FX:
- `rd`: domestic rate
- `rf`: foreign rate

---

## Output

The script returns:

- the **option price**
- the **time step** \( \Delta t \)
- the **up factor** \( u \)
- the **down factor** \( d \)
- the **risk-neutral probability** \( p \)
- the **root delta**
- the **underlying price tree**
- the **option value tree**
- the **early exercise flag tree**

It also prints a **summary table** and draws a **combined binomial tree visualization** showing:

- underlying asset prices at each node,
- option values at each node,
- and `EX` flags where early exercise is optimal.

---

## Why This Matters

Binomial trees are widely used in quantitative finance because they are:

- intuitive,
- flexible,
- and well suited to path-dependent exercise logic.

They are especially useful for:

- understanding option pricing step by step,
- valuing **American options**,
- identifying **early exercise decisions**,
- and translating financial theory into transparent numerical code.

This project highlights how option prices are built backward from maturity to the initial node using **risk-neutral pricing under no-arbitrage**.

---

## Project Structure

```text
.
├── binomial_tree.py
├── requirements.txt
└── README.md
