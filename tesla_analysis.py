import yfinance as yf #this library pulls data from yahoo finance
import pandas as pd #this allows python to manipulate csv data
import matplotlib.pyplot as plt #this function allows python to make charts

#downloads teslas historical stock data for one year.
tesla = yf.download( #uses yfinance to download historical data. 
    "TSLA",
    start="2025-09-18",
    end="2026-09-18",
    auto_adjust=False #controls whether yfinance adjusts historical prices
    #for stuff like stock splits and dividends. it will be false because
    #we can work with regular columns rather than automatically adjusted ones

)

print(tesla.head()) #head means show me the first 5 rows


###1.start of tesla closing price graph###
plt.figure(figsize=(12, 6)) #figsize controls dimensions so 12 in wide and
#6 in tall

plt.plot(tesla.index, tesla["Close"]) #plot creates the line graph. the
#index is the dates and the tesla["Close"] is tesla closing prices

plt.title("Tesla (TSLA) Daily Closing Price - One Year") #adds a title
plt.xlabel("Date") #adds x axis label
plt.ylabel("Closing Price ($)") #adds y axis label

plt.grid(True) #adds grid lines to the graph
plt.tight_layout() #automatically adjusts spacing around the graph

plt.show() #shows the graph

print("Number of observations:", len(tesla))
###end of closing price graph###


close = tesla["Close"]["TSLA"] #takes teslas close column and puts it in new var
volume = tesla["Volume"]["TSLA"]


###2.start of trade volume graph###
plt.figure(figsize=(12, 6))

plt.plot(volume.index, volume)

plt.title("Tesla (TSLA) Daily Trading Volume - One Year")
plt.xlabel("Date")
plt.ylabel("Trading Volume")
plt.grid(True)
plt.tight_layout()
plt.show()

volume_data = pd.DataFrame({ #creates a dataframe or table with two 
    #columns: close and volume
    "Close": close,
    "Volume": volume
})

highest_volume = volume_data.nlargest(10, "Volume")

print("\nHighest trading volume days:")
print(highest_volume)

average_volume = volume.mean()

print("\nAverage daily trading volume:")
print(average_volume)

volume_data["Daily Change"] = close.diff() #calculates the difference
#between today and yesterday's closing price
volume_data["Daily Return"] = close.pct_change() * 100 #calculates the %
#change from one day to the next. 

print("\nHighest volume days with price movements:")
print( #this combines volume and price movement
    volume_data.nlargest(10, "Volume")[
        ["Close", "Volume", "Daily Change", "Daily Return"]
    ] #find the 10 highest days for the columns we care about
)
###end of trade volume graph###


###3.start of moving average graph###
tesla["30-Day MA"] = close.rolling(window=30).mean()
tesla["50-Day MA"] = close.rolling(window=50).mean()
#take the closing price for the most recent 30 or 50 days and calculate
#their average. Then, python drops the oldest day and adds the newest day.
#this creates the moving average.

plt.figure(figsize=(12, 6))

plt.plot(close.index, close, label="Tesla Closing Price")
plt.plot(tesla.index, tesla["30-Day MA"], label="30-Day Moving Average")
plt.plot(tesla.index, tesla["50-Day MA"], label="50-Day Moving Average")

plt.title("Tesla (TSLA) Closing Price with 30-Day and 50-Day Moving Averages")
plt.xlabel("Date")
plt.ylabel("Price ($)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()


# these print statements perform functions on the close function
print("Number of observations:", len(close))
print("Mean:", close.mean())
print("Median:", close.median())
print("Standard deviation:", close.std())
print("Minimum:", close.min())
print("Maximum:", close.max())

minimum_date = close.idxmin() #find the index of the lowest price, the index
#is the date. then set it to minimum date
maximum_date = close.idxmax() #find the index of the highest price, then
#set it to the maximum price

print("Minimum closing price:")
print(minimum_date, close.min())

print("Maximum closing price:")
print(maximum_date, close.max())

tesla["Daily Change"] = close.diff() #calculates the difference between
#each row and the previous row.

largest_increase = tesla["Daily Change"].idxmax() #looks at the daily change
#and see the index of the maximum value, so it stores the date and sets it
#to the largest_increase
largest_decrease = tesla["Daily Change"].idxmin() #looks at the daily change
#and sees the index of the smallest value and stores the date and sets 

print("Largest daily increase:")
print(largest_increase, tesla.loc[largest_increase, "Daily Change"])
#.loc finds a specific row/column from my dataframe. go to the row represe
#nted by largest_increase, and give value from the daily_change column

print("Largest daily decrease:")
print(largest_decrease, tesla.loc[largest_decrease, "Daily Change"])
#go to row represented by smallest_increase and give value from daily_change

tesla["Daily Return"] = close.pct_change() * 100 #calculate the % change
#from yesterday to previous day and converts it to a whole #.

biggest_gain = tesla["Daily Return"].idxmax() #stores biggest gain
biggest_loss = tesla["Daily Return"].idxmin() #stores biggest loss

print("Largest percentage increase:")
print(biggest_gain, tesla.loc[biggest_gain, "Daily Return"], "%")
#.loc finds the specific cell with the biggest gain

print("Largest percentage decrease:")
print(biggest_loss, tesla.loc[biggest_loss, "Daily Return"], "%")
#finds the specific cell with the biggest loss

print("\nHighest trading volume days:")

print(
    pd.DataFrame({
        "Close": close,
        "Volume": volume
    }).nlargest(10,"Volume")
    #give me the close and volume of the 10 largest rows
)