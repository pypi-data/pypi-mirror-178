"""Example module in template package."""

import os

import numpy as np
import pandas as pd

from .geo import *
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn import set_config
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.impute import SimpleImputer
from sklearn.metrics import precision_score, recall_score, accuracy_score, f1_score
from sklearn.compose import ColumnTransformer

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import SGDRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

from keras.utils import to_categorical
from imblearn.over_sampling import SMOTE
from imblearn.over_sampling import RandomOverSampler
from collections import Counter
__all__ = ['Tool']


class Tool(object):
    """Class to interact with a postcode database file."""

    def __init__(self, postcode_file='', sample_labels='',
                 household_file=''):

        """
        Parameters
        ----------

        full_postcode_file : str, optional
            Filename of a .csv file containing geographic location
            data for postcodes.

        household_file : str, optional
            Filename of a .csv file containing information on households
            by postcode.
        """

        if postcode_file == '':
            full_postcode_file = os.sep.join((os.path.dirname(__file__),
                                              'resources',
                                              'postcodes_unlabelled.csv'))

        if household_file == '':
            household_file = os.sep.join((os.path.dirname(__file__),
                                          'resources',
                                          'households_per_sector.csv'))

        if sample_labels == '':
            labelled_samples = os.sep.join((os.path.dirname(__file__),
                                            'resources',
                                            'postcodes_sampled.csv'))
                                            
        self.label_data = pd.read_csv(labelled_samples) 

        self.postcodedb = pd.read_csv(full_postcode_file)
        self.householddb = pd.read_csv(household_file)

    def train(self, labelled_samples=''):
        """Train the model using a labelled set of samples.
        
        Parameters
        ----------
        
        labelled_samples : str, optional
            Filename of a .csv file containing a labelled set of samples.
        """
        if labelled_samples == '':
            labelled_samples = os.sep.join((os.path.dirname(__file__),
                                            'resources',
                                            'postcodes_sampled.csv'))
                                            
        self.label_data = pd.read_csv(labelled_samples)

    
    def get_useful_features(self, postcodes, features=['sector', 'easting', 'northing', 'localAuthority', 'altitude', 'soilType']):
        
        frame = self.postcodedb.copy()
        frame = frame.set_index('postcode')

        return frame.loc[postcodes,features]

        
    def get_easting_northing(self, postcodes):
        """Get a frame of OS eastings and northings from a collection
        of input postcodes.

        Parameters
        ----------

        postcodes: sequence of strs
            Sequence of postcodes.

        Returns
        -------

        pandas.DataFrame
            DataFrame containing only OSGB36 easthing and northing indexed
            by the input postcodes. Invalid postcodes (i.e. not in the
            input unlabelled postcodes file) return as NaN.
         """

        frame = self.postcodedb.copy()
        frame = frame.set_index('postcode')

        return frame.loc[postcodes, ['easting', 'northing']]

    def get_lat_long(self, postcodes):
        """Get a frame containing GPS latitude and longitude information for a
        collection of postcodes.

        Parameters
        ----------

        postcodes: sequence of strs
            Sequence of postcodes.

        Returns
        -------

        pandas.DataFrame
            DataFrame containing only WGS84 latitude and longitude pairs for
            the input postcodes. Invalid postcodes (i.e. not in the
            input unlabelled postcodes file) return as NAN.
        """
        es = self.get_easting_northing(postcodes)
        lat, lon = get_gps_lat_long_from_easting_northing(es["easting"].to_list(), es["northing"].to_list())

        return pd.DataFrame(np.concatenate([[lat], [lon]], axis=1), columns=["latitude", "longitude"], index=es.index)

    @staticmethod
    def get_flood_class_from_postcodes_methods():
        """
        Get a dictionary of available flood probablity classification methods
        for postcodes.

        Returns
        -------

        dict
            Dictionary mapping classification method names (which have
             no inate meaning) on to an identifier to be passed to the
             get_flood_class_from_postcode method.
        """
        flood_class_method = {'all_zero_risk': 0, 'RandomForestClassifier': 1}
        return flood_class_method


    def get_flood_class_from_postcodes(self, postcodes, method=0):
        """
        Generate series predicting flood probability classification
        for a collection of poscodes.

        Parameters
        ----------

        postcodes : sequence of strs
            Sequence of postcodes.
        method : int (optional)
            optionally specify (via a value in
            get_flood_class_from_postcodes_methods) the classification
            method to be used.

        Returns
        -------

        pandas.Series
            Series of flood risk classification labels indexed by postcodes.
        """

        assert method in [0,1], 'No such a method'
        assert isinstance(postcodes, list) or isinstance(postcodes, np.ndarray), 'postcodes must be a list or numpy array'
        if method == 0:
            return pd.Series(data=np.ones(len(postcodes), int),
                             index=np.asarray(postcodes),
                             name='riskLabel')
        else:
            OSBG36_cord = self.get_easting_northing(postcodes)
            eastings = OSBG36_cord['easting'].to_list()  
            northings = OSBG36_cord['northing'].to_list()
            OS_RLPredic = self.get_flood_class_from_OSGB36_locations(eastings, northings, method=method)

            PC_RLPrediction_Series = pd.Series(data=OS_RLPredic.values,
                                 index=[postcode for postcode in postcodes],
                                 name='riskLabel')  

            return PC_RLPrediction_Series

    @staticmethod
    def get_flood_class_from_locations_methods():
        """
        Get aB dictionary of available flood probablity classification methods
        for locations.

        Returns
        -------

        dict
            Dictionary mapping classification method names (which have
             no inate meaning) on to an identifier to be passed to the
             get_flood_class_from_OSGB36_locations and
             get_flood_class_from_OSGB36_locations method.
        """
                
        flood_class_method = {'Do Nothing': 0, 'RandomForestClassifier': 1}
        return flood_class_method

    def get_flood_class_from_OSGB36_locations(self, eastings, northings, method=0):
        """
        Generate series predicting flood probability classification
        for a collection of OSGB36_locations.

        Parameters
        ----------

        eastings : sequence of floats
            Sequence of OSGB36 eastings.
        northings : sequence of floats
            Sequence of OSGB36 northings.
        method : int (optional)
            optionally specify (via a value in
            self.get_flood_class_from_locations_methods) the classification
            method to be used.

        Returns
        -------

        pandas.Series
            Series of flood risk classification labels indexed by locations.
        """
        assert method in [0,1], 'No such a method'
        assert isinstance(eastings, list) or isinstance(eastings, np.ndarray), 'eastings must be a list or numpy array'
        assert isinstance(northings, list) or isinstance(northings, np.ndarray), 'northings must be a list or numpy array'

        if method == 0:
            return pd.Series(data=np.ones(len(eastings), int),
                             index=[(est, nth) for est, nth in
                                    zip(eastings, northings)],
                             name='riskLabel')
        elif method == 1:
            data = self.label_data.copy()
            y = data['riskLabel']
            X = data[[ 'easting', 'northing']]

            ros = RandomOverSampler(random_state=0)
            x_over, y_over = ros.fit_resample(X, y)

            rf_model = RandomForestClassifier().fit(x_over, y_over)


            ## predict
            cor_list = []
            for est,nor in zip(eastings, northings):
                cor_list.append([est,nor])
            

            RLPrediction = rf_model.predict(pd.DataFrame(cor_list))
            RLPrediction_Series = pd.Series(data=RLPrediction,
                             index=[(est, nth) for est, nth in
                                    zip(eastings, northings)],
                             name='riskLabel')
            return RLPrediction_Series

    def get_flood_class_from_WGS84_locations(self, latitudes, longitudes, rad=False, method=0):
        """
        Generate series predicting flood probability classification
        for a collection of WGS84 datum locations.

        Parameters
        ----------

        longitudes : sequence of floats
            Sequence of WGS84 longitudes.
        latitudes : sequence of floats
            Sequence of WGS84 latitudes.
        method : int (optional)
            optionally specify (via a value in
            self.get_flood_class_from_locations_methods) the classification
            method to be used.

        Returns
        -------

        pandas.Series
            Series of flood risk classification labels indexed by locations.
        """

        assert method in [0,1], 'No such a method'
        assert isinstance(latitudes, list) or isinstance(latitudes, np.ndarray), 'latitudes must be a list or numpy array'
        assert isinstance(longitudes, list) or isinstance(longitudes, np.ndarray), 'longitudes must be a list or numpy array'

        if method == 0:
            return pd.Series(data=np.ones(len(longitudes), int),
                             index=[(lng, lat) for lng, lat in
                                    zip(longitudes, latitudes)],
                             name='riskLabel')
        else:
            # convert from WGS84 to OSGB36
            eastings, northings = get_easting_northing_from_gps_lat_long(latitudes, longitudes, rads=rad)
            OS_RLPredic = self.get_flood_class_from_OSGB36_locations(eastings, northings,method)

            WG_RLPrediction_Series = pd.Series(data=OS_RLPredic.values,
                                 index=[(lat, lot) for lat, lot in
                                        zip( latitudes,longitudes)],
                                 name='riskLabel')    

            return WG_RLPrediction_Series
            

    @staticmethod
    def get_house_price_methods():
        """
        Get a dictionary of available flood house price regression methods.

        Returns
        -------

        dict
            Dictionary mapping regression method names (which have
             no inate meaning) on to an identifier to be passed to the
             get_median_house_price_estimate method.
        """
        return {'all_england_median':0, 'KNeighborsRegressor':1}

    def get_median_house_price_estimate(self, postcodes, method=0):
        """
        Generate series predicting median house price for a collection
        of poscodes.

        Parameters
        ----------

        postcodes : sequence of strs
            Sequence of postcodes.
        method : int (optional)
            optionally specify (via a value in
            self.get_house_price_methods) the regression
            method to be used.

        Returns
        -------

        pandas.Series
            Series of median house price estimates indexed by postcodes.
        """

        if method == 0:
            return pd.Series(data=np.full(len(postcodes), 245000.0),
                             index=np.asarray(postcodes),
                             name='medianPrice')
        
        elif method == 1:
            self.model = KNeighborsRegressor(algorithm='brute', n_neighbors=9, weights='distance')

            X = self.label_data[['easting', 'northing']]
            y = self.label_data.medianPrice

            self.model.fit(X, y)

            X_pre = get_useful_features(postcodes)

            return pd.Series(index=np.asarray(postcodes), data=np.asarray(self.model.predict(X_pre)), name='medianPrice')

        else:
            raise NotImplementedError

    @staticmethod
    def get_local_authority_methods():
        """
        Get a dictionary of available local authorithy classification methods.

        Returns
        -------

        dict
            Dictionary mapping regression method names (which have
             no inate meaning) on to an identifier to be passed to the
             get_altitude_estimate method.
        """
                
        class_method = {'Do Nothing': 0, 'RandomForestClassifier': 1}
        return class_method

    def get_local_authority_estimate(self, eastings, northings, method=0):
        """
        Generate series predicting local authorities in n for a sequence
        of OSGB36 locations.

        Parameters
        ----------

        eastingss : sequence of floats
            Sequence of OSGB36 eastings.
        northings : sequence of floats
            Sequence of OSGB36 northings.
        method : int (optional)
            optionally specify (via a value in
            self.get_altitude_methods) the regression
            method to be used.

        Returns
        -------

        pandas.Series
            Series of LocalAuthority indexed by OSGB36 locations.
        """
        assert method in [0,1], 'No such a method'
        assert isinstance(eastings, list) or isinstance(eastings, np.ndarray), 'eastings must be a list or numpy array'
        assert isinstance(northings, list) or isinstance(northings, np.ndarray), 'northings must be a list or numpy array'
        if method == 0:
            return pd.Series(data=np.full(len(eastings), 'Unknown'),
                             index=[(est, nth) for est, nth in
                                    zip(eastings, northings)],
                             name='localAuthority')
        elif method == 1:
            ## train model
            df2 = self.label_data.copy()
            y = df2['localAuthority']
            X = df2[[ 'easting', 'northing']]
            lencoder = LabelEncoder().fit(y)
            y = pd.Series(lencoder.transform(y))

            smote=SMOTE(random_state=1)
            X_smote, y_smote = smote.fit_resample(X, y)

            rf_model = RandomForestClassifier().fit(X_smote, y_smote)


            ## predict
            cor_list = []
            for est,nor in zip(eastings, northings):
                cor_list.append([est,nor])
            

            LAPrediction = rf_model.predict(pd.DataFrame(cor_list))
            LAPrediction = lencoder.inverse_transform(LAPrediction)
            LAPrediction_Series = pd.Series(data=LAPrediction,
                             index=[(est, nth) for est, nth in
                                    zip(eastings, northings)],
                             name='localAuthority')
            return LAPrediction_Series

    def get_total_value(self, postal_data):
        """
        Return a series of estimates of the total property values
        of a sequence of postcode units or postcode sectors.


        Parameters
        ----------

        postal_data : sequence of strs
            Sequence of postcode units or postcodesectors


        Returns
        -------

        pandas.Series
            Series of total property value estimates indexed by locations.
        """

        raise NotImplementedError

    def get_annual_flood_risk(self, postcodes, risk_labels=None):
        """
        Return a series of estimates of the total property values of a
        collection of postcodes.

        Risk is defined here as a damage coefficient multiplied by the.
        value under threat multiplied by the probability of an event.

        Parameters
        ----------

        postcodes : sequence of strs
            Sequence of postcodes.
        risk_labels: pandas.Series (optional)
            Series containing flood risk classifiers, as
            predicted by get_flood_class_from_postcodes.

        Returns
        -------

        pandas.Series
            Series of total annual flood risk estimates indexed by locations.
        """

        risk_labels = risk_labels or self.get_flood_class(postcodes)

        cost = self.get_total_value(risk_labels.index)

        raise NotImplementedError
