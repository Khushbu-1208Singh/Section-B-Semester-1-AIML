# Name - Khushbu Singh
# Class - Btech cse (AI&ML)
# Section - B
#Roll no. - 2501730161
#--------------------------------------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv("weather.csv")
print("CSV loaded successfully!\n")

print("Available columns:", df.columns.tolist())

# ---- MAP MY ACTUAL COLUMNS ----
date_col = "Date"
temp_col = "Temp3pm"       # used Temp3pm as main temperature
rain_col = "Rainfall"
hum_col  = "Humidity3pm"   # used Humidity3pm as main humidity

# Rename columns to standard names
df = df.rename(columns={
    date_col: "date",
    temp_col: "temperature",
    rain_col: "rainfall",
    hum_col: "humidity"
})

# Keep only the needed columns
df = df[["date", "temperature", "rainfall", "humidity"]]

# Clean data
df['date'] = pd.to_datetime(df['date'], errors='coerce')
df = df.dropna(subset=["date"])

df['temperature'] = pd.to_numeric(df['temperature'], errors='coerce').fillna(df['temperature'].mean())
df['rainfall'] = pd.to_numeric(df['rainfall'], errors='coerce').fillna(0)
df['humidity'] = pd.to_numeric(df['humidity'], errors='coerce').fillna(df['humidity'].median())

df['month'] = df['date'].dt.month

print("\nCleaned Data Preview:")
print(df.head())

# ---- STATISTICS ----
temps = df['temperature']

print("\n--- Temperature Stats ---")
print("Mean:", temps.mean())
print("Min:", temps.min())
print("Max:", temps.max())
print("Std:", temps.std())

# ---- PLOTS ----
plt.figure(figsize=(10,4))
plt.plot(df['date'], df['temperature'])
plt.title("Daily Temperature Trend")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.grid()
plt.savefig("daily_temperature.png")
plt.close()

monthly_rain = df.groupby('month')['rainfall'].sum()

plt.figure(figsize=(8,4))
plt.bar(monthly_rain.index, monthly_rain.values)
plt.title("Monthly Rainfall")
plt.xlabel("Month")
plt.ylabel("Rainfall")
plt.savefig("monthly_rainfall.png")
plt.close()

plt.figure(figsize=(6,4))
plt.scatter(df['temperature'], df['humidity'])
plt.title("Temperature vs Humidity")
plt.xlabel("Temperature (°C)")
plt.ylabel("Humidity (%)")
plt.savefig("humidity_vs_temp.png")
plt.close()

print("\nPlots saved successfully!")

# ---- EXPORT CLEAN DATA ----
df.to_csv("cleaned_weather.csv", index=False)
print("Cleaned CSV exported.")

# ---- EXPORT SUMMARY REPORT ----
with open("summary_report.txt", "w") as f:
    f.write("WEATHER SUMMARY REPORT\n\n")
    f.write(f"Mean Temperature: {temps.mean()}\n")
    f.write(f"Max Temperature: {temps.max()}\n")
    f.write(f"Min Temperature: {temps.min()}\n")
    f.write(f"Std Dev: {temps.std()}\n")
    f.write("\nMonthly Rainfall:\n")
    f.write(str(monthly_rain))

print("Summary report created successfully!")
