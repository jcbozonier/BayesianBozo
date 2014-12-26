from nose.tools import *

import sys
sys.path.append("/Users/justin/Documents/Code/BayesianBozo")

import bayesian_bozo

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
