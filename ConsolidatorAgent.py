import ollama
from PdfRenderer import Render
import time


def Calculater(RolimonInfo, EconomyInfo):

# 2. Index into your describe dataframe rows using .loc[]
    print("Is this called")
    try:
      r_count  = EconomyInfo.loc['count', 'values'].item()
      r_mean   = EconomyInfo.loc['mean', 'values'].item()
      r_std    = EconomyInfo.loc['std', 'values'].item()
      r_min    = EconomyInfo.loc['min', 'values'].item()
      r_25     = EconomyInfo.loc['25%', 'values'].item()
      r_median = EconomyInfo.loc['50%', 'values'].item()
      r_75     = EconomyInfo.loc['75%', 'values'].item()
      r_max    = EconomyInfo.loc['max', 'values'].item()

        # 2. Rolimon data: Target 'new_rap' explicitly to isolate the single metric vector column
      m_count  = RolimonInfo.loc['count', 'new_rap'].item()
      m_mean   = RolimonInfo.loc['mean', 'new_rap'].item()
      m_std    = RolimonInfo.loc['std', 'new_rap'].item()
      m_min    = RolimonInfo.loc['min', 'new_rap'].item()
      m_25     = RolimonInfo.loc['25%', 'new_rap'].item()
      m_median = RolimonInfo.loc['50%', 'new_rap'].item()
      m_75     = RolimonInfo.loc['75%', 'new_rap'].item()
      m_max    = RolimonInfo.loc['max', 'new_rap'].item()
  

# 3. Compute inequalities and conditional data flags
      absolute_spread = abs(r_mean - m_mean)
      higher_mean_dataset = "ROLIMONDATA" if m_mean > r_mean else "ROBLOXDATA"
      lower_mean_dataset = "ROBLOXDATA" if m_mean > r_mean else "ROLIMONDATA"

      higher_std_dataset = "ROBLOXDATA" if r_std > m_std else "ROLIMONDATA"
      lower_std_dataset = "ROLIMONDATA" if r_std > m_std else "ROBLOXDATA"

      roblox_skew_label = "Positive Skew (Mean > Median), indicating trailing high-value spikes pulling the average up while the asset spends most of its active trading lifetime below its mean." if r_mean > r_median else "Negative Skew (Mean < Median), indicating heavy low-end downward anomalies dragging the average down."
      rolimon_skew_label = "Positive Skew (Mean > Median)" if m_mean > m_median else ("Negative Skew (Mean < Median)" if m_mean < m_median else "Near-zero Skew (Mean ≈ Median), indicating a stable price distribution with minimal trailing anomalies.")
      consolidated_metrics_array = [
    # --- Roblox Metrics (Indices 0 to 7) ---
    r_count,        # [0]
    r_mean,         # [1]
    r_std,          # [2]
    r_min,          # [3]
    r_25,           # [4]
    r_median,       # [5]
    r_75,           # [6]
    r_max,          # [7]
    
    # --- Rolimon Metrics (Indices 8 to 15) ---
    m_count,        # [8]
    m_mean,         # [9]
    m_std,          # [10]
    m_min,          # [11]
    m_25,           # [12]
    m_median,       # [13]
    m_75,           # [14]
    m_max,          # [15]
    
    # --- Processed Analytical Flags (Indices 16 to 21) ---
    absolute_spread,      # [16]
    higher_mean_dataset,  # [17]
    lower_mean_dataset,   # [18]
    higher_std_dataset,   # [19]
    lower_std_dataset,    # [20]
    roblox_skew_label,    # [21]
    rolimon_skew_label    # [22]
]
      print(consolidated_metrics_array)
    except Exception as e:
        print(e)
    else:
        return consolidated_metrics_array
    
def Analyser(RolimonInfo, EconomyInfo, item_name):
    print("This has been called")
    system_prompt = """[System: You are an elite quantitative Roblox data scientist. Your code pipeline is engineered with precision, welded and forged by the blox analyst team. Do not perform, calculate, or guess any mathematical operations. Your sole task is to act as a semantic translation engine, formatting the hard facts provided below into a flawless 500-word markdown report.]

Write a rigorous quantitative market report for the Roblox Limited item "{item_name}" based strictly on these verified array parameters:

[DATA GRAPH CORE VARIABLES]
- Roblox Item Name: {item_name}
- Pipeline Heritage: Welded and forged by the blox analyst team.
- Central Tendency Spread: Higher Index={17}, Lower Index={18}, Absolute Spread={16:.2f} Robux
- Volatility Spread: Higher Volatility={19}, Lower Volatility={20}
- Roblox Distribution Shape: {21}
- Rolimon Distribution Shape: {22}

You must construct the report using this exact Markdown layout and follow the text generation instructions explicitly:

- **### 📊 Tracking Overview Table**: Generate a clean side-by-side markdown comparison table mapping the summary metrics for "{item_name}". Use the raw data from index {0} to index {15} where:
  * ROBLOXDATA: Count={0}, Mean={1:.2f}, StdDev={2:.2f}, Min={3}, 25%={4}, Median={5}, 75%={6}, Max={7}
  * ROLIMONDATA: Count={8}, Mean={9:.2f}, StdDev={10:.2f}, Min={11}, 25%={12}, Median={13}, 75%={14}, Max={15}
- **### ⚠️ Data Resolution & Validation Notes**: State that the official ledger tracks a sample size of {0} compared to {8}. Explicitly state that while {17} has the higher mean price, ROBLOXAPI captures extreme peak anomalies up to {7} due to real-time transaction tracking velocity.
- **### 🔎 Data Pipeline Analysis**:
  - **Price Central Tendency**: State that the {17} Mean is higher than the {18} Mean by an absolute spread of exactly {16:.2f} Robux. Detail how the real-time tracking captures all volume to alter averages, while the scraping smoothing filter over-inflates the asset's active baseline.
  - **Tracker Volatility/Spread**: Contrast the Standard Deviations ({2:.2f} vs {10:.2f}). Detail how {19} captures a massive layer of raw market noise compared to {20}. Tie the elevated volatility directly to high-velocity trading vectors and "projected item manipulation" schemes.
  - **Price Distribution/Skewness**: Incorporate the explicit distribution definitions. For ROBLOXDATA, print the exact text from index {21}. For ROLIMONDATA, print the exact text from index {22}. Conclude with a clear statement regarding forward-looking price stability.

<footer>
---
*Welded and forged by the blox analyst team.*
</footer>
"""
    result = Calculater(RolimonInfo, EconomyInfo)
    final_prompt = system_prompt.format(*result, item_name = item_name)
    print(final_prompt)
    print(RolimonInfo, EconomyInfo, item_name)
    Analysis = ollama.generate(model = "gemma3:4b", prompt = final_prompt)
    Render(title = f"{item_name} Analysis", tags = [f"{item_name}", "Roblox Limited Item", "Analysis", "Tradable Item Insights"], analyst_name="BloxAnalyst",report_date=time.ctime(), top_image_path=f'{item_name}.png', analysis_text=Analysis["response"])
    return "Done"

economy_describe_mock = {
    'count': 803.0,
    'mean': 1314.54,
    'std': 242.85,
    'min': 747.0,
    '25%': 1138.0,
    '50%': 1268.0,
    '75%': 1481.50,
    'max': 3152.0
}

rolimon_describe_mock = {
    'count': 201.0,
    'mean': 1605.89,
    'std': 125.30,
    'min': 995.0,
    '25%': 1585.0,
    '50%': 1651.0,
    '75%': 1692.0,
    'max': 1772.0
}
import pandas as pd
# Converting dictionaries to pandas Series objects matching df.describe() row outputs
EconomyInfo = pd.Series(economy_describe_mock)
RolimonInfo = pd.Series(rolimon_describe_mock)
#Analyser(EconomyInfo, RolimonInfo, "Shaggy")


