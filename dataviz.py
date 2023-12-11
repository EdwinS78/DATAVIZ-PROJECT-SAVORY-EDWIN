import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import pydeck as pdk
import geopandas as gpd
import streamlit as st
import pandas as pd
import altair as alt
from bokeh.plotting import figure, show, output_notebook
from bokeh.io import push_notebook
from bokeh.models import ColumnDataSource



__author__='Edwin SAVORY'
__copyright__='Copyright 2023'
__credits__=['SAVORY Edwin']
__version__='0.0.1'
__maintainer__='SAVORY Edwin'
__email__='edwin.savory@efrei.net'
__status__='Final Code'



st.title("Étude des accidents routiers en France et départements d'Outre-mer :car:")
st.write('---')
st.write("Dans le cadre du module data vizualisation de l'EFREI PARIS, j'ai l'occasion d'effectuer une étude sur les accident routiers en France et départements d'outre-mer. Dans le cadre de ce projet, une analyse et une représentation visuelle des données est nécessaire, afin de mettre en valeur les informations qui se révèleraient intéressantes pour répondre à la question suivante :")
st.write(' Comment les différents facteurs influencent-ils les accidents de la route ?')
st.write('---')
@st.cache_resource
def load_info():
    st.sidebar.text("SAVORY")
    st.sidebar.text("Edwin")
    st.sidebar.text("École : EFREI PARIS")
    st.sidebar.text("Promo 2025")
    st.sidebar.text("Classe : BIA2")


@st.cache_resource
def load_data():
    lx = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/a6ef711a-1f03-44cb-921a-0ce8ec975995', delimiter=';')
    cara = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/5fc299c0-4598-4c29-b74c-6a67b0cc27e7', delimiter=';')
    usg = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/62c20524-d442-46f5-bfd8-982c59763ec8', delimiter=';')
    v = pd.read_csv('https://www.data.gouv.fr/fr/datasets/r/c9742921-4427-41e5-81bc-f13af8bc31a0',delimiter=';')
    return lx, cara, usg, v

lx, cara, usg, v = load_data()

load_info()

colonne_inutiles_cara = ['com','col','adr']
colonne_inutiles_lx = ['voie','v1','v2','vosp','prof','pr','pr1','plan','lartpc']
colonne_inutiles_v =['senc','choc','manv','motor','occutc']
colonne_inutiles_usg= ['place','secu1','secu2','secu3','etatp']

lx = lx.drop(colonne_inutiles_lx,axis = 1)

cara = cara.drop(colonne_inutiles_cara,axis=1)



usg = usg.drop(colonne_inutiles_usg,axis =1)



v = v.drop(colonne_inutiles_v,axis = 1)

#jointure de lieux et caractéristique
@st.cache_resource
def first_merge_data(lx, cara):
    return pd.merge(lx, cara, left_on='Num_Acc', right_on='Accident_Id')

first_merge = first_merge_data(lx, cara)







#Il faut renomme la colonne des longitudes
first_merge = first_merge.rename(columns={'long':'lon'})
##avant d'utiliser la map, il faut convertir les données de position au bon format (il faut remplacer les virgules par des points)

first_merge['lat'] = pd.to_numeric(first_merge['lat'].str.replace(',', '.'))
first_merge['lon'] = pd.to_numeric(first_merge['lon'].str.replace(',', '.'))



##--------------------------------------------------------------------------------------------------------------------------------



#jointure de usagers et véhicules

@st.cache_resource
def second_merge_data(usg, v):
    return pd.merge(usg, v, on=['Num_Acc','id_vehicule','num_veh'], how='left')

second_merge = second_merge_data(usg, v)


##--------------------------------------------------------------------------------------------------------------------------------

#jointure pour avoir un dataset complet

@st.cache_resource
def full_merge(data1,data2):
    return pd.merge(data1,data2, on ='Num_Acc', how='left')

data = full_merge(second_merge,first_merge)

##--------------------------------------------------------------------------------------------------------------------------------

st.subheader('Apperçu des données du dataset de 2022: ')



st.dataframe(data.head(20))


st.write('---')


st.title('Analyse des accidents routiers')

unique_accidents = data['Accident_Id'].nunique()
st.write(f"Nombre total d'accidents uniques en 2022: {unique_accidents}")
passenger_count = data.groupby('Accident_Id').size()
st.write(f"Moyenne de passagers impliqués par accident : {passenger_count.mean()}")
st.write('---')





st.header('Répartition des accidents par gravité par usagers impliqués')
fig = px.bar(data['grav'].value_counts().reset_index(), x='index', y='grav', labels={'index': 'Gravité', 'grav': 'Nombre d\'accidents'})
st.plotly_chart(fig)
st.text("1 – Indemne ")
st.text("2 – Tué ")
st.text("3 – Blessé hospitalisé")
st.text("4 – Blessé léger")
st.text("4 – Non Renseigné")


st.header('Répartition des accidents selon le sexe')
fig = px.pie(data, names='sexe', title='Répartition des accidents selon le sexe')
st.plotly_chart(fig)
st.text("1 – Masculin ")
st.text("2 – Féminin ")
st.text("-1 – Non Renseigné")

##--------

data_unique_accidents = data.drop_duplicates(subset='Accident_Id', keep='first')



st.write('---')





# Carte des accidents
st.header('Carte des accidents')
unique_acc = data.drop_duplicates(subset='Accident_Id', keep='first')
st.map(unique_acc[['lat', 'lon']])

# Distribution des accidents par type d'obstacle
st.header('Distribution des accidents par type d\'obstacle')
chart = alt.Chart(unique_acc['obs'].value_counts().reset_index()).mark_bar().encode(
    x='index:O',
    y='obs:Q'
)
st.altair_chart(chart, use_container_width=True)
st.text("-1 – Non renseigné ")
st.text("0 – Sans objet")
st.text("1 – Véhicule en stationnement")
st.text("2 – Arbre")
st.text("3 – Glissière métallique")
st.text("4 – Glissière béton")
st.text("5 – Autre glissière")
st.text("6 – Bâtiment, mur, pile de pont")
st.text("7 – Support de signalisation verticale ou poste d’appel d’urgence")
st.text("8 – Poteau")
st.text("9 – Mobilier urbain")
st.text("10 – Parapet")
st.text("11 – Ilot, refuge, borne haute")
st.text("12 – Bordure de trottoir")
st.text("13 – Fossé, talus, paroi rocheuse")
st.text("14 – Autre obstacle fixe sur chaussée")
st.text("15 – Autre obstacle fixe sur trottoir ou accotement")
st.text("16 – Sortie de chaussée sans obstacle")
st.text("17 – Buse – tête d’aqueduc")

# Histogramme des accidents
st.header('Histogramme des accidents')
granularity = st.selectbox('Choisissez la temporalité:', ('Par mois', 'Par jour du mois', 'Par heure'))


if granularity == 'Par mois':
    month_counts = data['mois'].value_counts().reset_index()
    month_counts.columns = ['mois', 'count']

    month_counts = month_counts.sort_values('mois')

    chart = alt.Chart(month_counts).mark_bar().encode(
        x='mois:O',
        y='count:Q'
    )


elif granularity == 'Par jour du mois':
    month_to_filter = st.slider('Choisissez un mois', 1, 12)
    chart = alt.Chart(data_unique_accidents[data_unique_accidents['mois'] == month_to_filter]).mark_bar().encode(
        x='jour:O',
        y='count():Q'
    )
if granularity == 'Par heure':
    data_unique_accidents['heure'] = data_unique_accidents['hrmn'].str.slice(0, 2)
    
    chart = alt.Chart(data_unique_accidents).mark_bar().encode(
        alt.X("heure:O", bin=alt.Bin(maxbins=24), title='Heure'),
        y='count():Q',
        tooltip=['heure', 'count()']
    ).properties(
        width=700,
        height=400,
        title='Accidents par heure'
    )

st.altair_chart(chart, use_container_width=True)


options = {
    "tooltip": {"trigger": "item"},
    "legend": {"top": "5%", "left": "center"},
    "series": [
        {
            "name": "访问来源",
            "type": "pie",
            "radius": ["40%", "70%"],
            "avoidLabelOverlap": False,
            "itemStyle": {
                "borderRadius": 10,
                "borderColor": "#fff",
                "borderWidth": 2,
            },
            "label": {"show": False, "position": "center"},
            "emphasis": {
                "label": {"show": True, "fontSize": "40", "fontWeight": "bold"}
            },
            "labelLine": {"show": False},
            "data": [
                {"value": 1048, "name": "搜索引擎"},
                {"value": 735, "name": "直接访问"},
                {"value": 580, "name": "邮件营销"},
                {"value": 484, "name": "联盟广告"},
                {"value": 300, "name": "视频广告"},
            ],
        }
    ],
}
st_echarts(
    options=options, height="500px",
)

