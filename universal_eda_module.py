import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from markdown import markdown

# ========== Natural Language Formatter ========== #
def generate_natural_summary(conditions, df, label_encoders):
    desc_parts = []
    for feature, op, thresh in conditions:
        thresh = float(thresh)
        if feature in label_encoders:
            le = label_encoders[feature]
            values = df[feature].unique()
            if op == "<=":
                matched = [v for v in values if v <= thresh]
            else:
                matched = [v for v in values if v > thresh]
            labels = le.inverse_transform(sorted(set(matched)))
            desc_parts.append(f"{feature.capitalize()} is one of: {', '.join(labels)}")
        elif df[feature].nunique() <= 10:
            vals = [v for v in df[feature].unique() if v <= thresh] if op == "<=" else [v for v in df[feature].unique() if v > thresh]
            desc_parts.append(f"{feature.capitalize()} in {list(map(int, vals))}")
        else:
            if "age" in feature.lower():
                age_label = "younger" if op == "<=" else "older"
                desc_parts.append(f"{feature.capitalize()} {op} {thresh:.1f} ({age_label})")
            else:
                desc_parts.append(f"{feature.capitalize()} {op} {thresh:.1f}")
    return "; ".join(desc_parts)

# ========== Trend Detection ========== #
def print_trend_insights(df, target_col):
    insights = []
    for col in df.select_dtypes(include=['object', 'category', 'bool', 'int64']).columns:
        if col == target_col or df[col].nunique() > 10:
            continue
        means = df.groupby(col)[target_col].mean().sort_values()
        if means.is_monotonic_increasing:
            insights.append(f"✅ {target_col.title()} increases with {col}")
        elif means.is_monotonic_decreasing:
            insights.append(f"🔻 {target_col.title()} decreases with {col}")
        else:
            top = means.idxmax()
            insights.append(f"⭐ Highest {target_col} for {col} = {top} ({means.max():.2f})")
    return insights

# ========== Tree Rule Tracer ========== #
def trace_tree_path(model, X, leaf_id):
    tree = model.tree_
    feature_names = X.columns
    path = []

    def recurse(node, path):
        if node == leaf_id or tree.feature[node] == -2:
            return path
        feature = feature_names[tree.feature[node]]
        thresh = tree.threshold[node]
        left = tree.children_left[node]
        right = tree.children_right[node]
        if leaf_id in get_leaves(left):
            return recurse(left, path + [(feature, "<=", thresh)])
        else:
            return recurse(right, path + [(feature, ">", thresh)])

    def get_leaves(node):
        if tree.children_left[node] == -1:
            return [node]
        return get_leaves(tree.children_left[node]) + get_leaves(tree.children_right[node])

    return recurse(0, [])

# ========== Universal EDA Engine ========== #
def universal_eda_best_worst(path, target_col):
    output_lines = []
    df = pd.read_csv(path) if path.endswith('.csv') else pd.read_excel(path, engine='openpyxl')
    df = df.dropna(subset=[target_col])
    df_copy = df.copy()

    output_lines.append(f"# Universal EDA Report\n\n**Target**: {target_col}")

    # Task Type Detection
    is_classification = df[target_col].nunique() <= 20 and df[target_col].dtype in ['int64', 'object', 'bool', 'category']
    task = "classification" if is_classification else "regression"
    output_lines.append(f"\n**Detected task**: {task.title()}")

    # Label Encoding
    label_encoders = {}
    for col in df_copy.select_dtypes(include=['object', 'category', 'bool']):
        le = LabelEncoder()
        df_copy[col] = le.fit_transform(df_copy[col].astype(str))
        label_encoders[col] = le

    # Drop Unusable Features
    redundant = []
    for col in df_copy.columns:
        if col == target_col:
            continue
        if df_copy[col].nunique() <= 1 or df_copy[col].equals(df_copy[target_col]) or df_copy[col].nunique() > len(df_copy) * 0.5:
            redundant.append(col)

    if redundant:
        output_lines.append(f"\n**Dropped columns**: {', '.join(redundant)}")
        df_copy = df_copy.drop(columns=redundant)

    X = df_copy.drop(columns=[target_col])
    y = df_copy[target_col]

    # ==== EDA Takeaways ==== #
    output_lines.append("\n## EDA Takeaways")
    for col in X.columns:
        if df_copy[col].nunique() <= 10:
            group = df_copy.groupby(col)[target_col].mean()
            for val in group.index:
                val_label = label_encoders[col].inverse_transform([val])[0] if col in label_encoders else val
                msg = f"- When {col} = {val_label}, average {target_col} = {group[val]:.2f}"
                output_lines.append(msg)

    # ==== Trend Insights ==== #
    insights = print_trend_insights(df, target_col)
    output_lines.append("\n## 📈 Trend Insights")
    output_lines.extend(insights)

    # ==== Train Decision Tree ==== #
    model = DecisionTreeClassifier(max_depth=3) if is_classification else DecisionTreeRegressor(max_depth=3)
    X_train, _, y_train, _ = train_test_split(X, y, test_size=0.3, random_state=42)
    model.fit(X_train, y_train)

    leaf_ids = model.apply(X_train)
    leaf_scores = {}
    for leaf in np.unique(leaf_ids):
        leaf_y = y_train[leaf_ids == leaf]
        leaf_scores[leaf] = (
            leaf_y.value_counts(normalize=True).max() if is_classification else leaf_y.mean()
        )

    best_leaf = max(leaf_scores, key=leaf_scores.get)
    worst_leaf = min(leaf_scores, key=leaf_scores.get)

    # ==== Best & Worst Scenario ==== #
    best_conditions = trace_tree_path(model, X_train, best_leaf)
    worst_conditions = trace_tree_path(model, X_train, worst_leaf)

    best_desc = generate_natural_summary(best_conditions, df_copy, label_encoders)
    worst_desc = generate_natural_summary(worst_conditions, df_copy, label_encoders)

    output_lines.append(f"\n### ✅ Best-Case Scenario:\n- {best_desc}\n- Outcome: **{leaf_scores[best_leaf]:.2f}**")
    output_lines.append(f"\n### ❌ Worst-Case Scenario:\n- {worst_desc}\n- Outcome: **{leaf_scores[worst_leaf]:.2f}**")

    # ==== Save Markdown Summary ==== #
    with open("eda_summary.md", "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))

    # ==== Visualizations ==== #
    for col in X.columns:
        if df[col].nunique() <= 10:
            plt.figure(figsize=(6, 4))
            sns.barplot(x=col, y=target_col, data=df)
            plt.title(f"{target_col.title()} by {col}")
            plt.tight_layout()
            filename = re.sub(r'[^\w_.-]', '_', f"{col}_barplot.png")
            plt.savefig(filename)
            plt.close()