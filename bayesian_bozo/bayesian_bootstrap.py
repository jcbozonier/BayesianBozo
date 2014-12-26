import numpy
import itertools

def hdp_for(rounded_values, level=.95):
    groupings = {}
    for value in rounded_values:
        if not value in groupings:
            groupings[value] = 0
        groupings[value] += 1
    sorted_lifts = sorted(groupings.items(), key=lambda x: x[1], reverse=False)
    count = len(values)
    target_hdp_count = int(level*count)
    current_hdp_count = 0
    hdp_list = []
    while current_hdp_count < target_hdp_count:
        pair = sorted_lifts.pop()
        hdp_list.append(pair[0])
        current_hdp_count += pair[1]
    return [min(hdp_list), max(hdp_list)]

def fast_mean_sample(hypotheses, observations):
  p_hypotheses = numpy.random.dirichlet(observations)
  sampled_data = numpy.random.multinomial(sum(observations), p_hypotheses)
  return (sampled_data*hypotheses).sum()/sampled_data.sum()
  
def bayesian_bootstrap(numbers, sample_count=5000):
  for i in numbers:
    if not type(i) is int:
      raise TypeError('All data must be integers.') 
  histogram = list((k, len(list(g))) for k, g in itertools.groupby(sorted(numbers)))
  keys = map(lambda x: x[0], histogram)
  counts = map(lambda x: x[1], histogram)
  mean_samples = [fast_mean_sample(keys, counts) for i in range(0,sample_count)]
  mean_mean = numpy.mean(mean_samples)
  return {'mean_samples': mean_samples, 'expected_value':mean_mean, 'hdp_interval':hdp_for(mean_samples)}

def test_difference_of_proportions(control_successes, control_population, variant_successes, variant_population):
  if control_population == 0 or variant_population == 0:
    raise RuntimeError('There must be at least one observation in both control and variant populations.')
  return {
    'is_significant':False,
    'lift':{
      'lower_bound':-1,
      'upper_bound':1
    }
  }
