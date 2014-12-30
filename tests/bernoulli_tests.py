from nose.tools import *

import sys, numpy, math
sys.path.append("/Users/justin/Documents/Code/BayesianBozo")

import bayesian_bozo
import itertools

@raises(RuntimeError)
def no_observations_for_control_and_variant_test():
	bayesian_bozo.test_difference_of_proportions(0,0,0,0)

@raises(RuntimeError)
def no_observations_for_variant_test():
	bayesian_bozo.test_difference_of_proportions(0,1,0,0)

@raises(RuntimeError)
def no_observations_for_control_test():
	bayesian_bozo.test_difference_of_proportions(0,0,0,1)

def one_observation_for_each_no_success_test():
	result = bayesian_bozo.test_difference_of_proportions(0,1,0,1)
	assert 'is_significant' in result
	assert result['is_significant'] == False
	assert 'lift' in result
	assert 'lower_bound' in result['lift']
	assert 'upper_bound' in result['lift']
	assert result['lift']['lower_bound'] < 0 and 0 < result['lift']['upper_bound']

def obvious_increased_lift_test():
	result = bayesian_bozo.test_difference_of_proportions(0,10,10,10)
	assert result['is_significant'] == True
	assert 0 < result['lift']['lower_bound'] and 0 < result['lift']['upper_bound'], "should provide an HPD interval with zero excluded."

def ambiguous_lift_test():
	result = bayesian_bozo.test_difference_of_proportions(10,10,10,10)
	assert result['is_significant'] == False, 'Should never be statistically significant.'
	assert result['lift']['lower_bound'] < 0 and 0 < result['lift']['upper_bound'], "should provide an HPD interval with zero included."

@raises(RuntimeError)
def bayesian_bootstrap_lift_with_no_control_data_test():
	bayesian_bozo.bayesian_bootstrap_lift([],[1,2,3,4])

@raises(RuntimeError)
def bayesian_bootstrap_lift_with_no_variant_data_test():
	bayesian_bozo.bayesian_bootstrap_lift([1,2,3,4],[])

def bayesian_bootstrap_lift_with_single_data_point_test():
	sample_count = 2500
	result = bayesian_bozo.bayesian_bootstrap_lift([1], [2], sample_count=sample_count)
	assert result['mean_lift'] == 1.0
	assert sum(result['lift_samples']) == sample_count, 'Should only see a lift of 1: {0}'.format(sum(result['lift_samples']))

def bayesian_bootstrap_lift_with_two_data_point_test():
	result = bayesian_bozo.bayesian_bootstrap_lift([1,2], [3,4])
	assert result['mean_lift'] > 1.0
	assert not 0 in result['lift_samples'], 'Should be impossible to see a lift of zero with this data.'
	assert result['is_significant'] == True

def bayesian_bootstrap_lift_with_two_discrete_normal_distributions_test():
	control_data = [int(math.floor(i)) for i in numpy.random.normal(0,20,100)]
	variant_data = [int(math.floor(i)) for i in numpy.random.normal(0,20,100)]
	result = bayesian_bozo.bayesian_bootstrap_lift(control_data, variant_data)
	assert result['is_significant'] == False
	assert not float('-inf') in result['hdp'] and not float('inf') in result['hdp'], 'Should have somewhat of an idea of a range.'
	assert result['hdp'][0] < 0

def bayesian_bootstrap_lift_with_two_discrete_normal_distributions_more_samples_test():
	control_data = [int(round(i)) for i in numpy.random.normal(0,20,2000)]
	variant_data = [int(round(i)) for i in numpy.random.normal(0,20,2000)]
	result = bayesian_bozo.bayesian_bootstrap_lift(control_data, variant_data)
	assert result['is_significant'] == False
	assert not float('-inf') in result['hdp'] and not float('inf') in result['hdp'], 'Should have somewhat of an idea of a range.'
	assert result['hdp'][0] > -5, 'Should be smaller range than this.'
	assert result['hdp'][1] < 5, 'Should be smaller range than this.'

def bayesian_bootstrap_lift_with_two_discrete_normals_shifted_by_5_test():
	control_data = [int(round(i)) for i in numpy.random.normal(0,20,1000)]
	variant_data = [int(round(i)) for i in numpy.random.normal(5,20,1000)]
	result = bayesian_bozo.bayesian_bootstrap_lift(control_data, variant_data)
	assert result['is_significant'] == True
	assert result['hdp'][0] <= 5 and 5 <= result['hdp'][1] 