from statsmodels.tsa.arima.model import ARIMA
import backtrader as bt
from __future__ import (absolute_import, division, print_function,unicode_literals)
from FinForecast import ArimaForecast as af


class strat_simple(bt.Strategy):

    def __init__(self, close_enough_to_sell= .01, hold_count_max = 4):
        
        self.hold_count = 1 # nb de jours depuis la dernière best_predictioniction
        self.hold_count_max = hold_count_max
        self.best_prediction = 0
        self.actual_deviation_from_best_prediction = 0
        self.is_close_enough = bool(actual_deviation_from_best_prediction < close_enough_to_sell)

    def log(self, txt):
        ''' Logging function for this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('{0}: {1}'.format(dt.isoformat(), txt))
    
    def next(self):
        
        self.actual_deviation_from_best_prediction = (best_prediction - actual[i]) / best_prediction
        self.position = self.data.position_label[0]
        self.buy_count = self.data.buy_count[0]
        self.return_prediction = self.data.pred_rtn[0]
        self.return_actual = self.data.actual_rtn[0]

        self.log('Close_ {:.2f}'.format(self.data.close[0]))

        if self.position == 1:
            self.log('BUY CREATE_ {:.2f}'.format(self.data.close[0]))
            self.buy(size= self.buy_count)

        elif self.position == 2:
            self.log('SELL ALL_ {:.2f}'.format(self.data.close[0]))
            self.close()

        else:
            pass


class Strat_1d(bt.Strategy):
   
    def __init__(self, ARIMA_order= (1,0,1), window_size= 100):
        
        rolling_window = self.dataclose[0:-1*(window_size)])
        self.arima_forcast = af.arima_forecast(rolling_window, ARIMA_order)

    def log(self, txt, dt=None, doprint=False):
        
        if self.params.printlog or doprint: # Add if statement to only log of printlog or doprint is True
            dt = dt or self.datas[0].datetime.date(0)
            print('{0},{1}'.format(dt.isoformat(),txt))


    def next(self, close_enough_to_sell= .01, hold_count_max = 4))
        #AutoLabel_4(df, close_enough_to_sell= .01, return_actual_col= 'actual_rtn', return_predict_col= 'pred_rtn', 
        #        prediction_col= 'Pred_AC_j+5', actual_col= 'adjclose', hold_count_max = 4):
    """
        Apply investment stratery logic to a DataFrame with predicted stock values + returns,
        to return this DataFrame with position label column.
        
        Parameters:
            df (pd.DataFrame): DataFrame to apply logic to.
            close_enough_to_sell (float): How close the actual value should be from the best prediction 
                to sell the position at that value instead of waiting a few more days (hold_count_max)
            return_actual_col (str): Name of column containing actual return values
            return_predict_col (str): Name of column containing predicted return values
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
        return_predict = df[return_predict_col]
        actual = df[actual_col]
        
        i = 0
        position = 'Hold'
        ls_position = []
        buy_count = 0
        ls_buy_count = []
        
        prediction = df[prediction_col]
        best_prediction = 0
        actual_deviation_from_best_prediction = (best_prediction - actual[i]) / best_prediction
        is_close_enough = bool(actual_deviation_from_best_prediction < close_enough_to_sell)
        
        while i <= len(df)-1:
            if position == 'Sell' or position == 'Hold':
                # Si la prévision j+5 est positive et le titre a baissé depuis hier
                if return_predict[i] > 0 and return_actual[i] < 0:
                    if return_predict[i] > .15:
                        position = 'Buy' # change la position
                        best_prediction = prediction[i] # la pred d'aujourd'hui devient la meilleur pred
                        ls_position.append(position)
                        buy_count += 10
                        ls_buy_count.append(buy_count)
                        i+=1
                        if i == len(df):
                            continue
                        else:
                            actual_deviation_from_best_prediction = (best_prediction - actual[i]) / best_prediction
                            is_close_enough = bool(actual_deviation_from_best_prediction < close_enough_to_sell)
                            continue
                    elif return_predict[i] > .10:
                        position = 'Buy' # change la position
                        best_prediction = prediction[i] # la pred d'aujourd'hui devient la meilleur pred
                        ls_position.append(position)
                        buy_count += 10
                        ls_buy_count.append(buy_count)
                        i+=1
                        if i == len(df):
                            continue
                        else:
                            actual_deviation_from_best_prediction = (best_prediction - actual[i]) / best_prediction
                            is_close_enough = bool(actual_deviation_from_best_prediction < close_enough_to_sell)
                            continue
                    elif return_predict[i] > .05:
                        position = 'Buy' # change la position
                        best_prediction = prediction[i] # la pred d'aujourd'hui devient la meilleur pred
                        ls_position.append(position)
                        buy_count += 5
                        ls_buy_count.append(buy_count)
                        i+=1
                        if i == len(df):
                            continue
                        else:
                            actual_deviation_from_best_prediction = (best_prediction - actual[i]) / best_prediction
                            is_close_enough = bool(actual_deviation_from_best_prediction < close_enough_to_sell)
                            continue
                    else:
                        position = 'Buy' # change la position
                        best_prediction = prediction[i] # la pred d'aujourd'hui devient la meilleur pred
                        ls_position.append(position)
                        buy_count += 1
                        ls_buy_count.append(buy_count)
                        i+=1
                        continue
                        if i == len(df):
                            continue
                        else:
                            actual_deviation_from_best_prediction = (best_prediction - actual[i]) / best_prediction
                            is_close_enough = bool(actual_deviation_from_best_prediction < close_enough_to_sell)
                            continue
                else:
                    position = 'Hold'
                    ls_position.append(position)
                    ls_buy_count.append(buy_count)
                    i+=1
                    continue
                    
            elif position == 'Buy':
                while hold_count <= hold_count_max:                
                    # Sortir de la loop quand y'a plus de valeurs
                    if i > len(df)-1:
                        break
                    if return_predict[i] > .15:
                        position = 'Buy' # change la position
                        best_prediction = prediction[i] # la pred d'aujourd'hui devient la meilleur pred
                        ls_position.append(position)
                        buy_count += 10
                        ls_buy_count.append(buy_count)
                        i+=1
                        if i == len(df):
                            continue
                        else:
                            actual_deviation_from_best_prediction = (best_prediction - actual[i]) / best_prediction
                            is_close_enough = bool(actual_deviation_from_best_prediction < close_enough_to_sell)
                            continue
                    elif return_predict[i] > .10:
                        position = 'Buy' # change la position
                        best_prediction = prediction[i] # la pred d'aujourd'hui devient la meilleur pred
                        ls_position.append(position)
                        buy_count += 10
                        ls_buy_count.append(buy_count)
                        i+=1
                        if i == len(df):
                            continue
                        else:
                            actual_deviation_from_best_prediction = (best_prediction - actual[i]) / best_prediction
                            is_close_enough = bool(actual_deviation_from_best_prediction < close_enough_to_sell)
                            continue
                    elif return_predict[i] > .05:
                        position = 'Buy' # change la position
                        best_prediction = prediction[i] # la pred d'aujourd'hui devient la meilleur pred
                        ls_position.append(position)
                        buy_count += 5
                        ls_buy_count.append(buy_count)
                        i+=1
                        if i == len(df):
                            continue
                        else:
                            actual_deviation_from_best_prediction = (best_prediction - actual[i]) / best_prediction
                            is_close_enough = bool(actual_deviation_from_best_prediction < close_enough_to_sell)
                            continue
                    # Si la valeur atteint la meilleur prédiction plus tôt, on vend plus tôt.
                    elif actual[i] > best_prediction or is_close_enough == True:
                        position = 'Sell'
                        hold_count = 1 # réinit le hold_count
                        ls_position.append(position)
                        buy_count = 0
                        ls_buy_count.append(buy_count)
                        i+=1
                        break
                    # Si la meilleure prediction des 5 derniers jours < que la pred d'aujourd'hui
                    elif best_prediction < prediction[i]:
                        best_prediction = prediction[i] # la pred d'aujourd'hui devient la meilleur pred
                        position = 'Buy' # maintien de la position
                        hold_count = 1 # réinit le hold_count
                        buy_count += 1
                        ls_buy_count.append(buy_count)
                        ls_position.append(position)
                        i+=1
                        continue
                    elif hold_count == hold_count_max:
                        position = 'Sell' # limite atteinte, on vend
                        hold_count = 1 # réinit le hold_count
                        ls_position.append(position)
                        buy_count = 0
                        ls_buy_count.append(buy_count)
                        i+=1
                        break
                    # Si la meilleure pred > que la pred d'aujourd'hui
                    # et que le hold_count < 5
                    # garde la pred
                    else:
                        hold_count += 1 # incrément le hold_count
                        position = 'Hold' # maintien de la position
                        ls_position.append(position)
                        ls_buy_count.append(buy_count)
                        i+=1
                        continue
        
        # Add position labels results to df
        df['Position_label'] = ls_position
        df['buy_count'] = ls_buy_count
        
        return df