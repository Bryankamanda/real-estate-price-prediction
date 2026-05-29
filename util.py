#!/usr/bin/env python
# coding: utf-8

# In[2]:


# util.py
# Helper functions for Real Estate Price Prediction

import json
import pickle
import numpy as np

# Global variables
__locations = None
__property_types = None
__model = None
__data_columns = None


# ============================================================
# Predict Price
# ============================================================

def predict_price(
    bedrooms,
    property_type,
    location,
    has_gym,
    en_suite,
    swimming_pool,
    has_dsq,
    has_garden
):

    try:

        # Create empty feature vector
        x = np.zeros(len(__data_columns))

        # ----------------------------------------------------
        # Numerical features
        # ----------------------------------------------------

        x[0] = bedrooms
        x[1] = has_gym
        x[2] = en_suite
        x[3] = swimming_pool
        x[4] = has_dsq
        x[5] = has_garden

        # ----------------------------------------------------
        # Handle location
        # ----------------------------------------------------

        if location.lower() in __data_columns:
            loc_index = __data_columns.index(location.lower())
            x[loc_index] = 1

        # ----------------------------------------------------
        # Handle property type
        # ----------------------------------------------------

        if property_type.lower() in __data_columns:
            type_index = __data_columns.index(property_type.lower())
            x[type_index] = 1

        # ----------------------------------------------------
        # Predict
        # ----------------------------------------------------

        prediction = __model.predict([x])[0]

        return round(prediction, 2)

    except Exception as e:
        return str(e)


# ============================================================
# Get Locations
# ============================================================

def get_location_names():
    return __locations


# ============================================================
# Get Property Types
# ============================================================

def get_property_types():
    return __property_types


# ============================================================
# Load Model + Artifacts
# ============================================================

def load_saved_artifacts():

    global __data_columns
    global __locations
    global __property_types
    global __model

    print("Loading saved artifacts...")

    # --------------------------------------------------------
    # Load columns.json
    # --------------------------------------------------------

    with open("columns.json", "r") as f:
        __data_columns = json.load(f)['data_columns']

    # --------------------------------------------------------
    # Example structure assumption
    # --------------------------------------------------------

    # Adjust indexes depending on your dataset
    __locations = __data_columns[6:]
    __property_types = ['Apartment', 'Villa', 'Townhouse', 'Bungalow']

    # --------------------------------------------------------
    # Load trained model
    # --------------------------------------------------------

    with open("real_estate_model.pickle", "rb") as f:
        __model = pickle.load(f)

    print("Artifacts loaded successfully!")


