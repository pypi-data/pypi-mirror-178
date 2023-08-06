"""Example module in template package."""

import os

import numpy as np
import pandas as pd

from .geo import *
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsRegressor, KNeighborsClassifier
from imblearn.over_sampling import SMOTE
from imblearn.over_sampling import RandomOverSampler

import joblib

__all__ = ['Tool']


class Tool(object):
    """Class to interact with a postcode database file."""

    def __init__(self, household_file='', postcode_file='', sample_labels=''):
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

        self.postcodedb = pd.read_csv(full_postcode_file)
        self.householddb = pd.read_csv(household_file)
        self.model_dic = {
            "flood_label_model": None,
            "price_model_for_lower_price": None,
            "price_model_for_all": None,
            "authority_model": None,
            "rank_classifier": None,
            "price_model_for_higher_price":None
        }

        self.preprocess(sample_labels)

    def preprocess(self, labelled_samples=""):
        if labelled_samples == '':
            labelled_samples = os.sep.join((os.path.dirname(__file__),
                                            'resources',
                                            'postcodes_sampled.csv'))

        self.train_data = pd.read_csv(labelled_samples)
        flood_label_location_data = self.train_data[['easting', 'northing', 'riskLabel']]
        y = flood_label_location_data[['riskLabel']]
        X = flood_label_location_data[['easting', 'northing']]

        ros = RandomOverSampler(random_state=0)
        self.x_over, self.y_over = ros.fit_resample(X, y)
        # get house price
        house_price_data = self.train_data[['easting', 'northing', 'medianPrice']]
        house_price_data['rank'] = pd.cut(x=house_price_data['medianPrice'],
                                          bins=[house_price_data['medianPrice'].min() - 1,
                                                1000000,
                                                house_price_data['medianPrice'].max() + 1],
                                          labels=['low', 'high'])

        self.X_rank_price = house_price_data[['easting', 'northing']]
        self.y_rank_price = house_price_data[['rank']]

        high_price_data = house_price_data[house_price_data['rank'] == 'high'].drop(columns='rank')
        low_price_data = house_price_data[house_price_data['rank'] == 'low'].drop(columns='rank')

        # high low model's data
        self.X_high_price = high_price_data[['easting', 'northing']]

        self.y_high_price = high_price_data[['medianPrice']]

        self.X_low_price = low_price_data[['easting', 'northing']]

        self.y_low_price = low_price_data[['medianPrice']]

        self.X_price_total = self.train_data[['easting', 'northing']]

        self.y_price_total = self.train_data[['medianPrice']]
        # get authority

        authority_train_data = self.train_data[['easting', 'northing', 'localAuthority']]

        self.X_authority = authority_train_data[['easting', 'northing']]

        self.y_authority = authority_train_data[['localAuthority']]

        self.authority_lencoder = LabelEncoder().fit(self.y_authority)

    def train(self, labelled_samples=''):
        """Train the model using a labelled set of samples.
        
        Parameters
        ----------
        
        labelled_samples : str, optional
            Filename of a .csv file containing a labelled set of samples.
        """
        self.model_dic = {}
        flood_label_model = RandomForestClassifier().fit(self.x_over, self.y_over)

        self.model_dic['flood_label_model'] = flood_label_model

        # get house price_high_low
        ##rank predict
        rank_classifier = KNeighborsClassifier().fit(self.X_rank_price, self.y_rank_price)

        self.model_dic['rank_classifier'] = rank_classifier

        price_model_lower = KNeighborsRegressor(n_neighbors=8, weights='distance').fit(self.X_low_price,
                                                                                       self.y_low_price)

        self.model_dic['price_model_for_lower_price'] = price_model_lower

        price_model_high = KNeighborsRegressor(n_neighbors=8, weights='distance').fit(self.X_high_price,
                                                                                      self.y_high_price)

        self.model_dic['price_model_for_higher_price'] = price_model_high

        # get house price_all
        price_model_total = KNeighborsRegressor(algorithm='brute', n_neighbors=9, weights='distance')

        price_model_total.fit(self.X_price_total, self.y_price_total)

        self.model_dic['price_model_for_all'] = price_model_total

        y_authority = pd.Series(self.authority_lencoder.transform(self.y_authority))

        smote = SMOTE(random_state=1)

        X_smote, y_smote = smote.fit_resample(self.X_authority, y_authority)

        authority_model = RandomForestClassifier().fit(X_smote, y_smote)

        self.model_dic['authority_model'] = authority_model
        weights_path = os.path.join(os.path.dirname(__file__), "weights")
        if not os.path.exists(weights_path):
            os.mkdir(weights_path)
        for name, model in self.model_dic.items():
            joblib.dump(model, os.path.join(weights_path, name + ".pkl"))

    def load(self):
        weights_path = os.path.join(os.path.dirname(__file__), "weights")
        if os.path.exists(os.path.join(weights_path, list(self.model_dic.keys())[0] + '.pkl')):
            for name in self.model_dic.keys():
                self.model_dic[name] = joblib.load(os.path.join(weights_path, name + ".pkl"))
        else:
            raise BaseException("Weights file don't exist!")

    def get_useful_features(self, postcodes,
                            features=['sector', 'easting', 'northing', 'localAuthority', 'altitude', 'soilType']):
        if isinstance(postcodes, pd.Series):
            postcodes = postcodes.to_list()
        if not isinstance(postcodes, list) and not isinstance(postcodes, np.ndarray):
            postcodes = [postcodes]
        frame = self.postcodedb.copy()
        frame = frame.set_index('postcode')

        return frame.loc[postcodes, features]

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
        if isinstance(postcodes, pd.Series):
            postcodes = postcodes.to_list()
        if not isinstance(postcodes, list) and not isinstance(postcodes, np.ndarray):
            postcodes = [postcodes]


        frame = self.postcodedb.copy()
        if not sum(frame["postcode"].isin(postcodes)):
            return None

        frame = frame.set_index('postcode')
        # Convert to Capital
        for i, postcode in enumerate(postcodes):
            postcodes[i] = postcode.upper()

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
        if isinstance(postcodes, pd.Series):
            postcodes = postcodes.to_list()
        if not isinstance(postcodes, list) and not isinstance(postcodes, np.ndarray):
            postcodes = [postcodes]

        if not sum(self.postcodedb["postcode"].isin(postcodes)):
            return None
        es = self.get_easting_northing(postcodes)
        lat, lon = get_gps_lat_long_from_easting_northing(es["easting"].to_list(), es["northing"].to_list())

        return pd.DataFrame(np.concatenate([[lat], [lon]], axis=0).T, columns=["latitude", "longitude"], index=es.index)

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

    def get_flood_class_from_postcodes(self, postcodes, method=1):
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
        if isinstance(postcodes, pd.Series):
            postcodes = postcodes.to_list()
        if not isinstance(postcodes, list) and not isinstance(postcodes, np.ndarray):
            postcodes = [postcodes]

        if not sum(self.postcodedb["postcode"].isin(postcodes)):
            return None

        assert method in [0, 1], 'No such a method'
        if method == 0:
            return pd.Series(data=np.ones(len(postcodes), int),
                             index=np.asarray(postcodes),
                             name='riskLabel')
        elif method == 1:
            OSBG36_cord = self.get_easting_northing(postcodes)
            eastings = OSBG36_cord['easting'].to_list()
            northings = OSBG36_cord['northing'].to_list()
            OS_RLPredic = self.get_flood_class_from_OSGB36_locations(eastings, northings, method=method)

            PC_RLPrediction_Series = pd.Series(data=OS_RLPredic.values,
                                               index=[postcode for postcode in postcodes],
                                               name='riskLabel')

            return PC_RLPrediction_Series
        else:
            raise NotImplementedError

    @staticmethod
    def get_flood_class_from_locations_methods():
        """
        Get a dictionary of available flood probablity classification methods
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

    def get_flood_class_from_OSGB36_locations(self, eastings, northings, method=1):
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
        if isinstance(eastings, pd.Series):
            eastings = eastings.to_list()
            northings = northings.to_list()
        if not isinstance(eastings, list) and not isinstance(eastings, np.ndarray):
            eastings = [eastings]
            northings = [northings]
        assert len(northings) == len(eastings)
        assert method in [0, 1], 'No such a method'

        if method == 0:
            return pd.Series(data=np.ones(len(eastings), int),
                             index=[(est, nth) for est, nth in
                                    zip(eastings, northings)],
                             name='riskLabel')
        elif method == 1:
            cor_list = []
            for est, nor in zip(eastings, northings):
                cor_list.append([est, nor])

            model = self.model_dic['flood_label_model']

            RLPrediction = model.predict(pd.DataFrame(cor_list))

            RLPrediction_Series = pd.Series(data=RLPrediction,
                                            index=[(est, nth) for est, nth in
                                                   zip(eastings, northings)],
                                            name='riskLabel')
            return RLPrediction_Series
        else:
            raise NotImplementedError

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

        assert method in [0, 1], 'No such a method'
        if isinstance(latitudes, pd.Series):
            latitudes = latitudes.to_list()
            longitudes = longitudes.to_list()
        if not isinstance(latitudes, list) and not isinstance(latitudes, np.ndarray):
            latitudes = [latitudes]
            longitudes = [longitudes]
        assert len(latitudes) == len(longitudes)
        if method == 0:
            return pd.Series(data=np.ones(len(longitudes), int),
                             index=[(lng, lat) for lng, lat in
                                    zip(longitudes, latitudes)],
                             name='riskLabel')
        else:
            # convert from WGS84 to OSGB36
            eastings, northings = get_easting_northing_from_gps_lat_long(latitudes, longitudes, rads=rad)
            OS_RLPredic = self.get_flood_class_from_OSGB36_locations(eastings, northings, method)

        WG_RLPrediction_Series = pd.Series(data=OS_RLPredic.values,
                                           index=[(lat, lot) for lat, lot in
                                                  zip(latitudes, longitudes)],
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
        return {'all_england_median': 0, 'KNeighborsRegressor_total_value': 1,
                'KNeighborsRegressor_split_price_area': 2}

    def get_median_house_price_estimate(self, postcodes, method=2):
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
        if isinstance(postcodes, pd.Series):
            postcodes = postcodes.to_list()
        if not isinstance(postcodes, list) and not isinstance(postcodes, np.ndarray):
            postcodes = [postcodes]

        if not sum(self.postcodedb["postcode"].isin(postcodes)):
            return None

        if method == 0:
            return pd.Series(data=np.full(len(postcodes), 245000.0),
                             index=np.asarray(postcodes),
                             name='medianPrice')

        elif method == 1:

            model = self.model_dic['price_model_for_all']
            X_pre = self.get_useful_features(postcodes, ['easting', 'northing'])

            return pd.Series(index=np.asarray(postcodes), data=np.asarray(model.predict(X_pre)).flatten(),
                             name='medianPrice')
        elif method == 2:

            X_pre = self.get_useful_features(postcodes, ['easting', 'northing'])

            # get rank predict model
            rank_model = self.model_dic['rank_classifier']
            X_pre['rank'] = rank_model.predict(X_pre)

            # get differnet price set
            X_high = X_pre[X_pre['rank'] == 'high'].drop(columns='rank')
            X_low = X_pre[X_pre['rank'] == 'low'].drop(columns='rank')
            # get trained model
            low_model = self.model_dic['price_model_for_lower_price']
            high_model = self.model_dic['price_model_for_higher_price']
            if len(X_low) and len(X_high):
                low_result = pd.Series(index=X_low.index, data=np.asarray(low_model.predict(X_low).flatten()),
                                       name='medianPrice')
                high_result = pd.Series(index=X_high.index, data=np.asarray(high_model.predict(X_high).flatten()),
                                        name='medianPrice')

                return pd.concat([low_result, high_result])
            elif len(X_high):
                return pd.Series(index=X_high.index, data=np.asarray(high_model.predict(X_high).flatten()),
                                 name='medianPrice')
            elif len(X_low):
                return pd.Series(index=X_low.index, data=np.asarray(low_model.predict(X_low).flatten()),
                                 name='medianPrice')

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

    def get_local_authority_estimate(self, eastings, northings, method=1):
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
        assert method in [0, 1], 'No such a method'
        if isinstance(eastings, pd.Series):
            eastings = eastings.to_list()
            northings = northings.to_list()
        if not isinstance(eastings, list) and not isinstance(eastings, np.ndarray):
            eastings = [eastings]
            northings = [northings]
        assert len(northings) == len(eastings)
        if method == 0:
            return pd.Series(data=np.full(len(eastings), 'Unknown'),
                             index=[(est, nth) for est, nth in
                                    zip(eastings, northings)],
                             name='localAuthority')
        elif method == 1:
            model = self.model_dic['authority_model']
            cor_list = []
            for est, nor in zip(eastings, northings):
                cor_list.append([est, nor])

            LAPrediction = model.predict(pd.DataFrame(cor_list))
            LAPrediction = self.authority_lencoder.inverse_transform(LAPrediction)
            LAPrediction_Series = pd.Series(data=LAPrediction,
                                            index=[(est, nth) for est, nth in
                                                   zip(eastings, northings)],
                                            name='localAuthority')
            return LAPrediction_Series
        else:
            raise NotImplementedError

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

        if isinstance(postal_data, pd.Series):
            postal_data = postal_data.to_list()
        if not isinstance(postal_data, list) and not isinstance(postal_data, np.ndarray):
            postal_data = [postal_data]

        unlabel_postcode_file = os.sep.join((os.path.dirname(__file__),
                                             'resources',
                                             'unlabeledsampleWithHouseholdAndNearestStation.csv'))
        unlabeled_df = pd.read_csv(unlabel_postcode_file)
        length = postal_data[0].split(" ")
        postal_data_copy = postal_data.copy()
        if len(length[1]) != 3:
            postal_data = unlabeled_df[unlabeled_df['sector'].isin(postal_data)]['postcode'].tolist()
        median_price = self.get_median_house_price_estimate(postal_data)
        households = unlabeled_df[unlabeled_df['postcode'].isin(postal_data)]['households']
        households.index = postal_data
        num_units = unlabeled_df[unlabeled_df['postcode'].isin(postal_data)]['number of postcode units']
        num_units.index = postal_data
        total = median_price * households / num_units
        total.index = postal_data
        total.name = 'total property value'
        return total

    def get_annual_flood_risk(self, postcodes, risk_labels=None):
        """
        Return a series of estimates of the total property values of a
        collection of postcodes.

        Risk is defined here as a damage coefficient multiplied by the
        value under threat multiplied by the probability of an event.

        Parameterszz
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
        if isinstance(postcodes, pd.Series):
            postcodes = postcodes.to_list()
        if not isinstance(postcodes, list) and not isinstance(postcodes, np.ndarray):
            postcodes = [postcodes]

        if not sum(self.postcodedb["postcode"].isin(postcodes)):
            return None

        risk_labels = risk_labels or self.get_flood_class_from_postcodes(postcodes)

        cost = self.get_total_value(postcodes)

        damage_coefficient = 0.05

        risk_proba = [0.0001, 0.0005, 0.001, 0.005, 0.01, 0.015, 0.02, 0.03, 0.04, 0.05]
        risk_proba = np.array(risk_proba)

        risk_df = pd.DataFrame(data=risk_proba.T, columns=['risk_proba'], index=list(range(1, 11)))
        risk_proba = risk_df.loc[risk_labels.to_list()]["risk_proba"]
        risk_proba.index = postcodes

        annual_flood_risk = damage_coefficient * cost * risk_proba

        annual_flood_risk.name = 'Annual Flood Risk'
        return annual_flood_risk
