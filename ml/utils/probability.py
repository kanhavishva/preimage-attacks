# -*- coding: utf-8 -*-
import numpy as np
import networkx as nx
from math import log
from itertools import product
from operator import mul
from functools import reduce

from utils.log import getLogger

# The logger is declared at top-level here because otherwise there
# is an error when pickling a `Probability` object in Python multiprocessing
logger = getLogger('probability')

######################################################
#################### PROBABILITY #####################
######################################################

class Probability(object):

  def __init__(self, samples, data=None):
    self.samples = samples
    self.N = samples.shape[0]  # number of samples
    self.n = samples.shape[1]  # number of variables

    if data is not None:
      self.phats = np.load(data)
    else:
      logger.info('Computing marginals for %d random variables...' % self.n)

      self.phats = np.zeros((self.n, 2))
      for rv in range(self.n):
        phat = self.pHat([(rv, 0)])
        self.phats[rv, :] = (phat, 1.0 - phat)


  def save(self, filename):
    logger.info('Saving probability as "%s"...' % filename)
    np.save(filename, self.phats)


  def count(self, random_variables):
    """
    Accepts an array of tuples where each tuple is the random variable index
    and the value taken by that random variable. Returns the number of samples
    in the dataset where the RVs take their assigned values.
    """
    assert len(random_variables) > 0

    # Method 1
    rv_index, rv_value = random_variables[0]
    search = (self.samples.iloc[:, rv_index] == rv_value)

    for rv_index, rv_value in random_variables[1:]:
      search = search & (self.samples.iloc[:, rv_index] == rv_value)

    return self.samples.iloc[search.values].shape[0]

    """
    # Method 2: This is slower, don't use
    rv_indices = [rv_idx for rv_idx, _ in random_variables]
    rv_values = tuple(bool(rv_val) for _, rv_val in random_variables)
    df = self.samples.set_index(rv_indices).sort_index()
    try:
      return df.loc[rv_values].shape[0]
    except KeyError:
      return 0
    """


  def pHat(self, random_variables):
    return float(self.count(random_variables)) / self.N


  def iHat(self, rv_indices):
    """Mutual information score"""
    bit_sequences = product([0, 1], repeat=len(rv_indices))
    total = 0

    for rv_values in bit_sequences:
      rv_assignments = list(zip(rv_indices, rv_values))
      phat = self.pHat(rv_assignments)
      denominator = 1.0
      for rv_index, rv_val in rv_assignments:
        denominator *= self.phats[rv_index, rv_val]
      if phat == 0 or denominator == 0:
        continue
      total += phat * log(phat / denominator)

    return total
