import streamlit as st

import sys
#sys.path.append('packages/emagpy-master/src')
import time
import os
import numpy as np
import pandas as pd
from emagpy import Problem, EMagPy_version
import matplotlib.pyplot as plt

# change loading bar color
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


testdir = 'packages/emagpy-master/src/examples/cover-crop/'

def save_uploadedfile(uploadedfile):
     with open(os.path.join("tempDir",uploadedfile.name),"wb") as f:
         f.write(uploadedfile.getbuffer())
     return st.success("Saved File:{} to tempDir".format(uploadedfile.name))

#st.set_page_config(layout = "wide")
st.header("EmagPy web app")
st.write("Upload your csv file for on-demand EMI inversion")


uploaded_file = st.file_uploader("Choose a file", help="Upload file here", type=".csv")
if uploaded_file is not None:
	st.write(uploaded_file.name)
	df = pd.read_csv(uploaded_file)  #df = pd.read_csv(testdir + 'coverCrop.csv')
	df.to_csv("tempDir/temp.csv") # make a temp copy, because streamlit use BytesIO and error in `k.createSurvey()`

	k = Problem() # this create the main object
	k.createSurvey("tempDir/temp.csv")# this import the data 
	
	with st.expander("See data:"):

		fig, ax = plt.subplots()
		k.show(vmax=50,ax=ax)
		st.pyplot(fig)

		fig, ax = plt.subplots()
		k.showMap(coil='VCP0.71', contour=True, pts=True,ax=ax)
		st.pyplot(fig)

	with st.expander("See model:"):	
		k.setInit(depths0=[0.5, 1], # specify the BOTTOM of each layer (the last layer is infinite)
         		 conds0=[20, 20, 20],
         		 fixedConds=[False, False, False])# conductivity in mS/m
		k.invert() 
		fig, ax = plt.subplots(); k.showResults(ax=ax); st.pyplot(fig)
		fig, ax = plt.subplots(); k.showMisfit(ax=ax); st.pyplot(fig)
		fig, ax = plt.subplots(); k.showOne2one(ax=ax); st.pyplot(fig)

		slice_k = 0

		st.write("Show slices:")
		show_contour = st.checkbox('Interpolate?')
		slice_k = st.slider("Select slice",0,2,0)
		fig, ax = plt.subplots(); k.showSlice(islice=slice_k, contour=show_contour,
				 vmin=12, vmax=50,ax=ax); st.pyplot(fig)