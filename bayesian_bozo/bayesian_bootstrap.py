import numpy
import itertools

def hdp_for(values, level=.95):
    rounded_values = map(lambda x: round(x, 2), values)
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
  return (p_hypotheses*hypotheses).sum()

def bayesian_bootstrap(numbers, sample_count=5000):
  histogram = list((k, len(list(g)))
           for k, g in itertools.groupby(sorted(numbers)))
  keys = map(lambda x: x[0], histogram)
  counts = map(lambda x: x[1], histogram)
  mean_samples = [fast_mean_sample(keys, counts) for i in range(0,sample_count)]
  mean_mean = numpy.mean(mean_samples)
  return {'mean_samples': mean_samples, 'expected_value':mean_mean, 'hdp_interval':hdp_for(mean_samples)}
