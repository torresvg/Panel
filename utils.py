import plotly.express as px
import streamlit as st
from streamlit_extras.stylable_container import stylable_container

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def remote_css(url):
    st.markdown(f'<link href="{url}" rel="stylesheet">', unsafe_allow_html=True)   


def generateIconMetric(fa_icon):              
    return st.write(f'<div class="iconMetric" style="background-color:#5155c3;height:70px;width:70px;text-align:center"><i class="fa-solid {fa_icon} fa-2xl" style="line-height:50px;margin:auto;color:white;"></i></div>', unsafe_allow_html=True)        

def aplicarFormatoChart(fig,controls=False,legend=False,hoverTemplate=None):
    fig.update_layout(paper_bgcolor='white')
    fig.update_layout(plot_bgcolor='white')
    fig.update_layout(showlegend=legend)
    fig.update_layout(title_pad_l=50)
    fig.update_layout(
    #font_family="Open Sans",
    #font_color="#8dc73f",
    title_font_family="verdana",
    title_font_color="black",
    title_font_size=15,
    font_size=20,
    font_color="black"
    #legend_title_font_color="green"
    )

    if hoverTemplate:
        if hoverTemplate=="%":
            fig.update_traces(hovertemplate='<b>%{x}</b> <br> %{y:,.2%}')
        elif hoverTemplate=="$":
            fig.update_traces(hovertemplate='<b>%{x}</b> <br> $ %{y:,.1f}')
        elif hoverTemplate=="#":
            fig.update_traces(hovertemplate='<b>%{x}</b> <br> %{y:,.0f}')
    if controls:
        fig.update_xaxes(
            rangeslider_visible=True           
        )
    fig.update_layout(
            autosize=True,
            margin=dict(
                l=50,
                r=50,
                b=100,
                t=100,
                pad=4
            )
    )
    return fig

