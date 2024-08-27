
#import datetime
import pandas as pd
import streamlit as st
import altair as alt
import locale
import plotly.express as px
import utils

locale.setlocale(locale.LC_TIME, 'es_CO.utf8')

color_discrete_sequence=['#ef9c66','#fcdc94','#c8cfa0','#78aba8','#55ad9b']

st.set_page_config(
    page_title='Dashboard',
    page_icon='📉',
    layout='wide'
)
utils.local_css('app.css')

#
#*********************** GRAFICA **************************#
#
#st.title("Cantidad cortes de:blue[ fibra]")

doc1 = pd.ExcelFile('/Users/ValentinaGaviria/OneDrive - Telco Soluciones y Servicios/Documentos/Telefonica/Panel/Bitacora2024.xlsx')
doc2 = pd.ExcelFile('/Users/ValentinaGaviria/OneDrive - Telco Soluciones y Servicios/Documentos/Telefonica/Panel/Bitacora2023.xlsx')
doc3 = pd.ExcelFile('/Users/ValentinaGaviria/OneDrive - Telco Soluciones y Servicios/Documentos/Telefonica/Panel/Zonas.xlsx')

df1 = doc1.parse('Cortes de Fibra')  
df2 = doc2.parse('Cortes de Fibra')
df3 = doc3.parse('Hoja5')  

#st.header('Titulo si se requiere')

c = pd.concat([df1, df2, df3], ignore_index=True)

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
    dffibracausa = c.groupby(['CAUSA', 'MES']).size().reset_index(name='Afectación')
    fig = px.bar(dffibracausa,x="CAUSA",y="Afectación",title='CORTES DE FIBRA POR CAUSA',color='CAUSA',text_auto=',.0f', color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(showlegend=False)
    st.plotly_chart(utils.aplicarFormatoChart(fig), use_container_width=True)
with cc2:
    dfprincausa = c.groupby(['CAUSA', 'MES']).size().reset_index(name='Afectación')
    fig = px.bar(dfprincausa,x="CAUSA", y="Afectación",title='PRINCIPALES CAUSAS',color='CAUSA', color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(showlegend=False)
    st.plotly_chart(utils.aplicarFormatoChart(fig),use_container_width=True)
    
cc1, cc2 = st.columns([50, 50])
with cc1:
    dffibracausa = c.groupby(['CAUSA', 'MES']).size().reset_index(name='Afectación')
    fig = px.bar(dffibracausa,x="CAUSA", y="Afectación",title='CORTES DE FIBRA POR ZONA',color='CAUSA',color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(showlegend=False)
    st.plotly_chart(utils.aplicarFormatoChart(fig),use_container_width=True)
with cc2:
    dffibracausa = c.groupby(['CAUSA', 'MES']).size().reset_index(name='Afectación')
    #dffibracausa= c.groupby('CAUSA').agg({'Afectación':'sum'}).reset_index()
    fig = px.bar(dffibracausa,x="CAUSA", y="Afectación",title='CORTES DE FIBRA POR ZONA',color='CAUSA',color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(showlegend=False)
    st.plotly_chart(utils.aplicarFormatoChart(fig),use_container_width=True)

with st.container():
    dfcantfibra = c.groupby(['DEPARTAMENTO', 'MES']).size().reset_index(name='Enlace')
    fig = px.bar(dfcantfibra,x="DEPARTAMENTO", y="Enlace",title='NÚMERO DE ENLACES REINCIDENTES POR ZONA',color='DEPARTAMENTO',text_auto=',.0f', color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(showlegend=False)
    st.plotly_chart(utils.aplicarFormatoChart(fig),use_container_width=True)

cc1, cc2 = st.columns([50,50])
with cc1:
    dfcantfibra = c.groupby(['CAUSA', 'MES']).size().reset_index(name='Afectación')
    fig = px.bar(dfcantfibra,x="CAUSA", y="Afectación",title='NÚMERO DE ENLACES REINCIDENTES POR ZONA',color='CAUSA',text_auto=',.0f', color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(showlegend=False)
    st.plotly_chart(utils.aplicarFormatoChart(fig),use_container_width=True)
with cc2:
    dfcantfibra = c.groupby(['CAUSA', 'MES']).size().reset_index(name='Afectación')
    fig = px.bar(dffibracausa,x="CAUSA", y="Afectación",title='CORTES DE FIBRA POR ZONA',color='CAUSA', text_auto=',.0f', color_discrete_sequence=color_discrete_sequence)
    fig.update_layout(showlegend=False)
    st.plotly_chart(utils.aplicarFormatoChart(fig),use_container_width=True)

# c = pd.concat([df1, df2, df3], ignore_index=True)
# c.rename(columns = {'Tipo de Tramo':'TRAMO','Causa del daño':'CAUSA','Departamento':'DEPARTAMENTO','HORA INICIO':'HORA_INICIO','HORA RECUP, DE SERICIO':'HORA_RECUPERACION'}, inplace = True)
# c['EECC'] = c['EECC'].str.replace('cobra' , 'Cobra')
# c['EECC'] = c['EECC'].str.replace('inmel' , 'Inmel')
# c['Afectación'] = c['Afectación'].str.replace('si' , 'SI')
# c['Afectación'] = c['Afectación'].str.replace('no' , 'NO')
# c["CAUSA"] = c["CAUSA"].map(lambda x: 'Visita_Fallida' if x=="Visita Fallida" else x)
# c["DEPARTAMENTO"] = c["DEPARTAMENTO"].map(lambda x: 'VALLE_DEL_CAUCA' if x=="VALLE DEL CAUCA" else x)
# c = c[c['HORA_RECUPERACION'].notna()]
# c = c.dropna( how='any', subset=['CAUSA'])
# discard = ['Visita_Fallida']
# c = c[~c.CAUSA.str.contains('|'.join(discard))]
# c['MES'] = c['HORA_INICIO'].dt.strftime('%B')
# c['AÑO'] = c['HORA_INICIO'].dt.strftime('%Y')
# #*********** CAMPOS **********#
# c = c.groupby(['CAUSA', 'AÑO']).size().reset_index(name='Afectación')
# cc1 = (alt.Chart(c).mark_line().encode(x="CAUSA", y="Afectación", color='AÑO')).properties(title='CANTIDAD DE FIBRA POR CAUSA', width=300, height=400,colore=colore)
# text = cc1.mark_text(align='center', baseline='bottom', dy=-10).encode(text='Afectación:Q')
# st.altair_chart(cc1 + text, use_container_width=True)

#
#*********************** GRAFICA 2 **************************#
#

# c = pd.concat([df1, df2, df3], ignore_index=True)
# c.rename(columns = {'Tipo de Tramo':'TRAMO','Causa del daño':'CAUSA','Departamento':'DEPARTAMENTO','HORA INICIO':'HORA_INICIO','HORA RECUP, DE SERICIO':'HORA_RECUPERACION','Falla de Empalme de FiOp':'FALLAEMPALME','Vandalismo':'VANDALISMO','Corto Circuito':'CCIRCUITO'}, inplace = True)
# c['EECC'] = c['EECC'].str.replace('cobra' , 'Cobra')
# c['EECC'] = c['EECC'].str.replace('inmel' , 'Inmel')
# c['Afectación'] = c['Afectación'].str.replace('si' , 'SI')
# c['Afectación'] = c['Afectación'].str.replace('no' , 'NO')
# c["CAUSA"] = c["CAUSA"].map(lambda x: 'Visita_Fallida' if x=="Visita Fallida" else x)
# c["DEPARTAMENTO"] = c["DEPARTAMENTO"].map(lambda x: 'VALLE_DEL_CAUCA' if x=="VALLE DEL CAUCA" else x)
# c = c[c['HORA_RECUPERACION'].notna()]
# c = c.dropna( how='any', subset=['CAUSA'])
# discard = ['Visita_Fallida']
# c = c[~c.CAUSA.str.contains('|'.join(discard))]
# c['MES'] = c['HORA_INICIO'].dt.strftime('%B')
# c['AÑO'] = c['HORA_INICIO'].dt.strftime('%Y')
# #************ CAMPOS ************#
# value = ['Corto Circuito','Vandalismo','Falla de Empalme de FiOp']
# c = c[c.CAUSA.isin(value)]
# c = c.groupby(['MES', 'CAUSA']).size().reset_index(name='Cantidad')
# cc2 = (alt.Chart(c).mark_bar().encode(x="MES",y="Cantidad" , color='CAUSA')).properties(title='PRINCIPALES CAUSAS',width=400,height=400)
# text = cc2.mark_text(align='center',baseline='middle',dy=-15,color='black').encode(text='Cantidad:Q')
# st.altair_chart(cc2 + text, use_container_width=True)


#
#*********************** GRAFICA 3 **************************#
#
c = pd.concat([df1, df2, df3], ignore_index=True)
c.rename(columns = {'Tipo de Tramo':'TRAMO','Causa del daño':'CAUSA','Departamento':'DEPARTAMENTO','HORA INICIO':'HORA_INICIO','HORA RECUP, DE SERICIO':'HORA_RECUPERACION'}, inplace = True)
c['EECC'] = c['EECC'].str.replace('cobra' , 'Cobra')
c['EECC'] = c['EECC'].str.replace('inmel' , 'Inmel')
c['Afectación'] = c['Afectación'].str.replace('si' , 'SI')
c['Afectación'] = c['Afectación'].str.replace('no' , 'NO')
c["CAUSA"] = c["CAUSA"].map(lambda x: 'Visita_Fallida' if x=="Visita Fallida" else x)
c["DEPARTAMENTO"] = c["DEPARTAMENTO"].map(lambda x: 'VALLE_DEL_CAUCA' if x=="VALLE DEL CAUCA" else x)
c = c[c['HORA_RECUPERACION'].notna()]
c = c.dropna( how='any', subset=['CAUSA'])
discard = ['Visita_Fallida']
c = c[~c.CAUSA.str.contains('|'.join(discard))]
c['MES'] = c['HORA_INICIO'].dt.strftime('%B')
c['AÑO'] = c['HORA_INICIO'].dt.strftime('%Y')
#*********** CAMPOS **********#
c = c.groupby(['MES', 'Afectación']).size().reset_index(name='Cantidad')
cc3 = (alt.Chart(c).mark_bar().encode(x="MES",y="Cantidad" , color='Afectación')).properties(title='CANTIDAD CORTES DE FIBRA',width=400,height=400)
text = cc3.mark_text(align='center',baseline='top').encode(text='Cantidad:Q')
st.altair_chart(cc3  + text, use_container_width=True)


#
#*********************** GRAFICA 4 **************************#
#
c = pd.concat([df1, df2, df3], ignore_index=True)
c.rename(columns = {'Tipo de Tramo':'TRAMO','Causa del daño':'CAUSA','Departamento':'DEPARTAMENTO','HORA INICIO':'HORA_INICIO','HORA RECUP, DE SERICIO':'HORA_RECUPERACION','Zona':'ZONA'}, inplace = True)
c['EECC'] = c['EECC'].str.replace('cobra' , 'Cobra')
c['EECC'] = c['EECC'].str.replace('inmel' , 'Inmel')
c["CAUSA"] = c["CAUSA"].map(lambda x: 'Visita_Fallida' if x=="Visita Fallida" else x)
c["DEPARTAMENTO"] = c["DEPARTAMENTO"].map(lambda x: 'VALLE_DEL_CAUCA' if x=="VALLE DEL CAUCA" else x)
c = c[c['HORA_RECUPERACION'].notna()]
c = c.dropna( how='any', subset=['CAUSA'])
discard = ['Visita_Fallida']
c = c[~c.CAUSA.str.contains('|'.join(discard))]
c['MES'] = c['HORA_INICIO'].dt.strftime('%B')
c['AÑO'] = c['HORA_INICIO'].dt.strftime('%Y')
#************ CAMPOS ************#
c = c.groupby(['MES', 'DEPARTAMENTO']).size().reset_index(name='Afectación')
cc4 = (alt.Chart(c).mark_line().encode(x="MES", y="Afectación" , color='DEPARTAMENTO')).properties(title='CORTES DE FIBRA POR ZONA',width=400,height=450)
text = cc4.mark_text(align='center',baseline='top').encode(text='Afectación:Q')
st.altair_chart(cc4 + text, use_container_width=True)

#
#*********************** GRAFICA 5 **************************#
#
c = pd.concat([df1, df2, df3], ignore_index=True)
c.rename(columns = {'Tipo de Tramo':'TRAMO','Causa del daño':'CAUSA','Departamento':'DEPARTAMENTO','HORA INICIO':'HORA_INICIO','HORA RECUP, DE SERICIO':'HORA_RECUPERACION'}, inplace = True)
c['EECC'] = c['EECC'].str.replace('cobra' , 'Cobra')
c['EECC'] = c['EECC'].str.replace('inmel' , 'Inmel')
c["CAUSA"] = c["CAUSA"].map(lambda x: 'Visita_Fallida' if x=="Visita Fallida" else x)
c["DEPARTAMENTO"] = c["DEPARTAMENTO"].map(lambda x: 'VALLE_DEL_CAUCA' if x=="VALLE DEL CAUCA" else x)
c = c[c['HORA_RECUPERACION'].notna()]
c = c.dropna( how='any', subset=['CAUSA'])
discard = ['Visita_Fallida']
c = c[~c.CAUSA.str.contains('|'.join(discard))]
c['MES'] = c['HORA_INICIO'].dt.strftime('%B')
c['AÑO'] = c['HORA_INICIO'].dt.strftime('%Y')
#************ CAMPOS ************#
c = c.groupby(['DEPARTAMENTO']).size().reset_index(name='Enlace')
cc5 = (alt.Chart(c).mark_bar().encode(x="DEPARTAMENTO", y="Enlace")).properties(title='NÚMERO DE ENLACES REINCIDENTES POR ZONA 2024',width=6000,height=450)
text = cc5.mark_text(color='black',size=10,align='center',baseline='middle',dy=-10).encode(text='Enlace:Q')
st.altair_chart(cc5 + text, use_container_width=True)

#
#*********************** GRAFICA 6 **************************#
#
c = pd.concat([df1, df2, df3], ignore_index=True)
c.rename(columns = {'Tipo de Tramo':'TRAMO','Causa del daño':'CAUSA','Departamento':'DEPARTAMENTO','HORA INICIO':'HORA_INICIO','HORA RECUP, DE SERICIO':'HORA_RECUPERACION'}, inplace = True)
c['EECC'] = c['EECC'].str.replace('cobra' , 'Cobra')
c['EECC'] = c['EECC'].str.replace('inmel' , 'Inmel')
c['Afectación'] = c['Afectación'].str.replace('si' , 'SI')
c["CAUSA"] = c["CAUSA"].map(lambda x: 'Visita_Fallida' if x=="Visita Fallida" else x)
c["DEPARTAMENTO"] = c["DEPARTAMENTO"].map(lambda x: 'VALLE_DEL_CAUCA' if x=="VALLE DEL CAUCA" else x)
c = c[c['Afectación'] == 'NO']
c = c[c['HORA_RECUPERACION'].notna()]
c = c.dropna( how='any', subset=['CAUSA'])
discard = ['Visita_Fallida']
c = c[~c.CAUSA.str.contains('|'.join(discard))]
c['MES'] = c['HORA_INICIO'].dt.strftime('%B')
c['AÑO'] = c['HORA_INICIO'].dt.strftime('%Y')
#************ CAMPOS ************#
c = c.groupby(['MES', 'CAUSA']).size().reset_index(name='Cantidad')
cc6 = (alt.Chart(c).mark_bar().encode(x="MES", y="Cantidad", color='CAUSA')).properties(title='CORTES POR CAUSA SIN AFECTACIÓN',width=400,height=400,)
text = cc6.mark_text(align='center',baseline='top',dy=-15).encode(text='Cantidad:Q')
st.altair_chart(cc6 + text, use_container_width=True)

#
#*********************** GRAFICA 7 **************************#
#
c = pd.concat([df1, df2, df3], ignore_index=True)
c.rename(columns = {'Tipo de Tramo':'TRAMO','Causa del daño':'CAUSA','Departamento':'DEPARTAMENTO','HORA INICIO':'HORA_INICIO','HORA RECUP, DE SERICIO':'HORA_RECUPERACION'}, inplace = True)
c['EECC'] = c['EECC'].str.replace('cobra' , 'Cobra')
c['EECC'] = c['EECC'].str.replace('inmel' , 'Inmel')
c['Afectación'] = c['Afectación'].str.replace('si' , 'SI')
c["CAUSA"] = c["CAUSA"].map(lambda x: 'Visita_Fallida' if x=="Visita Fallida" else x)
c["DEPARTAMENTO"] = c["DEPARTAMENTO"].map(lambda x: 'VALLE_DEL_CAUCA' if x=="VALLE DEL CAUCA" else x)
c = c[c['Afectación'] == 'SI']
c = c[c['HORA_RECUPERACION'].notna()]
c = c.dropna( how='any', subset=['CAUSA'])
discard = ['Visita_Fallida']
c = c[~c.CAUSA.str.contains('|'.join(discard))]
c['MES'] = c['HORA_INICIO'].dt.strftime('%B')
c['AÑO'] = c['HORA_INICIO'].dt.strftime('%Y')
#************ CAMPOS ************#
c = c.groupby(['MES', 'CAUSA']).size().reset_index(name='Cantidad')
cc7 = (alt.Chart(c).mark_bar().encode(x="MES",y="Cantidad", color="CAUSA")).properties(title='CORTES POR CAUSA CON AFECTACIÓN',width=400,height=400)
text = cc7.mark_text(align='center',baseline='top',dy=-15).encode(text='Cantidad:Q')
st.altair_chart(cc7 + text, use_container_width=True)

