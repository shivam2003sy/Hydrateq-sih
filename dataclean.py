import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use('AGG')
import matplotlib
from scipy.cluster import hierarchy
import seaborn as sns


# Load data
def cleandata(raw_df):
    # Clustring data
    pars = ['ID', 'ShortID', 'SY', 'SM', 'TDS', 'pH', 'Ca', 'Mg', 'K', 'Na', 'KNa', 'Cl','SO4','HCO3', 'NO3', 'F']
    df = raw_df[pars].copy()
    # Check the charge balance error (CBE) 
    Ca   = 40
    Mg   = 24
    K    = 39
    Na   = 23
    Cl   = 35.5
    SO4  = 96
    HCO3 = 61
    NO3  = 62
    F    = 19
    CBE_cations = df['Ca'] * 2 / Ca + df['Mg'] * 2 / Mg + df['K'] * 1 / K + df['Na'] * 1 / Na

    CBE_anions= df['Cl'] * 1 / Cl + df['SO4'] * 2 / SO4 + df['HCO3'] * 1/ HCO3 + df['NO3'] * 1 / NO3 + df['F'] * 1 / 19

    CBE = abs((CBE_cations - CBE_anions) / (CBE_cations + CBE_anions)) * 100

    # print('--> Number of samples with CBE greater than 10% =', sum(CBE>=10))
    df['CBE'] = CBE

    df.loc[CBE>=10, ['ID', 'ShortID', 'SY', 'SM', 'CBE']]
    # Remove samples with CBE greater than 10%
    tmp_df = df[(df['CBE']<=10) | (df['CBE'].isnull())][['ID', 'ShortID', 'SY', 'SM', 'pH', 'Ca', 'Mg', 'KNa', 'Cl','SO4','HCO3', 'NO3', 'F', 'TDS']].dropna(axis=0, how='any')
    # The number of the remaining samples
    # print('Number of samples: ', tmp_df.shape[0])

    X_df = np.log(tmp_df[['pH', 'Ca', 'Mg', 'KNa', 'Cl','SO4','HCO3', 'NO3', 'F']])


    # Standardization 
    X = X_df.values
    rescaledX = StandardScaler().fit_transform(X)
    descriptive =tmp_df[['pH', 'Ca', 'Mg', 'KNa', 'Cl','SO4','HCO3', 'NO3', 'F', 'TDS']].describe()
    # descriptive.to_csv(r'C:\Users\shiva\OneDrive\Desktop\Hydrateq-backend\descriptivestatistics\file'+project_id+'.csv', index=False)
    Y_df = tmp_df[['ID', 'ShortID', 'SY', 'SM', 'pH', 'Ca', 'Mg', 'KNa', 'Cl','SO4','HCO3', 'NO3', 'F', 'TDS']]
    # print(tmp_df.nunique())
    
    sns.heatmap(descriptive.corr(), annot= True, cmap='coolwarm')
    # plt.show()
    plt.savefig("dataclean.jpg", format='jpg' ,
                bbox_inches='tight', dpi=300)
    plt.clf()
    return (descriptive ,Y_df,rescaledX)
def clustering(raw_df):
    (descriptive,Y_df,rescaledX) = cleandata(raw_df)
    n_samples, n_parameters = rescaledX.shape
    matplotlib.rcParams['lines.linewidth'] = 1.25
    Z = hierarchy.linkage(rescaledX, method='ward', metric='euclidean')

    # Set the location of phenon line
    max_d = 20

    # Figure settings of the dendrogram
    fig = plt.figure(figsize=(10, 8))

    # Axis settings
    left, bottom, width, height = 0.1, 0.35, 0.8, 0.35
    ax1 = fig.add_axes([left, bottom, width, height])

    # Customize the colors of the nine clusters
    colors=['#BA2F29', '#E9C832', '#8EBA42', '#67ACE6']
    hierarchy.set_link_color_palette(colors)

    # Plot the dendrogram
    hierarchy.dendrogram(Z, leaf_rotation=90, leaf_font_size=0, 
                        color_threshold=max_d, above_threshold_color='grey')
    hierarchy.set_link_color_palette(None)
    ax1.axhline(y=max_d, linestyle='-.', color='k', lw=1.25) 
    ax1.set_ylabel('Linkage distance', fontsize=13)
    ax1.set_yticklabels([0, 5, 10, 15, 20, 25, 30, 35], fontsize=10)
    ax1.set_xticks([])
    ax1.spines['top'].set_linewidth(1.25)
    ax1.spines['bottom'].set_linewidth(1.25)
    ax1.spines['left'].set_linewidth(1.25)
    ax1.spines['right'].set_linewidth(1.25)
    ax1.text(150, 20.5, '$Phenon$' + ' ' + '$Line$', fontsize=12)


    # Calculate number of clusters under the linkage distance of max_d
    n_clusters = np.max(np.unique(hierarchy.fcluster(Z, max_d, criterion='distance')))


    # Calculate the number of samples for each cluster
    cluster_size = [np.sum(hierarchy.fcluster(Z, max_d, criterion='distance')==i + 1) for i in range(n_clusters)]

    # The bottom figure showing the cluster names
    left, bottom, width, height = 0.1, 0.15, 0.8, 0.2
    ax2 = fig.add_axes([left, bottom, width, height])
    ax2.set_xlim(0, n_samples * 10)
    ax2.set_ylim(0, 2)

    # Dot line to split each cluster 
    cum_cluster_szie = np.cumsum(cluster_size) * 10
    for i in range(n_clusters - 1):
        ax2.plot([cum_cluster_szie[i], cum_cluster_szie[i]], [1.5, 2.0], linestyle='--', color='k', lw=1.5) 

        ax2.set_xticks([])
        ax2.set_yticks([])
            
        ax2.spines['top'].set_color('none')
        ax2.spines['bottom'].set_color('none')
        ax2.spines['left'].set_color('none')
        ax2.spines['right'].set_color('none')

        ax2.text(0                   + (cum_cluster_szie[0] -                   0) / 2, 1.5, 'C1 \nN=%d' %cluster_size[0], ha='center', va='bottom', fontsize=12)
        ax2.text(cum_cluster_szie[0] + (cum_cluster_szie[1] - cum_cluster_szie[0]) / 2, 1.5, 'C2 \nN=%d' %cluster_size[1], ha='center', va='bottom', fontsize=12)
        ax2.text(cum_cluster_szie[1] + (cum_cluster_szie[2] - cum_cluster_szie[1]) / 2, 1.5, 'C3 \nN=%d' %cluster_size[2], ha='center', va='bottom', fontsize=12)
        ax2.text(cum_cluster_szie[2] + (cum_cluster_szie[3] - cum_cluster_szie[2]) / 2, 1.5, 'C4 \nN=%d' %cluster_size[3], ha='center', va='bottom', fontsize=12)
    plt.savefig("clustring.jpg", format='jpg' ,
                    bbox_inches='tight', dpi=300)
    plt.clf()
        
    # plt.show()
    Y_df['SCI'] = hierarchy.fcluster(Z, max_d, criterion='distance')
    
    # print('Number of clusters:', n_clusters)
    # print('Samples in each cluster:', cluster_size)
    # print('Total samples:', np.sum(cluster_size))
    cluster_ids = Y_df['SCI'].values
    format_df = pd.DataFrame()
    format_df['Sample'] = Y_df['ShortID'].map(str) + '_' + Y_df['SY'].map(str) + '_'  + Y_df['SM'].map(str)
    format_df['Label'] = 'C' + Y_df['SCI'].map(str)

    format_df.loc[format_df['Label']=='C1', 'Color'] = '#BA2F29'
    format_df.loc[format_df['Label']=='C2', 'Color'] = '#E9C832'
    format_df.loc[format_df['Label']=='C3', 'Color'] = '#89C667'
    format_df.loc[format_df['Label']=='C4', 'Color'] = '#67ACE6'
    format_df['Marker'] = 'o'
    format_df['Size'] = 20
    format_df['Alpha'] = 0.6
    format_df['pH'] = Y_df['pH']
    format_df['Ca'] = Y_df['Ca']
    format_df['Mg'] = Y_df['Mg']
    # Since ther are missing values of K concentration,
    # we use KNa concentration represent Na and set K concentration to 0
    format_df['Na'] = Y_df['KNa']              
    format_df['K'] = 0
    format_df['HCO3'] = Y_df['HCO3']
    format_df['CO3'] = 0
    format_df['Cl'] = Y_df['Cl']
    format_df['SO4'] = Y_df['SO4']
    format_df['TDS'] = Y_df['TDS']
    # Reset the index
    format_df.reset_index(inplace=True, drop=True)
    format_df.to_csv('sample.csv')
    return (format_df)
# url ="https://raw.githubusercontent.com/jyangfsu/WQChartPy/main/data/data_Liu_et_al_2021.csv"
# raw_df = pd.read_csv(url)
# # print(cleandata(raw_df))
# print(clustering(raw_df))
