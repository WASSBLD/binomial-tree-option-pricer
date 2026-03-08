
# Binomial Tree Option Pricing under the CRR Model

This project implements a Cox-Ross-Rubinstein (CRR) binomial tree framework to price European and American options.

The objective is not only to compute the option price, but also to show the value of the option at each node of the tree and apply the pricing logic based on absence of arbitrage.

## Model Framework

The underlying asset price is modeled with a recombining binomial tree.

At each time step:

- The asset price can move up by a factor `u`
- Or move down by a factor `d`

The time step is:

- `dt = T / N`

where:

- `S0` is the initial asset price
- `K` is the strike price
- `T` is the maturity
- `N` is the number of steps
- `sigma` is the volatility

Using the CRR model:

- `u = exp(sigma * sqrt(dt))`
- `d = exp(-sigma * sqrt(dt))`

## Absence of Arbitrage Logic

The pricing is based on the principle of absence of arbitrage.

Under the risk-neutral measure, the option value is equal to the discounted expected value of future payoffs.

For equity options with dividend yield `q`, the risk-neutral probability is:

- `p = (exp((r - q) * dt) - d) / (u - d)`

where:

- `r` is the risk-free rate
- `q` is the dividend yield

For forex options, the domestic and foreign rates are used:

- `p = (exp((rd - rf) * dt) - d) / (u - d)`

where:

- `rd` is the domestic risk-free rate
- `rf` is the foreign risk-free rate

## Pricing Logic

At maturity, the option value is equal to its payoff.

For a call option:

- `payoff = max(S - K, 0)`

For a put option:

- `payoff = max(K - S, 0)`

The option price is then computed by backward induction.

For European options:

- `V = discount * (p * V_up + (1 - p) * V_down)`

For American options:

- `V = max(continuation value, intrinsic value)`

This means that for American options, the model checks at each node whether early exercise is optimal.

## Key Features

- Pricing of European call and put options
- Pricing of American call and put options
- Equity option pricing with risk-free rate and dividend yield
- Forex option pricing with domestic and foreign interest rates
- Node-by-node option valuation
- Early exercise logic for American options
- Combined tree output with stock prices and option values on the same lattice

## Why This Matters

Binomial trees are widely used in quantitative finance because they are intuitive and flexible.

They are especially useful for:

- Understanding option pricing step by step
- Valuing American options
- Showing early exercise decisions
- Connecting financial theory to numerical implementation

This project highlights how option prices are built backward from maturity to the initial node using no-arbitrage logic.

## Project Structure

├── binomial_tree.py  
├── requirements.txt  
└── README.md

## Technologies Used

- Python
- NumPy
- Pandas
- Matplotlib

## Example Output

The output shows:

- Final option price
- Up and down factors
- Risk-neutral probability
- Stock price tree
- Option value tree
- Early exercise flags for American options
- Combined graphical tree with stock prices and option values at each node

## Possible Extensions

- Automatic market data input from Yahoo Finance
- Sensitivity analysis for spot, volatility, and maturity
- Root delta and other Greeks
- Pricing for index and commodity options
- Comparison with Black-Scholes for European options
