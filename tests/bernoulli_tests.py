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
	for i in range(1,101):
		assert distribution[i-1] == distribution[i]
	assert round(sum(distribution),12) == 1

def binomial_distribution_with_no_success_one_observation_test():
	distribution = bayesian_bozo._test_creating_distribution(0,1)
	print distribution
	delta = round(distribution[0] - distribution[1], 12) # Rounding to avoid floating point error.
	print 'Target delta is ' + str(delta)
	for i in range(1,101):
		assert distribution[i] < distribution[i-1]
		print round(distribution[i-1] - distribution[i], 12)
		assert round(distribution[i-1] - distribution[i], 12) == delta
	assert distribution[0] > 0 and distribution[-1] == 0
	assert round(sum(distribution),12) == 1

def binomial_distribution_with_one_success_one_observation_test():
	distribution = bayesian_bozo._test_creating_distribution(1,1)
	print distribution
	delta = round(distribution[0] - distribution[1], 12) # Rounding to avoid floating point error.
	print 'Target delta is ' + str(delta)
	for i in range(1,101):
		assert distribution[i] > distribution[i-1]
		print round(distribution[i-1] - distribution[i], 12)
		assert round(distribution[i-1] - distribution[i], 12) == delta
	assert distribution[0] == 0 and distribution[-1] > 0
	assert round(sum(distribution),12) == 1

def binomial_distribution_with_one_success_two_observations_test():
	distribution = bayesian_bozo._test_creating_distribution(1,2)
	print distribution
	assert distribution[0] == 0
	assert distribution[-1] == 0
	assert distribution[50] > distribution[50-1]
	assert distribution[50] > distribution[50+1]
	assert round(sum(distribution),12) == 1

"""def obvious_increased_lift_test():
	result = bayesian_bozo.test_difference_of_proportions(0,10,10,10)
	assert result['is_significant'] == True
	assert 0 < result['lift']['lower_bound'] and 0 < result['lift']['upper_bound']"""
