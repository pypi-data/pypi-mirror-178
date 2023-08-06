import itertools
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats

def tukey_outliers(df, var, distance=3, mode="print"):
    """Function to identify outliers using the Tukey method.
    Args:
        df (pandas dataframe): Dataframe containing the variable of interest.
        var (str): Name of the variable of interest.
        distance (int): Distance from the median to use as the threshold for outliers. Default is 3.
        mode (str): Whether to print the outliers or return them as a list. Default is "print".
    Returns:
        list: List of outliers if mode is "return". Otherwise, None.
    """

    q1 = df[var].quantile(0.25)
    q3 = df[var].quantile(0.75)

    iqr = q3-q1
    outlier_lower = q1 - (iqr*distance)
    outlier_upper = q3 + (iqr*distance)
    mask_outlier = (df[var] < outlier_lower) | (df[var] > outlier_upper)
    if mode == "print":
        print(
            f"25th Percentile (Q1): {q1:.2f}\n75th Percentile (Q3): {q3:.2f}\nIQR: {iqr:.2f}")
        print(
            f"Will count cases as outlier with values less than {outlier_lower:.2f} or more than {outlier_upper:.2f}.")
        if df[mask_outlier].shape[0] == 0:
            print("With these criteria there are no outlier in the data")
        else:
            print("Showing outliers")
            print(df[mask_outlier][var].to_string())
    elif mode == "return":
        return list(df[mask_outlier][var].index.values)
    else:
        print("Mode must be 'print' or 'return'")


def qqs_over_groups_and_vars(df, group_label, vars_li, size=(15, 15)):
    """Function to plot QQ subplots for each variable in a list of variables, over groups in a categorical variable.
    Args:
        df (pandas dataframe): Dataframe containing the variables of interest.
        group_label (str): Name of the categorical variable to group by.
        vars_li (list): List of variables to plot.
        size (tuple): Size of the plot to draw subplots in. Default is (15, 15).
    Returns:
           None 
        """
    groups_li = df[group_label].unique()
    fig, axes = plt.subplots(len(groups_li), len(vars_li), figsize=size)
    fig.tight_layout(pad=5.0)
    plt.grid(False)

    x = 0
    y = 0
    for group, var in itertools.product(groups_li, vars_li):
        stats.probplot(df[df[group_label] == group][var],
                       dist="norm", plot=axes[y, x])
        axes[y, x].set_title(group + " - " + var)
        if x < (len(vars_li)-1):
            x += 1
        else:
            x = 0
            y += 1


def check_homoscedacity(y_var, group_var, df):
    """Function to check for homoscedacity using heuristics recommended by Blanca et al. (2018).
    Args:
        y_var (str): Name of the dependent variable.
        group_var (str): Name of the independent categorical variable to check homoscedasticity for.
        df (pandas dataframe): Dataframe containing the variables of interest.
    Returns:
        None 
    """

    var_ser = pd.Series(index=df[group_var].unique(), dtype=float)

    for group in df[group_var].unique():
        var_ser[group] = df[df[group_var] == group][y_var].var()

    min_var = (var_ser.idxmin(), var_ser.min())
    max_var = (var_ser.idxmax(), var_ser.max())
    var_ratio = max_var[1]/min_var[1]
    print(f"Smallest variance for {min_var[0]}: {min_var[1]:.2f}")
    print(f"Largest variance for {max_var[0]}: {max_var[1]:.2f}")
    print(f"Variance ratio: {var_ratio:.2f}")

    if var_ratio <= 1.5:
        print("Variance ratio is <= 1.5, F-test will be robust.")
        return
    else:
        print("Variance ratio is > 1.5. Now doing additional checks to see if F-test is robust.")

    # Create dataframe with variance and group sizes
    var_n_df = var_ser.to_frame(name="var")
    var_n_df["n"] = df.value_counts(subset=group_var)
    # get correlation between correlation and variance
    corr_var_n = var_n_df[["var", "n"]].corr().iloc[1, 0]

    if (corr_var_n >= 0) and (corr_var_n <= 0.5):
        print(
            f"Correlation between sample size and variance (pairing) is {corr_var_n:.2f}."
            f" That is between 0 and .5. F-test should be robust")
        return
    else:
        print(
            f"Correlation between sample size and variance (pairing) is {corr_var_n:.2f}.")

    # Compute coefficient of sample size variation
    coeff_n = var_n_df["var"].std()/var_n_df["var"].mean()
    if (corr_var_n > 0.5) and (coeff_n > .33) and (var_ratio > 2):
        print(f"Pairing is {corr_var_n:.2f}, so larger than .5."
              f" The coefficient of sample size variation is {coeff_n:.2f}, larger than .33."
              f" The variance ratio is {var_ratio:.2f}, larger than 2."
              f" F-test is too conserative (hurting power)")
    elif (corr_var_n < 0) and (corr_var_n >= -0.5) and (coeff_n > .16) and (var_ratio > 2):
        print(f"Pairing is {corr_var_n:.2f}, so smaller than 0 and larger than or equal to -.5."
              f" The coefficient of sample size variation is {coeff_n:.2f}, larger than .16."
              f" The variance ratio is {var_ratio:.2f}, larger than 2."
              f" F-test is too liberal (real alpha might be as high as .1 if variance ratio is 9 or smaller).")
    elif (corr_var_n < -0.5):
        print(f"Pairing is {corr_var_n:.2f}, so smaller than -.5."
              f" F-test is too liberal (real alpha might be as high as .2 if variance ratio is 9 or smaller).")
    else:
        print(
            f"Pairing is {corr_var_n:.2f}, coefficient of sample size variation is {coeff_n:.2f},"
            f" and the variance ratio is {var_ratio:.2f}."
            f" This specific combination should have robust F-test, but look into the paper",
            f" ('Effect of variance ratio on ANOVA robustness: Might 1.5 be the limit?', Blanca et al., 2018)",
            f" to be sure."
            )
