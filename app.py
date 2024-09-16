import pandas as pd
import streamlit as st
import locale
# import altair as alt
import plotly.express as px
# import utils

locale.setlocale(locale.LC_TIME, 'es_CO.utf8')

color_discrete_sequence=['#def9c4','#9cdba6','#50b498','#468585','#c4dad2','#80b9ad','#40a578','#1679ab','#8decb4','#124076','#80bcbd','#c3e2c2','#a7d397','#d2e0fb']

st.set_page_config(page_title='Dashboard', page_icon='📉',layout='wide')

# utils.local_css('app.css')
doc1 = pd.ExcelFile('/Users/ValentinaGaviria/OneDrive - Telco Soluciones y Servicios/Documentos/Telefonica/Panel/ZONA.xlsx')
doc2 = pd.ExcelFile('/Users/ValentinaGaviria/OneDrive - Telco Soluciones y Servicios/Documentos/Telefonica/Panel/Bitacora2024.xlsx')
doc3 = pd.ExcelFile('/Users/ValentinaGaviria/OneDrive - Telco Soluciones y Servicios/Documentos/Telefonica/Panel/Bitacora2023.xlsx')

df1 = doc1.parse('Hoja1')
df2 = doc2.parse('Cortes de Fibra')
df3 = doc3.parse('Cortes de Fibra')
mergzona = pd.merge(df1, df2, on=['Departamento'])
c = pd.concat([df2, df3, mergzona], ignore_index=True)

c.rename(columns={'Tipo de Tramo': 'TRAMO','Causa del daño': 'CAUSA','Departamento': 'DEPARTAMENTO','HORA INICIO': 'HORA_INICIO','HORA RECUP, DE SERICIO': 'HORA_RECUPERACION','Corto circuito': 'CCIRCUITO'}, inplace=True)
#c["CAUSA"] = c["CAUSA"].map(lambda x: 'Visita_Fallida' if x == "Visita Fallida" else x)
c['EECC'] = c['EECC'].str.replace('cobra', 'Cobra')
c['EECC'] = c['EECC'].str.replace('inmel', 'Inmel')
c['CAUSA'] = c['CAUSA'].str.replace('visita Fallida', 'Visita Fallida')
c['Afectación'] = c['Afectación'].str.replace('si', 'SI')
c['Afectación'] = c['Afectación'].str.replace('no', 'NO')
c["DEPARTAMENTO"] = c["DEPARTAMENTO"].map(lambda x: 'VALLE_DEL_CAUCA' if x == "VALLE DEL CAUCA" else x)
c = c[c['HORA_RECUPERACION'].notna()]
c = c.dropna(how='any', subset=['CAUSA'])
c['MES'] = c['HORA_INICIO'].dt.strftime('%B')
c['AÑO'] = c['HORA_INICIO'].dt.strftime('%Y')
c['MA'] = c['HORA_INICIO'].dt.strftime('%B-%Y')
c = c.dropna(subset=['Afectación'])
orden_m = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
c['MES'] = pd.Categorical(c['MES'], categories=orden_m, ordered=True)
#c = c.drop_duplicates(subset=['DEPARTAMENTO'])

cc1, cc2 = st.columns([50, 50])
with cc1:
    df = c.groupby(['CAUSA', 'AÑO']).size().reset_index(name='Count')
    df = df.sort_values(by='Count', ascending=False)
    fig = px.bar(df,x="CAUSA",y="Count",color="AÑO",title='CORTES DE FIBRA POR CAUSA',text_auto=',.0f',color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(xaxis_title=None,yaxis_title=None, yaxis=dict(showgrid=False, showticklabels=False),xaxis_tickangle=-45,barmode='group',showlegend=True )
    st.plotly_chart(fig, use_container_width=True)
with cc2:
    df = c.groupby(['MA', 'CAUSA']).size().reset_index(name='Incidente')
    value = ['Corto Circuito', 'Vandalismo', 'Falla de Empalme de FiOp']
    df = df[df['CAUSA'].isin(value)]
    fig = px.bar(df,x="MA",y="Incidente",color="CAUSA",title='CAUSAS PRINCIPALES ',text_auto=',.0f',color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(xaxis_title=None,yaxis_title=None, yaxis=dict(showgrid=False,  showticklabels=False ),xaxis_tickangle=-45,barmode='stack',showlegend=True)
    st.plotly_chart(fig, use_container_width=True)
    
st.header('Detalles de cortes FO Planta Interna')
cc1, cc2 = st.columns([50, 50])
with cc1:
    df = c.groupby(['MES', 'Afectación']).size().reset_index(name='Conteo')
    fig = px.bar(df, x="MES", y="Conteo", color="Afectación", title='CANTIDAD DE CORTES DE FIBRA', text_auto=',.0f',color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(xaxis_title=None,yaxis_title=None, yaxis=dict(showgrid=False,  showticklabels=False ),xaxis_tickangle=-45,barmode='stack',showlegend=True)
    st.plotly_chart(fig, use_container_width=True)
with cc2:
    df = c.groupby(['MES', 'Zona']).size().reset_index(name='Incidente')
    fig = px.bar(df, x="MES", y="Incidente", color="Zona", title='CORTES DE FIBRA POR ZONA', text_auto=',.0f',color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(xaxis_title=None,yaxis_title=None, yaxis=dict(showgrid=False,  showticklabels=False ),xaxis_tickangle=-45,barmode='stack',showlegend=True)
    st.plotly_chart(fig, use_container_width=True)
    
#enlace, estado, incidente, departamento, zona
with st.container():
    df = c.groupby(['DEPARTAMENTO', 'Zona']).size().reset_index(name='Incidente')
    fig = px.bar(df, x="DEPARTAMENTO", y="Incidente", color="Zona", title='NÚMERO DE ENLACES REINCIDENTES POR ZONA 2024', text_auto=',.0f',color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(xaxis_title=None,yaxis_title=None, yaxis=dict(showgrid=False,  showticklabels=False ),xaxis_tickangle=-45,barmode='stack',showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

st.header('Causas FO Nacional 2023 a 2024')

with st.container():
    c_no = c[c['Afectación'] == 'NO']
    df = c_no.groupby(['MES', 'CAUSA']).size().reset_index(name='Conteo')
    fig = px.bar(df, x="MES", y="Conteo", color="CAUSA", title='CORTES POR CAUSA SIN AFECTACIÓN', text_auto=',.0f', color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(xaxis_title=None,yaxis_title=None,yaxis=dict(showgrid=False, showticklabels=False),xaxis_tickangle=-45,barmode='stack',showlegend=True)
    st.plotly_chart(fig, use_container_width=True)

with st.container():
    c_si = c[c['Afectación'] == 'SI']
    df = c_si.groupby(['MES', 'CAUSA']).size().reset_index(name='Conteo')
    fig = px.bar(df, x="MES", y="Conteo", color="CAUSA", title='CORTES POR CAUSA CON AFECTACIÓN', text_auto=',.0f', color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(xaxis_title=None,yaxis_title=None,yaxis=dict(showgrid=False, showticklabels=False),xaxis_tickangle=-45,barmode='stack',showlegend=True)
    st.plotly_chart(fig, use_container_width=True)


cc1, cc2 = st.columns([50, 50])
with cc1:
    df = c.groupby(['DEPARTAMENTO', 'CAUSA']).size().reset_index(name='Conteo')
    value = ['Visita Fallida']
    df = df[df['CAUSA'].isin(value)]
    fig = px.bar(df,x="DEPARTAMENTO",y="Conteo",color="CAUSA",title='VISITAS FALLIDAS POR DEPARTAMENTO',text_auto=',.0f',color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(xaxis_title=None,yaxis_title=None, yaxis=dict(showgrid=False,  showticklabels=True),xaxis_tickangle=-45,barmode='stack',showlegend=True)
    st.plotly_chart(fig, use_container_width=True)
with cc2:
    df = c.groupby(['CAUSA']).size().reset_index(name='Conteo')
    value = ['Visita Fallida']
    df = df[df['CAUSA'].isin(value)]
    fig = px.bar(df,x="CAUSA",y="Conteo",color=None,title='CAUSAS VISITAS FALLIDAS',text_auto=',.0f',color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(xaxis_title=None,yaxis_title=None, yaxis=dict(showgrid=False,  showticklabels=True),xaxis_tickangle=-45,barmode='stack',showlegend=True)
    st.plotly_chart(fig, use_container_width=True)