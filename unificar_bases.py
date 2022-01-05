#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 16:30:43 2021

@author: mila
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os as os

datapath = '/home/daniu/Documentos/Mecon/datos/'

os.chdir(datapath)

for i in range(11,19):
    exec("""Datos1_20{} = pd.read_csv("personas_20{}.csv", sep=';').drop('anio' ,axis='columns')""".format(i,i))
    exec("""Datos2_20{} = pd.read_csv("personas_indicadores_genero_20{}.csv", sep=';')""".format(i,i))

df = pd.merge(Datos1_2011, Datos2_2011, on="persona_id")
