#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 12:07:32 2024

@author: borfebor
"""

import streamlit as st

def pmol_from_mass(w, bp):
    """
    input
        w = weight of DNA in ng
        bp = base pairs of the fragment
    
    returns:
        pmol in given mass of DNA
    """
    return (w * 1000) / (bp * 650)

def mass_from_pmol(pmol, bp):
    """
    input
        pmol = pmol of X DNA fragment
        bp = base pairs of the fragment
    
    returns:
        weight of DNA in ng
    """
    return (pmol * (bp * 650)) / 1000

def dna_volume(c, w):
    """
    input
        c = DNA fragment concentration (ng/µL)
        w = used DNA mass for x amount

    returns:
        volume of DNA fragment to add
    """
    return w / c

def dilute_to_10(m, c):
    """
    input
        c = DNA fragment concentration (ng/µL)
        w = used DNA mass for x amount

    returns:
        volume of original PCR DNA to dilute in 10 µL water
    """
    return m*20/c

item = [(250, 5000),(400, 200), (200, 10500)]

st.header('George Cloning')
st.subheader('What else?')

n_fragments = st.slider('How many DNA fragments do you want to assembly?', 2, 6, 3)

c1, c2, c3= st.columns(3)

#item = list()
 
for c in range(n_fragments):
    name = f'fragment {c+1}'
    name_temp = c1.text_input('Fragment name', name)
    bp_temp = c2.number_input('Fragment lenght (bp)', 0, 30000, 100 + c)
    m_temp = c3.number_input('Fragment concentration (ng/µL)', 0, 4000, 50 + c)

    item.append((m_temp, bp_temp))
#st.text_input('Give me some names for the fragments')

if n_fragments < 4:
   min_pmol, max_pmol = 0.03, 0.2
else:
   min_pmol, max_pmol = 0.1, 0.2
    
min_vol, max_vol = 0.5, 2.5

st.subheader(f'Assembly with {n_fragments} fragments')

fragments_bp = [i[1] for i in item]
vector_length = max(fragments_bp)
vector_index = fragments_bp.index(vector_length)

st.write(f'Vector fragment is the fragment #{vector_index+1} ')

for n, f in enumerate(item):
    
    name = f'Fragment {n+1}'
    
    c, bp = f[0], f[1]
    
    if n == vector_index:
        ratio = 1
    elif bp > 250:
        ratio = 2
    else:
        ratio = 5

    pmol = 0.03*ratio
    
    m = mass_from_pmol(pmol, bp)
    µl = dna_volume(c, m)
    
    if µl > max_vol:
        st.write(f'Diluting {name}')
    
    if µl < min_vol:
        st.write(c, 'ng/µL, which we need', m, 'ng') 
        v = m*100/c
        water = 100 - v
        c = m
        st.markdown(f"""Prepare a dilution of Fragment {n} in another eppi:
        {water} µL of water
        {v} µL of Fragment {n+1} PCR DNA""")
        µl = dna_volume(c, m)
        name = f'Diluted {name}'
    
    st.write(f'Fragment {n+1}: add {m} ng ({pmol} pmol) = {µl} µl of {name}')
#def available_dna(c, )