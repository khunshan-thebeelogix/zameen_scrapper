import pandas as pd
from sklearn.preprocessing import LabelEncoder
import pickle



# Load the saved model
with open('model_week.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

# Load the label encoder
with open('label_encoder.pkl', 'rb') as file:
    label_encoder = pickle.load(file)


def predict_price():
    # Get the request data
    # data = request.get_json()
    new_data = pd.DataFrame({
        'location': ['DHA'],
        'area': [10],
        'week': [3]  # Update the week numbers accordingly
    })

    # Example: Predict prices for new weekly data
    new_data = pd.DataFrame(new_data)

    # Preprocess the new data
    new_data['area'] = new_data['area']
    new_data['location_encoded'] = label_encoder.transform(new_data['location'])
    X_new = new_data[['location_encoded', 'area', 'week']]

    # Make predictions
    predicted_prices = loaded_model.predict(X_new)
    new_data['predicted_price'] = predicted_prices

    # Format the predicted prices
    new_data['predicted_price'] = new_data['predicted_price'].map('{:,.2f}'.format)

    # Prepare the response
    response = {
        'predictions': new_data[['location', 'area', 'week', 'predicted_price']].to_dict(orient='records')
    }

    print(response)

predict_price()