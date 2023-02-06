

import pandas as pd
import numpy as np


class DataProcessor:
    def __init__(self, path):
        self.path = path

    def get_raw_data(self):
        self.raw_data = pd.read_csv(self.path)
        return self

    def clean_data(self) -> pd.DataFrame:
        stress_cat = pd.CategoricalDtype(categories=[
                                         'low', 'slightly elevated', 'average', 'high', 'over whelming'], ordered=True)
        bp_cat = pd.CategoricalDtype(categories=[
                                     'normal', 'prehypertension', 'hypertension', 'hypertensive crisis'], ordered=True)

        def calc_bmi(df):
            return df.weight_kg / ((df.height_cm/100)**2)

        self.clean_data = (self.raw_data
                           .rename(columns=lambda c: c.lower().replace(' ', '_'))
                           .assign(sex=lambda df_: df_.sex.astype('category'),
                                   ethnicity=lambda df_: df_.ethnicity.astype(
                                       'category'),
                                   state=lambda df_: df_.state.astype(
                                       'category'),
                                   age=lambda df_: df_.age.astype('int32'),
                                   height_cm=lambda df_: df_.height_cm.astype(
                                       'float16'),
                                   weight_kg=lambda df_: df_.weight_lb.astype(
                                       'float16')/2.204,
                                   bmi=lambda df_: calc_bmi(df_),
                                   systolic_bp=lambda df_: df_.systolic_bp.astype(
                                       'int32'),
                                   diastolic_bp=lambda df_: df_.diastolic_bp.astype(
                                       'int32'),
                                   hypertension_category=lambda df_: pd.cut(df_.systolic_bp,
                                                                            bins=[
                                                                                0, 120, 139, 140, 800],
                                                                            labels=['normal', 'prehypertension', 'hypertension', 'hypertensive crisis']).astype(bp_cat),
                                   resting_heart_rate=lambda df_: df_.resting_heart_rate.astype(
                                       'int8'),
                                   fasting_blood_glucose=lambda df_: df_.fasting_blood_glucose.astype(
                                       'int32'),
                                   fasting_triglycerides=lambda df_: df_.fasting_triglycerides.astype(
                                       'int32'),
                                   alzeimers=lambda df_: df_.alzeimers.replace(
                                       {'yes': True, 'no': False}).astype('bool'),
                                   hours_of_sleep=lambda df_: df_.hours_of_sleep.astype(
                                       'int32'),
                                   stress_level=lambda df_: df_.stress_level.astype(
                                       stress_cat)
                                   )
                           .drop(columns=['weight_lb'])
                           )
        return self
# git test
