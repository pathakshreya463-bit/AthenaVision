import pandas as pd

# -----------------------------
# Read Webcam Data
# -----------------------------

webcam_df = pd.read_csv(
    "datasets/rawdata/occupancy_raw.csv"
)

webcam_df = webcam_df.dropna()
webcam_df = webcam_df.drop_duplicates()

webcam_df["Source"] = "webcam"
webcam_df["File_Name"] = ""

webcam_df = webcam_df[
    ["Source", "File_Name", "Time", "People_Count"]
]

# -----------------------------
# Read Image Data
# -----------------------------

image_df = pd.read_csv(
    "datasets/rawdata/image_analysis_raw.csv"
)

image_df = image_df.dropna()
image_df = image_df.drop_duplicates()

image_df["Source"] = "image"
image_df["Time"] = ""

image_df = image_df.rename(
    columns={
        "Image_Name": "File_Name"
    }
)

image_df = image_df[
    ["Source", "File_Name", "Time", "People_Count"]
]

# -----------------------------
# Combine Data
# -----------------------------

athena_df = pd.concat(
    [webcam_df, image_df],
    ignore_index=True
)

# Remove duplicates again
athena_df = athena_df.drop_duplicates()

# Save master dataset
athena_df.to_csv(
    "datasets/cleaneddata/athena_cleaned.csv",
    index=False
)

print("\n=== ATHENA CLEANED DATA ===\n")
print(athena_df)

print("\nTotal Records:", len(athena_df))
print("Saved to datasets/cleaneddata/athena_cleaned.csv")