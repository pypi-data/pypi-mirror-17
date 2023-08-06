import copy
import sys
if sys.version_info < (3,):
    range = xrange

import numpy as np
import pandas as pd
import scipy.stats as ss
import matplotlib.pyplot as plt
import seaborn as sns

from .. import inference as ifr
from .. import distributions as dst
from .. import tsm as tsm
from .. import data_check as dc

from .kalman import *

class LLT(tsm.TSM):
    """ Inherits time series methods from TSM class.

    **** LOCAL LINEAR TREND MODEL ****

    Parameters
    ----------
    data : pd.DataFrame or np.array
        Field to specify the time series data that will be used.

    integ : int (default : 0)
        Specifies how many time to difference the time series.

    target : str (pd.DataFrame) or int (np.array)
        Specifies which column name or array index to use. By default, first
        column/array will be selected as the dependent variable.
    """

    def __init__(self,data,integ=0,target=None):

        # Initialize TSM object
        super(LLT,self).__init__('LLT')

        # Latent Variables
        self.integ = integ
        self.param_no = 3
        self.max_lag = 0
        self._z_hide = 0 # Whether to cutoff variance latent variables from results
        self.supported_methods = ["MLE","PML","Laplace","M-H","BBVI"]
        self.default_method = "MLE"
        self.model_name = "LLT"
        self.multivariate_model = False

        # Format the data
        self.data, self.data_name, self.is_pandas, self.index = dc.data_check(data,target)
        self.data = self.data.astype(np.float)
        self.data_original = self.data

        # Difference data
        for order in range(self.integ):
            self.data = np.diff(self.data)
            self.data_name = "Differenced " + self.data_name

        self._create_latent_variables()

    def _create_latent_variables(self):
        """ Creates model latent variables

        Returns
        ----------
        None (changes model attributes)
        """

        self.latent_variables.add_z('Sigma^2 irregular',ifr.Uniform(transform='exp'),dst.q_Normal(0,3))
        self.latent_variables.add_z('Sigma^2 level',ifr.Uniform(transform='exp'),dst.q_Normal(0,3))
        self.latent_variables.add_z('Sigma^2 trend',ifr.Uniform(transform='exp'),dst.q_Normal(0,3))

    def _forecast_model(self,beta,h):
        """ Creates forecasted states and variances

        Parameters
        ----------
        beta : np.ndarray
            Contains untransformed starting values for latent variables

        Returns
        ----------
        a : np.ndarray
            Forecasted states

        P : np.ndarray
            Variance of forecasted states
        """     

        T, Z, R, Q, H = self._ss_matrices(beta)
        return llt_univariate_kalman_fcst(self.data,Z,H,T,Q,R,0.0,h)

    def _model(self,data,beta):
        """ Creates the structure of the model

        Parameters
        ----------
        data : np.array
            Contains the time series

        beta : np.array
            Contains untransformed starting values for latent variables

        Returns
        ----------
        a,P,K,F,v : np.array
            Filted states, filtered variances, Kalman gains, F matrix, residuals
        """     

        T, Z, R, Q, H = self._ss_matrices(beta)

        return llt_univariate_kalman(data,Z,H,T,Q,R,0.0)

    def _ss_matrices(self,beta):
        """ Creates the state space matrices required

        Parameters
        ----------
        beta : np.array
            Contains untransformed starting values for latent variables

        Returns
        ----------
        T, Z, R, Q, H : np.array
            State space matrices used in KFS algorithm
        """     

        T = np.identity(2)
        T[0][1] = 1
        
        Z = np.zeros(2)
        Z[0] = 1

        R = np.identity(2)
        Q = np.identity(2)
        H = np.identity(1)*self.latent_variables.z_list[0].prior.transform(beta[0])
        Q[0][0] = self.latent_variables.z_list[1].prior.transform(beta[1])
        Q[1][1] = self.latent_variables.z_list[2].prior.transform(beta[2])

        return T, Z, R, Q, H

    def neg_loglik(self,beta):
        """ Creates the negative log likelihood of the model

        Parameters
        ----------
        beta : np.array
            Contains untransformed starting values for latent variables

        Returns
        ----------
        The negative log logliklihood of the model
        """         
        _, _, _, F, v = self._model(self.data,beta)
        loglik = 0.0
        for i in range(0,self.data.shape[0]):
            loglik += np.linalg.slogdet(F[:,:,i])[1] + np.dot(v[i],np.dot(np.linalg.pinv(F[:,:,i]),v[i]))
        return -(-((self.data.shape[0]/2)*np.log(2*np.pi))-0.5*loglik.T[0].sum())

    def plot_predict(self,h=5,past_values=20,intervals=True,**kwargs):      
        """ Makes forecast with the estimated model

        Parameters
        ----------
        h : int (default : 5)
            How many steps ahead would you like to forecast?

        past_values : int (default : 20)
            How many past observations to show on the forecast graph?

        intervals : Boolean
            Would you like to show 95% prediction intervals for the forecast?

        Returns
        ----------
        - Plot of the forecast
        """     

        figsize = kwargs.get('figsize',(10,7))

        if self.latent_variables.estimated is False:
            raise Exception("No latent variables estimated!")
        else:
            # Retrieve data, dates and (transformed) latent variables         
            a, P = self._forecast_model(self.latent_variables.get_z_values(),h)
            date_index = self.shift_dates(h)
            plot_values = a[0][-h-past_values:]
            forecasted_values = a[0][-h:]
            lower = forecasted_values - 1.98*np.power(P[0][0][-h:] + self.latent_variables.z_list[0].prior.transform(self.latent_variables.get_z_values()[0]),0.5)
            upper = forecasted_values + 1.98*np.power(P[0][0][-h:] + self.latent_variables.z_list[0].prior.transform(self.latent_variables.get_z_values()[0]),0.5)
            lower = np.append(plot_values[-h-1],lower)
            upper = np.append(plot_values[-h-1],upper)

            plot_index = date_index[-h-past_values:]

            plt.figure(figsize=figsize)
            if intervals == True:
                plt.fill_between(date_index[-h-1:], lower, upper, alpha=0.2)            

            plt.plot(plot_index,plot_values)
            plt.title("Forecast for " + self.data_name)
            plt.xlabel("Time")
            plt.ylabel(self.data_name)
            plt.show()

    def plot_fit(self,intervals=True,**kwargs):
        """ Plots the fit of the model

        Parameters
        ----------
        intervals : Boolean
            Whether to plot 95% confidence interval of states

        Returns
        ----------
        None (plots data and the fit)
        """

        figsize = kwargs.get('figsize',(10,7))
        series_type = kwargs.get('series_type','Smoothed')

        if self.latent_variables.estimated is False:
            raise Exception("No latent variables estimated!")
        else:
            date_index = copy.deepcopy(self.index)
            date_index = date_index[self.integ:self.data_original.shape[0]+1]

            if series_type == 'Smoothed':
                mu, V= self.smoothed_state(self.data,self.latent_variables.get_z_values())
            elif series_type == 'Filtered':
                mu, V, _, _, _ = self._model(self.data,self.latent_variables.get_z_values())
            else:
                mu, V = self.smoothed_state(self.data,self.latent_variables.get_z_values())

            mu0 = mu[0][:-1]
            mu1 = mu[1][:-1]
            Vlev = V[0][0][:-1]
            Vtrend = V[0][1][:-1]   

            plt.figure(figsize=figsize) 
            
            plt.subplot(2, 2, 1)
            plt.title(self.data_name + " Raw and " + series_type)   

            if intervals == True:
                alpha =[0.15*i/float(100) for i in range(50,12,-2)]
                plt.fill_between(date_index[2:], mu0[2:] + 1.98*np.sqrt(Vlev[2:]), mu0[2:] - 1.98*np.sqrt(Vlev[2:]), alpha=0.15,label='95% C.I.')   

            plt.plot(date_index,self.data,label='Data')
            plt.plot(date_index,mu0,label=series_type,c='black')
            plt.legend(loc=2)
            
            plt.subplot(2, 2, 2)

            if intervals == True:
                alpha =[0.15*i/float(100) for i in range(50,12,-2)]
                plt.fill_between(date_index[2:], mu0[2:] + 1.98*np.sqrt(Vlev[2:]), mu0[2:] - 1.98*np.sqrt(Vlev[2:]), alpha=0.15,label='95% C.I.')   

            plt.title(self.data_name + " Local Level")  
            plt.plot(date_index,mu0,label='Local Level')
            plt.legend(loc=2)
            
            plt.subplot(2, 2, 3)

            if intervals == True:
                alpha =[0.15*i/float(100) for i in range(50,12,-2)]
                plt.fill_between(date_index[2:], mu1[2:] + 1.98*np.sqrt(Vtrend[2:]), mu1[2:] - 1.98*np.sqrt(Vtrend[2:]), alpha=0.15,label='95% C.I.')   

            plt.title(self.data_name + " Trend")    
            plt.plot(date_index,mu1,label='Stochastic Trend')
            plt.legend(loc=2)

            plt.subplot(2, 2, 4)
            plt.title("Measurement Noise")  
            plt.plot(date_index[1:self.data.shape[0]],self.data[1:self.data.shape[0]]-mu0[1:self.data.shape[0]],label='Irregular term')
            plt.show()              

    def predict(self,h=5):      
        """ Makes forecast with the estimated model

        Parameters
        ----------
        h : int (default : 5)
            How many steps ahead would you like to forecast?

        Returns
        ----------
        - pd.DataFrame with predictions
        """     

        if self.latent_variables.estimated is False:
            raise Exception("No latent variables estimated!")
        else:
            # Retrieve data, dates and (transformed) latent variables         
            a, P = self._forecast_model(self.latent_variables.get_z_values(),h)
            date_index = self.shift_dates(h)
            forecasted_values = a[0][-h:]

            result = pd.DataFrame(forecasted_values)
            result.rename(columns={0:self.data_name}, inplace=True)
            result.index = date_index[-h:]

            return result

    def predict_is(self, h=5, fit_once=True):
        """ Makes dynamic in-sample predictions with the estimated model

        Parameters
        ----------
        h : int (default : 5)
            How many steps would you like to forecast?

        fit_once : boolean
            (default: True) Fits only once before the in-sample prediction; if False, fits after every new datapoint

        Returns
        ----------
        - pd.DataFrame with predicted values
        """     

        predictions = []

        for t in range(0,h):
            x = LLT(integ=self.integ,data=self.data_original[:(-h+t)])
            if fit_once is False:
                x.fit(printer=False)
            if t == 0:
                if fit_once is True:
                    x.fit(printer=False)
                    saved_lvs = x.latent_variables
                predictions = x.predict(1)
            else:
                if fit_once is True:
                    x.latent_variables = saved_lvs
                predictions = pd.concat([predictions,x.predict(1)])

        predictions.rename(columns={0:self.data_name}, inplace=True)
        predictions.index = self.index[-h:]

        return predictions

    def plot_predict_is(self,h=5,**kwargs):
        """ Plots forecasts with the estimated model against data
            (Simulated prediction with data)

        Parameters
        ----------
        h : int (default : 5)
            How many steps to forecast

        Returns
        ----------
        - Plot of the forecast against data 
        """     

        figsize = kwargs.get('figsize',(10,7))

        plt.figure(figsize=figsize)
        predictions = self.predict_is(h)
        data = self.data[-h:]
        plt.plot(predictions.index,data,label='Data')
        plt.plot(predictions.index,predictions,label='Predictions',c='black')
        plt.title(self.data_name)
        plt.legend(loc=2)   
        plt.show()          

    def simulation_smoother(self,beta):
        """ Koopman's simulation smoother - simulates from states given
        model latent variables and observations

        Parameters
        ----------

        beta : np.array
            Contains untransformed starting values for latent variables

        Returns
        ----------
        - A simulated state evolution
        """         

        T, Z, R, Q, H = self._ss_matrices(beta)

        # Generate e_t+ and n_t+
        rnd_h = np.random.normal(0,np.sqrt(H),self.data.shape[0]+1)
        q_dist = ss.multivariate_normal([0.0, 0.0], Q)
        rnd_q = q_dist.rvs(self.data.shape[0]+1)

        # Generate a_t+ and y_t+
        a_plus = np.zeros((T.shape[0],self.data.shape[0]+1)) 
        a_plus[0,0] = np.mean(self.data[0:5])
        y_plus = np.zeros(self.data.shape[0])

        for t in range(0,self.data.shape[0]+1):
            if t == 0:
                a_plus[:,t] = np.dot(T,a_plus[:,t]) + rnd_q[t,:]
                y_plus[t] = np.dot(Z,a_plus[:,t]) + rnd_h[t]
            else:
                if t != self.data.shape[0]:
                    a_plus[:,t] = np.dot(T,a_plus[:,t-1]) + rnd_q[t,:]
                    y_plus[t] = np.dot(Z,a_plus[:,t]) + rnd_h[t]

        alpha_hat,_ = self.smoothed_state(self.data,beta)
        alpha_hat_plus,_ = self.smoothed_state(y_plus,beta)
        alpha_tilde = alpha_hat - alpha_hat_plus + a_plus
    
        return alpha_tilde

    def smoothed_state(self,data,beta):
        """ Creates the negative log marginal likelihood of the model

        Parameters
        ----------

        data : np.array
            Data to be smoothed

        beta : np.array
            Contains untransformed starting values for latent variables

        Returns
        ----------
        - Smoothed states
        """         

        T, Z, R, Q, H = self._ss_matrices(beta)
        alpha, V = llt_univariate_KFS(data,Z,H,T,Q,R,0.0)
        return alpha, V