
import pandas as pd
import streamlit as st
import locale
import plotly.express as px
import utils

locale.setlocale(locale.LC_TIME, 'es_CO.utf8')

color_discrete_sequence=['#ef9c66','#fcdc94','#c8cfa0','#78aba8','#ace2e1','#ebc49f','#b99470']

st.set_page_config(
    page_title='Dashboard',
    page_icon='📉',
    layout='wide'
)

utils.local_css('app.css')

doc1 = pd.ExcelFile('/Users/ValentinaGaviria/OneDrive - Telco Soluciones y Servicios/Documentos/Telefonica/Panel/Bitacora2024.xlsx')
doc2 = pd.ExcelFile('/Users/ValentinaGaviria/OneDrive - Telco Soluciones y Servicios/Documentos/Telefonica/Panel/Bitacora2023.xlsx')
doc3 = pd.ExcelFile('/Users/ValentinaGaviria/OneDrive - Telco Soluciones y Servicios/Documentos/Telefonica/Panel/Zonas.xlsx')

df1 = doc1.parse('Cortes de Fibra')
df2 = doc2.parse('Cortes de Fibra')
df3 = doc3.parse('Hoja5')

c = pd.concat([df1, df2, df3], ignore_index=True)

st.header('Titulo')

c.rename(columns={'Tipo de Tramo': 'TRAMO','Causa del daño': 'CAUSA','Departamento': 'DEPARTAMENTO','HORA INICIO': 'HORA_INICIO','HORA RECUP, DE SERICIO': 'HORA_RECUPERACION'}, inplace=True)
c['EECC'] = c['EECC'].str.replace('cobra', 'Cobra')
c['EECC'] = c['EECC'].str.replace('inmel', 'Inmel')
c['Afectación'] = c['Afectación'].str.replace('si', 'SI')
c['Afectación'] = c['Afectación'].str.replace('no', 'NO')
c["CAUSA"] = c["CAUSA"].map(lambda x: 'Visita_Fallida' if x == "Visita Fallida" else x)
c["DEPARTAMENTO"] = c["DEPARTAMENTO"].map(lambda x: 'VALLE_DEL_CAUCA' if x == "VALLE DEL CAUCA" else x)
c = c[c['HORA_RECUPERACION'].notna()]
c = c.dropna(how='any', subset=['CAUSA'])
discard = ['Visita_Fallida']
c = c[~c.CAUSA.str.contains('|'.join(discard))]
c['MES'] = c['HORA_INICIO'].dt.strftime('%B')
c['AÑO'] = c['HORA_INICIO'].dt.strftime('%Y')
c = c.dropna(subset=['Afectación'])

cc1, cc2 = st.columns([50, 50])
with cc1:
    dffibracausa = c.groupby(['MES']).size().reset_index(name='Afectación')
    fig = px.bar(dffibracausa,x="MES",y="Afectación",title='CORTES DE FIBRA POR CAUSA',color='Afectación',text_auto=',.0f', color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(showlegend=False)
    st.plotly_chart(utils.aplicarFormatoChart(fig), use_container_width=True)
with cc2:
    dfprincausa = c.groupby(['MES']).size().reset_index(name='Afectación')
    value = ['Corto Circuito','Vandalismo','Falla de Empalme de FiOp']
    dfprincausa = c[c.CAUSA.isin(value)]
    fig = px.bar(dfprincausa,x="MES", y="Afectación",title='PRINCIPALES CAUSAS',color='CAUSA', text_auto=',.0f',color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(showlegend=False)
    st.plotly_chart(utils.aplicarFormatoChart(fig),use_container_width=True)
    
cc1, cc2 = st.columns([50, 50])
with cc1:
    dfcortefibra= c.groupby(['MES']).size().reset_index(name='Afectación')
    fig = px.bar(dfcortefibra,x="MES", y="Afectación",title='CANTIDAD CORTES DE FIBRA',color='Afectación',text_auto=',.0f',color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(showlegend=False)
    st.plotly_chart(utils.aplicarFormatoChart(fig),use_container_width=True)
with cc2:
    dffibrazona = c.groupby(['MES']).size().reset_index(name='Zona')
    #dffibracausa= c.groupby('CAUSA').agg({'Afectación':'sum'}).reset_index()
    fig = px.bar(dffibrazona,x="MES", y="Zona",title='CORTES DE FIBRA POR ZONA',color='Zona',text_auto=',.0f',color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(showlegend=False)
    st.plotly_chart(utils.aplicarFormatoChart(fig),use_container_width=True)

with st.container():
    dfcantreinc = c.groupby(['DEPARTAMENTO', 'MES']).size().reset_index(name='Zona')
    fig = px.bar(dfcantreinc,x="DEPARTAMENTO", y="Zona",title='NÚMERO DE ENLACES REINCIDENTES POR ZONA',color='Zona',text_auto=',.0f', color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(showlegend=False)
    st.plotly_chart(utils.aplicarFormatoChart(fig),use_container_width=True)

cc1, cc2 = st.columns([50,50])
with cc1:
    dfcassinafec = c.groupby(['MES']).size().reset_index(name='Afectación')
    fig = px.bar(dfcassinafec,x="MES",y="Afectación",title='CORTES POR CAUSA SIN AFECTACIÓN',color='Afectación',text_auto=',.0f', color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(showlegend=False)
    st.plotly_chart(utils.aplicarFormatoChart(fig), use_container_width=True)
with cc2:
    dfcasconafec = c.groupby(['MES']).size().reset_index(name='Afectación')
    fig = px.bar(dfcasconafec,x="MES", y="Afectación",title='CORTES POR CAUSA CON AFECTACIÓN', color='Afectación',text_auto=',.0f', color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(showlegend=False)
    st.plotly_chart(utils.aplicarFormatoChart(fig),use_container_width=True)


