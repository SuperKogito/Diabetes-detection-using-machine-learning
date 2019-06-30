import math 
import warnings 
import numpy as np
import pandas as pd
from scipy import stats
from DfPlotter import DfPlotter
import matplotlib.pyplot as plt 
from MLapproaches import MLtests
from sklearn.preprocessing import MinMaxScaler  


# filter warnings
warnings.filterwarnings("ignore")

def set_up_matplotlib_style():
    plt.rcParams['axes.grid']       = True
    plt.rcParams['grid.color']      = 'w'
    plt.rcParams['grid.linestyle']  = '--'
    plt.rcParams['grid.linewidth']  = .2
    plt.rcParams['axes.edgecolor']  = 'white'
    plt.rcParams['axes.facecolor']  = '#1d1f21'
    plt.rcParams['axes.labelcolor'] = 'white'
    plt.rcParams['boxplot.meanprops.color']            = '#1d1f21'
    plt.rcParams['boxplot.capprops.color']             = '#1d1f21'
    plt.rcParams['boxplot.flierprops.markeredgecolor'] = '#1d1f21'
    plt.rcParams['boxplot.meanprops.markeredgecolor']  = '#1d1f21'
    plt.rcParams['boxplot.meanprops.markerfacecolor']  = '#1d1f21'
    plt.rcParams['boxplot.whiskerprops.color']         = '#1d1f21'
    plt.rcParams['figure.edgecolor']  = '#1d1f21'
    plt.rcParams['figure.facecolor']  = '#1d1f21'
    plt.rcParams['lines.color']       = '#1d1f21'
    plt.rcParams['patch.edgecolor']   = '#1d1f21'
    plt.rcParams['patch.facecolor']   = '#1d1f21'
    plt.rcParams['savefig.edgecolor'] = '#1d1f21'
    plt.rcParams['savefig.facecolor'] = '#1d1f21'
    plt.rcParams['text.color']        = 'white'
    plt.rcParams['xtick.color']       = 'white'
    plt.rcParams['ytick.color']       = 'white'


def average_list(numerical_list):
    numerical_list = [0 if math.isnan(x) else x for x in numerical_list]
    return sum(numerical_list) / len(numerical_list)

def test_trafos(raw_data):
    """
    Plots for data transformations effects
    """
    # raw data
    ml_tests   = MLtests()
    ml_tests.run(raw_data, "raw correct data")
    accuracies.append(average_list(ml_tests.accuracies.values()))
    sensitivity.append(average_list(ml_tests.sensitivities.values()))
    specificity.append(average_list(ml_tests.specificities.values()))
    
    # remove outliers and plot results
    data = remove_outliers(raw_data)
    ml_tests.run(data, "data without outliers")
    accuracies.append(average_list(ml_tests.accuracies.values()))
    sensitivity.append(average_list(ml_tests.sensitivities.values()))
    specificity.append(average_list(ml_tests.specificities.values()))
    
    # equalize data and plot results
    data = equalize_data(raw_data)
    ml_tests.run(data, "equilized data")
    accuracies.append(average_list(ml_tests.accuracies.values()))
    sensitivity.append(average_list(ml_tests.sensitivities.values()))
    specificity.append(average_list(ml_tests.specificities.values()))
    
    # scale data and plot results
    data = scale_data(raw_data)
    ml_tests.run(data, "scaled data")
    accuracies.append(average_list(ml_tests.accuracies.values()))
    sensitivity.append(average_list(ml_tests.sensitivities.values()))
    specificity.append(average_list(ml_tests.specificities.values()))
    
    # equalize data and plot results
    data = scale_data(raw_data)
    data = equalize_data(data)
    ml_tests.run(data, "scaled and equalized data")
    accuracies.append(average_list(ml_tests.accuracies.values()))
    sensitivity.append(average_list(ml_tests.sensitivities.values()))
    specificity.append(average_list(ml_tests.specificities.values()))

    # no outliers scale data and plot results
    data = remove_outliers(raw_data)
    data = scale_data(data)
    data = equalize_data(data)
    ml_tests.run(data, "scaled and equalized data without outliers")
    accuracies.append(average_list(ml_tests.accuracies.values()))
    sensitivity.append(average_list(ml_tests.sensitivities.values()))
    specificity.append(average_list(ml_tests.specificities.values()))
    
def drop_column_values(data, column_name, value):
    '''
    Delete certain dataframe rows based on the value of a certain column element 
    '''
    # Get names of indexes for which column Age has value 30
    indices = data[ data[column_name] == value ].index
    # Delete these row indexes from dataFrame
    data.drop(indices , inplace = True)

def equalize_data(data):
    '''
    Equilize the number of samples in each outcome class
    '''
    # equlize the number of samples as a function of outputs
    l0    = data[data["Outcome"] == 0 ].shape[0]
    l1    = data[data["Outcome"] == 1 ].shape[0]
    min_l = l0 * (l0 < l1) + l1 * (l0 > l1) 
    df    = data[data["Outcome"] == 1 ].iloc[:min_l,:]
    df    = df.append(data[data["Outcome"] == 0 ].iloc[:min_l,:])
    return df
  
def scale_data(data):
    scaler = MinMaxScaler(feature_range=(0, 1))
    data   = pd.DataFrame(scaler.fit_transform(data.values),  columns = column_names)
    return data

def remove_outliers(data):
    data['Insulin'] = data['Insulin'] * .001
    data            = data[(np.abs(stats.zscore(data)) < 3).all(axis=1)]
    return data

def plot_boxplots_after_transformations(data):
    # plot raw data
    fig = plt.figure(figsize = (20, 12))
    plt.subplots_adjust(left = 0.12, right = 0.95, bottom = 0.05, top = 0.95, 
                        wspace = 0.35, hspace = 0.25)
    plt.subplot(2, 2, 1)
    plt.title('Raw correct data')
    data.boxplot(vert = False, labels = column_names, patch_artist = True)
    
    # remove outliers and plot results
    plt.subplot(2, 2, 2)
    plt.title('Data without outliers')
    data = remove_outliers(data)
    data.boxplot(vert = False, labels = column_names, patch_artist = True)
    
    # scale data and plot results
    plt.subplot(2 , 2, 3)
    plt.title('Scaled Data')
    data = scale_data(data)
    data.boxplot(vert = False, labels = column_names, patch_artist = True)
    
    # equilize data and plot results
    plt.subplot(2, 2, 4)
    plt.title('Equilized Data')
    data = equalize_data(data)
    data.boxplot(vert = False, labels = column_names, patch_artist = True)
    plt.show()
    
    # save fig
    fig.savefig('data_manipulations.png')
    return data

def metrics_line_plots(accuracies, specificity, sensitivity):
    fig2 = plt.figure(figsize = (15, 8))
    plt.subplots_adjust(left = 0.05, right = 0.95, bottom = 0.1, top = 0.95,
                        wspace = 0.25, hspace = 0.5)
    plt.plot(range(len(accuracies)), accuracies, marker='o', linestyle='dashed', label="Accuracies")
    plt.plot(range(len(sensitivity)), sensitivity, color= "magenta", marker='o', linestyle='dashed', label="Sensitivity")
    plt.plot(range(len(specificity)), specificity, 'green', marker='o', linestyle='dashed', label="Specificities" )
    
    plt.xticks(range(len(specificity)), x_labels)
    plt.ylim(.5,1)
    plt.yticks([i/100 for i in range(50, 101, 5)])
    plt.legend()
    plt.show()
    fig2.savefig('dataTrafos.png')
    
    
# Uncomment if needed: set_up_matplotlib_style()
# define column names
column_names = ["Pregnancies",                "Glucose", "Blood_pressure", 
                "Skin_thickness",             "Insulin", "Bmi",
                "Diabetes_Pedigree_Function", "Age",     "Outcome"]

# define plotter and tester
df_plotter = DfPlotter(column_names)
ml_tests   = MLtests()

# load data 
data = pd.read_csv('diabetes.csv', names = column_names)

# drop erroneous rows
for cname in ['Glucose', 'Blood_pressure', 'Skin_thickness', 'Insulin', 'Bmi']:
    drop_column_values(data, cname, 0)

accuracies, sensitivity, specificity = [], [], []
x_labels = ["Raw correct data", "data without outliers", "equilized data",
            "scaled data", "scaled and equalized data",
            "scaled and equalized data \n without outliers"]

# test tranformations
test_trafos(data)
metrics_line_plots(accuracies, specificity, sensitivity)

# no outliers scale data and plot results
data = remove_outliers(data)
data = scale_data(data)
data = equalize_data(data)

# plot correlation & densities
df_plotter.plot_overview(data)
df_plotter.plot_correlation(data)
df_plotter.plot_pairplot(data)
df_plotter.plot_bars(data)

# classifiers performances
ml_tests.run(data, "scaled and equalized data without outliers")