import requests
import time

def get_location():
    # Fetch IP address
    ip_response = requests.get("https://api.ipify.org?format=json")
    ip_data = ip_response.json()
    ip_address = ip_data["ip"]

    # Fetch location based on IP address
    location_response = requests.get(f"https://ipinfo.io/{ip_address}/json")
    location_data = location_response.json()
    return location_data

def get_band_condition(solar_flux, a_index, k_index, x_ray, sunspots):
    # Determine band condition based on solar data
    condition = "Unknown"  # Default condition
    
    # Define thresholds for solar parameters
    if solar_flux >= 150 and a_index <= 7 and k_index <= 1 and x_ray == "C" and sunspots >= 50:
        condition = "Good"
    elif solar_flux >= 100 and a_index <= 15 and k_index <= 2 and x_ray in ["B", "C"] and sunspots >= 20:
        condition = "Fair"
    else:
        condition = "Poor"
    
    return condition

def main():
    while True:
        # Fetch solar data (replace with your data source)
        # Example data:
        solar_flux = 214
        a_index = 272
        k_index = 6
        x_ray = "C5.8"
        sunspots = 148
        
        # Fetch location information
        location_data = get_location()
        country = location_data.get("country", "Unknown")
        city = location_data.get("city", "Unknown")
        print(f"Location: {city}, {country}")

        # Calculate band conditions
        band_conditions = {
            "80m-40m": get_band_condition(solar_flux, a_index, k_index, x_ray[0], sunspots),
            "30m-20m": get_band_condition(solar_flux, a_index, k_index, x_ray[0], sunspots),
            "17m-15m": get_band_condition(solar_flux, a_index, k_index, x_ray[0], sunspots),
            "12m-10m": get_band_condition(solar_flux, a_index, k_index, x_ray[0], sunspots)
        }
        
        # Print band conditions
        print("Band Conditions:")
        for band, condition in band_conditions.items():
            print(f"{band}: {condition}")
        
        # Wait for 30 minutes before updating again
        time.sleep(1800)  # 1800 seconds = 30 minutes

if __name__ == "__main__":
    main()
