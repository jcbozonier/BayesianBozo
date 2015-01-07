import numpy, random, itertools, math

def hdp_for(rounded_values, level=.95):
    groupings = {}
    for value in rounded_values:
        if not value in groupings:
            groupings[value] = 0
        groupings[value] += 1
    sorted_lifts = sorted(groupings.items(), key=lambda x: x[1], reverse=False)
    count = len(rounded_values)
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
  return (sampled_data*hypotheses).sum()/(1.0*sampled_data.sum())
  
def bayesian_bootstrap(numbers, sample_count=2500):
  for i in numbers:
    if not type(i) is int:
      raise TypeError('All data must be integers.') 
  histogram = list((k, len(list(g))) for k, g in itertools.groupby(sorted(numbers)))
  keys = map(lambda x: x[0], histogram)
  counts = map(lambda x: x[1], histogram)
  mean_samples = [fast_mean_sample(keys, counts) for i in range(0,sample_count)]
  mean_mean = numpy.mean(mean_samples)
  return {'mean_samples': mean_samples, 'expected_value':mean_mean, 'hdp_interval':hdp_for(mean_samples)}

def bayesian_bootstrap_diff(control_numbers, variant_numbers, sample_count=2500):
  if len(control_numbers) == 0 or len(variant_numbers) == 0:
    raise RuntimeError('Must have at least one data point for control data')

  control_sampled_data = bayesian_bootstrap(control_numbers)
  variant_sampled_data = bayesian_bootstrap(variant_numbers)

  sampled_mean_lifts = []

  for i in range(0,sample_count):
    sampled_control_mean = random.choice(control_sampled_data['mean_samples'])
    sampled_variant_mean = random.choice(variant_sampled_data['mean_samples'])
    sampled_mean_lifts.append(sampled_variant_mean - sampled_control_mean)

  hdp = hdp_for(sampled_mean_lifts)
  
  return {
    'mean_diff':numpy.mean(sampled_mean_lifts),
    'diff_samples': sampled_mean_lifts,
    'is_significant': 0. < hdp[0] and 0. < hdp[1],
    'hdp': hdp
  }

def _compute_bootstrapped_lift_data(control_successes, control_population, variant_successes, variant_population):
  samples = []
  for i in range(0,2500):
    control_rate_sample = numpy.random.beta(1 + control_successes, 1 + control_population - control_successes)
    variant_rate_sample = numpy.random.beta(1 + variant_successes, 1 + variant_population - variant_successes)
    if control_rate_sample == 0:
      if variant_rate_sample == 0:
        samples.append(0.)
      else:
        samples.append(float('inf')) 
    else:
      samples.append(variant_rate_sample/control_rate_sample - 1)
  return dict((k, len(list(g))) for k, g in itertools.groupby(sorted(samples)))

def _create_unimodal_hpd(distribution):
  total_observations = 1.*sum(distribution.values())
  sorted_bins = [(x[0], x[1]/total_observations) for x in sorted(distribution.items(), key=lambda x: x[1], reverse=True)]
  min_value = None
  max_value = None
  current_level = 0
  current_index = 0
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
  return [min_value, max_value]

def test_difference_of_proportions(control_successes, control_population, variant_successes, variant_population):
  if control_population == 0 or variant_population == 0:
    raise RuntimeError('There must be at least one observation in both control and variant populations.')
  lift_distribution = _compute_bootstrapped_lift_data(control_successes, control_population, variant_successes, variant_population)
  unimodal_hpd = _create_unimodal_hpd(lift_distribution)
  return {
    'is_significant':0 < unimodal_hpd[0] and 0 < unimodal_hpd[1],
    'lift':{
      'lower_bound':unimodal_hpd[0],
      'upper_bound':unimodal_hpd[1]
    }
  }

def bayesian_bootstrap_lift(control_numbers, variant_numbers, sample_count=2500):
  if len(control_numbers) == 0 or len(variant_numbers) == 0:
    raise RuntimeError('Must have at least one data point for control data')
  control_sampled_data = bayesian_bootstrap(control_numbers)
  variant_sampled_data = bayesian_bootstrap(variant_numbers)

  sampled_mean_lifts = []

  for i in range(0,sample_count):
    sampled_control_mean = random.choice(control_sampled_data['mean_samples'])
    sampled_variant_mean = random.choice(variant_sampled_data['mean_samples'])
    if sampled_control_mean == 0. and sampled_variant_mean != 0.:
      sampled_mean_lifts.append(float('inf'))
    elif sampled_control_mean == 0. and sampled_variant_mean == 0.:
      sampled_mean_lifts.append(0.)
    else:
      sampled_mean_lifts.append((sampled_variant_mean-sampled_control_mean)/(1.*sampled_control_mean))

  hdp = hdp_for(sampled_mean_lifts)
  
  return {
    'mean_lift':numpy.mean(sampled_mean_lifts),
    'lift_samples': sampled_mean_lifts,
    'is_significant': 0. < hdp[0] and 0. < hdp[1],
    'hdp': hdp
  }
