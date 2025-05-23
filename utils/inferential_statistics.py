import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from scipy.stats import norm
from scipy.stats import ttest_ind, mannwhitneyu




class IndependentGroupsAnalysis:
    """
    Analyse the difference between two independent groups.

     This class performs:
    - Welch's T-Test or Mann-Whitney U Test for hypothesis testing
      (Welch's assumes normality and unequal variance; Mann-Whitney is non-parametric)
    - Cohen's d or Cliff's Delta for effect size estimation
    - Histogram plotting to visualize group differences

    Interpretation:
    - Cohen's d: Measures how many standard deviations apart the group means are.
      (0.2 = small, 0.5 = medium, 0.8 = large effect)
    - Cliff's Delta: Measures the probability that one group will have higher values than another.
      (0.1 = small, 0.3 = medium, 0.5+ = large effect)
    """

    def __init__(self):
        pass

    def load_data(
        self, group_a: np.ndarray, group_b: np.ndarray, alpha: float = 0.05
    ) -> None:
        """
        Load the data for both groups and define the significance level.

        Parameters:
        - group_a: np.ndarray - Data for group A
        - group_b: np.ndarray - Data for group B
        - alpha: float - Significance level for the hypothesis test (default 0.05)
        """
        self.group_a = np.array(group_a)
        self.group_b = np.array(group_b)
        self.alpha = alpha
        self.mean_a = np.mean(self.group_a)
        self.mean_b = np.mean(self.group_b)
        self.median_a = np.median(self.group_a)
        self.median_b = np.median(self.group_b)

    def _manwhitney(self):
        """
        Perform the Mann-Whitney U test, a non-parametric alternative to the t-test.
        Stores U-statistic and p-value.
        """
        self.mu_U, self.p_value = mannwhitneyu(
            self.group_a, self.group_b, alternative="two-sided"
        )

    def _cliffs_delta(self) -> None:
        """
        Fast Cliff's Delta using NumPy broadcasting (O(n log n)).
        Compute Cliff's Delta effect size, a non-parametric alternative to Cohen's d.
        It measures the probability that one group tends to have larger values than the other.

        """
        a = self.group_a
        b = self.group_b
        n = len(a) * len(b)

        # Use numpy broadcasting to speed up comparisons
        diff_matrix = np.subtract.outer(a, b)
        greater = np.sum(diff_matrix > 0)
        less = np.sum(diff_matrix < 0)

        self.cliff_delta_effect_size = round((greater - less) / n, 3)

    def _welch_t_test(self) -> None:
        """
        Perform Welch's t-test (for unequal variances) on the two groups.
        Stores t-statistic and p-value.
        """
        self.t_stat, self.p_value = ttest_ind(
            self.group_a, self.group_b, equal_var=False, alternative="two-sided"
        )

    def _cohen_d(self) -> None:
        """
        Perform Welch's t-test (for unequal variances) on the two groups.
        Stores t-statistic and p-value.
        """
        self.mean_difference = self.mean_a - self.mean_b
        self.group_a_var = np.var(self.group_a, ddof=1)
        self.group_b_var = np.var(self.group_b, ddof=1)
        self.pooled_std = np.sqrt((self.group_a_var + self.group_b_var) / 2)
        self.cohen_d_effect_size = round(self.mean_difference / self.pooled_std, 3)

    def test_groups(self) -> None:
        """
        Run Welch's t-test and compute Cohen's d.
        """
        self._welch_t_test()
        self._cohen_d()

    def test_non_parametric_groups(self) -> None:
        """
        Run Mann-Whitney U test and compute Cliff's Delta.
        """
        self._manwhitney()
        self._cliffs_delta()

    def summarise_mu(self) -> None:
        print(self.p_value, self.mu_U)

    def summarise(self) -> None:
        """
        Print a summary of the t-test and effect size results.
        """
        print("=" * 60)
        print(f"Group A mean: {self.mean_a:.3f} | Group B mean: {self.mean_b:.3f}")
        if hasattr(self, "t_stat") and self.t_stat is not None:
            print(f"t-statistic: {self.t_stat:.3f}")
        else:
            print(f"U-statistic: {self.mu_U:.3f}")

        if (
            hasattr(self, "cohen_d_effect_size")
            and self.cohen_d_effect_size is not None
        ):
            print(f"Cohen's d (effect size): {self.cohen_d_effect_size}")
        else:
            print(f"Cliff's Delta (effect size): {self.cliff_delta_effect_size}")

        if self.p_value < self.alpha:
            print("✅ Statistically significant difference between groups.")
        else:
            print("❌ No statistically significant difference between groups.")
        print("=" * 60)

    def describe(self) -> str:
        """
        Print basic descriptive statistics for both groups.
        """
        from scipy.stats import skew, kurtosis

        print("Descriptive Statistics:\n" + "=" * 60)
        for label, group in zip(["Group A", "Group B"], [self.group_a, self.group_b]):
            print(f"{label}:")
            print(f"  Min      : {min(group):.3f}")
            print(f"  Max      : {max(group):.3f}")
            print(f"  n        : {len(group):.3f}")
            print(f"  Mean     : {np.mean(group):.3f}")
            print(f"  Median   : {np.median(group):.3f}")
            print(f"  Std Dev  : {np.std(group, ddof=1):.3f}")
            print(f"  Skew     : {skew(group):.3f}")
            print(f"  Kurtosis : {kurtosis(group):.3f}")
            print("-" * 60)

    def results(self) -> dict:
        """
        Return a dictionary of the statistical test results.

        Returns:
        - dict with t_statistic, p_value, cohen_d, mean_group_a, mean_group_b
        """
        return {
            "t_statistic": self.t_stat,
            "p_value": self.p_value,
            "cohen_d": self.cohen_d_effect_size,
            "mean_group_a": self.mean_a,
            "mean_group_b": self.mean_b,
        }

    def results_mu(self) -> dict:
        """
        Returns a dictionary of the statistical test

        Returns:
        - dict with U statistic, p_value, cliff's delta,median_group_a, median_group_b
        """
        return {
            "mannwhitney_u": self.mu_U,
            "p_value": self.p_value,
            "cliffs_delta": self.cliff_delta_effect_size,
            "median_group_b": self.median_a,
            "median_group_b": self.median_b,
        }

    def plot_distributions(
        self,
        label_a="Group A",
        label_b="Group B",
        xlabel="Value",
        title="Distribution of Values by Category (t-test)",
        density: bool = True,
    ) -> None:
        """
        Plot histogram of the distributions for both groups.

        Parameters:
        - label_a: str - Label for group A
        - label_b: str - Label for group B
        - xlabel: str - X-axis label
        - title: str - Plot title
        """
        sns.set_theme(style="whitegrid")

        fig, ax = plt.subplots(figsize=(9, 6))

        ax.hist(
            self.group_a,
            edgecolor="white",
            alpha=0.8,
            label=label_a,
            density=density,
            bins=int(np.sqrt(len(self.group_a) + len(self.group_b))),
        )
        ax.hist(
            self.group_b,
            edgecolor="white",
            alpha=0.4,
            label=label_b,
            density=density,
            bins=int(np.sqrt(len(self.group_a) + len(self.group_b))),
        )

        if hasattr(self, "cohen_d_effect_size"):
            stat_label = f"t-value: {self.t_stat:.3f}"
            effect_label = f"Effect Size d = {self.cohen_d_effect_size:.3f}"
        else:
            stat_label = f"U-statistic: {self.mu_U:.3f}"
            effect_label = f"Cliff's Delta = {self.cliff_delta_effect_size:.3f}"

        ax.text(
            0.02,
            0.95,
            f"p-value: {self.p_value:.3f}\n" f"{stat_label}\n" f"{effect_label}",
            transform=ax.transAxes,
            fontsize=12,
            fontweight="bold",
            verticalalignment="top",
            bbox=dict(
                boxstyle="round,pad=0.3", facecolor="white", edgecolor="grey", alpha=0.6
            ),
        )

        ax.set_title(title, fontsize=14, weight="bold")
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel("", fontsize=12)
        ax.legend(title="Group")

        sns.despine()

        plt.tight_layout()
        plt.show()

