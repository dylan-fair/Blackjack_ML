import pandas as pd
import tensorflow as tf

def model_decision(dealer_card, player_value, count, num_hits):
    model = tf.keras.models.load_model('basic_model_highlow.keras')
    
    d = {'dealer_card':[dealer_card], 'player_initial_value':[player_value], 'hit':[1], 'count':[count], 'num_hits': [num_hits]} 
    input_df = pd.DataFrame(data=d)
    prediction = model.predict(input_df)
    if prediction > 0.48:
        return 1
    else:
        return 0
