import tkinter as tk
from tkinter import ttk
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone

def fetch_data():
    url = "https://www.hamqsl.com/solarxml.php"
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "xml")
        update_time = soup.find("updated").text
        updated_label.config(text="Last Updated: " + update_time)

        # Fetch A index, K index, and solar flux
        solar_flux = soup.find("solarflux").text
        a_index = soup.find("aindex").text.strip()
        k_index = soup.find("kindex").text.strip()

        # Update the respective labels
        solar_flux_label.config(text="Solar Flux: " + solar_flux)
        a_index_label.config(text="A Index: " + a_index)
        k_index_label.config(text="K Index: " + k_index)

        hf_conditions = soup.find("calculatedconditions")
        for band_condition in hf_conditions.find_all("band"):
            band_name = band_condition["name"]
            time = band_condition["time"]
            condition = band_condition.text
            
            # Check if condition contains the word "Poor", change text color to red
            if "Poor" in condition:
                color = "red"
            else:
                color = "green"

            if time == "day":
                day_conditions[band_name].config(text=band_name + " day = " + condition, fg=color)
            else:
                night_conditions[band_name].config(text=band_name + " night = " + condition, fg=color)
    
    # Schedule the fetch_data function to be called again after 10 minutes (600,000 milliseconds)
    root.after(600000, fetch_data)

def update_time_clocks():
    # Get current GMT time
    gmt_time = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")

    # Get current local time
    local_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Update time labels
    gmt_label.config(text="GMT Time: " + gmt_time)
    local_label.config(text="Local Time: " + local_time)

    # Schedule the update_time_clocks function to be called again after 1 second (1000 milliseconds)
    root.after(1000, update_time_clocks)

# Create the root window
root = tk.Tk()
root.title("HF Propagation Conditions")
root.configure(bg='black')

# Keep the window always on top
root.attributes('-topmost', True)

# Label for last update time
updated_label = tk.Label(root, text="", font=("Helvetica", 12, "bold"), fg="green", bg="black")
updated_label.pack()

# Separator line
separator = tk.Label(root, text="------------------------------------", font=("Helvetica", 12, "bold"), fg="green", bg="black")
separator.pack()

# Labels for A index, K index, and solar flux
solar_flux_label = tk.Label(root, text="", font=("Helvetica", 12, "bold"), fg="green", bg="black")
solar_flux_label.pack()
a_index_label = tk.Label(root, text="", font=("Helvetica", 12, "bold"), fg="green", bg="black")
a_index_label.pack()
k_index_label = tk.Label(root, text="", font=("Helvetica", 12, "bold"), fg="green", bg="black")
k_index_label.pack()

# Separator line
separator2 = tk.Label(root, text="------------------------------------", font=("Helvetica", 12, "bold"), fg="green", bg="black")
separator2.pack()

# Labels for HF propagation conditions
hf_conditions_frame = tk.Frame(root, bg="black")
hf_conditions_frame.pack()
day_conditions = {}
night_conditions = {}
bands = ["80m-40m", "30m-20m", "17m-15m", "12m-10m"]
for band in bands:
    day_label = tk.Label(hf_conditions_frame, text=band + " day = ", font=("Helvetica", 10, "bold"), fg="green", bg="black")
    day_label.grid(sticky="w")
    day_conditions[band] = day_label

    night_label = tk.Label(hf_conditions_frame, text="  " + band + " night = ", font=("Helvetica", 10, "bold"), fg="green", bg="black")
    night_label.grid(sticky="w", row=hf_conditions_frame.grid_size()[1] - 1, column=1)
    night_conditions[band] = night_label

# Separator line
separator3 = tk.Label(root, text="------------------------------------", font=("Helvetica", 12, "bold"), fg="green", bg="black")
separator3.pack()

# Labels for GMT and local time
time_frame = tk.Frame(root, bg="black")
time_frame.pack()

gmt_label = tk.Label(time_frame, text="", font=("Helvetica", 12, "bold"), fg="green", bg="black")
gmt_label.pack(side="left")

local_label = tk.Label(time_frame, text="", font=("Helvetica", 12, "bold"), fg="green", bg="black")
local_label.pack(side="left")

# Label for additional information
additional_info_label = tk.Label(root, text="Khanfar@2024", font=("Helvetica", 12, "bold"), fg="green", bg="black")
additional_info_label.pack()

# Fetch data initially when the application starts
fetch_data()

# Update time labels continuously
update_time_clocks()

root.mainloop()
