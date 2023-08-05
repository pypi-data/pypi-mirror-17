try:
    import cPickle as pickle
except:
    import pickle
import datetime
import math
import random
import sys

# import auto_ml.predictor
from auto_ml import Predictor
from auto_ml import utils

from sklearn.metrics import mean_squared_error

validation_start_date = datetime.datetime(2016, 8, 1)
# Helper function to write a new set of data_dev
def write_data_dev_to_file(all_rows, threshold=0.99):
    # Keep more of the validation data (min of 10x what we're keeping for dev, or all)
    threshold = float(threshold)
    validation_data_threshold = float(1 - min((1 - threshold) * 10, 1))
    print('threshold')
    print(threshold)
    data_dev = []
    for row in all_rows:
        if row['created_at_in_local_time'] > validation_start_date and random.random() > validation_data_threshold:
            data_dev.append(row)
        elif random.random() > threshold:
            data_dev.append(row)

    with open('data_dev' + str(threshold) + '.pkl', 'wb') as write_file:
        pickle.dump(data_dev, write_file, protocol=2)

    print('Successfullly wrote data_dev to file at ' + 'data_dev' + str(threshold) + '.pkl')
    print('len(data_dev):')
    print(len(data_dev))

    # Return the shortened data_dev, and immediately run it through the rest of our process!
    return data_dev

# saving here so autocomplete works :)
col_names = ['created_at_in_local_time', 'max_20_percentile_item_prep_time', 'max_20_percentile_category_prep_time', 'avg_median_item_prep_time', 'avg_median_category_prep_time', 'max_80_percentile_item_prep_time', 'max_80_percentile_category_prep_time', 'subtotal', 'total_items_in_order', 'max_original_item_price', 'min_original_item_price', 'avg_num_orders_item_appearing_in', 'avg_num_orders_category_appearing_in', 'num_items_with_low_prev_order_count', 'num_categories_with_low_prev_order_count', 'store_starting_point_id', 'market_id', 'submarket_id', 'district_id', 'store_starting_point_id', 'price_range', 'composite_score', 'is_partner', 'rest_price_range', 'restaurant_order_place_latency', 'restaurant_avg_prep_time', 'count_orders_over_100_subtotal', 'restaurant_total_orders', 'rest_avg_rest_order_place_latency_large_orders', 'rest_avg_rest_prep_time_large_orders', 'rest_rest_order_place_latency_lunch_rush_hour', 'rest_rest_order_place_latency_dinner_rush_hour', 'rest_rest_prep_time_lunch_rush_hour', 'rest_rest_prep_time_dinner_rush_hour', 'rest_avg_r2c', 'rest_avg_r2c_vs_estimates', 'rest_avg_r2c_estimates', 'is_automated', 'order_protocol_fax', 'order_protocol_dasher_place', 'order_protocol_phone', 'order_protocol_ipad', 'order_protocol_online_order', 'order_protocol_email', 'preference_level', 'direct_r2c_est_duration', 'flf', 'avg_sp_r2c_estimates', 'sp_avg_r2c', 'sp_avg_r2c_vs_estimates', 'avg_sm_r2c_estimates', 'sm_avg_r2c', 'sm_avg_r2c_vs_estimates', 'avg_district_r2c_estimates', 'district_avg_r2c', 'district_avg_r2c_vs_estimates', 'y_actual_delivery_duration', 'subpredictor_y_order_place_duration', 'subpredictor_y_prep_time_duration', 'subpredictor_y_order_placer_escalated', 'subpredictor_y_refund_was_issued', 'y_current_calculated_estimated_delivery_duration', 'y_current_estimated_delivery_duration']

props_to_delete = [
    # 'subpredictor_y_prep_time_duration',
    # 'subpredictor_y_order_place_duration',
    'subpredictor_y_refund_was_issued',
    'y_current_calculated_estimated_delivery_duration',
    'y_current_calculated_estimated_delivery_duration',
    'y_current_estimated_delivery_duration'
]
# props_to_delete = ['y_current_estimated_delivery_duration', 'y_current_calculated_estimated_delivery_duration']

# Helper function to delete property names from a row of data
def delete_prop_names(row, props_to_delete):
    for prop in props_to_delete:
        try:
            del row[prop]
        except:
            pass
    return row


def calculate_rmse(preds, actuals):
    rmse = mean_squared_error(actuals, preds)**0.5
    return rmse


# Helper function to remove certain "columns" from our dataset.
# This allows us to pass in the predicted values from our current model in the input, and then compare how our new model is doing compared to what's currently live.
def split_output(X, output_column_name):
    y = []
    for row in X:
        y.append(
            row.pop(output_column_name)
        )

    return X, y


# Default Values
file_to_load = 'data_dev0.995.pkl'
write_data_dev = False

# Figure out which file to load, and if we want to create a new dev dataset
if len(sys.argv) > 1:
    if sys.argv[1] in set(['write_file', 'shorten', 'shorten_data','make_dev_data', 'make_data_dev']):
        file_to_load = 'data_all.pkl'
        write_data_dev = True
        if len(sys.argv) > 2:
            threshold = sys.argv[2]
        else:
            threshold = 0.995
    elif sys.argv[1] in set(['full', 'long', 'full_dataset', 'all_data', 'all']):
        file_to_load = 'data_all.pkl'
    elif sys.argv[1] in set(['small', '90', '10']):
        file_to_load = 'data_dev0.9.pkl'
    elif sys.argv[1] in set(['medium', '50', 'half']):
        file_to_load = 'data_dev0.5.pkl'
    else:
        # allow the user to use their own thresholds (like 0.95)
        file_to_load = 'data_dev' + sys.argv[1] + '.pkl'

# This column holds our y values
target_col = 'y_actual_delivery_duration'
current_target_col = 'y_current_estimated_delivery_duration'
bad_vals = set([None, float('nan'), float('Inf')])
max_target_col_threshold = 120 * 60
min_target_col_threshold = 5 * 60
max_subpredictor_y_prep_time_duration_threshold = 120 * 60
min_subpredictor_y_prep_time_duration_threshold = 2 * 60

refund_issued_vals = []
escalated_vals = []

# Load our data
with open(file_to_load) as read_file:
    all_rows = pickle.load(read_file)
    print('\n\nLoaded the data in file: ' + file_to_load)

    if write_data_dev:
        all_rows = write_data_dev_to_file(all_rows, threshold)

    # Split data into train and test
    training_data = []
    testing_data = []
    testing_data_bad = []

    y_current_estimated_delivery_duration = []
    # y_current_calculated_estimated_delivery_duration = []

    y_current_estimated_delivery_duration_bad = []
    # y_current_calculated_estimated_delivery_duration_bad = []

    for row in all_rows:


        # Make sure we only include vals that are relevant.
        if row[target_col] not in bad_vals and row[current_target_col] not in bad_vals:
            refund_issued_vals.append(row['subpredictor_y_refund_was_issued'])
            refund_issued_vals.append(row['subpredictor_y_order_placer_escalated'])

            # Test Data
            # # Currently taking 50% of our data for test data
            # if random.random() > 0.5:
            if row['created_at_in_local_time'] > validation_start_date:

                if min_target_col_threshold <= row[target_col] <= max_target_col_threshold and min_subpredictor_y_prep_time_duration_threshold <= row['subpredictor_y_prep_time_duration'] <= max_subpredictor_y_prep_time_duration_threshold:

                    # Grab current prediction values to compare against
                    # y_current_calculated_estimated_delivery_duration.append(row.pop('y_current_calculated_estimated_delivery_duration'))
                    y_current_estimated_delivery_duration.append(row.pop('y_current_estimated_delivery_duration'))

                    row = delete_prop_names(row, props_to_delete)
                    testing_data.append(row)

                else:
                    y_current_estimated_delivery_duration_bad.append(row.pop('y_current_estimated_delivery_duration', None))

                    row = delete_prop_names(row, props_to_delete)
                    testing_data_bad.append(row)

            # Training Data
            else:
                # Clean row of all vals that might induce overfitting (this includes the current estimator's predicted vals that we might want to benchmark against)
                row = delete_prop_names(row, props_to_delete)
                training_data.append(row)

print('We have loaded, split, and cleaned the raw data! Here\'s the first item in the dataset to show you an example.')
print(training_data[0])

# split out out output column so we have a proper X, y dataset
X_test, y_test = split_output(testing_data, target_col)
X_test_bad, y_test_bad = split_output(testing_data_bad, target_col)

# X_test = testing_data
# y_test_log = [math.log(val) for val in y_test]
# y_current_calculated_estimated_delivery_duration_log = [math.log(val) for val in y_current_calculated_estimated_delivery_duration]
# y_current_estimated_delivery_duration_log = [math.log(val) for val in y_current_estimated_delivery_duration]
# print('RMSE of ' + 'y_current_calculated_estimated_delivery_duration expressed in natural logs')
# print(calculate_rmse(y_current_calculated_estimated_delivery_duration_log, y_test_log))
# print('RMSE of ' + 'y_current_calculated_estimated_delivery_duration in their full scale')
# print(calculate_rmse(y_current_calculated_estimated_delivery_duration, y_test))
# print('RMSE of ' + 'y_current_estimated_delivery_duration expressed in natural logs')
# print(calculate_rmse(y_current_estimated_delivery_duration_log, y_test_log))
# print('RMSE of ' + 'y_current_estimated_delivery_duration in their full scale')
# print(calculate_rmse(y_current_estimated_delivery_duration, y_test))
print('RMSE of ' + target_col)
print(calculate_rmse(y_current_estimated_delivery_duration, y_test))

# print('subpredictor_y_refund_was_issued')
# print(refund_issued_vals)
# print('subpredictor_y_order_placer_escalated')
# print(escalated_vals)


# GET conflat from Jessica. Confirmation Latency. build that in as a subpredictor.
# Recent deliveries that are comparable
# Subpredictor for teh number of delivery events (communications between dasher and customer)
# Batch rates, and triple batch rates. asslat as well. supply generally.
#


ml_predictor = Predictor(
    type_of_estimator='regressor',
    column_descriptions={
        'y_actual_delivery_duration': 'output',
        'created_at_in_local_time': 'date',
        'store_starting_point_id': 'categorical',
        'market_id': 'categorical',
        'submarket_id': 'categorical',
        'district_id': 'categorical'
        # ,'subpredictor_y_prep_time_duration': 'regressor'
        # ,'subpredictor_y_order_place_duration': 'regressor'
        # ,'subpredictor_y_refund_was_issued': 'classifier'
        # ,'subpredictor_y_order_placer_escalated': 'classifier'
        })

print('************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************************')

ml_predictor.train(training_data, perform_feature_selection=True, X_test=X_test, y_test=y_test, ml_for_analytics=True, compute_power=5, take_log_of_y=False, add_cluster_prediction=True, model_names=['XGBRegressor'], num_weak_estimators=5)
# ml_predictor.train(training_data, perform_feature_selection=True, ml_for_analytics=False, compute_power=1, take_log_of_y=False, add_cluster_prediction=False)

print('Here is our score on the holdout data including a bunch of bad/outlier values')
# print(X_test[:3])
print(ml_predictor.score(X_test + X_test_bad, y_test + y_test_bad))

print('Here is our current system\'s RMSE on only these extreme cases:')
print(calculate_rmse(y_current_estimated_delivery_duration_bad, y_test_bad))
print('Here is our newly trained predictor\'s performance on only these extreme cases:')
print(ml_predictor.score(X_test_bad, y_test_bad))
