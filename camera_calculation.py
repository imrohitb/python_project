import openpyxl

# Constants
bitrate_kbps = 512  # Bitrate in Kbps
total_cameras = 20
recording_days = 75

# Calculate storage consumed per day for one camera in GB
daily_storage_per_camera_gb = (bitrate_kbps * 1000 * 60 * 60 * 24) / (8 * 1024 ** 3)

# Calculate total storage for 1 day for all cameras in GB
total_storage_1_day_gb = daily_storage_per_camera_gb * total_cameras

# Calculate total storage for 60 days for all cameras in TB
total_storage_60_days_tb = (daily_storage_per_camera_gb * recording_days * total_cameras) / 1024

# Print results
print(f"Daily Storage per Camera (GB): {daily_storage_per_camera_gb:.2f}")
print(f"Total Storage for 1 Day (GB) for All Cameras: {total_storage_1_day_gb:.2f}")
print(f"Total Storage for {recording_days} Days (TB) for All Cameras: {total_storage_60_days_tb:.2f}")

# Create a new workbook and select the active worksheet
wb = openpyxl.Workbook()
ws = wb.active

# Add headers
headers = ["Settings", "Values", "Formula"]
ws.append(headers)

# Data and formulas
data_with_formulas = [
    ("Bitrate (Kbps)", bitrate_kbps, ""),
    ("Frame Rate", 15, ""),
    ("Resolution", "5MP", ""),
    ("Schedule", "Continuous", ""),
    ("Total Cameras", total_cameras, ""),
    ("Recording Required Days", recording_days, ""),
    ("Total Storage Consumed per Day (GB)", daily_storage_per_camera_gb, "=(B2*1000*60*60*24)/(8*1024^3)"),
    ("Total Storage for 60 Days (TB)", total_storage_60_days_tb, "=B7*60*B5/1024"),
    ("Total Storage for 1 Day (GB) for All Cameras", total_storage_1_day_gb, "=B7*B5")
]

# Append data to the worksheet
for row in data_with_formulas:
    ws.append(row)

# Save the workbook
file_path = "Storage_Calculation_with_1Day.xlsx"
wb.save(file_path)

print(f"Excel file created and saved as {file_path}")
