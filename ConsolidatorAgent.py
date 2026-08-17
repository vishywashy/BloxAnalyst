import ollama
from PdfRenderer import Render
import time
def Analyser(RolimonInfo, EconomyInfo, item_name):
    system = f"""You are a quantitative data scientist specializing in the Roblox economy, Virtual Asset Trading, and algorithmic tracking of high-tier Limited Items.

I will provide you with summary statistics (df.describe() outputs) for two datasets tracking the price history of the exact same individual Roblox Limited item: one from the official Roblox API and one from Rolimon's scraped index.

Please perform a rigorous side-by-side analytical comparison of these datasets based on the mathematical rules of descriptive statistics and the structural mechanics of the Roblox economy.

Follow these execution constraints perfectly:
1. Context Integration (Data Architecture Gaps): Ground the analysis in tracking a single Roblox Limited item. Explicitly attribute variance to data collection methods: the official Roblox API captures a comprehensive, real-time ledger of every single transaction, whereas the third-party Rolimon's API utilizes an intermittent polling/background web-scraping frequency that acts as an inadvertent statistical smoothing filter.
2. Rigid Logic Safeguard: Before writing any descriptive text, you must programmatically evaluate the relationship between the metrics. If Metric A > Metric B, your text must explicitly state "A is higher than B". Any inversion of this rule will break the pipeline.
3. Outlier and Liquidity Validation: Scan the Minimum and Maximum price boundaries. Explain price peaks and crashes using trading mechanics:
   - High-end spikes in RobloxAPI = high-velocity premium trades or rapid-fire flash buys missed by scraping cycles.
   - Low-end crashes in RolimonData = rapid "snipes," underpriced listings caught mid-scrape, or a difference in how the platforms filter out bot anomalies or "poisoned" items.
4. Skewness and Market Stability: Mathematically define skewness using the Pearson mode skewness relationship (Mean vs. Median):
   - Positive Skew (Mean > Median): Indicates trailing high-value spikes pulling the average up; the asset spends most of its time trading below its mean.
   - Negative Skew (Mean < Median): Indicates heavy low-end downward anomalies dragging the average down; the asset's active baseline is higher than its mean.
5. Trading Risk Context: Factor in the impact of "projected item manipulation" (artificial price inflation via low-volume, high-value shell accounts) and how it artificially inflates standard deviation.

Format your output using this clean Markdown structure:

- **### 📊 Tracking Overview Table**: A side-by-side markdown table comparing all available metrics for the item.
- **### ⚠️ Data Resolution & Validation Notes**: An analysis detailing how sample sizes, collection latency, and outlier handling impacted recorded peaks and crashes.
- **### 🔎 Data Pipeline Analysis**: Deep bulleted insights detailing:
  - **Price Central Tendency**: Breaking down the absolute spread (RobloxAPI Mean - RolimonData Mean) and explaining which index over- or under-inflates value.
  - **Tracker Volatility/Spread**: Contrasting the Standard Deviations to define true market noise vs. smoothed indices.
  - **Price Distribution/Skewness**: Explicitly stating the distribution skew for both datasets and what it means for forward-looking price stability.
- **### ✅ Pipeline Logic Check**: A short 2-sentence confirmation block at the very end explicitly stating: "Logic Verification: Confirmed that [Insert Higher Mean] > [Insert Lower Mean] and [Insert Higher SD] > [Insert Lower SD]."

"""

    Analysis = ollama.generate(model = "qwen2.5-coder:7b",  options={"temperature":0, "num_thread": 8}, prompt = f"""ROBLOXDATA:{EconomyInfo}, ROLIMONDATA:{RolimonInfo}""", system = system)
    print(Analysis["response"]+"This is where its meant to go")
    print(f'{item_name}'+'-----This is the name of the item for reference')
    Render(title = f"{item_name} Analysis", tags = [f"{item_name}", "Roblox Limited Item", "Analysis", "Tradable Item Insights"], analyst_name="BloxAnalyst",report_date=time.ctime(), top_image_path=f'{item_name}.png', analysis_text=Analysis["response"])
    return Analysis["response"]


