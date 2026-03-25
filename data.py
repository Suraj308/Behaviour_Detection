import numpy as np
import pandas as pd

np.random.seed(42)

# -----------------------------
# sigmoid probability function
# -----------------------------
def sigmoid(x):
    return 1 / (1 + np.exp(-x))


# -----------------------------
# personality types
# -----------------------------
player_types = ["honest", "strategic", "nervous", "confident"]

# -----------------------------
# stress patterns
# -----------------------------
stress_patterns = [
    "stable",
    "increase",
    "decrease",
    "panic_final",
    "early_stress"
]


# ------------------------------------------------
# generate correlated facial signals for phase 1
# ------------------------------------------------
def generate_phase1(player):

    # hidden emotional states
    stress_base = np.random.normal(0.30, 0.08)
    confidence_base = np.random.normal(0.60, 0.10)
    strategic_bias=0

    if player == "honest":
        confidence_base += 0.15
        stress_base -= 0.05

    elif player == "strategic":
        strategic_bias=0.08
        stress_base += 0.05
        if np.random.rand()<0.5:
            confidence_base += np.random.normal(0.75,0.08)
        else:
            confidence_base += np.random.normal(0.45,0.12)

    elif player == "nervous":
        stress_base += 0.15
        confidence_base -= 0.10

    elif player == "confident":
        confidence_base += 0.20
        stress_base -= 0.10

    # correlated signals
    blink_rate = abs(np.random.normal(0.25 + 0.6*stress_base, 0.05))
    brow_tension = abs(np.random.normal(0.20 + 0.5*stress_base + strategic_bias, 0.04))
    mouth_tension = abs(np.random.normal(0.20 + 0.4*stress_base, 0.05))
    gaze_variance = abs(np.random.normal(0.10 + 0.5*stress_base +strategic_bias, 0.04))

    gaze_stability = abs(np.random.normal(0.60 + 0.4*confidence_base, 0.05))
    head_motion = abs(np.random.normal(0.15 - 0.10*confidence_base, 0.03))

    blink_variance = abs(np.random.normal(0.05 + 0.3*stress_base, 0.02))


    lip_compression = abs(np.random.normal(0.20 + 0.3*stress_base + strategic_bias, 0.05))

    facial_expression_stability = abs(np.random.normal(0.70 + 0.2*confidence_base, 0.08))

    stress_mean = abs(stress_base)
    stress_variance = abs(np.random.normal(0.05 + 0.2*stress_base, 0.02))
    stress_slope = abs(np.random.normal(0.03 + 0.2*stress_base, 0.02))

    return {
        "blink_rate": blink_rate,
        "blink_variance": blink_variance,
        "brow_tension": brow_tension,
        "lip_compression": lip_compression,
        "mouth_tension": mouth_tension,
        "gaze_stability": gaze_stability,
        "gaze_variance": gaze_variance,
        "head_motion": head_motion,
        "facial_expression_stability": facial_expression_stability,
        "stress_mean": stress_mean,
        "stress_variance": stress_variance,
        "stress_slope": stress_slope
    }


# ------------------------------------------------
# temporal drift for phase evolution
# ------------------------------------------------
def drift_signals(previous):

    new = {}

    for k, v in previous.items():
        drift = np.random.normal(0, 0.02)
        new[k] = np.clip(v+drift,0,1)

    return new


# ------------------------------------------------
# apply stress pattern across phases
# ------------------------------------------------
def apply_stress_pattern(pattern, s1, s2, s4):

    if pattern == "increase":
        s2["blink_rate"] += 0.05
        s4["blink_rate"] += 0.08
        s2["brow_tension"] += 0.04
        s4["brow_tension"] += 0.06

    elif pattern == "decrease":
        s2["blink_rate"] -= 0.03
        s4["blink_rate"] -= 0.05

    elif pattern == "panic_final":
        s4["blink_rate"] += 0.10
        s4["brow_tension"] += 0.10

    elif pattern == "early_stress":
        s1["blink_rate"] += 0.08
        s2["blink_rate"] += 0.05

    return s1, s2, s4


# ------------------------------------------------
# trait calculations (your formulas)
# ------------------------------------------------
def compute_traits(s):

    confidence = (
        0.35*s["gaze_stability"]
        -0.25*s["blink_rate"]
        -0.20*s["head_motion"]
        -0.20*s["mouth_tension"]
    )

    honesty = (
        0.40*s["facial_expression_stability"]
        +0.30*s["gaze_stability"]
        -0.20*s["stress_variance"]
        -0.10*s["blink_variance"]
    )

    cunning = (
        0.35*s["brow_tension"]
        +0.30*s["lip_compression"]
        +0.20*s["blink_variance"]
        +0.15*s["gaze_variance"]
    )

    stress = (
        0.30*s["blink_rate"]
        +0.30*s["brow_tension"]
        +0.20*s["mouth_tension"]
        +0.20*s["stress_slope"]
    )

    hesitation = (
        0.30*s["blink_variance"]
        +0.30*s["gaze_variance"]
        +0.20*s["head_motion"]
        +0.20*s["mouth_tension"]
    )

    return confidence, honesty, cunning, stress, hesitation


# ------------------------------------------------
# dataset generation
# ------------------------------------------------
rows = []

for _ in range(10000):

    player = np.random.choice(player_types)
    pattern = np.random.choice(stress_patterns)

    # phase 1
    s1 = generate_phase1(player)

    # phase 2 (temporal drift)
    s2 = drift_signals(s1)

    # phase 4 (drift again)
    s4 = drift_signals(s2)

    # apply stress pattern
    s1, s2, s4 = apply_stress_pattern(pattern, s1, s2, s4)

    # compute traits
    c1,h1,cu1,st1,he1 = compute_traits(s1)
    c2,h2,cu2,st2,he2 = compute_traits(s2)
    c4,h4,cu4,st4,he4 = compute_traits(s4)

    # behavioral shift
    c3 = c2 - c1
    st3 = st2 - st1
    he3 = he2 - he1

    # combine phases
    confidence_total = 0.4*c1 + 0.2*c2 + 0.2*c3 + 0.2*c4
    honesty_total = 0.4*h1 + 0.2*h2 + 0.2*h2 + 0.2*h4
    cunning_total = 0.4*cu1 + 0.2*cu2 + 0.2*cu2 + 0.2*cu4
    stress_total = 0.4*st1 + 0.2*st2 + 0.2*st3 + 0.2*st4
    hesitation_total = 0.4*he1 + 0.2*he2 + 0.2*he3 + 0.2*he4

    # probability
    P_change = sigmoid(
    0.9 * cunning_total +
    1.1 * stress_total +
    0.8 * hesitation_total -
    1.0 * confidence_total -
    0.7 * honesty_total -
    0.2

    )

    # irrational random switching
    irrational_prob = np.random.uniform(0.03,0.07)
    if np.random.rand() < irrational_prob:
        decision_change = np.random.choice([0,1])
    else:
        decision_change = np.random.binomial(1, P_change)

    row = {
        **s1,
        "confidence_total": confidence_total,
        "honesty_total": honesty_total,
        "cunning_total": cunning_total,
        "stress_total": stress_total,
        "hesitation_total": hesitation_total,
        "P_change": P_change,
        "decision_change": decision_change
    }

    rows.append(row)


df = pd.DataFrame(rows)

df.to_csv("synthetic_behavior_dataset.csv", index=False)

print("Dataset generated:", df.shape)