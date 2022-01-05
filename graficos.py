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
import warnings
warnings.filterwarnings("ignore")

datapath = '/home/daniu/Documentos/Mecon/datos/'
figspath = '/home/daniu/Documentos/Mecon/figs/'
tablespath = '/home/daniu/Documentos/Mecon/tablas/'

os.chdir(datapath)

for i in range(11,19):
    exec("""Datos1_20{} = pd.read_csv("personas_20{}.csv", sep=';').drop('anio' ,axis='columns')""".format(i,i))
    exec("""Datos2_20{} = pd.read_csv("personas_indicadores_genero_20{}.csv", sep=';')""".format(i,i))

# Creo un nuevo df que tenga el porcentaje de publicaciones de mujeres y varones para cada año

anios = pd.date_range('01-2011', '01-2018', freq='AS')
columnas = ['Publicaciones mujeres (%)',
            'Publicaciones hombres (%)',
            'Publicaciones mujeres media (per capita)',
            'Publicaciones hombres media (per capita)',
            'Publicaciones mujeres SD (per capita)',
            'Publicaciones hombres SD (per capita)',
            'Total publicaciones (N)']

df_publ_por_genero = pd.DataFrame(index=anios, columns=columnas)

for i, iyear in enumerate(range(2011,2019)):
    exec("""df = pd.merge(Datos1_{}, Datos2_{}, on="persona_id")""".format(iyear,iyear))

    df_clean = df.replace({ -1: np.nan})

    prod_total = int(df_clean['produccion_cantidad_articulos_total'].sum())

    prod_hombres = df_clean.loc[df_clean['sexo_id'] == 2, 'produccion_cantidad_articulos_total'].sum()
    cant_hombres = df_clean.loc[df_clean['sexo_id'] == 2, 'produccion_cantidad_articulos_total'].count()

    prod_mujeres = df_clean.loc[df_clean['sexo_id'] == 1, 'produccion_cantidad_articulos_total'].sum()
    cant_mujeres = df_clean.loc[df_clean['sexo_id'] == 1, 'produccion_cantidad_articulos_total'].count()

    std_hombres = df_clean.loc[df_clean['sexo_id'] == 2, 'produccion_cantidad_articulos_total'].std()
    std_mujeres = df_clean.loc[df_clean['sexo_id'] == 1, 'produccion_cantidad_articulos_total'].std()

    df_publ_por_genero.iloc[i,0] = prod_mujeres/prod_total * 100
    df_publ_por_genero.iloc[i,1] = prod_hombres/prod_total * 100
    df_publ_por_genero.iloc[i,2] = prod_mujeres/cant_mujeres
    df_publ_por_genero.iloc[i,3] = prod_hombres/cant_hombres
    df_publ_por_genero.iloc[i,4] = std_mujeres
    df_publ_por_genero.iloc[i,5] = std_hombres
    df_publ_por_genero.iloc[i,6] = prod_total

df_publ_por_genero.astype('float').round(2)
df_publ_por_genero.to_csv(tablespath + 'cantidad_publicaciones_por_genero.csv')


# Creo un nuevo df que tenga el porcentaje de publicaciones de mujeres y varones para cada año considerando las distintas bandas de edades
columnas = ['Publicaciones mujeres (%)',
            'Publicaciones hombres (%)',
            'Cantidad mujeres (Nm)',
            'Cantidad hombres (Nh)',
            'Publicaciones mujeres media (per capita)',
            'Publicaciones hombres media (per capita)',
            'Publicaciones mujeres SD (per capita)',
            'Publicaciones hombres SD (per capita)',
            'Total publicaciones (N)']

rangos = ['20-30','30-40','40-50','50-60','60+']
index = pd.MultiIndex.from_product([anios, rangos])
edades = [[20,30], [30,40], [40,50], [50,60], [60,1000]]
df_publ_por_genero_edad = pd.DataFrame(index=index, columns=columnas)

for i, iyear in enumerate(range(2011,2019)):
    exec("""df = pd.merge(Datos1_{}, Datos2_{}, on="persona_id")""".format(iyear,iyear))

    df_clean = df.replace({ -1: np.nan})

    itime = anios[i].strftime("%Y-%m-%d")

    for j, jedad in enumerate(edades):

        prod_total = int(df_clean.loc[(df_clean['edad'] >= jedad[0]) & (df_clean['edad'] < jedad[1]), 'produccion_cantidad_articulos_total'].sum())

        p_hombres = df_clean.loc[(df_clean['sexo_id'] == 2) & (df_clean['edad'] >= jedad[0]) & (df_clean['edad'] < jedad[1]),
                    'produccion_cantidad_articulos_total'].sum()
        p_mujeres = df_clean.loc[(df_clean['sexo_id'] == 1) & (df_clean['edad'] >= jedad[0]) & (df_clean['edad'] < jedad[1]),
                    'produccion_cantidad_articulos_total'].sum()
        q_hombres = df_clean.loc[(df_clean['sexo_id'] == 2) & (df_clean['edad'] >= jedad[0]) & (df_clean['edad'] < jedad[1]),
                    'produccion_cantidad_articulos_total'].count()
        q_mujeres = df_clean.loc[(df_clean['sexo_id'] == 1) & (df_clean['edad'] >= jedad[0]) & (df_clean['edad'] < jedad[1]),
                    'produccion_cantidad_articulos_total'].count()
        std_hombres = df_clean.loc[(df_clean['sexo_id'] == 2) & (df_clean['edad'] >= jedad[0]) & (df_clean['edad'] < jedad[1]),
                    'produccion_cantidad_articulos_total'].std()
        std_mujeres = df_clean.loc[(df_clean['sexo_id'] == 1) & (df_clean['edad'] >= jedad[0]) & (df_clean['edad'] < jedad[1]),
                    'produccion_cantidad_articulos_total'].std()

        jrango = rangos[j]

        df_publ_por_genero_edad.loc[(itime, jrango), 'Publicaciones mujeres (%)'] = p_mujeres/prod_total * 100
        df_publ_por_genero_edad.loc[(itime, jrango), 'Publicaciones hombres (%)'] = p_hombres/prod_total * 100
        df_publ_por_genero_edad.loc[(itime, jrango), 'Cantidad mujeres (Nm)'] = q_mujeres
        df_publ_por_genero_edad.loc[(itime, jrango), 'Cantidad hombres (Nh)'] = q_hombres
        df_publ_por_genero_edad.loc[(itime, jrango), 'Publicaciones mujeres media (per capita)'] = p_mujeres/q_mujeres
        df_publ_por_genero_edad.loc[(itime, jrango), 'Publicaciones hombres media (per capita)'] = p_hombres/q_hombres
        df_publ_por_genero_edad.loc[(itime, jrango), 'Publicaciones mujeres SD (per capita)'] = std_hombres
        df_publ_por_genero_edad.loc[(itime, jrango), 'Publicaciones hombres SD (per capita)'] = std_mujeres
        df_publ_por_genero_edad.loc[(itime, jrango), 'Total publicaciones (N)'] = prod_total

df_publ_por_genero_edad = df_publ_por_genero_edad.astype('float').round(2)
df_publ_por_genero_edad.to_csv(tablespath + 'cantidad_publicaciones_por_genero_y_edad.csv')
#
# for j, jedad in enumerate(edades):
#
#     jrango = rangos[j]
#
#     df_temp = df_publ_por_genero_edad.loc[(slice(None),jrango), :]
#     print(jrango)
#     print(df_temp.mean())

# Creo un nuevo df que tenga el porcentaje de publicaciones de mujeres y varones para cada año considerando la categoria conicet

categoria = np.arange(1,14,1)
label_categoria = ['Investigador asistente', 'Investigador adjunto',
                    'Investigador independiente', 'Investigador principal',
                    'Investigador superior', 'Becario doctoral',
                    'Becario postdoctoral', 'Personal de apoyo',
                    'Gestión CyT', 'Pasante', 'Otro personal Conicet',
                    'Investigador correspondiente', 'Investigador superior emérito']

columnas = ['Publicaciones mujeres (%)',
            'Publicaciones hombres (%)',
            'Publicaciones mujeres (per capita)',
            'Publicaciones hombres (per capita)',
            'Publicaciones mujeres SD (per capita)',
            'Publicaciones hombres SD (per capita)',
            'Total publicaciones (N)',
            'Cantidad de mujeres (Nm)',
            'Cantidad de hombres (Nh)']

index = pd.MultiIndex.from_product([anios, label_categoria])
df_publ_por_genero_cat_conicet = pd.DataFrame(index=index, columns=columnas)

for i, iyear in enumerate(range(2011,2019)):
    exec("""df = pd.merge(Datos1_{}, Datos2_{}, on="persona_id")""".format(iyear,iyear))

    df_clean = df.replace({ -1: np.nan})

    itime = anios[i].strftime("%Y-%m-%d")

    for j, jseniority in enumerate(label_categoria):

        prod_total = int(df_clean.loc[df_clean['categoria_conicet_id'] == j+1, 'produccion_cantidad_articulos_total'].sum())

        p_hombres = df_clean.loc[(df_clean['sexo_id'] == 2) & (df_clean['categoria_conicet_id'] == j+1),
                    'produccion_cantidad_articulos_total'].sum()
        p_mujeres = df_clean.loc[(df_clean['sexo_id'] == 1) & (df_clean['categoria_conicet_id'] == j+1),
                    'produccion_cantidad_articulos_total'].sum()
        q_hombres = df_clean.loc[(df_clean['sexo_id'] == 2) & (df_clean['categoria_conicet_id'] == j+1),
                    'produccion_cantidad_articulos_total'].count()
        q_mujeres = df_clean.loc[(df_clean['sexo_id'] == 1) & (df_clean['categoria_conicet_id'] == j+1),
                    'produccion_cantidad_articulos_total'].count()
        std_hombres = df_clean.loc[(df_clean['sexo_id'] == 2) & (df_clean['categoria_conicet_id'] == j+1),
                    'produccion_cantidad_articulos_total'].std()
        std_mujeres = df_clean.loc[(df_clean['sexo_id'] == 1) & (df_clean['categoria_conicet_id'] == j+1),
                    'produccion_cantidad_articulos_total'].std()

        df_publ_por_genero_cat_conicet.loc[(itime, jseniority), 'Publicaciones mujeres (%)'] = p_mujeres/prod_total * 100
        df_publ_por_genero_cat_conicet.loc[(itime, jseniority), 'Publicaciones hombres (%)'] = p_hombres/prod_total * 100
        df_publ_por_genero_cat_conicet.loc[(itime, jseniority), 'Publicaciones mujeres (per capita)'] = p_mujeres/q_mujeres
        df_publ_por_genero_cat_conicet.loc[(itime, jseniority), 'Publicaciones hombres (per capita)'] = p_hombres/q_hombres
        df_publ_por_genero_cat_conicet.loc[(itime, jseniority), 'Publicaciones mujeres SD (per capita)'] = std_mujeres
        df_publ_por_genero_cat_conicet.loc[(itime, jseniority), 'Publicaciones hombres SD (per capita)'] = std_hombres


        df_publ_por_genero_cat_conicet.loc[(itime, jseniority), 'Total publicaciones (N)'] = prod_total

        df_publ_por_genero_cat_conicet.loc[(itime, jseniority), 'Cantidad de mujeres (Nm)'] = q_mujeres
        df_publ_por_genero_cat_conicet.loc[(itime, jseniority), 'Cantidad de hombres (Nh)'] = q_hombres

df_publ_por_genero_cat_conicet = df_publ_por_genero_cat_conicet.astype('float').round(2)

df_publ_por_genero_cat_conicet.to_csv(tablespath + 'cantidad_publicaciones_por_genero_y_categoria_conicet.csv')
#
# for j, jseniority in enumerate(label_categoria):
#     df_temp = df_publ_por_genero_cat_conicet.loc[(slice(None),jseniority), :]
#    print(jseniority)
#    print(df_temp.mean())

columnas = ['Cantidad de mujeres (Nm)', 'Cantidad de hombres (Nh)', 'Porcentaje de mujeres (%)', 'Porcentaje de hombres (%)']
df_cantidad_rrhh_categoria = pd.DataFrame(index=label_categoria, columns=columnas)

for j, jseniority in enumerate(label_categoria):
    q_mujeres = df_publ_por_genero_cat_conicet.loc[(slice(None),jseniority), 'Cantidad de mujeres (Nm)'].sum()
    df_cantidad_rrhh_categoria.iloc[j,0] = q_mujeres
    q_hombres = df_publ_por_genero_cat_conicet.loc[(slice(None),jseniority), 'Cantidad de hombres (Nh)'].sum()
    df_cantidad_rrhh_categoria.iloc[j,1] = q_hombres

    q_tot = q_mujeres + q_hombres
    df_cantidad_rrhh_categoria.iloc[j,2] = q_mujeres/q_tot * 100
    df_cantidad_rrhh_categoria.iloc[j,3] = q_hombres/q_tot * 100

# plots de verdad
color_h = 'teal'
color_m = 'indigo'

# Figura 0
figname = 'boxplot_cantidad_publicaciones_por_genero'
fontsize = 8
xlabels = ['Mujeres','Hombres']
gm = []
gh = []

for i, iyear in enumerate(range(2011,2019)):
    exec("""df = pd.merge(Datos1_{}, Datos2_{}, on="persona_id")""".format(iyear,iyear))

    df_clean = df.replace({ -1: np.nan})
    # plots a la cachurra
    df_h = df_clean.loc[df_clean['sexo_id']==2,'produccion_cantidad_articulos_total'].values
    df_m = df_clean.loc[df_clean['sexo_id']==1,'produccion_cantidad_articulos_total'].values

    gh.append(df_h.tolist())
    gm.append(df_m.tolist())

gm = [item for sublist in gm for item in sublist]
gh = [item for sublist in gh for item in sublist]

data = pd.DataFrame(gm, columns=['mujeres'])
data['hombres'] = pd.DataFrame(gh)

tabla = data.describe()

# Figura 1
figname = 'evolucion_cantidad_publicaciones_por_genero'
fontsize = 8
x = np.arange(1, len(df_publ_por_genero)+1)
xlabels = np.arange(2011, 2019)
yh = df_publ_por_genero["Publicaciones hombres media (per capita)"]
ym = df_publ_por_genero["Publicaciones mujeres media (per capita)"]

fig = plt.figure(figsize=(7,4))
ax = plt.axes([0.1, 0.1, 0.85, 0.85])
gm = ax.bar(x-0.2, ym, width=0.4, color=color_m, alpha=.5, label='Femenino')
gh = ax.bar(x+0.2, yh, width=0.4, color=color_h, alpha=.5, label='Masculino')
ax.tick_params('both', labelsize=fontsize)
ax.legend(fontsize=fontsize)
ax.grid(axis='y', lw=0.5, linestyle=':', color='dimgrey')
ax.set_xticks(x)
ax.set_xticklabels(xlabels, fontsize=fontsize)
ax.set_yticks([0,1,2,3,4])
ax.set_ylim([0,4])

ax.set_xlabel('Año', fontsize=fontsize)
ax.set_ylabel('Cantidad de publicaciones\n(per capita)', fontsize=fontsize)

tpubl = df_publ_por_genero["Total publicaciones (N)"]
bx = ax.twinx()
bx.plot(x, tpubl, '*-', lw=0.5, color='blue')
bx.tick_params(labelsize=fontsize)
bx.set_ylabel('Total publicaciones', fontsize=fontsize, color='blue')
bx.set_ylim([160000, 240000])
bx.tick_params(axis="y", labelcolor="blue")

fig.savefig(figspath + figname + '.png', dpi=300, bbox_inches='tight')
fig.savefig(figspath + figname + '.pdf', bbox_inches='tight')

# Figura 2
figname = 'cantidad_publicaciones_por_genero_y_edad'
fontsize = 8

lista_h_mean = []
lista_h_std = []
lista_m_mean = []
lista_m_std = []

for j, jedad in enumerate(edades):

    jrango = rangos[j]

    df_temp = df_publ_por_genero_edad.loc[(slice(None),jrango), :]
    mean_h = df_temp['Publicaciones hombres media (per capita)'].mean()
    std_h = df_temp['Publicaciones hombres media (per capita)'].std()

    lista_h_mean.append(mean_h)
    lista_h_std.append(std_h)

    mean_m = df_temp['Publicaciones mujeres media (per capita)'].mean()
    std_m = df_temp['Publicaciones mujeres media (per capita)'].std()

    lista_m_mean.append(mean_m)
    lista_m_std.append(std_m)

x = np.arange(1, len(lista_h_mean)+1)
xlabels = rangos
yh = lista_h_mean
ym = lista_m_mean
lista_m_std = [0.11, 0.15, 0.14, 0.24, 0.55]
lista_h_std = [0.14, 0.17, 0.19, 0.24, 0.55]

xlabels = ['20 a 30\naños', '30 a 40\naños', '40 a 50\naños', '50 a 60\naños', '60+\naños']

fig = plt.figure(figsize=(6,4))
ax = plt.axes([0.1, 0.1, 0.85, 0.85])
gm = ax.bar(x-0.2, ym, width=0.4, color=color_m, alpha=.5, yerr=lista_m_std, label='Femenino')
gh = ax.bar(x+0.2, yh, width=0.4, color=color_h, alpha=.5, yerr=lista_h_std, label='Masculino')
ax.tick_params('both', labelsize=fontsize)
# ax.set_title('2)', fontsize=fontsize, loc='left')
ax.legend(fontsize=fontsize, loc='upper right')
ax.set_xticks(x)
ax.set_xticklabels(xlabels, fontsize=fontsize)
#ax.set_yticks([0,1,2])
ax.grid(axis='y', lw=0.5, linestyle=':', color='dimgrey')
ax.set_xlabel('Rango de edad', fontsize=fontsize)
ax.set_ylabel('Cantidad de publicaciones\n(per capita)', fontsize=fontsize)
fig.savefig(figspath + figname + '.png', dpi=300, bbox_inches='tight')
fig.savefig(figspath + figname + '.pdf', bbox_inches='tight')

# Figura 4
figname = 'cantidad_publicaciones_por_genero_y_categoria_conicet'
fontsize = 8

xlabels = label_categoria[0:7]
xlabels = ['Becario doctoral',
 'Becario postdoctoral',
 'Investigador asistente',
 'Investigador adjunto',
 'Investigador independiente',
 'Investigador principal',
 'Investigador superior']

x = np.arange(1, len(xlabels)+1)

fig = plt.figure(figsize=(8,4))
ax = plt.axes([0.1, 0.1, 0.85, 0.85])

for j, jseniority in enumerate(xlabels):
    df_temp = df_publ_por_genero_cat_conicet.loc[(slice(None),jseniority), :]

    yh = df_temp['Publicaciones hombres (per capita)'].mean()
    ym = df_temp['Publicaciones mujeres (per capita)'].mean()

    yh_std = df_temp['Publicaciones hombres (per capita)'].std()
    ym_std = df_temp['Publicaciones mujeres (per capita)'].std()

    gm = ax.bar(x[j]-0.2, ym, width=0.4, color=color_m, alpha=.5, yerr = ym_std, label='Femenino')
    gh = ax.bar(x[j]+0.2, yh, width=0.4, color=color_h, alpha=.5, yerr = yh_std, label='Masculino')
    if j==0:
        ax.legend(fontsize=fontsize, loc='upper left')

ax.tick_params('both', labelsize=fontsize)
# ax.set_title('1)', fontsize=fontsize, loc='left')
ax.set_xticks(x)
xlabels = ['Becario\ndoctoral',
 'Becario\npostdoctoral',
 'Investigador\nasistente',
 'Investigador\nadjunto',
 'Investigador\nindependiente',
 'Investigador\nprincipal',
 'Investigador\nsuperior',
]
ax.grid(axis='y', lw=0.5, linestyle=':', color='dimgrey')

ax.set_xticklabels(xlabels, fontsize=fontsize)
ax.set_yticks([0,4,8,12,16, 20, 24, 28, 32])
ax.set_xlabel('Categoría', fontsize=fontsize)
ax.set_ylabel('Cantidad de publicaciones\n(per capita)', fontsize=fontsize)

fig.savefig(figspath + figname + '.png', dpi=300, bbox_inches='tight')
fig.savefig(figspath + figname + '.pdf', bbox_inches='tight')

##############################################################################
#Tipos de publicaciones

###Publicaciones Q1

anios = pd.date_range('01-2011', '01-2018', freq='AS')
columnas = ['Publicaciones Q1 mujeres (%)',
            'Publicaciones Q1 hombres (%)',
            'Publicaciones mujeres Q1 (per capita)',
            'Publicaciones hombres Q1 (per capita)',
            'Total publicaciones Q1 (N)']

df_publ_por_genero_Q1 = pd.DataFrame(index=anios, columns=columnas)

for i, iyear in enumerate(range(2011,2019)):
    exec("""df = pd.merge(Datos1_{}, Datos2_{}, on="persona_id")""".format(iyear,iyear))

    df_clean = df.replace({ -1: np.nan})


    prod_total_Q1 = int(df_clean['produccion_cantidad_articulos_SJR_Q1'].sum())

    prod_hombres_Q1 = df_clean.loc[df_clean['sexo_id'] == 2, 'produccion_cantidad_articulos_SJR_Q1'].sum()
    cant_hombres_Q1 = df_clean.loc[df_clean['sexo_id'] == 2, 'produccion_cantidad_articulos_SJR_Q1'].count()

    prod_mujeres_Q1 = df_clean.loc[df_clean['sexo_id'] == 1, 'produccion_cantidad_articulos_SJR_Q1'].sum()
    cant_mujeres_Q1 = df_clean.loc[df_clean['sexo_id'] == 1, 'produccion_cantidad_articulos_SJR_Q1'].count()

    df_publ_por_genero_Q1.iloc[i,0] = prod_mujeres_Q1/prod_total_Q1 * 100
    df_publ_por_genero_Q1.iloc[i,1] = prod_hombres_Q1/prod_total_Q1 * 100
    df_publ_por_genero_Q1.iloc[i,2] = prod_mujeres_Q1/cant_mujeres_Q1
    df_publ_por_genero_Q1.iloc[i,3] = prod_hombres_Q1/cant_hombres_Q1
    df_publ_por_genero_Q1.iloc[i,4] = prod_total_Q1

df_publ_por_genero_Q1.astype('float').round(2)
df_publ_por_genero_Q1.to_csv(tablespath + 'cantidad_publicaciones_Q1_por_genero.csv')


##### Publicaciones Q2

anios = pd.date_range('01-2011', '01-2018', freq='AS')
columnas = ['Publicaciones Q2 mujeres (%)',
            'Publicaciones Q2 hombres (%)',
            'Publicaciones mujeres Q2 (per capita)',
            'Publicaciones hombres Q2 (per capita)',
            'Total publicaciones Q2 (N)']

df_publ_por_genero_Q2 = pd.DataFrame(index=anios, columns=columnas)

for i, iyear in enumerate(range(2011,2019)):
    exec("""df = pd.merge(Datos1_{}, Datos2_{}, on="persona_id")""".format(iyear,iyear))
    df_clean = df.replace({ -1: np.nan})


    prod_total_Q2 = int(df_clean['produccion_cantidad_articulos_SJR_Q2'].sum())

    prod_hombres_Q2 = df_clean.loc[df_clean['sexo_id'] == 2, 'produccion_cantidad_articulos_SJR_Q2'].sum()
    cant_hombres_Q2 = df_clean.loc[df_clean['sexo_id'] == 2, 'produccion_cantidad_articulos_SJR_Q2'].count()

    prod_mujeres_Q2 = df_clean.loc[df_clean['sexo_id'] == 1, 'produccion_cantidad_articulos_SJR_Q2'].sum()
    cant_mujeres_Q2 = df_clean.loc[df_clean['sexo_id'] == 1, 'produccion_cantidad_articulos_SJR_Q2'].count()

    df_publ_por_genero_Q2.iloc[i,0] = prod_mujeres_Q2/prod_total_Q2 * 100
    df_publ_por_genero_Q2.iloc[i,1] = prod_hombres_Q2/prod_total_Q2 * 100
    df_publ_por_genero_Q2.iloc[i,2] = prod_mujeres_Q2/cant_mujeres_Q2
    df_publ_por_genero_Q2.iloc[i,3] = prod_hombres_Q2/cant_hombres_Q2
    df_publ_por_genero_Q2.iloc[i,4] = prod_total_Q2

df_publ_por_genero_Q2.astype('float').round(2)
df_publ_por_genero_Q2.to_csv(tablespath + 'cantidad_publicaciones_Q2_por_genero.csv')


##### Publicaciones Q3

anios = pd.date_range('01-2011', '01-2018', freq='AS')
columnas = ['Publicaciones Q3 mujeres (%)',
            'Publicaciones Q3 hombres (%)',
            'Publicaciones mujeres Q3 (per capita)',
            'Publicaciones hombres Q3 (per capita)',
            'Total publicaciones Q3 (N)']

df_publ_por_genero_Q3 = pd.DataFrame(index=anios, columns=columnas)

for i, iyear in enumerate(range(2011,2019)):
    exec("""df = pd.merge(Datos1_{}, Datos2_{}, on="persona_id")""".format(iyear,iyear))
    df_clean = df.replace({ -1: np.nan})


    prod_total_Q3 = int(df_clean['produccion_cantidad_articulos_SJR_Q3'].sum())

    prod_hombres_Q3 = df_clean.loc[df_clean['sexo_id'] == 2, 'produccion_cantidad_articulos_SJR_Q3'].sum()
    cant_hombres_Q3 = df_clean.loc[df_clean['sexo_id'] == 2, 'produccion_cantidad_articulos_SJR_Q3'].count()

    prod_mujeres_Q3 = df_clean.loc[df_clean['sexo_id'] == 1, 'produccion_cantidad_articulos_SJR_Q3'].sum()
    cant_mujeres_Q3 = df_clean.loc[df_clean['sexo_id'] == 1, 'produccion_cantidad_articulos_SJR_Q3'].count()

    df_publ_por_genero_Q3.iloc[i,0] = prod_mujeres_Q3/prod_total_Q3 * 100
    df_publ_por_genero_Q3.iloc[i,1] = prod_hombres_Q3/prod_total_Q3 * 100
    df_publ_por_genero_Q3.iloc[i,2] = prod_mujeres_Q3/cant_mujeres_Q3
    df_publ_por_genero_Q3.iloc[i,3] = prod_hombres_Q3/cant_hombres_Q3
    df_publ_por_genero_Q3.iloc[i,4] = prod_total_Q3

df_publ_por_genero_Q3.astype('float').round(2)
df_publ_por_genero_Q3.to_csv(tablespath + 'cantidad_publicaciones_Q3_por_genero.csv')


##### Publicaciones Q4

anios = pd.date_range('01-2011', '01-2018', freq='AS')
columnas = ['Publicaciones Q4 mujeres (%)',
            'Publicaciones Q4 hombres (%)',
            'Publicaciones mujeres Q4 (per capita)',
            'Publicaciones hombres Q4 (per capita)',
            'Total publicaciones Q4 (N)']

df_publ_por_genero_Q4 = pd.DataFrame(index=anios, columns=columnas)

for i, iyear in enumerate(range(2011,2019)):
    exec("""df = pd.merge(Datos1_{}, Datos2_{}, on="persona_id")""".format(iyear,iyear))
    df_clean = df.replace({ -1: np.nan})


    prod_total_Q4 = int(df_clean['produccion_cantidad_articulos_SJR_Q4'].sum())

    prod_hombres_Q4 = df_clean.loc[df_clean['sexo_id'] == 2, 'produccion_cantidad_articulos_SJR_Q4'].sum()
    cant_hombres_Q4 = df_clean.loc[df_clean['sexo_id'] == 2, 'produccion_cantidad_articulos_SJR_Q4'].count()

    prod_mujeres_Q4 = df_clean.loc[df_clean['sexo_id'] == 1, 'produccion_cantidad_articulos_SJR_Q4'].sum()
    cant_mujeres_Q4 = df_clean.loc[df_clean['sexo_id'] == 1, 'produccion_cantidad_articulos_SJR_Q4'].count()

    df_publ_por_genero_Q4.iloc[i,0] = prod_mujeres_Q4/prod_total_Q4 * 100
    df_publ_por_genero_Q4.iloc[i,1] = prod_hombres_Q4/prod_total_Q4 * 100
    df_publ_por_genero_Q4.iloc[i,2] = prod_mujeres_Q4/cant_mujeres_Q4
    df_publ_por_genero_Q4.iloc[i,3] = prod_hombres_Q4/cant_hombres_Q4
    df_publ_por_genero_Q4.iloc[i,4] = prod_total_Q4

df_publ_por_genero_Q4.astype('float').round(2)
df_publ_por_genero_Q4.to_csv(tablespath + 'cantidad_publicaciones_Q4_por_genero.csv')



####   NBR
anios = pd.date_range('01-2011', '01-2018', freq='AS')
columnas = ['Publicaciones NBR mujeres (%)',
            'Publicaciones NBR hombres (%)',
            'Publicaciones mujeres NBR (per capita)',
            'Publicaciones hombres NBR (per capita)',
            'Total publicaciones NBR (N)']

df_publ_por_genero_NBR = pd.DataFrame(index=anios, columns=columnas)

for i, iyear in enumerate(range(2011,2019)):
    exec("""df = pd.merge(Datos1_{}, Datos2_{}, on="persona_id")""".format(iyear,iyear))
    df_clean = df.replace({ -1: np.nan})


    prod_total_NBR = int(df_clean['produccion_cantidad_articulos_NBR'].sum())

    prod_hombres_NBR = df_clean.loc[df_clean['sexo_id'] == 2, 'produccion_cantidad_articulos_NBR'].sum()
    cant_hombres_NBR = df_clean.loc[df_clean['sexo_id'] == 2, 'produccion_cantidad_articulos_NBR'].count()

    prod_mujeres_NBR = df_clean.loc[df_clean['sexo_id'] == 1, 'produccion_cantidad_articulos_NBR'].sum()
    cant_mujeres_NBR = df_clean.loc[df_clean['sexo_id'] == 1, 'produccion_cantidad_articulos_NBR'].count()

    df_publ_por_genero_NBR.iloc[i,0] = prod_mujeres_NBR/prod_total_NBR * 100
    df_publ_por_genero_NBR.iloc[i,1] = prod_hombres_NBR/prod_total_NBR * 100
    df_publ_por_genero_NBR.iloc[i,2] = prod_mujeres_NBR/cant_mujeres_NBR
    df_publ_por_genero_NBR.iloc[i,3] = prod_hombres_NBR/cant_hombres_NBR
    df_publ_por_genero_NBR.iloc[i,4] = prod_total_NBR

df_publ_por_genero_NBR.astype('float').round(2)
#df_publ_por_genero_NBR.to_csv(tablespath + 'cantidad_publicaciones_NBR_por_genero.csv')

##### capitulos libros

anios = pd.date_range('01-2011', '01-2018', freq='AS')
columnas = ['Publicaciones cap mujeres (%)',
            'Publicaciones cap hombres (%)',
            'Publicaciones mujeres cap (per capita)',
            'Publicaciones hombres cap (per capita)',
            'Total publicaciones cap (N)']

df_publ_por_genero_cap = pd.DataFrame(index=anios, columns=columnas)

for i, iyear in enumerate(range(2011,2019)):
    exec("""df = pd.merge(Datos1_{}, Datos2_{}, on="persona_id")""".format(iyear,iyear))
    df_clean = df.replace({ -1: np.nan})


    prod_total_cap = int(df_clean['produccion_cantidad_capitulos_libro'].sum())

    prod_hombres_cap = df_clean.loc[df_clean['sexo_id'] == 2, 'produccion_cantidad_capitulos_libro'].sum()
    cant_hombres_cap = df_clean.loc[df_clean['sexo_id'] == 2, 'produccion_cantidad_capitulos_libro'].count()

    prod_mujeres_cap = df_clean.loc[df_clean['sexo_id'] == 1, 'produccion_cantidad_capitulos_libro'].sum()
    cant_mujeres_cap = df_clean.loc[df_clean['sexo_id'] == 1, 'produccion_cantidad_capitulos_libro'].count()

    df_publ_por_genero_cap.iloc[i,0] = prod_mujeres_cap/prod_total_cap * 100
    df_publ_por_genero_cap.iloc[i,1] = prod_hombres_cap/prod_total_cap * 100
    df_publ_por_genero_cap.iloc[i,2] = prod_mujeres_cap/cant_mujeres_cap
    df_publ_por_genero_cap.iloc[i,3] = prod_hombres_cap/cant_hombres_cap
    df_publ_por_genero_cap.iloc[i,4] = prod_total_cap

df_publ_por_genero_cap.astype('float').round(2)
#df_publ_por_genero_cap.to_csv(tablespath + 'cantidad_publicaciones_cap_por_genero.csv')

##### libros

anios = pd.date_range('01-2011', '01-2018', freq='AS')
columnas = ['Publicaciones libros mujeres (%)',
            'Publicaciones libros hombres (%)',
            'Publicaciones mujeres libros (per capita)',
            'Publicaciones hombres libros (per capita)',
            'Total publicaciones libros (N)']

df_publ_por_genero_libros = pd.DataFrame(index=anios, columns=columnas)

for i, iyear in enumerate(range(2011,2019)):
    exec("""df = pd.merge(Datos1_{}, Datos2_{}, on="persona_id")""".format(iyear,iyear))
    df_clean = df.replace({ -1: np.nan})


    prod_total_libros = int(df_clean['produccion_cantidad_capitulos_libro'].sum())

    prod_hombres_libros = df_clean.loc[df_clean['sexo_id'] == 2, 'produccion_cantidad_libros'].sum()
    cant_hombres_libros = df_clean.loc[df_clean['sexo_id'] == 2, 'produccion_cantidad_libros'].count()

    prod_mujeres_libros = df_clean.loc[df_clean['sexo_id'] == 1, 'produccion_cantidad_libros'].sum()
    cant_mujeres_libros = df_clean.loc[df_clean['sexo_id'] == 1, 'produccion_cantidad_libros'].count()

    df_publ_por_genero_libros.iloc[i,0] = prod_mujeres_libros/prod_total_libros * 100
    df_publ_por_genero_libros.iloc[i,1] = prod_hombres_libros/prod_total_libros * 100
    df_publ_por_genero_libros.iloc[i,2] = prod_mujeres_libros/cant_mujeres_libros
    df_publ_por_genero_libros.iloc[i,3] = prod_hombres_libros/cant_hombres_libros
    df_publ_por_genero_libros.iloc[i,4] = prod_total_libros

df_publ_por_genero_libros.astype('float').round(2)




###### Figura Tipos de publicacion

columnas=['Publicaciones mujeres (per capita)',
            'Publicaciones hombres (per capita)']
categ_publ=['Q1', 'Q2', 'Q3', 'Q4', 'NBR', 'CapLibro', 'Libro']
df_publ_por_genero_categ = pd.DataFrame(index=categ_publ, columns=columnas)


df_publ_por_genero_categ.iloc[0,0] = df_publ_por_genero_Q1['Publicaciones mujeres Q1 (per capita)'].mean()
df_publ_por_genero_categ.iloc[0,1] = df_publ_por_genero_Q1['Publicaciones hombres Q1 (per capita)'].mean()
df_publ_por_genero_categ.iloc[1,0] = df_publ_por_genero_Q2['Publicaciones mujeres Q2 (per capita)'].mean()
df_publ_por_genero_categ.iloc[1,1] = df_publ_por_genero_Q2['Publicaciones hombres Q2 (per capita)'].mean()
df_publ_por_genero_categ.iloc[2,0] = df_publ_por_genero_Q3['Publicaciones mujeres Q3 (per capita)'].mean()
df_publ_por_genero_categ.iloc[2,1] = df_publ_por_genero_Q3['Publicaciones hombres Q3 (per capita)'].mean()
df_publ_por_genero_categ.iloc[3,0] = df_publ_por_genero_Q4['Publicaciones mujeres Q4 (per capita)'].mean()
df_publ_por_genero_categ.iloc[3,1] = df_publ_por_genero_Q4['Publicaciones hombres Q4 (per capita)'].mean()
df_publ_por_genero_categ.iloc[4,0] = df_publ_por_genero_NBR['Publicaciones mujeres NBR (per capita)'].mean()
df_publ_por_genero_categ.iloc[4,1] = df_publ_por_genero_NBR['Publicaciones hombres NBR (per capita)'].mean()
df_publ_por_genero_categ.iloc[5,0] = df_publ_por_genero_cap['Publicaciones mujeres cap (per capita)'].mean()
df_publ_por_genero_categ.iloc[5,1] = df_publ_por_genero_cap['Publicaciones hombres cap (per capita)'].mean()
df_publ_por_genero_categ.iloc[6,0] = df_publ_por_genero_libros['Publicaciones mujeres libros (per capita)'].mean()
df_publ_por_genero_categ.iloc[6,1] = df_publ_por_genero_libros['Publicaciones hombres libros (per capita)'].mean()


figname = 'Tipo_publicaciones_por_genero'
fontsize = 8
x = np.arange(0, 7)
xlabels = categ_publ
yh = df_publ_por_genero_categ["Publicaciones hombres (per capita)"]
ym = df_publ_por_genero_categ["Publicaciones mujeres (per capita)"]
fig = plt.figure(figsize=(7,4))
ax = plt.axes([0.1, 0.1, 0.85, 0.85])
gm = ax.bar(x-0.2, ym, width=0.4, color=color_m, alpha=.5, label='Femenino')
gh = ax.bar(x+0.2, yh, width=0.4, color=color_h, alpha=.5, label='Masculino')
ax.tick_params('both', labelsize=fontsize)
ax.legend(fontsize=fontsize)
ax.set_xticks(x)
ax.set_xticklabels(xlabels, fontsize=fontsize)
ax.set_yticks([0,0.25, 0.5, 0.75, 1, 1.25])
ax.set_ylim([0, 1.25])
ax.set_xlabel('Tipo de publicación', fontsize=fontsize)
ax.set_ylabel('Promedio de publicaciones\n(per capita)', fontsize=fontsize)
ax.grid(axis='y', lw=0.5, linestyle=':', color='dimgrey')
fig.savefig(figspath + figname + '.png', dpi=300, bbox_inches='tight')
fig.savefig(figspath + figname + '.pdf', bbox_inches='tight')



####### Patentes

##### Patentes solicitadas

anios = pd.date_range('01-2011', '01-2018', freq='AS')
columnas = ['Patentes solicitadas mujeres (%)',
            'Patentes solicitadas hombres (%)',
            'Cant mujeres (Nm)',
            'Cant hombres (Nh)',
            'Patentes solicitadas mujeres (per capita)',
            'Patentes solicitadas hombres (per capita)',
            'Total patentes solicitadas (N)']

df_publ_por_genero_patsol = pd.DataFrame(index=anios, columns=columnas)

for i, iyear in enumerate(range(2011,2019)):
    exec("""df = pd.merge(Datos1_{}, Datos2_{}, on="persona_id")""".format(iyear,iyear))
    df_clean = df.replace({ -1: np.nan})


    prod_total_patsol = int(df_clean['produccion_patentes_solicitadas'].sum())

    prod_hombres_patsol = df_clean.loc[df_clean['sexo_id'] == 2, 'produccion_patentes_solicitadas'].sum()
    cant_hombres_patsol = df_clean.loc[df_clean['sexo_id'] == 2, 'produccion_patentes_solicitadas'].count()

    prod_mujeres_patsol = df_clean.loc[df_clean['sexo_id'] == 1, 'produccion_patentes_solicitadas'].sum()
    cant_mujeres_patsol = df_clean.loc[df_clean['sexo_id'] == 1, 'produccion_patentes_solicitadas'].count()

    df_publ_por_genero_patsol.iloc[i,0] = prod_mujeres_patsol/prod_total_patsol * 100
    df_publ_por_genero_patsol.iloc[i,1] = prod_hombres_patsol/prod_total_patsol * 100
    df_publ_por_genero_patsol.iloc[i,2] = prod_mujeres_patsol
    df_publ_por_genero_patsol.iloc[i,3] = prod_hombres_patsol
    df_publ_por_genero_patsol.iloc[i,4] = prod_mujeres_patsol/cant_mujeres_patsol
    df_publ_por_genero_patsol.iloc[i,5] = prod_hombres_patsol/cant_hombres_patsol
    df_publ_por_genero_patsol.iloc[i,6] = prod_total_patsol

df_publ_por_genero_patsol.astype('float').round(2)
df_publ_por_genero_patsol.to_clipboard()

##### Patentes otorgadas

anios = pd.date_range('01-2011', '01-2018', freq='AS')
columnas = ['Patentes otorgadas mujeres (%)',
            'Patentes otorgadas hombres (%)',
            'Cant mujeres (Nm)',
            'Cant hombres (Nh)',
            'Patentes otorgadas mujeres (per capita)',
            'Patentes otorgadas hombres (per capita)',
            'Total patentes otorgadas (N)']

df_publ_por_genero_patoto = pd.DataFrame(index=anios, columns=columnas)

for i, iyear in enumerate(range(2011,2019)):
    exec("""df = pd.merge(Datos1_{}, Datos2_{}, on="persona_id")""".format(iyear,iyear))
    df_clean = df.replace({ -1: np.nan})

    prod_total_patoto = int(df_clean['produccion_patentes_otorgadas'].sum())

    prod_hombres_patoto = df_clean.loc[df_clean['sexo_id'] == 2, 'produccion_patentes_otorgadas'].sum()
    cant_hombres_patoto = df_clean.loc[df_clean['sexo_id'] == 2, 'produccion_patentes_otorgadas'].count()

    prod_mujeres_patoto = df_clean.loc[df_clean['sexo_id'] == 1, 'produccion_patentes_otorgadas'].sum()
    cant_mujeres_patoto = df_clean.loc[df_clean['sexo_id'] == 1, 'produccion_patentes_otorgadas'].count()

    df_publ_por_genero_patoto.iloc[i,0] = prod_mujeres_patoto/prod_total_patoto * 100
    df_publ_por_genero_patoto.iloc[i,1] = prod_hombres_patoto/prod_total_patoto * 100
    df_publ_por_genero_patoto.iloc[i,2] = prod_mujeres_patoto
    df_publ_por_genero_patoto.iloc[i,3] = prod_hombres_patoto
    df_publ_por_genero_patoto.iloc[i,4] = prod_mujeres_patoto/cant_mujeres_patoto
    df_publ_por_genero_patoto.iloc[i,5] = prod_hombres_patoto/cant_hombres_patoto
    df_publ_por_genero_patoto.iloc[i,6] = prod_total_patoto

df_publ_por_genero_patsol.astype('float').round(2)
df_publ_por_genero_patoto.to_clipboard()
# Figura Patentes

columnas=['Patentes mujeres (per capita)',
            'Patentes hombres (per capita)']
categ_publ=['Patentes Solicitadas', 'Patentes Otorgadas']

df_patentes_por_genero = pd.DataFrame(index=categ_publ, columns=columnas)

df_patentes_por_genero.iloc[0,0] =df_publ_por_genero_patsol['Patentes solicitadas mujeres (per capita)'].mean()
df_patentes_por_genero.iloc[0,1] = df_publ_por_genero_patsol['Patentes solicitadas hombres (per capita)'].mean()
df_patentes_por_genero.iloc[1,0] =df_publ_por_genero_patoto['Patentes otorgadas mujeres (per capita)'].mean()
df_patentes_por_genero.iloc[1,1] = df_publ_por_genero_patoto['Patentes otorgadas hombres (per capita)'].mean()


figname = 'Patentes_por_genero'
fontsize = 8
x = np.arange(0, 2)
xlabels = categ_publ
yh = df_patentes_por_genero["Patentes hombres (per capita)"]
ym = df_patentes_por_genero["Patentes mujeres (per capita)"]
fig = plt.figure(figsize=(7,4))
ax = plt.axes([0.1, 0.1, 0.85, 0.85])
gm = ax.bar(x-0.2, ym, width=0.4, color=color_m, alpha=.5, label='Femenino')
gh = ax.bar(x+0.2, yh, width=0.4, color=color_h, alpha=.5, label='Masculino')
ax.tick_params('both', labelsize=fontsize)
ax.legend(fontsize=fontsize)
ax.set_xticks(x)
ax.set_xticklabels(xlabels, fontsize=fontsize)
ax.set_yticks([0,0.01])
ax.set_xlabel('', fontsize=fontsize)
ax.set_ylabel('Promedio\n(per capita)', fontsize=fontsize)
fig.savefig(figspath + figname + '.png', dpi=300, bbox_inches='tight')
fig.savefig(figspath + figname + '.pdf', bbox_inches='tight')
