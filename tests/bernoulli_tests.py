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

def binomial_distribution_creation_test():
	distribution = bayesian_bozo._test_creating_distribution(0,0)
	print distribution
	assert len(distribution) == 101
	for i in distribution:
		assert i == 1/101.

def binomial_distribution_with_no_success_one_observation_test():
	distribution = bayesian_bozo._test_creating_distribution(0,1)
	print distribution
	for i in range(1,101):
		assert distribution[i-1] > distribution[i]

"""def obvious_increased_lift_test():
	result = bayesian_bozo.test_difference_of_proportions(0,10,10,10)
	assert result['is_significant'] == True
	assert 0 < result['lift']['lower_bound'] and 0 < result['lift']['upper_bound']"""
