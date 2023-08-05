import datetime

from sklearn.base import BaseEstimator, TransformerMixin


class FeatureEngineer(BaseEstimator, TransformerMixin):

    # Future: consider a dates_since_min_date feature. This has a high risk of over-fitting though, so I'd prefer not to include it easily.
    def __init__(self, date_cols):
        self.date_cols = date_cols


    def fit(self, X, y=None):
        return self


    def extract_features(self, row, date_val, date_col):

        row[date_col + '_day_of_week'] = str(date_val.weekday())
        row[date_col + '_hour'] = date_val.hour

        minutes_into_day = date_val.hour * 60 + date_val.minute

        if row[date_col + '_day_of_week'] in (5,6):
            row[date_col + '_is_weekend'] = True
        elif row[date_col + '_day_of_week'] == 4 and row[date_col + '_hour'] > 16:
            row[date_col + '_is_weekend'] = True
        else:
            row[date_col + '_is_weekend'] = False

            # Grab rush hour times for the weekdays.
            # We are intentionally not grabbing them for the weekends, since weekend behavior is likely very different than weekday behavior.
            if minutes_into_day < 120:
                row[date_col + '_is_late_night'] = True
            elif minutes_into_day < 11.5 * 60:
                row[date_col + '_is_off_peak'] = True
            elif minutes_into_day < 13.5 * 60:
                row[date_col + '_is_lunch_rush_hour'] = True
            elif minutes_into_day < 17.5 * 60:
                row[date_col + '_is_off_peak'] = True
            elif minutes_into_day < 20 * 60:
                row[date_col + '_is_dinner_rush_hour'] = True
            elif minutes_into_day < 22.5 * 60:
                row[date_col + '_is_off_peak'] = True
            else:
                row[date_col + '_is_late_night'] = True

        return row


    def transform(self, X, y=None):
        for idx, row in enumerate(X):

            for date_col in self.date_cols:
                date_val = row.pop(date_col, False)

                # make sure this property exists for this row
                if date_val:

                    # make sure that value is actually a datetime object
                    if type(date_val) not in (datetime.date, datetime.datetime):
                        print('This value is not a date:')
                        print(date_val)
                        try:
                            date_val = datetime.datetime(date_val)
                        except:
                            pass

                    row = self.extract_features(row, date_val, date_col)
                    X[idx] = row

        return X

