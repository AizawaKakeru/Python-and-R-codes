import pandas as pd 
import numpy as np 
from bioinfokit import analys,visuz
data = pd.read_csv('merged_result_2.csv',usecols=['PVALUE_EPACTS','#CHROM'])
data1 = data['PVALUE_EPACTS']
#print(data1)
data3 = data.dropna(subset=['PVALUE_EPACTS'])
print(data3)
visuz.marker.mhat(df=data3, chr='#CHROM',pv='PVALUE_EPACTS',gwasp=5E-08,gwas_sign_line=True,markeridcol='MARKER',r=6000, figname='/gpfs/data/user/aditya/PED_files/VCF_chunk/output2/epacts/CRP/PCA/epacts_files/CRP_PCA_Manhattan_plot_epacts')

