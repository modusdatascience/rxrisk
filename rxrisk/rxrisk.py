import pandas as pd 
import os
from clinvoc.ndc import NDC
from modulecache.invalidators import FileChangeInvalidator
from modulecache.backends import PickleBackend
from clinvoc.code_collections import CodeCollection
from .resources import resources


'''
TODO: use weights in riskrx_mappings somehow 
'''

vocab = NDC()

# create ndc to atc mappings 
def _map_ndc_to_atc():

    ndc_to_atc = {}
    ndc_atc_df = pd.read_csv(os.path.join(resources, "ndc_atc4_mapping_raw.csv"))
    
    for _, row in ndc_atc_df.iterrows():
        # standardizes, but do we need some error catching? 
        ndc = vocab.standardize(row['NDC'])
        atc = row['ATC4']
        ndc_to_atc[ndc] = atc
            
    return ndc_to_atc
        

# create atc to category mappings 
def _atc_to_cat(values):
    atc_to_rxrisk = pd.read_csv(os.path.join(resources, "rxriskv_mappings.csv"))
    atc_to_cat = {}
    
    for _, row in atc_to_rxrisk.iterrows():
        print(row)
        subgroups = row['Subgroups'].split(',')
        for subgroup in subgroups: 
            atc_to_cat[subgroup] = row['Category']
    
    return atc_to_cat

# connect ndcs to categories
def _ndc_to_risk_categories(values, mappings):
    ndc_cat = {}
    for ndc in values: 
        if values[ndc] in mappings.keys(): 
            cat = mappings[values[ndc]]
            if cat in ndc_cat: 
                ndc_cat[cat].add(ndc)
            else:
                ndc_cat[cat] = set([ndc])
    
    risk_categories = {}
    for cat, c_arr in ndc_cat.items(): 
        risk_categories[(cat, vocab.vocab_domain, vocab.vocab_name)] = c_arr
        
    return risk_categories
            
        
def _construct_ndc_cat():    
    values = _map_ndc_to_atc()
    mappings = _atc_to_cat(values)
    risk_categories = _ndc_to_risk_categories(values, mappings)
    return risk_categories


cache_filename = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'ndc_cat_cache.pkl')
suppress = globals().keys()
with PickleBackend(cache_filename, suppress) as cache, FileChangeInvalidator(cache, os.path.abspath(__file__)):
    code_set = CodeCollection(*_construct_ndc_cat().items(), name='rxrisk')
