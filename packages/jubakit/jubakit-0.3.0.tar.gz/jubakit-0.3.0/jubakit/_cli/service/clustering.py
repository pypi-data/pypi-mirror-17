# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from jubatus.clustering.types import *

from .generic import GenericCLI
from ..args import Arguments, TDatum
from ..util import *

class ClusteringCLI(GenericCLI):
  @classmethod
  def _name(cls):
    return 'clustering'

  @Arguments(TDatum)
  def do_push(self, d):
    """Syntax: push datum_key datum_value [...]
    Add a point. Bulk request is not supported.
    """
    self._verbose("datum = {0}".format(d))
    if not self.client.push([d]):
      print("Failed")

  @Arguments()
  def do_get_revision(self):
    """Syntax: get_revision
    Return the revision of the cluster.
    """
    print(self.client.get_revision())

  @Arguments()
  def do_get_core_members(self):
    """Syntax: get_core_members
    Return the coreset of the cluster.
    """
    result = self.client.get_core_members()
    for cluster in result:
      print("[Cluster]")
      for member in cluster:
        print("  Datum: {0}".format(member.point))
        print("  (weight: {0})".format(member.weight))

  @Arguments()
  def do_get_k_center(self):
    """Syntax: get_k_center
    Returns k cluster centers.
    """
    result = self.client.get_k_center()
    for cluster in result:
      print("[Cluster]")
      print("  Datum: {0}".format(cluster))

  @Arguments(TDatum)
  def do_get_nearest_center(self, d):
    """Syntax: get_nearest_center datum_key datum_value [...]
    Returns nearest cluster center without adding point to cluster.
    """
    self._verbose("datum = {0}".format(d))
    result = self.client.get_nearest_center(d)
    print(result)

  @Arguments(TDatum)
  def do_get_nearest_members(self, d):
    """Syntax: get_nearest_members datum_key datum_value [...]
    Returns nearest summary of cluster(coreset) from point.
    """
    self._verbose("datum = {0}".format(d))
    result = self.client.get_nearest_members(d)
    for member in result:
      print("Datum: {0}".format(member.point))
      print("(weight: {0})".format(member.weight))
