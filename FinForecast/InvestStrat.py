import pandas as pd

def add_returns(df, return_actual_col=  'actual_rtn', return_predit_col= 'pred_rtn', prediction_col= 'Pred_AC_j+5', actual_col= 'Adj Close'):
    """
    Add actual returns and predicted returns columns computed from actual prices and predicted prices

        Parameters:
        df (pd.DataFrame): DataFrame to add columns to.
        return_actual_col (str): Name of column to be use for actual return values
        return_predit_col (str): Name of column to be use for predicted return values
        prediction_col (str): Name of column containing predicted stock price values
        actual_col (str): Name of column containing actual stock price values
            
    Return:
        df with [return_predit_col] and [return_actual_col] added
    """
    # Rendement prédit
    df[return_predit_col] =  (df[prediction_col] - df[actual_col]) / df[prediction_col]
    # Rendement actuel sur intervale d'une journée
    df[return_actual_col] = df[actual_col].pct_change()

    return df

def AutoLabel(df, return_actual_col= 'actual_rtn', return_predit_col= 'pred_rtn', prediction_col= 'Pred_AC_j+5', hold_count_max = 4):
    """
    Apply investment stratery logic to a DataFrame with predicted stock values + returns,
    to return this DataFrame with position label column.
    
    Parameters:
        df (pd.DataFrame): DataFrame to apply logic to.
        return_actual_col (str): Name of column containing actual return values
        return_predit_col (str): Name of column containing predicted return values
        prediction_col (str): Name of column containing predicted stock price values
        hold_count_max (positive int): Max delay in days to hold position before selling 
            or appearing of a better prediction to reset the hold count.
            
    Return:
        df with ['Position_label'] added
    """
    
    hold_count = 1 # nb de jours depuis la dernière best_predictioniction
    hold_count_max = hold_count_max
    
    return_actual = df[return_actual_col]    
    return_predit = df[return_predit_col]
    
    prediction = df[prediction_col]
    best_prediction = 0
    
    i = 0
    position = 'Hold'
    ls_position = []
    
    while i <= len(df)-1:
        if position == 'Sell' or position == 'Hold':
            # Si la prévision j+5 est positive et le titre a baissé depuis hier
            if return_predit[i] > 0 and return_actual[i] < 0: 
                position = 'Buy' # change la position
                best_prediction = prediction[i] # la pred d'aujourd'hui devient la meilleur pred
                ls_position.append(position)
                i+=1
                continue
            else:
                position = 'Hold'
                ls_position.append(position)
                i+=1
                continue
                
        elif position == 'Buy':
            while hold_count <= hold_count_max:
                # Sortir de la loop quand y'a plus de valeurs
                if i > len(df)-1:
                    break
                # Si la meilleure prediction des 5 derniers jours < que la pred d'aujourd'hui
                if best_prediction < prediction[i]:
                    best_prediction = prediction[i] # la pred d'aujourd'hui devient la meilleur pred
                    hold_count = 1 # réinit le hold_count
                    position = 'Hold' # maintien de la position
                    ls_position.append(position)
                    i+=1
                    continue
                elif hold_count == hold_count_max:
                    position = 'Sell' # limite atteinte, on vend
                    hold_count = 1 # réinit le hold_count
                    ls_position.append(position)
                    i+=1
                    break
                else:
                    # Si la meilleure pred > que la pred d'aujourd'hui
                    # et que le hold_count < 5
                    # garde la pred
                    hold_count += 1 # incrément le hold_count
                    position = 'Hold' # maintien de la position
                    ls_position.append(position)
                    i+=1
                    continue
    
    # Add position labels results to df
    df['Position_label'] = ls_position
    
    return df

def AutoLabel_2(df, close_enough_to_sell= .01, return_actual_col= 'actual_rtn', return_predit_col= 'pred_rtn', 
                prediction_col= 'Pred_AC_j+5', actual_col= 'adjclose', hold_count_max = 4):
    """
    Apply investment stratery logic to a DataFrame with predicted stock values + returns,
    to return this DataFrame with position label column.
    
    Parameters:
        df (pd.DataFrame): DataFrame to apply logic to.
        close_enough_to_sell (float): How close the actual value should be from the best prediction 
            to sell the position at that value instead of waiting a few more days (hold_count_max)
        return_actual_col (str): Name of column containing actual return values
        return_predit_col (str): Name of column containing predicted return values
        prediction_col (str): Name of column containing predicted stock price values
        actual_col (str): Name of column containing actual stock price values of the day
        hold_count_max (positive int): Max delay in days to hold position before selling 
            or appearing of a better prediction to reset the hold count.
            
    Return:
        df with ['Position_label'] added
    """
    
    hold_count = 1 # nb de jours depuis la dernière best_predictioniction
    hold_count_max = hold_count_max
    
    return_actual = df[return_actual_col]    
    return_predit = df[return_predit_col]
    actual = df[actual_col]
    
    i = 0
    position = 'Hold'
    ls_position = []
    
    prediction = df[prediction_col]
    best_prediction = 0
    actual_deviation_from_best_prediction = (best_prediction - actual[i]) / best_prediction
    is_close_enough = bool(actual_deviation_from_best_prediction < close_enough_to_sell)
    
    while i <= len(df)-1:
        if position == 'Sell' or position == 'Hold':
            # Si la prévision j+5 est positive et le titre a baissé depuis hier
            if return_predit[i] > 0 and return_actual[i] < 0: 
                position = 'Buy' # change la position
                best_prediction = prediction[i] # la pred d'aujourd'hui devient la meilleur pred
                ls_position.append(position)
                i+=1
                if i == len(df):
                    continue
                else:
                    actual_deviation_from_best_prediction = (best_prediction - actual[i]) / best_prediction
                    is_close_enough = bool(actual_deviation_from_best_prediction < close_enough_to_sell)
                    continue
            else:
                position = 'Hold'
                ls_position.append(position)
                i+=1
                continue
                
        elif position == 'Buy':
            while hold_count <= hold_count_max:                
                # Sortir de la loop quand y'a plus de valeurs
                if i > len(df)-1:
                    break                
                # Si la valeur atteint la meilleur prédiction plus tôt, on vend plus tôt.
                elif actual[i] > best_prediction or is_close_enough == True:
                    position = 'Sell'
                    hold_count = 1 # réinit le hold_count
                    ls_position.append(position)
                    i+=1
                    break
                # Si la meilleure prediction des 5 derniers jours < que la pred d'aujourd'hui
                elif best_prediction < prediction[i]:
                    best_prediction = prediction[i] # la pred d'aujourd'hui devient la meilleur pred
                    position = 'Hold' # maintien de la position
                    hold_count = 1 # réinit le hold_count
                    ls_position.append(position)
                    i+=1
                    continue
                elif hold_count == hold_count_max:
                    position = 'Sell' # limite atteinte, on vend
                    hold_count = 1 # réinit le hold_count
                    ls_position.append(position)
                    i+=1
                    break
                # Si la meilleure pred > que la pred d'aujourd'hui
                # et que le hold_count < 5
                # garde la pred
                else:
                    hold_count += 1 # incrément le hold_count
                    position = 'Hold' # maintien de la position
                    ls_position.append(position)
                    i+=1
                    continue
    
    # Add position labels results to df
    df['Position_label'] = ls_position
    
    return df


def TradeTest(df, fond= 100, close_value_col= 'Adj Close', position_col= 'Position_label'):
    """
    Test a trade strategy by taking a DataFrame of labeled investment positions and 
    stock prices per instance for a given investment period.
    The fund starts a default 100$ and function return the total of the fund at the end of investing period.

    Parameters:
        df (pd.DataFrame): DataFrame to test trade strategy on.
        fond (int): Initial value of the investment fund.
        close_value_col (str): Name of column containing actual values.
        position_col (str): Name of column containing positions labels.
            
    Return:
        fond (float): Total of the fond at the end of investing period.

    Note:
        If 'buy' was the last position, the total must be adjusted to reflect total assest value (fond +  placement)
    """

    fond = 100
    placement = 0
    valeur_fermeture = df[close_value_col]
    position = df[position_col]
    
    for i in range(len(df)):
        if position[i] == 'Buy':
            # Achat d'une action
            placement = valeur_fermeture[i] 
            # Retrait du coût d'achat du fond
            fond = fond - placement 
        
        elif position[i] == 'Sell': 
            # Vente de l'action
            # (Ajustement de la valeur au moment de la vente seulement)
            placement = valeur_fermeture[i] 
            # Dépôt de la vente au fond
            fond = fond + placement 
    
    return fond
    