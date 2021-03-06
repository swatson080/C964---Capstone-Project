# Stephen Watson - C964 Capstone Project

# Import libraries
import tkinter
from tkinter import ttk, messagebox

import numpy as np
import math
import csv
from datetime import date
import pandas as pd
from matplotlib.backends._backend_tk import NavigationToolbar2Tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from tkinter import *
import matplotlib.pyplot as plt
from PIL import ImageTk, Image

# Function definitions
# Command function for the login button - checks entered username and password and unhides the main window if correct
def onClickLogin(username, password):
    if username == 'admin' and password == 'password1':
        writeLoginAttempt(username, password, 'SUCCESS')
        root.deiconify()
        loginWindow.destroy()
    else:
        writeLoginAttempt(username, password, 'FAILURE')
        messagebox.showerror(title='Error', message='Invalid username or password')

# Command function for the login cancel button - destroys the loginWindow and the root widget, then exits the program
def onClickCancel():
    if messagebox.askyesno('Quit', 'Are you sure you want to quit?'):
        loginWindow.destroy()
        root.destroy()
        quit()
    else:
        return

# Command function for the quit button in the main window
def onClickQuit():
    if messagebox.askyesno('Quit', 'Are you sure you want to quit?'):
        root.destroy()
        quit()
    else:
        return

# Draws a scatterplot
# Parameters: featureName indicates which feature is being used, r indicates the row to place the plot figure in
# frame indicates which frame object to place the plot in
def drawScatterPlot(featureName, r, frame):
    scatterPlotFig = Figure(figsize=(3, 2), tight_layout=True)
    scatterPlotCanvas = FigureCanvasTkAgg(scatterPlotFig, frame)
    ax = scatterPlotFig.add_subplot()
    scatterPlotCanvas.get_tk_widget().grid(row=r, column=0)
    ax.scatter(houseSaleData[featureName], houseSaleData['price'], alpha=0.2)
    if featureName == 'bedrooms' or featureName == 'bathrooms' or featureName == 'floors':
        ax.set_xlabel('Number of %s' % featureName)
    elif featureName == 'sqft_living':
        ax.set_xlabel('Sqare Ft Living Space')
    elif featureName == 'sqft_lot':
        ax.set_xlabel('Sqare Ft Lot Space')
    ax.set_ylabel('Price')

def onSelectCol1Combobox(event):
    if col1comboBox.get() == 'Bedrooms':
        drawScatterPlot('bedrooms', 1, frame0)
    elif col1comboBox.get() == 'Bathrooms':
        drawScatterPlot('bathrooms', 1, frame0)
    elif col1comboBox.get() == 'Floors':
        drawScatterPlot('floors', 1, frame0)
    elif col1comboBox.get() == 'Sq. ft. living':
        drawScatterPlot('sqft_living', 1, frame0)
    elif col1comboBox.get() == 'Sq. ft. lot':
        drawScatterPlot('sqft_lot', 1, frame0)
    return

# Clears all selection fields
def onClickClear():
    bedroomCombobox.set('')
    bathroomCombobox.set('')
    floorCombobox.set('')
    conditionCombobox.set('')
    waterfrontCombobox.set('')
    yrBuiltCombobox.set('')
    yrRenovatedCombobox.set('')
    sqFtLivingTextbox.delete(0, 'end')
    sqFtLotTextbox.delete(0, 'end')
    predictionTextbox.config(state='normal')
    predictionTextbox.delete(0, 'end')
    predictionTextbox.config(state='readonly')

# Appends to the errorLog.txt file
# error: the error message generated by the application
# inp: the input that triggered the error message
def writeErrorLog(error, inp):
    with open('errorLog.txt', 'a') as errorLog:
        logData = str(date.today()) + ': Error: \'' + error + '\' Input: \'' + inp + '\' End Input\n'
        errorLog.write(logData)
    errorLog.close()

# Appends to the loginAttempts.txt file
# username: the username that was used in the login attempt
# password: the password the was used in the login attempt
# result: one of 'SUCCESS' or 'FAILURE'
def writeLoginAttempt(username, password, result):
    with open('loginAttempts.txt', 'a') as loginAttempts:
        logData = str(date.today()) + ': Username: \'' + username + '\' Password: \'' + password + '\' Result: ' + result + '\n'
        loginAttempts.write(logData)
    loginAttempts.close()

# Appends to the errorLog.txt file
# error: the error message generated by the application
# yrBuilt, yrRenovated: the input pair that triggered the error message
def writeErrorLogYear(error, yrBuilt, yrRenovated):
    with open('errorLog.txt', 'a') as errorLog:
        logData = str(date.today()) + ': Error: \'' + error + '\' Year Built Input: \'' + yrBuilt + '\' Year Renovated Input: \'' + yrRenovated + '\' End Input\n'
        errorLog.write(logData)
    errorLog.close()

def verifyEntry():
    if bedroomCombobox.get() == '':
        writeErrorLog('Missing value for bedroom', bedroomCombobox.get())
        messagebox.showerror('Error', 'Missing value for bedroom')
        return False
    elif bathroomCombobox.get() == '':
        writeErrorLog('Missing value for bathroom', bathroomCombobox.get())
        messagebox.showerror('Error', 'Missing value for bathroom')
        return False
    elif floorCombobox.get() == '':
        writeErrorLog('Missing value for floors', floorCombobox.get())
        messagebox.showerror('Error', 'Missing value for floors')
        return False
    elif conditionCombobox.get() == '':
        writeErrorLog('Missing value for condition', conditionCombobox.get())
        messagebox.showerror('Error', 'Missing value for condition')
        return False
    elif waterfrontCombobox.get() == '':
        writeErrorLog('Missing value for waterfront', waterfrontCombobox.get())
        messagebox.showerror('Error', 'Missing value for waterfront')
        print('Waterfront bad')
        return False
    elif yrBuiltCombobox.get() == '':
        writeErrorLog('Missing value for year built', yrBuiltCombobox.get())
        messagebox.showerror('Error', 'Missing value for year built')
        return False
    elif yrRenovatedCombobox.get() == '':
        writeErrorLog('Missing value for year renovated', yrRenovatedCombobox.get())
        messagebox.showerror('Error', 'Missing value for year renovated')
        return False
    elif yrRenovatedCombobox.get() <= yrBuiltCombobox.get():
        writeErrorLogYear('Year renovated should be later than year built', yrBuiltCombobox.get(), yrRenovatedCombobox.get())
        messagebox.showerror('Error', 'Year renovated should be later than year built')
        return False
    elif sqFtLivingTextbox.get() == '' or not sqFtLivingTextbox.get().isnumeric():
        if sqFtLivingTextbox.get() == '':
            writeErrorLog('Missing value for square feet of living space', sqFtLivingTextbox.get())
            messagebox.showerror('Error', 'Missing value for square feet of living space')
        elif not sqFtLivingTextbox.get().isnumeric():
            writeErrorLog('Square foot living space should be numeric (no commas)', sqFtLivingTextbox.get())
            messagebox.showerror('Error', 'Square foot living space should be numeric (no commas)')
        return False
    elif sqFtLotTextbox.get() == '' or not sqFtLotTextbox.get().isdecimal():
        if sqFtLotTextbox.get() == '':
            writeErrorLog('Missing value for square feet of lot space', sqFtLotTextbox.get())
            messagebox.showerror('Error', 'Missing value for square feet of lot space')
        elif not sqFtLotTextbox.get().isdecimal():
            writeErrorLog('Square foot lot space should be numeric (no commas)', sqFtLotTextbox.get())
            messagebox.showerror('Error', 'Square foot lot space should be numeric (no commas)')
        return False
    else:
        return True

# Generates a predicted house price
def onClickPredict():
    # First we need to verify the data
    if verifyEntry():
        if waterfrontCombobox.get() == 'Yes':
            waterFront = 1
        else:
            waterFront = 0
        if yrRenovatedCombobox.get() == 'N/A':
            yrRenovated = 0
        else:
            yrRenovated = yrRenovatedCombobox.get()
        # Assign each feature with its respective value
        predictionData = {'bedrooms': [bedroomCombobox.get()], 'bathrooms': [bathroomCombobox.get()],
                          'sqft_living': [sqFtLivingTextbox.get()], 'sqft_lot': [sqFtLotTextbox.get()],
                          'floors': [floorCombobox.get()],'waterfront': [waterFront],
                          'condition': [conditionCombobox.get()], 'yr_built': [yrBuiltCombobox.get()],
                          'yr_renovated': [yrRenovated]}

        # Generate a data frame object to use in prediction
        predictionDf = pd.DataFrame(predictionData)

        # Get the predicted price of the house
        predictedPrice = mlModel.predict(predictionDf)[0]

        predictionTextbox.config(state='normal')
        predictionTextbox.delete(0, 'end')
        predictionTextbox.insert(0, '{:,.0f}'.format(predictedPrice))
        predictionTextbox.config(state='readonly')

# Testing pandas and sklearn

# Read in the csv file
houseSaleData = pd.read_csv("kc_house_data_cleaned_final_feature_set.csv")
# Mark the first row as the header
houseSaleData.head()

# Below line prints the csv data that was just read in
#print(houseSaleData)
salePrice = houseSaleData.price

inputVector = houseSaleData.drop(['price'], axis = 1)
inputVectorTrain, inputVectorTest, salePriceTrain, salePriceTest = train_test_split(inputVector, salePrice, test_size=0.20)

# Create the linear regression model
mlModel = LinearRegression()

mlModel.fit(inputVectorTrain, salePriceTrain)

salePricePrediction = mlModel.predict(inputVectorTest)

# Assign each feature with its respective value
#data = {'bedrooms' : [3], 'bathrooms' : [2.5], 'sqft_living' : [1780], 'sqft_lot' : [16532], 'floors' : [2], 'waterfront' : [0], 'view' : [0], 'condition' : [3], 'grade' : [7], 'sqft_above' : [1780], 'sqft_basement' : [0], 'yr_built' : [1993], 'yr_renovated' : [0], 'sqft_living15' : [1600], 'sqft_lot15' : [5000]}
data = {'bedrooms' : [3], 'bathrooms' : [1], 'sqft_living' : [1500], 'sqft_lot' : [10000], 'floors' : [1], 'waterfront' : [0], 'condition' : [3], 'yr_built' : [1965], 'yr_renovated' : [2012]}

# Generate a data frame object to use in prediction
test = pd.DataFrame(data)

#print(test.shape)
# Get the predicted price of the house
predictedPrice = mlModel.predict(test)[0]
adjustedPredictedPrice = predictedPrice * 1.159

# Print the predicted price of the house
#print('Predicted house price: {:,.2f}'.format((mlModel.predict(test)[0])))
print('Predicted house price: {:,.2f}'.format(predictedPrice))
print('Predicted house price adjusted for inflation: {:,.2f}'.format(adjustedPredictedPrice))

# Print data regarding the generated model
print('Coefficients: ', mlModel.coef_)
print(mlModel.feature_names_in_)
print('Intercept: ', mlModel.intercept_)
print('Mean squared error (MSE): %.2f' % mean_squared_error(salePriceTest, salePricePrediction))
print('Root mean squared error (RMSE): %.2f' % math.sqrt(mean_squared_error(salePriceTest, salePricePrediction)))
print('Coefficient of determination (R^2): %.2f' % r2_score(salePriceTest, salePricePrediction))

# Build GUI - login screen and main screen
root = Tk()
root.title('House Price Predictor')

loginWindow = Toplevel()
loginWindow.geometry('220x100')
loginWindow.title('House Price Predictor')

usernameLabel = Label(loginWindow, text='Username: ').grid(row=0, column=0, pady=5, sticky='W')
usernameEntry = Entry(loginWindow)
usernameEntry.grid(row=0, column=1)
passwordLabel = Label(loginWindow, text='Password: ').grid(row=1, column=0, pady=5, sticky='W')
passwordEntry = Entry(loginWindow, show='*')
passwordEntry.grid(row=1, column=1)
loginButton = Button(loginWindow, text='Login', command=lambda:onClickLogin(usernameEntry.get(), passwordEntry.get())).grid(row=2,column=0, padx=20)
cancelButton = Button(loginWindow, text='Cancel', command=lambda: onClickCancel())
cancelButton.grid(row=2, column=1, padx=10)

# Bind the onClickLogin method to the Enter key
loginWindow.bind('<Return>', lambda event: onClickLogin(usernameEntry.get(), passwordEntry.get()))

# frame0 contains plots and graphics for the main window
frame0 = Frame(root, bd=3, bg='white')
# Frame 1 contains the house feature combobox widgets
frame1 = Frame(root, bd=3)

# Put plots in frame0
histogramFig = Figure(figsize=(3, 2), tight_layout=True)
histogramCanvas = FigureCanvasTkAgg(histogramFig, frame0)
# NavigationToolbar2Tk(histogramCanvas, root)
axHistogram = histogramFig.add_subplot()
histogramCanvas.get_tk_widget().grid(row=0, column=0)
houseSaleData['price'].plot(kind='hist', legend=True, ax=axHistogram)
axHistogram.set_title('House Price Distribution')

drawScatterPlot('bedrooms', 1, frame0)

# Place label and combobox in frame0
scatterplotLabel = Label(frame0, bg='white', text='Choose a feature')

col1comboBox = ttk.Combobox(frame0, state='readonly')
col1comboBox['values'] = ('Bedrooms', 'Bathrooms', 'Floors', 'Sq. ft. living', 'Sq. ft. lot')
# Set value of the combo box to 'Bedrooms'
col1comboBox.current(0)
col1comboBox.bind('<<ComboboxSelected>>', onSelectCol1Combobox)

# Position the label and combobox in frame0
scatterplotLabel.grid(row=2, column=0)
col1comboBox.grid(row=3, column=0)

# Position elements in frame1

# Generate a range of years for use in the year built and year renovated comboboxes
yearRange = []
for i in reversed(range(1800, date.today().year + 1)):
    yearRange.append(i)

# Bedroom selection
bedroomLabel = Label(frame1, text='Bedrooms:', pady=10)
bedroomCombobox = ttk.Combobox(frame1, state='readonly')
bedroomCombobox['values'] = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
bedroomLabel.grid(row=0, column=0)
bedroomCombobox.grid(row=0, column=1)

# Bathroom selection
bathroomLabel = Label(frame1, text='Bathrooms:', pady=10)
bathroomCombobox = ttk.Combobox(frame1, state='readonly')
bathroomCombobox['values'] = (1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10, 10.5)
bathroomLabel.grid(row=1, column=0)
bathroomCombobox.grid(row=1, column=1)

# Floor selection
floorLabel = Label(frame1, text='Floors:', pady=10)
floorCombobox = ttk.Combobox(frame1, state='readonly')
floorCombobox['values'] = (1, 1.5, 2, 2.5, 3, 3.5)
floorLabel.grid(row=2, column=0)
floorCombobox.grid(row=2, column=1)

# Condition selection
conditionLabel = Label(frame1, text='Condition:', pady=10)
conditionNote = Label(frame1, text='(1: Worst - 3: Average - 5: Best)', padx=10)
conditionCombobox = ttk.Combobox(frame1, state='readonly')
conditionCombobox['values'] = (1, 2, 3, 4, 5)
conditionLabel.grid(row=3, column=0)
conditionCombobox.grid(row=3, column=1)
conditionNote.grid(row=3, column=2)

# Waterfront selection
waterfrontLabel = Label(frame1, text='Waterfront:', pady=10)
waterfrontCombobox = ttk.Combobox(frame1, state='readonly')
waterfrontCombobox['values'] = ('Yes', 'No')
waterfrontLabel.grid(row=4, column=0)
waterfrontCombobox.grid(row=4, column=1)

# Year built combobox
yrBuiltLabel = Label(frame1, text='Year built:', pady=10)
yrBuiltCombobox = ttk.Combobox(frame1, state='readonly')
yrBuiltCombobox['values'] = (yearRange)
yrBuiltLabel.grid(row=5, column=0)
yrBuiltCombobox.grid(row=5, column=1)

# Year renovated textbox
yrRenovatedLabel = Label(frame1, text='Year renovated:', pady=10)
yrRenovatedCombobox = ttk.Combobox(frame1, state='readonly')
# Add option to list to indicate house has never been renovated
yearRange.insert(0, 'N/A')
yrRenovatedCombobox['values'] = (yearRange)
yrRenovatedCombobox.grid(row=6, column=1)
yrRenovatedLabel.grid(row=6, column=0)

# Square foot living space textbox
sqFtLivingLabel = Label(frame1, text='Sq ft living space:', pady=10)
sqFtLivingTextbox = Entry(frame1)
sqFtLivingLabel.grid(row=7, column=0)
sqFtLivingTextbox.grid(row=7, column=1)

# Square foot lot space textbox
sqFtLotLabel = Label(frame1, text='Sq ft lot space:', pady=10)
sqFtLotTextbox = Entry(frame1)
sqFtLotLabel.grid(row=8, column=0)
sqFtLotTextbox.grid(row=8, column=1)

# Add clear button
clearButton = Button(frame1, text='Clear Selections', width=20, command=onClickClear)
clearButton.grid(row=9, column=0, pady=20, padx=20)

# Add get prediction button
predictButton = Button(frame1, text='Get Prediction', width=20, command=onClickPredict)
predictButton.grid(row=9, column=1, pady=20, padx=20)

# Add quit button
quitButton = Button(frame1, text='Quit', width=20, command=onClickQuit)
quitButton.grid(row=9,column=2,pady=20)

# Add prediction label and text box
predictionLabel = Label(frame1, text='Predicted Price:')
predictionTextbox = Entry(frame1, state='readonly')
predictionLabel.grid(row=10, column=0)
predictionTextbox.grid(row=10, column=1)

# Position the frames on the window
frame0.grid(row=0, column=0, rowspan=4, padx=5, pady=5)
frame1.grid(row=0, column=1, rowspan=2)

# Assign the protocol handler for the window managers - called when 'X' button is clicked
root.protocol('WM_DELETE_WINDOW', onClickQuit)
loginWindow.protocol('WM_DELETE_WINDOW', onClickCancel)
# Hide the main window until after successful login
root.withdraw()
# Display the window and run the app
root.mainloop()