import pandas as pd
from scipy.stats import t
from math import sqrt

if __name__ == "__main__":
    # info: pearson correlation
    df = pd.read_csv("https://bit.ly/3mw9AvL", delimiter=",")
    correlations = df.corr(method="pearson")
    print(correlations)

    # info: T-Significant
    n = 10
    lower_cv = t(n - 1).ppf(.025)
    upper_cv = t(n - 1).ppf(0.975)

    r = 0.957586
    test_value = r / sqrt((1-r**2) / (n - 2))

    print("TEST VALUE: {}".format(test_value))
    print(f"CRITICAL RANGE: {lower_cv}, {upper_cv}")

    if test_value < lower_cv or test_value > upper_cv:
        print("CORRELATION PROVEN, REJECT H0")
    else:
        print("CORRELATION NOT PROVEN, FAILED T0 REJECT H0")

    # info: Calculate p-value
    if test_value > 0:
        p_value = 1.0 - t(n - 1).cdf(test_value)
    else:
        p_value = t(n - 1).cdf(test_value)
    p_value = p_value * 2
    print(f"P-VALUE: {p_value}")
