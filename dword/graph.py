import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

def show_daily_count(data: dict):
# Converting data to a DataFrame
  df = pd.DataFrame(list(data.items()), columns=['Word', 'Timestamp'])

  # Extracting date (year-month-day) only for grouping
  df['Date'] = df['Timestamp'].dt.date
  date_range = pd.date_range(start=df['Date'].min(), end=pd.Timestamp.today().date(), freq='D')
  daily_counts = df.groupby('Date').size().reindex(date_range, fill_value=0)

  # Plotting
  plt.figure(figsize=(12, 6))
  daily_counts.plot(kind='bar', color='skyblue')
  plt.title("Daily Word Count from Oldest Date to Today")
  plt.xlabel("Date")
  plt.ylabel("Word Count")
  plt.xticks(rotation=45, ha='right')
  plt.tight_layout()
  plt.show()