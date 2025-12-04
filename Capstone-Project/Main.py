# Name : Khushbu Singh
# Roll No. : 2501730161
# Course : B Tech CSE(AI&ML)
# Section : B
# Assignment : 5
#=============================================================
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
#=============================================================
# TASK 1: DATA INGESTION & VALIDATION
# ============================================================

def load_energy_data(data_folder="data"):
    folder = Path(data_folder)
    all_files = list(folder.glob("*.csv"))

    if not all_files:
        raise ValueError(" No CSV files found in /data folder")

    df_list = []

    for file in all_files:
        try:
            df = pd.read_csv(file, on_bad_lines="skip")
            df["building"] = file.stem  # building name
            df["timestamp"] = pd.to_datetime(df["timestamp"])
            df_list.append(df)

        except Exception as e:
            print(f" Error reading {file}: {e}")

    df_final = pd.concat(df_list, ignore_index=True)
    return df_final


# ============================================================
# TASK 2: AGGREGATION LOGIC
# ============================================================

def calculate_daily_totals(df):
    df = df.set_index("timestamp")
    return df.resample("D")["kwh"].sum()


def calculate_weekly_totals(df):
    df = df.set_index("timestamp")
    return df.resample("W")["kwh"].sum()


def building_summary(df):
    return df.groupby("building")["kwh"].agg(["mean", "min", "max", "sum"])


# ============================================================
# TASK 3: OOP MODELING
# ============================================================

class MeterReading:
    def __init__(self, timestamp, kwh):
        self.timestamp = timestamp
        self.kwh = kwh


class Building:
    def __init__(self, name):
        self.name = name
        self.readings = []

    def add_reading(self, reading):
        self.readings.append(reading)

    def calculate_total_consumption(self):
        return sum(r.kwh for r in self.readings)

    def generate_report(self):
        return f"{self.name}: {self.calculate_total_consumption()} kWh"


class BuildingManager:
    def __init__(self):
        self.buildings = {}

    def add_reading(self, building_name, reading):
        if building_name not in self.buildings:
            self.buildings[building_name] = Building(building_name)
        self.buildings[building_name].add_reading(reading)

    def generate_reports(self):
        return [b.generate_report() for b in self.buildings.values()]


# ============================================================
# TASK 4: DASHBOARD VISUALIZATION
# ============================================================

def create_dashboard(df):
    df = df.copy()
    df["date"] = df["timestamp"].dt.date
    df["hour"] = df["timestamp"].dt.hour

    # Daily trend
    daily = df.groupby(["date", "building"])["kwh"].sum().reset_index()

    # Weekly average
    df["week"] = df["timestamp"].dt.isocalendar().week
    weekly = df.groupby("building")["kwh"].mean()

    plt.figure(figsize=(12, 15))

    # ----------------- Line Chart (Daily Trend) -----------------
    plt.subplot(3, 1, 1)
    for b in df["building"].unique():
        temp = daily[daily["building"] == b]
        plt.plot(temp["date"], temp["kwh"], label=b)

    plt.title("Daily Energy Consumption Trend")
    plt.xlabel("Date")
    plt.ylabel("kWh")
    plt.legend()

    # ----------------- Bar Chart (Weekly Usage) -----------------
    plt.subplot(3, 1, 2)
    plt.bar(weekly.index, weekly.values)
    plt.title("Average Weekly Consumption per Building")
    plt.ylabel("kWh")

    # ----------------- Scatter Plot (Peak-Hour) -----------------
    plt.subplot(3, 1, 3)
    plt.scatter(df["hour"], df["kwh"], alpha=0.6)
    plt.title("Hourly Peak Consumption")
    plt.xlabel("Hour of Day")
    plt.ylabel("kWh")

    plt.tight_layout()
    plt.savefig("dashboard.png")
    print(" Dashboard saved as dashboard.png")


# ============================================================
# TASK 5: EXPORT RESULTS
# ============================================================

def export_results(df, summary):
    df.to_csv("cleaned_energy_data.csv", index=False)
    summary.to_csv("building_summary.csv")

    # Campus total
    total = df["kwh"].sum()

    # Highest consuming building
    highest = summary["sum"].idxmax()

    # Peak load time
    peak_time = df.loc[df["kwh"].idxmax(), "timestamp"]

    # Make summary
    text = (
        f"Total Campus Consumption: {total} kWh\n"
        f"Highest Consuming Building: {highest}\n"
        f"Peak Load Time: {peak_time}\n"
    )

    with open("summary.txt", "w") as f:
        f.write(text)

    print(" Files saved: cleaned_energy_data.csv, building_summary.csv, summary.txt")


# ============================================================
# MAIN EXECUTION
# ============================================================

def main():
    print(" Loading data...")
    df = load_energy_data()

    print(" Calculating summaries...")
    daily = calculate_daily_totals(df)
    weekly = calculate_weekly_totals(df)
    summary = building_summary(df)

    print(" Running OOP model...")
    manager = BuildingManager()
    for _, row in df.iterrows():
        reading = MeterReading(row["timestamp"], row["kwh"])
        manager.add_reading(row["building"], reading)

    print(" OOP Reports:")
    for r in manager.generate_reports():
        print(" -", r)

    print(" Generating dashboard...")
    create_dashboard(df)

    print(" Exporting data and summary...")
    export_results(df, summary)

    print(" Done! Assignment successfully completed.")


if __name__ == "__main__":
    main()
