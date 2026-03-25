import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix , accuracy_score


# LOAD DATASET

df = pd.read_csv("synthetic_behavior_dataset.csv")

# PREPARE DATA

X = df.drop(["decision_change", "P_change"], axis=1)
y = df["decision_change"]


# TRAIN-TEST SPLIT

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# TRAIN MODEL
model = RandomForestClassifier(
    n_estimators=300,
    max_depth=8,
    min_samples_split=5,
    random_state=42
)


model.fit(X_train, y_train)

# MODEL EVALUATION

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)
print("\nModel Accuracy:", accuracy)

# CONFUSION MATRIX
cm = confusion_matrix(y_test, y_pred)

print("\nConfusion Matrix:\n", cm)

# SAMPLE PREDICTION

num_samples = 5
threshold = 0.45

print("\n===== SAMPLE PREDICTIONS =====\n")

for i in range(num_samples):

    # select sample
    sample = X_test.iloc[i].values.reshape(1, -1)

    # actual value
    actual = y_test.iloc[i]

    # probabilities
    probs = model.predict_proba(sample)[0]
    prob_stay = probs[0]
    prob_change = probs[1]

    # prediction using threshold
    prediction = 1 if prob_change > threshold else 0

    # correctness check
    correct = "✅ Correct" if prediction == actual else "❌ Wrong"

    print(f"Sample {i+1}")
    print(f"Probability → Stay: {prob_stay:.3f}, Change: {prob_change:.3f}")
    print(f"Predicted: {prediction} | Actual: {actual} → {correct}")

    # interpretation
    if prob_change > 0.7:
        print("Interpretation: High likelihood of switching (strong behavioral signals)")
    elif prob_change > 0.5:
        print("Interpretation: Moderate likelihood of switching")
    else:
        print("Interpretation: Likely to remain committed")

    print("-" * 50)