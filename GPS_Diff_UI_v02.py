import math
import pandas as pd
import tkinter as tk
from tkinter import messagebox, filedialog

def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon1 - lon2
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    r = 6371  # Radius of Earth in kilometers
    return r * c

def convert_to_gps(c, isW=False):
    if ' ' not in c:
        gps = float(c)
    else:
        nums = c.split()
        gps = round(float(nums[0]) + float(nums[1]) / 60, 8)
        
    if isW and gps > 0:
        gps *= -1
    
    return gps

def select_file():
    global filepath
    filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if filepath:
        file_var.set(f"Selected file: {filepath}")

def calculate_closest_point(event=None):
    if not filepath:
        messagebox.showerror("File Error", "Please select a CSV file first.")
        return
    
    df = pd.read_csv(filepath)
    
    try:
        n_input = n_entry.get()
        w_input = w_entry.get()
        
        if not n_input or not w_input:
            messagebox.showerror("Input Error", "Please enter both N and W coordinates.")
            return
        
        n_gps = convert_to_gps(n_input, False)
        w_gps = convert_to_gps(w_input, True)

        lat_var.set(f"Calculated GPS Latitude: {n_gps}")
        long_var.set(f"Calculated GPS Longitude: {w_gps}")
        
        min_distance_km = float('inf')
        closest_point = None

        for index, row in df.iterrows():
            lat, lon = row['Lat'], row['Long']
            distance_km = haversine(n_gps, w_gps, lat, lon)
            if distance_km < min_distance_km:
                min_distance_km = distance_km
                closest_point = row

        min_distance_ft = min_distance_km * 3280.84
        
        output = f"Closest point:\n{closest_point}\nMinimum Haversine distance: {min_distance_km:.2f} km\nMinimum Haversine distance: {min_distance_ft:.2f} ft"
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, output)

    except Exception as e:
        messagebox.showerror("Error", str(e))

# GUI setup
root = tk.Tk()
root.title("Haversine Distance Calculator")

frame = tk.Frame(root, padx=10, pady=10)
frame.pack(padx=10, pady=10)

tk.Button(frame, text="Select Lat/Long File", command=select_file).grid(row=0, columnspan=2, pady=10)

file_var = tk.StringVar()
tk.Label(frame, textvariable=file_var).grid(row=1, columnspan=2, sticky='w')

tk.Label(frame, text="Enter N coordinates (degrees minutes):").grid(row=2, column=0, sticky="w")
n_entry = tk.Entry(frame)
n_entry.grid(row=2, column=1)

tk.Label(frame, text="Enter W coordinates (degrees minutes):").grid(row=3, column=0, sticky="w")
w_entry = tk.Entry(frame)
w_entry.grid(row=3, column=1)

lat_var = tk.StringVar()
tk.Label(frame, textvariable=lat_var).grid(row=5, column=0, sticky='w')

long_var = tk.StringVar()
tk.Label(frame, textvariable=long_var).grid(row=6, column=0, sticky='w')

tk.Button(frame, text="Calculate", command=calculate_closest_point).grid(row=4, columnspan=2, pady=10)

result_text = tk.Text(frame, height=12, wrap="word")
result_text.grid(row=7, columnspan=2, sticky="w")

# Bind the Enter key to the calculate button
root.bind('<Return>', calculate_closest_point)

filepath = None

root.mainloop()
