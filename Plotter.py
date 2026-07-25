import matplotlib.pyplot as plt
from datetime import datetime
def PlotGraph(DataPoints, actual_time, oldrap_list, newrap_list, name):
    BG_COLOR = "#0B132B"       # Ultra-deep navy canvas background
    CARD_COLOR = "#1C2541"     # Slate blue for the inner grid space
    GRID_COLOR = "#3A506B"     # Muted blue for grid accents
    TEXT_MAIN = "#FFFFFF"      # Crisp white for main headings
    TEXT_MUTED = "#5BC0BE"     # Electric teal for subheadings/ticks

# 2. Initialize the Canvas with Outer Figure Background
    fig, ax = plt.subplots(figsize=(12, 6), facecolor=BG_COLOR)

# 3. Style the Inner Graph Area
    ax.set_facecolor(CARD_COLOR)

# 4. Clean up the Chart Borders (Spines)
# Removes the harsh box look and sets a subtle bottom boundary line 
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(GRID_COLOR)
    ax.spines['bottom'].set_color(GRID_COLOR)
    ax.spines['left'].set_linewidth(1.2)
    ax.spines['bottom'].set_linewidth(1.2)

# 5. Format the Grid Lines
    ax.grid(True, linestyle=":", color=GRID_COLOR, alpha=0.4, zorder=0)

# 6. Customize Axis Ticks and Labels
    ax.tick_params(colors=TEXT_MUTED, labelsize=10, width=1.2)

# 7. Add Typography Anchors
    ax.set_title(f"{name.upper()} MARKET PERFORMANCE", color=TEXT_MAIN, fontsize=14, fontweight="bold", pad=20, loc="left")
    ax.set_xlabel("TIMELINE INDEX", color=TEXT_MUTED, fontsize=10, fontweight="bold", labelpad=12)
    ax.set_ylabel("METRIC VALUE", color=TEXT_MUTED, fontsize=10, fontweight="bold", labelpad=12)

# 8. Render the Blank Canvas
    plt.tight_layout()

# 3. Change the inner axes background color
    Itemvalues = [i["value"] for i in DataPoints["priceDataPoints"]]
    Dates = [i["date"] for i in DataPoints["priceDataPoints"]]
    print(Dates)
    Dates = [datetime.strptime(i , "%Y-%m-%dT%H:%M:%SZ") for i in Dates]
    Formatted_Dates = [datetime.strftime(i, "%d-%m-%Y") for i in Dates]
    ax.plot(Dates, Itemvalues, linestyle='-', color='#00A2FF', linewidth=1)
    ax.plot(actual_time, oldrap_list, linestyle='-', color="#FF0400", linewidth=1)
    ax.plot(actual_time, newrap_list,linestyle='-', color="#16FF3D", linewidth=1)
    plt.show()
   
