import sys
if sys.version_info < (3,):
    range = xrange

import numpy as np
import pandas as pd
import scipy.stats as ss
import matplotlib.pyplot as plt
import seaborn as sns
from patsy import dmatrices, dmatrix, demo_data

from .. import inference as ifr
from .. import distributions as dst
from .. import output as op
from .. import tests as tst
from .. import tsm as tsm
from .. import data_check as dc

from .arma_recursions import arimax_recursion

class ARIMAX(tsm.TSM):
    """ Inherits time series methods from TSM parent class.

    **** AUTOREGRESSIVE INTEGRATED MOVING AVERAGE EXOGENOUS (ARIMAX) MODELS ****

    Parameters
    ----------
    data : pd.DataFrame
        Field to specify the univariate time series data that will be used.

    formula : string
        patsy string notation describing the regression

    ar : int
        Field to specify how many AR lags the model will have.

    ma : int
        Field to specify how many MA lags the model will have.

    integ : int (default : 0)
        Specifies how many times to difference the time series.
    """

    def __init__(self, data, formula, ar, ma, integ=0):

        # Initialize TSM object
        super(ARIMAX,self).__init__('ARIMAX')

        # Latent Variables
        self.ar = ar
        self.ma = ma
        self.integ = integ
        self.model_name = "ARIMAX(" + str(self.ar) + "," + str(self.integ) + "," + str(self.ma) + ")"
        self.z_no = self.ar + self.ma + 2
        self.max_lag = max(self.ar, self.ma)
        self._z_hide = 0 # Whether to cutoff latent variables from results table
        self.supported_methods = ["MLE", "PML", "Laplace", "M-H", "BBVI"]
        self.default_method = "MLE"
        self.multivariate_model = False

        # Format the data
        self.is_pandas = True # This is compulsory for this model type
        self.data_original = data.copy()
        self.formula = formula
        self.y, self.X = dmatrices(formula, data)
        self.y_name = self.y.design_info.describe()
        self.X_names = self.X.design_info.describe().split(" + ")
        self.y = self.y.astype(np.float) 
        self.X = self.X.astype(np.float) 
        self.z_no = self.X.shape[1]
        self.data_name = self.y_name
        self.y = np.array([self.y]).ravel()
        self.data = self.y.copy()
        self.X = np.array([self.X])[0]
        self.index = data.index

        # Difference data
        for order in range(0, self.integ):
            self.y = np.diff(self.y)
            self.data = np.diff(self.data)
            self.data_name = "Differenced " + self.data_name

        self.ar_matrix = self._ar_matrix()
        self._create_latent_variables()

    def _ar_matrix(self):
        """ Creates the Autoregressive matrix

        Returns
        ----------
        X : np.ndarray
            Autoregressive Matrix
        """

        if self.ar != 0:
            X = self.data[(self.max_lag-1):-1]
            for i in range(1, self.ar):
                X = np.vstack((X,self.data[(self.max_lag-i-1):-i-1]))
            return X
        else:
            return np.zeros(self.data.shape[0]-self.max_lag)

    def _create_latent_variables(self):
        """ Creates the model's latent variables

        Returns
        ----------
        None (changes model attributes)
        """

        for ar_term in range(self.ar):
            self.latent_variables.add_z('AR(' + str(ar_term+1) + ')', ifr.Normal(0, 0.5, transform=None), dst.q_Normal(0, 3))

        for ma_term in range(self.ma):
            self.latent_variables.add_z('MA(' + str(ma_term+1) + ')', ifr.Normal(0, 0.5, transform=None), dst.q_Normal(0, 3))

        for z in range(len(self.X_names)):
            self.latent_variables.add_z('Beta ' + self.X_names[z], ifr.Normal(0, 3, transform=None), dst.q_Normal(0, 3))

        self.latent_variables.add_z('Sigma', ifr.Uniform(transform='exp'), dst.q_Normal(0, 3))
        self.z_no = len(self.latent_variables.z_list)

    def _model(self, beta):
        """ Creates the structure of the model (model matrices, etc)

        Parameters
        ----------
        beta : np.ndarray
            Contains untransformed starting values for the latent variables

        Returns
        ----------
        mu : np.ndarray
            Contains the predicted values (location) for the time series

        Y : np.ndarray
            Contains the length-adjusted time series (accounting for lags)
        """     

        Y = self.y[self.max_lag:]

        # Transform latent variables
        z = np.array([self.latent_variables.z_list[k].prior.transform(beta[k]) for k in range(beta.shape[0])])

        # Constant and AR terms
        if self.ar == 0:
            mu = np.transpose(self.ar_matrix)
        elif self.ar == 1:
            mu = np.transpose(self.ar_matrix)*z[:-1-self.ma-len(self.X_names)][0]
        else:
            mu = np.matmul(np.transpose(self.ar_matrix),z[:-1-self.ma-len(self.X_names)])

        # X terms
        mu = mu + np.matmul(self.X[self.integ+self.max_lag:],z[self.ma+self.ar:(self.ma+self.ar+len(self.X_names))])

        # MA terms
        if self.ma != 0:
            mu = arimax_recursion(z, mu, Y, self.max_lag, Y.shape[0], self.ar, self.ma)

        return mu, Y 

    def _mean_prediction(self, mu, Y, h, t_z, X_oos):
        """ Creates a h-step ahead mean prediction

        Parameters
        ----------
        mu : np.array
            The past predicted values

        Y : np.array
            The past data

        h : int
            How many steps ahead for the prediction

        t_z : np.array
            A vector of (transformed) latent variables

        X_oos : np.array
            Out of sample X data

        Returns
        ----------
        h-length vector of mean predictions
        """     

        # Create arrays to iterate over
        Y_exp = Y.copy()
        mu_exp = mu.copy()

        # Loop over h time periods          
        for t in range(0,h):
            new_value = 0
            if self.ar != 0:
                for j in range(0, self.ar):
                    new_value += t_z[j]*Y_exp[-j-1]

            if self.ma != 0:
                for k in range(0, self.ma):
                    if k >= t:
                        new_value += t_z[k+self.ar]*(Y_exp[-k-1]-mu_exp[-k-1])

            # X terms
            new_value += np.matmul(X_oos[t,:],t_z[self.ma+self.ar:(self.ma+self.ar+len(self.X_names))])            
            Y_exp = np.append(Y_exp,[new_value])
            mu_exp = np.append(mu_exp,[0]) # For indexing consistency

        return Y_exp

    def _sim_prediction(self, mu, Y, h, t_z, X_oos, simulations):
        """ Simulates a h-step ahead mean prediction (with randomly drawn disturbances)

        Parameters
        ----------
        mu : np.ndarray
            The past predicted values

        Y : np.ndarray
            The past data

        h : int
            How many steps ahead for the prediction

        t_z : np.ndarray
            A vector of (transformed) latent variables

        X_oos : np.ndarray
            Out of sample X data

        simulations : int
            How many simulations to perform

        Returns
        ----------
        Matrix of simulations
        """     

        sim_vector = np.zeros([simulations,h])

        for n in range(0, simulations):
            # Create arrays to iteratre over
            Y_exp = Y.copy()
            mu_exp = mu.copy()

            # Loop over h time periods          
            for t in range(0, h):
                new_value = np.random.randn(1)*t_z[-1]

                if self.ar != 0:
                    for j in range(0, self.ar):
                        new_value += t_z[j]*Y_exp[-j-1]

                if self.ma != 0:
                    for k in range(0, self.ma):
                        if k >= t:
                            new_value += t_z[k+self.ar]*(Y_exp[-k-1]-mu_exp[-k-1])

                # X terms
                new_value += np.matmul(X_oos[t,:], t_z[self.ma+self.ar:(self.ma+self.ar+len(self.X_names))])            

                Y_exp = np.append(Y_exp, [new_value])
                mu_exp = np.append(mu_exp, [0]) # For indexing consistency

            sim_vector[n] = Y_exp[-h:]

        return np.transpose(sim_vector)

    def _summarize_simulations(self, mean_values, sim_vector, date_index, h, past_values):
        """ Produces forecasted values to plot, along with prediction intervals

        Parameters
        ----------
        mean_values : np.ndarray
            Mean predictions for h-step ahead forecasts

        sim_vector : np.ndarray
            N simulation predictions for h-step ahead forecasts

        date_index : pd.DateIndex or np.ndarray
            Dates for the simulations

        h : int
            How many steps ahead are forecast

        past_values : int
            How many past observations to include in the forecast plot

        intervals : Boolean
            Would you like to show prediction intervals for the forecast?
        """         

        error_bars = []
        for pre in range(5,100,5):
            error_bars.append(np.insert([np.percentile(i,pre) for i in sim_vector] - mean_values[-h:],0,0))
        forecasted_values = mean_values[-h-1:]
        plot_values = mean_values[-h-past_values:]
        plot_index = date_index[-h-past_values:]
        return error_bars, forecasted_values, plot_values, plot_index
        
    def neg_loglik(self, beta):
        """ Creates the negative log-likelihood of the model

        Parameters
        ----------
        beta : np.ndarray
            Contains untransformed starting values for latent variables

        Returns
        ----------
        The negative logliklihood of the model
        """     

        mu, Y = self._model(beta)
        return -np.sum(ss.norm.logpdf(Y, loc=mu, scale=self.latent_variables.z_list[-1].prior.transform(beta[-1])))

    def plot_fit(self, **kwargs):
        """ 
        Plots the fit of the model against the data
        """

        figsize = kwargs.get('figsize',(10,7))
        plt.figure(figsize=figsize)
        date_index = self.index[max(self.ar, self.ma):self.data.shape[0]]
        mu, Y = self._model(self.latent_variables.get_z_values())
        plt.plot(date_index, Y, label='Data')
        plt.plot(date_index, mu, label='Filter', c='black')
        plt.title(self.data_name)
        plt.legend(loc=2)   
        plt.show()          

    def plot_predict(self, h=5, past_values=20, intervals=True, oos_data=None, **kwargs):
        """ Plots forecasts with the estimated model

        Parameters
        ----------
        h : int (default : 5)
            How many steps ahead would you like to forecast?

        past_values : int (default : 20)
            How many past observations to show on the forecast plot?

        intervals : Boolean
            Would you like to show prediction intervals for the forecast?

        oos_data : pd.DataFrame
            Data for the variables to be used out of sample (ys can be NaNs)

        Returns
        ----------
        - Plot of the forecast
        """     

        figsize = kwargs.get('figsize',(10,7))

        if self.latent_variables.estimated is False:
            raise Exception("No latent variables estimated!")
        else:
            # Sort/manipulate the out-of-sample data
            _, X_oos = dmatrices(self.formula, oos_data)
            X_oos = np.array([X_oos])[0]
            X_pred = X_oos[:h]

            # Retrieve data, dates and (transformed) latent variables
            mu, Y = self._model(self.latent_variables.get_z_values())         
            date_index = self.shift_dates(h)
            t_z = self.transform_z()

            # Get mean prediction and simulations (for errors)
            mean_values = self._mean_prediction(mu, Y, h, t_z, X_pred)
            sim_values = self._sim_prediction(mu, Y, h, t_z, X_pred, 15000)
            error_bars, forecasted_values, plot_values, plot_index = self._summarize_simulations(mean_values, sim_values, date_index, h, past_values)

            plt.figure(figsize=figsize)
            if intervals == True:
                alpha =[0.15*i/float(100) for i in range(50,12,-2)]
                for count, pre in enumerate(error_bars):
                    plt.fill_between(date_index[-h-1:], forecasted_values-pre, forecasted_values+pre,alpha=alpha[count])            
            plt.plot(plot_index,plot_values)
            plt.title("Forecast for " + self.data_name)
            plt.xlabel("Time")
            plt.ylabel(self.data_name)
            plt.show()

    def predict_is(self, h=5, fit_once=True):
        """ Makes dynamic out-of-sample predictions on in-sample data with the estimated model

        Parameters
        ----------
        h : int (default : 5)
            How many steps would you like to forecast?

        fit_once : boolean
            Whether to fit the model once at the beginning (True), or fit every iteration (False)

        Returns
        ----------
        - pd.DataFrame with predicted values
        """     

        predictions = []

        for t in range(0, h):
            data1 = self.data_original.iloc[:-(h+t),:]
            data2 = self.data_original.iloc[-h+t:,:]
            x = ARIMAX(ar=self.ar, ma=self.ma, integ=self.integ, formula=self.formula, data=data1)

            if fit_once is False:
                x.fit(printer=False)
            if t == 0:
                if fit_once is True:
                    x.fit(printer=False)
                    saved_lvs = x.latent_variables
                predictions = x.predict(1, oos_data=data2)
            else:
                if fit_once is True:
                    x.latent_variables = saved_lvs
                predictions = pd.concat([predictions,x.predict(h=1, oos_data=data2)])
        
        predictions.rename(columns={0:self.y_name}, inplace=True)
        predictions.index = self.index[-h:]

        return predictions

    def plot_predict_is(self, h=5, fit_once=True, **kwargs):
        """ Plots dynamic in-sample forecasts with the estimated model against the data 

        Parameters
        ----------
        h : int (default : 5)
            How many steps to forecast

        fit_once : boolean
            Whether to fit the model once at the beginning (True), or fit every iteration (False)

        Returns
        ----------
        - Plot of the forecast against data 
        """     

        figsize = kwargs.get('figsize',(10,7))

        plt.figure(figsize=figsize)
        predictions = self.predict_is(h)
        data = self.data[-h:]

        plt.plot(predictions.index, data, label='Data')
        plt.plot(predictions.index, predictions, label='Predictions', c='black')
        plt.title(self.data_name)
        plt.legend(loc=2)   
        plt.show()          

    def predict(self, h=5, oos_data=None):
        """ Makes forecast with the estimated model

        Parameters
        ----------
        h : int (default : 5)
            How many steps ahead would you like to forecast?

        oos_data : pd.DataFrame
            Data for the variables to be used out of sample (ys can be NaNs)

        Returns
        ----------
        - pd.DataFrame with predicted values
        """     

        if self.latent_variables.estimated is False:
            raise Exception("No latent_variables estimated!")
        else:
            # Sort/manipulate the out-of-sample data
            _, X_oos = dmatrices(self.formula, oos_data)
            X_oos = np.array([X_oos])[0]
            X_pred = X_oos[:h]
            mu, Y = self._model(self.latent_variables.get_z_values())         
            date_index = self.shift_dates(h)
            t_z = self.transform_z()

            mean_values = self._mean_prediction(mu, Y, h, t_z, X_pred)
            forecasted_values = mean_values[-h:]
            result = pd.DataFrame(forecasted_values)
            result.rename(columns={0:self.data_name}, inplace=True)
            result.index = date_index[-h:]

            return result