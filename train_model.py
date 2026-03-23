import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
import joblib

# Load dataset
df = pd.read_csv("purchase_regret_dataset.csv")

# Encode categorical columns
le = LabelEncoder()
for col in ["Mood","Urgency_Level","Brand_Familiarity","Purchase_Category","Peer_Influence"]:
    df[col] = le.fit_transform(df[col])

# Features and target
X = df.drop("Regret", axis=1)
y = df["Regret"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save model
joblib.dump(model, "regret_model.pkl")

print("Model trained and saved.")
