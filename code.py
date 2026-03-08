import numpy as np
import pandas as pd
import matplotlib.pyplot as plt



# INPUTS

data = {
    "asset_type": "equity",      # "equity" or "forex"
    "option_type": "put",        # "call" or "put"
    "style": "european",         # "european" or "american"

    "S0": 50.0,
    "K": 52.0,
    "T": 2.0,
    "sigma": 0.30,
    "N": 10,

    # equity
    "r": 0.05,
    "q": 0.00,

    # forex
    "rd": 0.05,
    "rf": 0.02
}


# PAYOFF

def payoff(S, K, option_type):
    if option_type == "call":
        return max(S - K, 0.0)
    else:
        return max(K - S, 0.0)



# PRICER

def price_binomial(d):
    S0 = d["S0"]
    K = d["K"]
    T = d["T"]
    sigma = d["sigma"]
    N = d["N"]

    asset_type = d["asset_type"].lower()
    option_type = d["option_type"].lower()
    style = d["style"].lower()

    r = d["r"]
    q = d["q"]
    rd = d["rd"]
    rf = d["rf"]

    dt = T / N
    u = np.exp(sigma * np.sqrt(dt))
    d_down = np.exp(-sigma * np.sqrt(dt))

    if asset_type == "forex":
        growth = rd - rf
        discount = np.exp(-rd * dt)
    else:
        growth = r - q
        discount = np.exp(-r * dt)

    p = (np.exp(growth * dt) - d_down) / (u - d_down)

    if p <= 0 or p >= 1:
        raise ValueError("La probabilité risque-neutre p est hors de (0,1).")

   
    # Underlying asset price tree
    
    stock_tree = []
    for i in range(N + 1):
        row = []
        for j in range(i + 1):
            S = S0 * (u ** j) * (d_down ** (i - j))
            row.append(S)
        stock_tree.append(row)


    # Payoff at maturity
   
    values = []
    for S in stock_tree[-1]:
        values.append(payoff(S, K, option_type))

    option_tree = [None] * (N + 1)
    flag_tree = [None] * (N + 1)

    option_tree[N] = values.copy()
    flag_tree[N] = ["PAYOFF"] * len(values)

    
    # Backward Induction
    
    for i in range(N - 1, -1, -1):
        new_values = []
        new_flags = []

        for j in range(i + 1):
            continuation = discount * (p * values[j + 1] + (1 - p) * values[j])

            if style == "american":
                intrinsic = payoff(stock_tree[i][j], K, option_type)

                if intrinsic > continuation:
                    value = intrinsic
                    flag = "EX"
                else:
                    value = continuation
                    flag = ""
            else:
                value = continuation
                flag = ""

            new_values.append(value)
            new_flags.append(flag)

        values = new_values
        option_tree[i] = values.copy()
        flag_tree[i] = new_flags.copy()

    # delta 
    if N >= 1:
        delta_root = (option_tree[1][1] - option_tree[1][0]) / (stock_tree[1][1] - stock_tree[1][0])
    else:
        delta_root = np.nan

    return {
        "price": option_tree[0][0],
        "dt": dt,
        "u": u,
        "d": d_down,
        "p": p,
        "delta_root": delta_root,
        "stock_tree": stock_tree,
        "option_tree": option_tree,
        "flag_tree": flag_tree
    }



# Table content

def summary_table(result, d):
    df = pd.DataFrame({
        "Valeur": [
            d["asset_type"],
            d["option_type"],
            d["style"],
            d["S0"],
            d["K"],
            d["T"],
            d["sigma"],
            d["N"],
            round(result["dt"], 4),
            round(result["u"], 4),
            round(result["d"], 4),
            round(result["p"], 4),
            round(result["delta_root"], 4),
            round(result["price"], 4)
        ]
    }, index=[
        "Asset type",
        "Option type",
        "Style",
        "S0",
        "K",
        "T",
        "sigma",
        "N",
        "dt",
        "u",
        "d",
        "p",
        "Root delta",
        "Option price"
    ])
    return df



# draw tree
# on each noed:
# - up:underlying asset price
# - down:option price
# - EX : early exercise if optimal

def draw_combined_tree(stock_tree, option_tree, flag_tree, title):
    N = len(stock_tree) - 1

    fig, ax = plt.subplots(figsize=(2.6 * (N + 1), 6))
    ax.set_title(title, fontsize=14)
    ax.axis("off")

    pos = {}

    # cordinates
    for i in range(N + 1):
        for j in range(i + 1):
            x = i
            y = 2 * j - i
            pos[(i, j)] = (x, y)

    # branches
    for i in range(N):
        for j in range(i + 1):
            x1, y1 = pos[(i, j)]
            x2, y2 = pos[(i + 1, j)]
            x3, y3 = pos[(i + 1, j + 1)]

            ax.plot([x1, x2], [y1, y2], color="black", linewidth=1.5)
            ax.plot([x1, x3], [y1, y3], color="black", linewidth=1.5)

    # neods and text
    for i in range(N + 1):
        for j in range(i + 1):
            x, y = pos[(i, j)]
            S = stock_tree[i][j]
            V = option_tree[i][j]
            flag = flag_tree[i][j]

            ax.scatter(x, y, s=35, color="black")

            # underlying asset price up
            ax.text(
                x, y + 0.25,
                f"{S:.2f}",
                ha="center", va="bottom",
                fontsize=11
            )

            # option price down
            ax.text(
                x, y - 0.28,
                f"{V:.2f}",
                ha="center", va="top",
                fontsize=11,
                color="darkblue"
            )

            # early exercise
            if flag == "EX":
                ax.text(
                    x + 0.16, y - 0.55,
                    "EX",
                    ha="left", va="top",
                    fontsize=9,
                    color="darkred",
                    fontweight="bold"
                )

    plt.tight_layout()
    plt.show()



# RUN

result = price_binomial(data)
summary = summary_table(result, data)

print("\nFINAL OUTPUT")
print("=" * 50)
print(summary.to_string())

draw_combined_tree(
    result["stock_tree"],
    result["option_tree"],
    result["flag_tree"],
    "Binomial Tree: Stock Price + Option Value"
)
