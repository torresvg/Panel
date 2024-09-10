
import pandas as pd
import streamlit as st
import locale
# import altair as alt
import plotly.express as px
# import utils

locale.setlocale(locale.LC_TIME, 'es_CO.utf8')

color_discrete_sequence=['#ef9c66','#fcdc94','#c8cfa0','#78aba8','#b4b0a3','#ace2e1','#b16d2b','#b99470']

st.set_page_config(
    page_title='Dashboard',
    page_icon='📉',
    layout='wide')

# utils.local_css('app.css')

doc1 = pd.ExcelFile('/Users/ValentinaGaviria/OneDrive - Telco Soluciones y Servicios/Documentos/Telefonica/Panel/Bitacora2024.xlsx')
doc2 = pd.ExcelFile('/Users/ValentinaGaviria/OneDrive - Telco Soluciones y Servicios/Documentos/Telefonica/Panel/Bitacora2023.xlsx')
doc3 = pd.ExcelFile('/Users/ValentinaGaviria/OneDrive - Telco Soluciones y Servicios/Documentos/Telefonica/Panel/ZONAS.xlsx')

df1 = doc1.parse('Cortes de Fibra')
df2 = doc2.parse('Cortes de Fibra')
df3 = doc3.parse('Hoja1')

c = pd.concat([df1, df2, df3], ignore_index=True)

# st.header('Tableros')

c.rename(columns={'Tipo de Tramo': 'TRAMO','Causa del daño': 'CAUSA','Departamento': 'DEPARTAMENTO','HORA INICIO': 'HORA_INICIO','HORA RECUP, DE SERICIO': 'HORA_RECUPERACION','Corto circuito': 'CCIRCUITO','Zona':'ZONA'}, inplace=True)
c['EECC'] = c['EECC'].str.replace('cobra', 'Cobra')
c['EECC'] = c['EECC'].str.replace('inmel', 'Inmel')
c['CAUSA'] = c['CAUSA'].str.replace('visita Fallida', 'Visita Fallida')
c['Afectación'] = c['Afectación'].str.replace('si', 'SI')
c['Afectación'] = c['Afectación'].str.replace('no', 'NO')
c["CAUSA"] = c["CAUSA"].map(lambda x: 'Visita_Fallida' if x == "Visita Fallida" else x)
c["DEPARTAMENTO"] = c["DEPARTAMENTO"].map(lambda x: 'VALLE_DEL_CAUCA' if x == "VALLE DEL CAUCA" else x)
c = c[c['HORA_RECUPERACION'].notna()]
c = c.dropna(how='any', subset=['CAUSA']) 
discard = ['Visita_Fallida']
c = c[~c['CAUSA'].str.contains('|'.join(discard))]
c['MES'] = c['HORA_INICIO'].dt.strftime('%B')
c['AÑO'] = c['HORA_INICIO'].dt.strftime('%Y')
c = c.dropna(subset=['Afectación'])
orden_m = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
c['MES'] = pd.Categorical(c['MES'], categories=orden_m, ordered=True)


cc1, cc2 = st.columns([50, 50])
with cc1:
    df = c.groupby(['CAUSA', 'AÑO']).size().reset_index(name='Afectación')
    df = df.sort_values(by='Afectación', ascending=False)
    fig = px.bar(df,x="CAUSA",y="Afectación",color="AÑO",title='CORTES DE FIBRA POR CAUSA',text_auto=',.0f',color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(xaxis_title="Causa",yaxis_title=None, yaxis=dict(showgrid=False, showticklabels=False),xaxis_tickangle=-45,barmode='group',showlegend=True )
    st.plotly_chart(fig, use_container_width=True)

with cc2:
    df = c.groupby(['MES', 'CAUSA']).size().reset_index(name='Afectación')
    value = ['Corto Circuito', 'Vandalismo', 'Falla de Empalme de FiOp']
    df = df[df['CAUSA'].isin(value)]
    fig = px.bar(df,x="MES",y="Afectación",color="CAUSA",title='CAUSAS PRINCIPALES ',text_auto=',.0f',color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(xaxis_title="Mes",yaxis_title=None, yaxis=dict(showgrid=False,  showticklabels=False ),xaxis_tickangle=-45,barmode='stack',showlegend=True)
    st.plotly_chart(fig, use_container_width=True)
    
st.header('Detalles de cortes FO Planta Interna')
cc1, cc2 = st.columns([50, 50])
with cc1:
    df = c.groupby(['MES', 'Afectación']).size().reset_index(name='Conteo')
    fig = px.bar(df, x="MES", y="Conteo", color="Afectación", title='CANTIDAD DE CORTES DE FIBRA', text_auto=',.0f',color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(xaxis_title="Causa",yaxis_title=None, yaxis=dict(showgrid=False,  showticklabels=False ),xaxis_tickangle=-45,barmode='stack',showlegend=True)
    st.plotly_chart(fig, use_container_width=True)
with cc2:
    df = c.groupby(['MES']).size().reset_index(name='DEPARTAMENTO')
    fig = px.bar(df,x="MES", y="DEPARTAMENTO",title='CORTES DE FIBRA POR ZONA',color='DEPARTAMENTO',text_auto=',.0f',color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(xaxis_title="Mes",yaxis_title=None, yaxis=dict(showgrid=False,  showticklabels=False ),xaxis_tickangle=-45,barmode='stack',showlegend=True)
    st.plotly_chart(fig,use_container_width=True)

with st.container():
    df = c.groupby('DEPARTAMENTO').size().reset_index(name='Afectación')
    fig = px.bar(df, x="DEPARTAMENTO", y="Afectación",title='NÚMERO DE AFECTACIONES POR DEPARTAMENTO',
    text_auto=',4.0f',color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(xaxis_title="Departamento",yaxis_title=None,yaxis=dict(showgrid=False, showticklabels=False),xaxis_tickangle=-45,barmode='group',showlegend=True)
    st.plotly_chart(fig, use_container_width=True)
 
st.header('Causas FO Nacional Jun 2023 a Jun 2024')
cc1, cc2 = st.columns([50,50])
with cc1:
    df = c.groupby(['MES', 'CAUSA']).size().reset_index(name='Afectación')
    fig = px.bar( df,x="MES",y="Afectación",color="CAUSA",title='CORTES POR CAUSA SIN AFECTACIÓN',text_auto=',.0f',color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(xaxis_title="Mes",yaxis_title=None, yaxis=dict(showgrid=False,  showticklabels=False ),xaxis_tickangle=-45,barmode='stack',showlegend=True)
    st.plotly_chart(fig, use_container_width=True)
with cc2:
    df = c.groupby(['MES', 'CAUSA']).size().reset_index(name='Afectación')
    fig = px.bar( df,x="MES",y="Afectación",color="CAUSA",title='CORTES POR CAUSA CON AFECTACIÓN ',text_auto=',.0f',color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(xaxis_title="Mes",yaxis_title=None, yaxis=dict(showgrid=False,  showticklabels=False ),xaxis_tickangle=-45,barmode='stack',showlegend=True)
    st.plotly_chart(fig, use_container_width=True)


