import pandas as pd
import random
import pickle
from sklearn.ensemble import RandomForestClassifier

def generate_dataset(n=3000):
    data = []

    for _ in range(n):
        age = random.randint(18, 65)
        session = random.uniform(1, 60)
        pages = random.randint(1, 25)
        purchase = random.uniform(0, 1000)
        mobile = random.choice([0, 1])

        # 🔥 IMPROVED LOGIC (balanced data)
        if session < 10 or pages < 5 or purchase < 100:
            churn = 1
        else:
            churn = 0

        data.append([
            age,
            session / 60,
            pages,
            purchase / 1000,
            mobile,
            churn
        ])

    df = pd.DataFrame(data, columns=[
        "age",
        "session_duration",
        "pages_visited",
        "purchase_amount",
        "is_mobile",
        "churn"
    ])

    return df

# Generate dataset
df = generate_dataset()

# Split features and target
X = df.drop("churn", axis=1)
y = df["churn"]

# Train model
model = RandomForestClassifier(n_estimators=150, max_depth=8)
model.fit(X, y)

# Save model
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

print("🔥 Model retrained successfully with balanced data!")