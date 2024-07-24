from LightPipes import *
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st


with st.sidebar:
    st.markdown("**Basic Parameters**")
    wavelength = st.number_input("Wavelength(nm)", 1064.0)*nm
    N=st.number_input("Grid Size", 400) 
    z = 1000*mm
    f = 1000*mm
    mode = st.radio("Mode", options=["Uniform", "Gaussian", "Annular"])
    st.write('<style>div.row-widget.stRadio > div{flex-direction:row;}</style>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Annular Mask Setting**")
    tab1, tab2 = st.columns(2)
    with tab1:
        size = st.number_input("Computation Size (mm)", min_value = 5.0,  value = 10.0, step = 0.2)*mm
    with tab2:
        beam_size = st.number_input("Gaussian Beam Radius (mm)", min_value = 0.5,value=2.0, step = 0.2)*mm

    tab1, tab2 = st.columns(2)
    with tab1:
        dr1 = np.multiply(st.number_input("dr1 (mm)", 0.1, max_value=size/2/mm), mm)
    with tab2: 
        dr2 = np.multiply(st.number_input("dr2 (mm)", 0.1, max_value=size/2/mm), mm)
    [r1, r2] = np.multiply(st.slider("Ring radius (mm)", min_value=0.0, max_value=size/2/mm, value=(0.0, size/4/mm)),mm)

F_initial=Begin(size,wavelength,N);
F_gauss=GaussBeam(F_initial, beam_size)

F_inner=CircScreen(r1-dr1/2,0,0,F_gauss)
F_inner=CircAperture(r1+dr2/2,0,0,F_inner)
F_outter=CircScreen(r2-dr2/2,0,0,F_gauss)
F_outter=CircAperture(r2+dr2/2,0,0,F_outter)

if mode =="Uniform":
    F_conbined = Begin(size,wavelength,N)
if mode =="Gaussian":
    F_conbined = F_gauss
if mode =="Annular":
    F_conbined = BeamMix(F_inner, F_outter)


x = y = F_conbined.xvalues/mm
# x = y = F_conbined.xvalues/mm

tab1, tab2 = st.columns(2)
with tab1:
    fig = plt.figure()
    plt.imshow(Intensity(F_gauss), extent =[x.min(),x.max(), y.min(), y.max()])
    plt.title("Gaussian Input")
    st.pyplot(fig)
with tab2:
    fig = plt.figure()
    plt.imshow(Intensity(F_conbined), extent =[x.min(),x.max(), y.min(), y.max()])
    plt.title("Modified Input")
    st.pyplot(fig)


plot_select = st.multiselect("Plot Select", default = "Lateral PSF", options=["Lateral PSF", "Axial PSF","Crossection"])

if "Lateral PSF" in plot_select:
    F_Lateral_PSF=Forvard(f,F_conbined)
    F_Lateral_PSF=Lens(f,F_Lateral_PSF)
    F_Lateral_PSF=Forvard(z,F_Lateral_PSF) #Propagate to the far field
    
    fig = plt.figure(figsize=(8,8))
    plt.imshow(Intensity(F_Lateral_PSF, 1))
    plt.title("Lateral PSF")
    
    st.pyplot(fig)
    
if "Axial PSF" in plot_select:
    with st.form(key="input_form"):
        col1, col2, col3 = st.columns(3)
        with col1: 
            z_min = st.number_input("Min z (mm)", value = f/2/mm)*mm
        with col2: 
            z_max = st.number_input("Max z (mm)", value = (f+f/2)/mm)*mm
        with col3: 
            num = st.number_input("Number of z slices", value = 200)    
        z_list = np.linspace(z_min, z_max, num)
        submitted = st.form_submit_button("Submit", use_container_width=True)
  
        
        if submitted:
            my_bar = st.progress(0.0, text="Operation in progress. Please wait.")
            F_Axial_PSF_list = []
            for k, z_val in enumerate(z_list):
                F_Axial_PSF=Forvard(f,F_conbined)
                F_Axial_PSF = Lens(f,F_Axial_PSF)
                F_Axial_PSF = Forvard(z_val,F_Axial_PSF) #Propagate to the far field
                idx = int(F_Axial_PSF.grid_dimension/2)
                crossection = Intensity(F_Axial_PSF, 0)[:,idx]
                F_Axial_PSF_list.append(crossection)
                my_bar.progress((k + 1)/(len(z_list)+1), text="Operation in progress. Please wait.")
        
            my_bar.empty()
            F_Axial_PSF_list = np.array(F_Axial_PSF_list)
            fig = plt.figure(figsize=(8,8))
            plt.imshow(F_Axial_PSF_list)
            plt.title("Axial PSF")
            st.pyplot(fig)
    

if "Crossection" in plot_select:
    z = st.slider("z position (mm)", max_value = f*2/mm, value = f/mm)*mm
    F_Crossection=Forvard(f,F_conbined)
    F_Crossection = Lens(f,F_Crossection)
    F_Crossection_z0=Forvard(f,F_Crossection) #Propagate to the far field
    F_Crossection_z1=Forvard(z,F_Crossection) #Propagate to the far field
        
    idx = int(F_Crossection_z0.grid_dimension/2)
    cross_z0 = Intensity(F_Crossection_z0, 0)[:,idx]
    cross_z1 = Intensity(F_Crossection_z1, 0)[:,idx]
    cross_z1_2D = Intensity(F_Crossection_z1, 0)
    xaxis = F_Crossection_z1.xvalues/mm
    
    col1, col2 = st.columns(2)
    with col1:
        fig = plt.figure()
        plt.imshow(cross_z1_2D)
        plt.legend()
        plt.title("Crossection")
        st.pyplot(fig)
    with col2:
        fig, ax = plt.subplots()
        ax.plot(xaxis, cross_z0,  ':', c="red", label="@focal")
        ax.plot(xaxis, cross_z1, c="blue", label="compare")
        plt.legend()
        plt.title("Crossection")
        ax.set_aspect('auto')
        plt.grid()
        st.pyplot(fig)
        st.write("위 그림은 Focal position 위치 및 특정 Z 위치에서의 빔 프로파일을 비교하는 그림입니다")
    
     

    






# f = st.slider("Focal length(mm): ", value=200, min_value=50, max_value=500)*mm
# f1=st.number_input("[sub] Focal length (m): ", value=10)*m
# f2=f1*f/(f1-f)
# frac=f/f1
# newsize=frac*size

# F_temp=Lens(f1,0,0,st.session_state["Fnear_rec"]);
# F_temp=LensFresnel(f2,f,F_temp);
# F_temp=Convert(F_temp);
