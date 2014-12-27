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

def _test_creating_distribution(successes, population, bins=101):
  distribution = numpy.array([1]*bins)/(1.*bins)
  for index in range(0,bins):
    hypothesis = index/(bins*1. - 1)
    distribution[index] = (hypothesis)**successes * (1-hypothesis)**(population-successes)
  distribution = distribution/distribution.sum()
  return distribution

def _compute_exact_lift_data(control_distribution, variant_distribution):
  lifts = []
  for i in control_distribution:
    for k in variant_distribution:
      if i == 0. and k > 0.:
        #print 'Parameters yielding infinity: {0}, {1}'.format(i,k)
        #print 'Types of parameters: {0}, {1}'.format(type(i), type(k))
        continue
      elif i == 0. and k == 0.:
        lift = 0
      else:
        lift = (k - i)/(1. * i)
      lifts.append(lift)
  return dict((k, len(list(g))) for k, g in itertools.groupby(sorted(lifts)))


def _create_unimodal_hpd(distribution):
  total_observations = 1.*sum(distribution.values())
  sorted_bins = [(x[0], x[1]/total_observations) for x in sorted(distribution.items(), key=lambda x: x[1], reverse=True)]
  min_value = None
  max_value = None
  current_level = 0
  current_index = 0
  print sorted_bins[0:100]
  while current_level < .95:
    i = sorted_bins[current_index]
    if min_value == None:
      min_value = i[0]
    if max_value == None:
      max_value = i[0]
    if i[0] < min_value:
      min_value = i[0]
    if i[0] > max_value:
      max_value = i[0]
    current_level += i[1]
    current_index += 1
  print current_level
  return [min_value, max_value]

def test_difference_of_proportions(control_successes, control_population, variant_successes, variant_population):
  if control_population == 0 or variant_population == 0:
    raise RuntimeError('There must be at least one observation in both control and variant populations.')
  control_distribution = _test_creating_distribution(control_successes, control_population)
  variant_distribution = _test_creating_distribution(variant_successes, variant_population)

  lift_distribution = _compute_exact_lift_data(control_distribution, variant_distribution)
  #print sorted(lift_distribution.items(), key=lambda x: x[1])
  unimodal_hpd = _create_unimodal_hpd(lift_distribution)

  print unimodal_hpd

  return {
    'is_significant':0 < unimodal_hpd[0] and 0 < unimodal_hpd[1],
    'lift':{
      'lower_bound':-1,
      'upper_bound':1
    }
  }
