import streamlit as st
import numpy as np
import pandas as pd
import pickle
from tmdbv3api import TMDb,Movie,TV
import base64
tmbd=TMDb()
tmbd.api_key='2215513a27c6c9c83bc6f993628cf9dc'
distances=pickle.load(open('distsnces.pkl','rb'))
names=pd.DataFrame(pickle.load(open('moviedata.pkl','rb')))
tv=TV()
show = tv.popular()
nams=[]
for i in show:
    nams.append(i.name)
def recommand(movie):
    movie_idx=names[names['title']==movie].index[0]
    distance=distances[movie_idx]
    indexes=sorted(enumerate(distance),reverse=True,key=lambda x:x[1])[1:6]
    movie_id=[]
    for i in indexes:
        movie_id.append(names.iloc[i[0]].movie_id)
    movie_posters=poster(movie_id)
    return movie_posters
def poster(name):
    mov=Movie()
    posters=[]
    for i in name:
     post=mov.details(i)
     posters.append("https://image.tmdb.org/t/p/w500/"+post.poster_path)
    return posters
def show_poster(show):
    tv1=TV()
    show = tv1.search(show)
    ids=[]
    posters=[]
    for i in show:
     ids.append(i.id)
     shows=tv.similar(ids[0])
     for j in shows:
      posters.append("https://image.tmdb.org/t/p/w500/"+j.poster_path)
    posters=posters[1:6]
    return posters 
    
@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_background(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img,unsafe_allow_html=True)

set_background('pictures4.jpg')
st.title('Movie Recommadation System')
movie=st.selectbox('select movie',names['title'].values)
if st.button('recommand'):
    posters=recommand(movie)
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.image(posters[0])
    with col2:
        st.image(posters[1])
    with col3:
        st.image(posters[2])
    with col4:
        st.image(posters[3])
    with col5:
        st.image(posters[4])
st.title('TV shows Recommadation System ')
show=st.selectbox('select show',nams)
if st.button('recommandshow'):
    sh=show_poster(show)
    col1,col2,col3,col4,col5=st.columns(5)
    with col1:
        st.image(sh[0])
    with col2:
        st.image(sh[1])
    with col3:
        st.image(sh[2])
    with col4:
        st.image(sh[3])
    with col5:
        st.image(sh[4])


    






