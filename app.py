import pandas as pd
import streamlit as st
import locale
import datetime
import plotly.express as px
import plotly.graph_objects as go
#import altair as alt
#import utils
#import time
#import random
#import numpy as np

locale.setlocale(locale.LC_TIME, 'es_CO.utf8')
color_discrete_sequence=['#def9c4','#9cdba6','#50b498','#468585','#c4dad2','#80b9ad','#40a578','#1679ab','#8decb4','#124076','#80bcbd','#c3e2c2','#a7d397','#d2e0fb']
st.set_page_config(page_title='Dashboard', page_icon='📉',layout='wide')

#****************************BITACORASs*****************************************#
doc1 = pd.read_excel('ZONA.xlsx', sheet_name='Hoja1')
doc2 = pd.read_excel('Bitacora2023.xlsx', sheet_name='Cortes de Fibra')
doc3 = pd.read_excel('Bitacora2024.xlsx', sheet_name='Cortes de Fibra')
c1 = pd.concat([doc2, doc3], ignore_index=True)
mergzona = pd.merge(doc1, c1, on=['Departamento'])

#****************************************************************************#

#*****************************FILTROS****************************************#
mergzona.rename(columns={'Tipo de Tramo': 'TRAMO','Causa del daño': 'CAUSA','Departamento': 'DEPARTAMENTO','HORA INICIO': 'HORA_INICIO','HORA RECUP, DE SERICIO': 'HORA_RECUPERACION','Corto circuito': 'CCIRCUITO'}, inplace=True)
# c['EECC'] = c['EECC'].str.replace('cobra', 'Cobra')
# c['EECC'] = c['EECC'].str.replace('inmel', 'Inmel')
mergzona['CAUSA'] = mergzona['CAUSA'].str.replace('visita Fallida', 'Visita Fallida')
mergzona['Afectación'] = mergzona['Afectación'].str.replace('si', 'SI')
mergzona['Afectación'] = mergzona['Afectación'].str.replace('no', 'NO')
mergzona["DEPARTAMENTO"] = mergzona["DEPARTAMENTO"].map(lambda x: 'VALLE_DEL_CAUCA' if x == "VALLE DEL CAUCA" else x)
# c = c[mergzona['HORA_RECUPERACION'].notna()]
mergzona = mergzona.dropna(how='any', subset=['CAUSA'])
mergzona['MES'] = mergzona['HORA_INICIO'].dt.strftime('%B')
mergzona['AÑO'] = mergzona['HORA_INICIO'].dt.strftime('%Y')
mergzona['MA'] = mergzona['HORA_INICIO'].dt.strftime('%B-%Y')

mergzona = mergzona.dropna(subset=['Afectación'])
orden_m = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
mergzona['MES'] = pd.Categorical(mergzona['MES'], categories=orden_m, ordered=True)
filcolumnas = ['HORA_INICIO', 'Incidente', 'CAUSA', 'DEPARTAMENTO', 'Zona', 'Afectación', 'Enlace', 'AÑO', 'MES', 'MA']
dfc = mergzona[filcolumnas]
dfc['Enlace_Unico'] = dfc['Enlace']

#
for departamento in dfc['DEPARTAMENTO'].unique():
    mask = dfc['DEPARTAMENTO'] == departamento
    enlaces = dfc.loc[mask, 'Enlace']
    duplicados = enlaces[enlaces.duplicated(keep=False)]
    dfc.loc[mask & dfc['Enlace'].isin(duplicados), 'Enlace_Unico'] = ''
dfc
#***********************************************************************************#

#***********************************GRAFICAS****************************************#

cc1, cc2 = st.columns([50, 50])
with cc1:
    df = dfc.groupby(['CAUSA', 'AÑO']).size().reset_index(name='Conteo')
    df['CAUSA'] = df['CAUSA'].apply(lambda x: None if x == 'Visita Fallida' else x)
    df = df.sort_values(by='Conteo', ascending=False)
    fig = px.bar(df,x="CAUSA",y="Conteo",color="AÑO",title='CORTES DE FIBRA POR CAUSA',text_auto=',.0f',color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(xaxis_title=None,yaxis_title=None, yaxis=dict(showgrid=False, showticklabels=False),xaxis_tickangle=0,barmode='group',showlegend=True)
    suma = df.groupby('CAUSA')['Conteo'].sum().reset_index()
    fig.update_traces(textfont_size=15, textposition="outside", cliponaxis=False)
    st.plotly_chart(fig, use_container_width=True)

with cc2:
    causas = ['Vandalismo', 'Intervención de Terceros. No Identificados', 'Falla de Empalme de FiOp', 'Falla en la Red FiOp','Otros']
    df23 = dfc[dfc['AÑO'] == '2023']
    df24 = dfc[dfc['AÑO'] == '2024']
    mes24 = df24['HORA_INICIO'].dt.month.nunique()
    df23['CAUSA'] = df23['CAUSA'].apply(lambda x: x if x in causas[:-1] else 'Otros')
    df24['CAUSA'] = df24['CAUSA'].apply(lambda x: x if x in causas[:-1] else 'Otros')
    cont23 = df23['CAUSA'].value_counts().reindex(causas, fill_value=0)
    cont24 = df24['CAUSA'].value_counts().reindex(causas, fill_value=0)
    t23 = cont23.sum()
    t24 = cont24.sum()
    res = pd.DataFrame({'Causa': causas,'2023': (cont23.values / t23 * 100),'2024': (cont24.values / t24 * 100)})
    res['Var A/A'] = ((res['2024'] - res['2023']) / res['2023'].replace(0, pd.NA)) * 100
    res['2023'] = res['2023'].apply(lambda x: f"{x:.2f}%")
    res['2024'] = res['2024'].apply(lambda x: f"{x:.2f}%")
    res['Var A/A'] = res['Var A/A']. apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A")
    res.rename(columns={'2024': f'2024 ({mes24} Meses)'}, inplace=True)
    res.set_index('Causa', inplace=True)
    res


# with cc2:
#       campos especificos 
#     causas = ['Vandalismo', 'Intervención de Terceros. No Identificados', 'Falla de Empalme de FiOp', 'Falla en la Red FiOp','Otros']
#       filtrar los datos del año 
#     df23 = dfc[dfc['AÑO'] == '2023']
#     df24 = dfc[dfc['AÑO'] == '2024']
#       conteo de los meses existentes en el data
#     mes24 = df24['HORA_INICIO'].dt.month.nunique()
#       Si la causa no está en la lista predefinida, se clasifica como "Otros".
#     df23['CAUSA'] = df23['CAUSA'].apply(lambda x: x if x in causas[:-1] else 'Otros')
#     df24['CAUSA'] = df24['CAUSA'].apply(lambda x: x if x in causas[:-1] else 'Otros')
#       conteo de las ocurrencias de cada causa
#     cont23 = df23['CAUSA'].value_counts().reindex(causas, fill_value=0)
#     cont24 = df24['CAUSA'].value_counts().reindex(causas, fill_value=0)
#       conteo de la suma 
#     t23 = cont23.sum()
#     t24 = cont24.sum()
#       se crea un data que calcule los porcentajes de los incidentes por causa, conteo de las causa del 23, la suma total de los incidentes
#     res = pd.DataFrame({'Causa': causas,'2023': (cont23.values / t23 * 100).round(2),'2024': (cont24.values / t24 * 100).round(2)})
#       se calcula la variación porccentual entre los dos años, se resta el porcentaje del año 2023 del porcentaje del año 2024, cuanto ha cambiado en relacion con el año anterior, dividiendolo en 100 para convertirlo en porcentaje
#     res['Var A/A'] = ((res['2024'] - res['2023']) / res['2023'].replace(0, pd.NA)) * 100
#       se da formato a los valores en porcentaje con dos decimales y var con un decimal 
#     res['2023'] = res['2023'].apply(lambda x: f"{x:.2f}%")
#     res['2024'] = res['2024'].apply(lambda x: f"{x:.2f}%")
#     res['Var A/A'] = res['Var A/A']. apply(lambda x: f"{x:.1f}%" if pd.notna(x) else "N/A")
#       se renombra para que aparezcan los meses actuales 
#     res.rename(columns={'2024': f'2024 ({mes24} Meses)'}, inplace=True)
#     res.set_index('Causa', inplace=True)
#       se imprime
#     res


with st.container():
    dfc['MES'] = pd.Categorical(dfc['MES'], categories=orden_m, ordered=True)
    df = dfc.groupby(['MA', 'CAUSA']).size().reset_index(name='Incidente')
    value = ['Corto Circuito', 'Vandalismo', 'Falla de Empalme de FiOp']
    df = df[df['CAUSA'].isin(value)]
    fig = px.bar(df,x="MA",y="Incidente",color="CAUSA",title='CAUSAS PRINCIPALES',text_auto=',.0f',color_discrete_sequence=color_discrete_sequence)
    suma = df.groupby('MA')['Incidente'].sum().reset_index()
    fig.add_scatter(x=suma['MA'], y=suma['Incidente'], mode='lines+markers+text', name='Suma', line=dict(color='yellow', width=1.5), text=suma['Incidente'],textposition='top center', hoverinfo='text',hovertext=suma['Incidente'], showlegend=False)
    fig.update_layout(xaxis_title=None,yaxis_title=None, yaxis=dict(showgrid=False,  showticklabels=False ),xaxis_tickangle=-45,barmode='stack',showlegend=True)
    st.plotly_chart(fig, use_container_width=True)
    
st.header('Detalles de cortes FO Planta Interna')
# cc1, cc2 = st.columns([50, 50])
# with cc1:
with st.container():
    df = dfc.groupby(['MES', 'Afectación']).size().reset_index(name='Conteo')
    fig = px.bar(df, x="MES", y="Conteo", color="Afectación", title='CANTIDAD DE CORTES DE FIBRA', text_auto=',.0f',color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(xaxis_title=None,yaxis_title=None, height=400,width=800,yaxis=dict(showgrid=False,  showticklabels=False ),xaxis_tickangle=-45,barmode='stack',showlegend=True)
    fig.update_traces(textfont_size=15, textposition="outside", cliponaxis=False)
    st.plotly_chart(fig, use_container_width=True)

with st.container():
    df = dfc.groupby(['MES', 'Zona']).size().reset_index(name='Incidente')
    fig = px.bar(df, x="MES", y="Incidente", color="Zona", title='CORTES DE FIBRA POR ZONA', text_auto=',.0f',color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(xaxis_title=None,yaxis_title=None, yaxis=dict(showgrid=False,  showticklabels=False ),xaxis_tickangle=-45,barmode='stack',showlegend=True,legend=dict(orientation='h', yanchor='bottom',xanchor='center', y=-0.5,x=0.5, title=dict(text='')))
    st.plotly_chart(fig, use_container_width=True)
    
with st.container():
    current_year = datetime.datetime.now().year 
    aactual = dfc[dfc['AÑO'] == str(current_year)]
    uni = aactual.drop_duplicates(subset=['DEPARTAMENTO', 'Zona', 'Enlace_Unico'])
    df = uni.groupby(['DEPARTAMENTO', 'Zona']).size().reset_index(name='Incidente')
    fig = px.bar(df, x="DEPARTAMENTO", y="Incidente", color="Zona", title='NÚMERO DE ENLACES REINCIDENTES POR ZONA 2024', text_auto=',.0f', color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(xaxis_title=None,yaxis_title=None,yaxis=dict(showgrid=False, showticklabels=False),xaxis_tickangle=-45,barmode='stack',showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

# with st.container():
#     uni = aactual.drop_duplicates(subset=['DEPARTAMENTO', 'Zona', 'Enlace_Unico'])
#     df = df.groupby(['DEPARTAMENTO', 'Zona']).size().reset_index(name='Incidente')
#     fig = go.Figure()
#     fig.update_traces(textfont_size=15, textposition="outside", cliponaxis=False)
#     fig.add_trace(go.Bar(x=[df.Zona, df.DEPARTAMENTO],y=df.Incidente, textposition='outside'))
#     fig.update_layout(xaxis_title=None,yaxis_title=None,yaxis=dict(showgrid=False, showticklabels=False),xaxis_tickangle=-90,barmode='stack',showlegend=False, margin=dict(l=10, r=10, t=20, b=10),title='NÚMERO DE ENLACES REINCIDENTES POR ZONA 2024')
#     st.plotly_chart(fig, use_container_width=True)

st.header('Causas FO Nacional 2023 a 2024')
with st.container():
    c_no = dfc[dfc['Afectación'] == 'NO']
    df = c_no.groupby(['MES', 'CAUSA']).size().reset_index(name='Conteo')
    df['CAUSA'] = df['CAUSA'].apply(lambda x: None if x == 'Visita Fallida' else x)
    fig = px.bar(df, x="MES", y="Conteo", color="CAUSA", title='CORTES POR CAUSA SIN AFECTACIÓN', text_auto=',.0f', color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(xaxis_title=None,yaxis_title=None,yaxis=dict(showgrid=False, showticklabels=False),xaxis_tickangle=-45,barmode='stack',showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

with st.container():
    c_si = dfc[dfc['Afectación'] == 'SI']
    df = c_si.groupby(['MES', 'CAUSA']).size().reset_index(name='Conteo')
    df['CAUSA'] = df['CAUSA'].apply(lambda x: None if x == 'Visita Fallida' else x)
    fig = px.bar(df, x="MES", y="Conteo", color="CAUSA", title='CORTES POR CAUSA CON AFECTACIÓN', text_auto=',.0f', color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(xaxis_title=None,yaxis_title=None,yaxis=dict(showgrid=False, showticklabels=False),xaxis_tickangle=-45,barmode='stack',showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

cc1, cc2 = st.columns([50, 50])
with cc1:
    df = dfc.groupby(['DEPARTAMENTO', 'CAUSA']).size().reset_index(name='Conteo')
    value = ['Visita Fallida']
    df = df[df['CAUSA'].isin(value)]
    fig = px.bar(df,x="DEPARTAMENTO",y="Conteo",color="CAUSA",title='VISITAS FALLIDAS POR DEPARTAMENTO',text_auto=',.0f',color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(xaxis_title=None,yaxis_title=None, yaxis=dict(showgrid=False,  showticklabels=True),xaxis_tickangle=-45,barmode='stack',showlegend=True)
    st.plotly_chart(fig, use_container_width=True)
with cc2:
    df = dfc.groupby(['CAUSA']).size().reset_index(name='Conteo')
    value = ['Visita Fallida']
    df = df[df['CAUSA'].isin(value)]
    fig = px.bar(df,x="CAUSA",y="Conteo",color=None,title='CAUSAS VISITAS FALLIDAS',text_auto=',.0f',color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(xaxis_title=None,yaxis_title=None, yaxis=dict(showgrid=False,  showticklabels=True),xaxis_tickangle=-45,barmode='stack',showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

#***********************************************************************************#