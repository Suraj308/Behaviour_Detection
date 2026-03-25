#Import

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# LOAD DATASET

df = pd.read_csv("synthetic_behavior_dataset.csv")

print("Dataset Shape:", df.shape)
print("\nFirst 5 Rows:\n", df.head())


# DATA INSPECTION

print("\nSummary Statistics:\n", df.describe())
print("\nColumns:\n", df.columns)

# BEHAVIOR VALIDATION

print("\nBehavior Validation (Group Means):\n")

validation = df.groupby("decision_change")[[
    "stress_total",
    "confidence_total",
    "hesitation_total",
    "cunning_total"
]].mean()

print(validation)

# VISUALIZATION

# Stress distribution
plt.hist(df["stress_total"], bins=30)
plt.title("Stress Distribution")
plt.xlabel("Stress")
plt.ylabel("Frequency")
plt.show()


# Confidence distribution
plt.hist(df["confidence_total"], bins=30)
plt.title("Confidence Distribution")
plt.xlabel("Confidence")
plt.ylabel("Frequency")
plt.show()

# Stay vs Switch
#Stress
plt.hist(df[df["decision_change"]==0]["stress_total"], bins=30, alpha=0.5, label="Stay")
plt.hist(df[df["decision_change"]==1]["stress_total"], bins=30, alpha=0.5, label="Switch")

plt.legend()
plt.title("Stress Comparison")
plt.show()

#Confidence
plt.hist(df[df["decision_change"]==0]["confidence_total"], bins=30, alpha=0.5, label="Stay")
plt.hist(df[df["decision_change"]==1]["confidence_total"], bins=30, alpha=0.5, label="Switch")

plt.legend()
plt.title("Confidence Comparison")
plt.show()
