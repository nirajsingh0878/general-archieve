# train_model.py (Run this once to create your model file)
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
import os

# Load a sample dataset
iris = load_iris()
X, y = iris.data, iris.target

# Train a simple model
model = LogisticRegression(max_iter=200) # Increased max_iter for convergence
model.fit(X, y)

# Ensure the models directory exists
models_dir = 'app/models'
os.makedirs(models_dir, exist_ok=True)

# Save the model
model_path = os.path.join(models_dir, 'my_model.pkl')
with open(model_path, 'wb') as f:
    pickle.dump(model, f)
print(f"Model trained and saved to {model_path}")