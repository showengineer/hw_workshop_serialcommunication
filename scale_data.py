import pandas as pd
import numpy as np

# 1. Read the Excel file
input_file = "CONTINUOUS_TIME_GreenhouseGasses.xlsx"
df = pd.read_excel(input_file)

# 2. Melt the data to long format (Country, Year, Value)
df_long = df.melt(id_vars="Country", var_name="Year", value_name="Value")

# 3. Apply log() to all values (natural log)
df_long["LogValue"] = np.log(df_long["Value"])

# 4. Min-max scale log values to 0-255 and convert to int
log_min = df_long["LogValue"].min()
log_max = df_long["LogValue"].max()

a, b = 100, 255
df_long["Scaled255"] = (a + (df_long["LogValue"] - log_min) / (log_max - log_min) * (b - a)).round().astype(int)

# 5. Pivot back to wide format for the scaled values
df_scaled = df_long.pivot(index="Country", columns="Year", values="Scaled255").reset_index()

# 6. Write the scaled data to a new Excel file
output_file = "edited_data.xlsx"
df_scaled.to_excel(output_file, index=False)

print(f"Log-transformed and 0-255 scaled data saved to {output_file}")
