import pandas as pd

# Read cleaned dataset
df = pd.read_csv(
    "datasets/cleaneddata/athena_cleaned.csv"
)

# Separate data sources
webcam_data = df[df["Source"] == "webcam"]
image_data = df[df["Source"] == "image"]

print("\n===== ATHENAVISION ANALYTICS =====\n")

# -------------------------
# Webcam Statistics
# -------------------------

print("WEBCAM STATISTICS")
print("-----------------")

print("Total Records:",
      webcam_data["People_Count"].count())

print("Average Occupancy:",
      round(webcam_data["People_Count"].mean(), 2))

print("Maximum Occupancy:",
      webcam_data["People_Count"].max())

print("Minimum Occupancy:",
      webcam_data["People_Count"].min())

print()

# -------------------------
# Image Statistics
# -------------------------

print("IMAGE STATISTICS")
print("----------------")

print("Total Records:",
      image_data["People_Count"].count())

print("Average Occupancy:",
      round(image_data["People_Count"].mean(), 2))

print("Maximum Occupancy:",
      image_data["People_Count"].max())

print("Minimum Occupancy:",
      image_data["People_Count"].min())

print()

# -------------------------
# Most Crowded Image
# -------------------------

most_crowded = image_data.loc[
    image_data["People_Count"].idxmax()
]

print("MOST CROWDED IMAGE")
print("------------------")

print("Image Name:",
      most_crowded["File_Name"])

print("People Count:",
      most_crowded["People_Count"])