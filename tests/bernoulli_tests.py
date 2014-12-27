from nose.tools import *

import sys
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

def binomial_distribution_with_n_bin_support_test():
	distribution = bayesian_bozo._test_creating_distribution(0,0,bins=1001)
	assert len(distribution) == 1001
	for i in range(1,1001):
		assert distribution[i-1] == distribution[i]
	assert round(sum(distribution),12) == 1

def binomial_distribution_with_one_success_two_observations_n_bin_test():
	distribution = bayesian_bozo._test_creating_distribution(1,2, bins=1001)
	print distribution
	assert distribution[0] == 0
	assert distribution[-1] == 0
	assert distribution[500] > distribution[500-1]
	assert distribution[500] > distribution[500+1]
	assert round(sum(distribution),12) == 1

def compute_exact_lift_between_same_distribution_of_no_observations_test():
	control = bayesian_bozo._test_creating_distribution(0,0, bins=101)
	variant = bayesian_bozo._test_creating_distribution(0,0, bins=101)
	lift_histogram = bayesian_bozo._compute_exact_lift_data(control, variant)
	assert sum(lift_histogram.values()) == len(control)**2
	assert lift_histogram[0] == len(control)**2

def compute_exact_lift_between_same_distribution_with_observations_test():
	control = bayesian_bozo._test_creating_distribution(1,2, bins=101)
	variant = bayesian_bozo._test_creating_distribution(1,2, bins=101)
	lift_histogram = bayesian_bozo._compute_exact_lift_data(control, variant)

	print sorted(lift_histogram.items(), key=lambda x: x[1])

	assert lift_histogram[-1] >= 1
	print 'Number of occurences of zero lift: {0}'.format(lift_histogram[0])
	assert lift_histogram[0] == 151

	for k,v in lift_histogram.items():
		if k != 0 and k != -1:
			assert v < lift_histogram[0]

def create_unimodal_hpd_test():
	unimodal_hpd = bayesian_bozo._create_unimodal_hpd({
		1:2.5,
		3:20,
		5:55,
		7:20,
		10:2.5,
	})
	print unimodal_hpd
	assert unimodal_hpd == [3,7]

def obvious_increased_lift_test():
	result = bayesian_bozo.test_difference_of_proportions(0,20,20,20)
	assert result['is_significant'] == True
	#assert 0 < result['lift']['lower_bound'] and 0 < result['lift']['upper_bound']
