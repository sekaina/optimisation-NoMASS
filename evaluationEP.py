#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 17:44:21 2018

@author: yannis

"""
import numpy as np
import logging
import logging.handlers

from eppy import modeleditor
from eppy.modeleditor import IDF
import energyplus_wrapper as ep

import config
import fitnessesEP

import logzero
from logzero import logger
from logzero import setup_logger

log_format = '%(message)s'
monitfmt = logzero.LogFormatter(fmt=log_format)

monitoringlog = setup_logger(logfile="monitoring.log", 
                             level=logging.INFO, 
                             formatter=monitfmt)
logzero.loglevel(logging.DEBUG)



IDDPATH = config.IDDPATH
EPLUSPATH = config.EPLUSPATH

IDFPATH = "./model/"
LIBFILE = "./model/material.idf"
LIBWINDOW = "./model/windows.idf"

EPWFILE = IDFPATH + "Paris_Orly.epw"


def feasible(ind):
    """Feasibility function for the individual. Returns True if feasible False
    otherwise."""

    incomp = [[10, 3],[10, 4],[20, 3],[20, 4],[30, 3],[30, 4],[40, 3],
              [40, 4],[1, 4],[4, 4],[21, 4],[31, 4],[8, 0],[18, 0],[28, 0],
              [38, 0],[9, 0],[9, 1],[19, 0],[19, 1],[29, 0],[29, 1],[39, 0],
              [39, 1]]

    if [ind[0], ind[3]] in incomp:
        return False
    elif[ind[4], ind[7]] in incomp:
        return False
    elif[ind[8], ind[11]] in incomp:
        return False
    return True


def evaluation(ind):

    fitness = fitnessesEP.evaluate(ind)
    
    if config.CONSTRAINTS:
        if not feasible(ind):
            return fitness*2
    
    return fitness
    
    

if __name__ == "__main__":
    import random
    indiv = ((random.sample(range(27), 3) + random.sample(range(5), 1)) * 3
             + random.sample(range(12), 12))
    logger.debug(indiv)
    #output = evaluate_phasing(indiv)
    #logger.info(output)
