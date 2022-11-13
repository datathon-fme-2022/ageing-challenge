#!/usr/bin/env python3


import numpy
from matplotlib import pyplot
import pandas
import math


with open("./data/OpenDataBCN/padro_viu_sola_edat_quinquennal.csv") as f:
    df = pandas.read_csv(f)

# convert age range e.g. str("45-49 anys") ~> int(45)
# if "<25 anys" ~> NaN ~> int(0)
df["Edat_quinquennal"] = pandas.to_numeric(df["Edat_quinquennal"].str[0:2],
                  downcast="integer",
                  errors="coerce") # coerce gives NaNs
df["Edat_quinquennal"] = df["Edat_quinquennal"].fillna(0.0).astype("int32")

# filter seniors, here considered age ≥ 60 years
df = df[df["Edat_quinquennal"] >= 60]

## only execute each of these commented blocks separately

'''
## print bar diagram of seniors by age, iter. by year; to later create a .gif
for anny in range(2007, 2023):
    subdf = df[df["Any"] == anny][["Edat_quinquennal", "Nombre"]]
    subdf = subdf.groupby("Edat_quinquennal").sum().reset_index()

    fig, ax = pyplot.subplots()
    pyplot.ylim(0, 21000)
    ax.set_xlabel("Age range")
    ax.set_ylabel("Number of people")
    ax.set_title(f"Senior citizens that live alone\nin Barcelona, year {anny}")
    pyplot.bar(subdf["Edat_quinquennal"], subdf["Nombre"],
               width=5, align="edge")
    pyplot.savefig(f"bcn_alone{anny}.png")
    pyplot.clf()
'''

# ------------------------------------------------------------------------------
'''
## plot total alone seniors by year

df = df[["Any", "Nombre"]].groupby("Any").sum().reset_index()

# line graph
fig, ax = pyplot.subplots()
ax.set_xlabel("Year")
ax.set_ylabel("Number of people")
ax.set_title("Senior citizens (age ≥ 60) that live alone in Barcelona by year")
pyplot.plot(df["Any"], df["Nombre"])

# linear regression
coef = numpy.polyfit(df["Any"], df["Nombre"], 1)
poly1d_fn = numpy.poly1d(coef)
pyplot.plot(df["Any"], df["Nombre"], 'bo', df["Any"], poly1d_fn(df["Any"]))

pyplot.show()
'''

# ------------------------------------------------------------------------------
'''
## plot seniors per year, for each district

df = df[df["Codi_Districte"] != 99] # "No consta"

districtes = {
    1:"Ciutat Vella",
    2:"Eixample",
    3:"Sants-Montjuïc",
    4:"Les Corts",
    5:"Sarrià-Sant Gervasi",
    6:"Gràcia",
    7:"Horta-Guinardó",
    8:"Nou Barris",
    9:"Sant Andreu",
    10:"Sant Martí"
}

district_coefs = []


for districte in pandas.unique(df["Codi_Districte"]):
    subdf = df[df["Codi_Districte"] == districte]
    subdf = subdf[["Any", "Nombre"]].groupby("Any").sum().reset_index()

    # plot line graph
    fig, ax = pyplot.subplots()
    ax.set_xlabel("Year")
    ax.set_ylabel("Number of people")
    ax.set_title(f"{districtes[districte]}")
    pyplot.plot(subdf["Any"], subdf["Nombre"])

    # linear regression
    coef = numpy.polyfit(subdf["Any"], subdf["Nombre"], 1)
    district_coefs.append((districtes[districte], coef[0]))

    # plot linear regression
    poly1d_fn = numpy.poly1d(coef)
    pyplot.plot(subdf["Any"], subdf["Nombre"], 'bo',
                subdf["Any"], poly1d_fn(subdf["Any"]))

    pyplot.savefig(f"dist{districte}.png")

# print correct colors for map thru sigmoid tanh
# 85.64 is the mean of abs of slopes of linear regression line of districts
def sig(x):
    return math.tanh(x / 85.64)

for c in district_coefs:
    print(c[0] + "\t" + str(numpy.sign(sig(c[1])))
               + "\t" + str(1   -  abs(sig(c[1]))))

# time to use GIMP for painting the map with the correct colors

'''

# ------------------------------------------------------------------------------
'''
## linear prediction

df = df[df["Codi_Districte"] != 99] # "No consta"

prediction = 0.0

for districte in pandas.unique(df["Codi_Districte"]):
    subdf = df[df["Codi_Districte"] == districte]
    subdf = subdf[["Any", "Nombre"]].groupby("Any").sum().reset_index()
    
    coef = numpy.polyfit(subdf["Any"], subdf["Nombre"], 1)
    poly1d_fn = numpy.poly1d(coef)
    prediction += poly1d_fn(2050)

print(f"by 2050: {int(round(prediction))} alone seniors") # ≈ 125000
'''

