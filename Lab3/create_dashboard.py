import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np
import pandas as pd

# Load data
df = pd.read_csv('Final_Sales_Weather.csv')

# Calculate KPIs
total_net_sales = df['Net_Sales'].sum()
total_gross_sales = df['Gross_Sales'].sum()
total_discount = df['Discount_Amount'].sum()
total_qty = df['Quantity'].sum()
total_orders = df['Sales_ID'].nunique()
aov = df['Net_Sales'].mean()

# Groupings
branch_summary = df.groupby('Branch_Name').agg(
    Net_Sales=('Net_Sales', 'sum'),
    Quantity=('Quantity', 'sum'),
    Orders=('Sales_ID', 'count')
).reset_index()

category_summary = df.groupby('Category').agg(
    Net_Sales=('Net_Sales', 'sum'),
    Quantity=('Quantity', 'sum')
).reset_index()

product_summary = df.groupby(['Category', 'Product_Name']).agg(
    Net_Sales=('Net_Sales', 'sum'),
    Quantity=('Quantity', 'sum')
).reset_index().sort_values('Net_Sales', ascending=False)

rain_summary = df.groupby('Rain_Status').agg(
    Net_Sales=('Net_Sales', 'sum'),
    Orders=('Sales_ID', 'count'),
    Avg_Net_Sales=('Net_Sales', 'mean')
).reset_index()

temp_summary = df.groupby('Temperature_Level').agg(
    Net_Sales=('Net_Sales', 'sum'),
    Orders=('Sales_ID', 'count'),
    Avg_Net_Sales=('Net_Sales', 'mean')
).reset_index()

date_summary = df.groupby('Date').agg(
    Net_Sales=('Net_Sales', 'sum'),
    Precipitation=('Precipitation', 'mean'),
    Temp_Mean=('Temperature_Mean', 'mean')
).reset_index()

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 10

# Create figure
fig = plt.figure(figsize=(18, 12), dpi=150)
fig.patch.set_facecolor('#f8f9fa')

# Colors
dark_navy = '#1e293b'

# Title & Subtitle
fig.text(0.04, 0.95, "Sales & Weather Performance Analytics Dashboard", fontsize=22, fontweight='bold', color=dark_navy)
fig.text(0.04, 0.925, "Automated Multi-source ETL Pipeline Output | Data Period: Sep 1–15, 2026", fontsize=12, color='#64748b')

def draw_kpi_card(ax, title, value, color_code):
    ax.axis('off')
    rect = mpatches.FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0.02,rounding_size=0.1",
                                   color='#ffffff', ec='#cbd5e1', lw=1.5, transform=ax.transAxes)
    ax.add_patch(rect)
    ax.text(0.5, 0.68, title, fontsize=9, fontweight='bold', color='#64748b', ha='center', va='center')
    ax.text(0.5, 0.32, value, fontsize=15, fontweight='bold', color=color_code, ha='center', va='center')

# KPI Cards Row
draw_kpi_card(fig.add_axes([0.04, 0.83, 0.14, 0.075]), "TOTAL NET SALES", f"฿{total_net_sales:,.0f}", '#0f172a')
draw_kpi_card(fig.add_axes([0.198, 0.83, 0.14, 0.075]), "TRANSACTIONS", f"{total_orders} Orders", '#2563eb')
draw_kpi_card(fig.add_axes([0.356, 0.83, 0.14, 0.075]), "QUANTITY SOLD", f"{total_qty:,} Units", '#16a34a')
draw_kpi_card(fig.add_axes([0.514, 0.83, 0.14, 0.075]), "AVG ORDER VALUE", f"฿{aov:,.2f}", '#d97706')
draw_kpi_card(fig.add_axes([0.672, 0.83, 0.14, 0.075]), "TOTAL DISCOUNT", f"฿{total_discount:,.0f}", '#dc2626')
draw_kpi_card(fig.add_axes([0.83, 0.83, 0.13, 0.075]), "GROSS SALES", f"฿{total_gross_sales:,.0f}", '#475569')

# --- Chart 1: Daily Trend - Sales vs Rain (Combo Chart) ---
ax1 = fig.add_axes([0.04, 0.46, 0.51, 0.30])
date_labels = [d[5:] for d in date_summary['Date']]
x = np.arange(len(date_labels))

bars = ax1.bar(x - 0.15, date_summary['Net_Sales'], width=0.4, color='#3b82f6', label='Net Sales (฿)', alpha=0.85)
ax1.set_ylabel('Net Sales (฿)', color='#1e3a8a', fontweight='bold')
ax1.tick_params(axis='y', labelcolor='#1e3a8a')
ax1.set_xticks(x)
ax1.set_xticklabels(date_labels, rotation=45, ha='right')
ax1.set_title('Daily Sales Trend & Mean Precipitation (Sep 2026)', fontsize=12, fontweight='bold', loc='left', pad=10)
ax1.set_ylim(0, max(date_summary['Net_Sales']) * 1.15)

ax1_twin = ax1.twinx()
line = ax1_twin.plot(x + 0.15, date_summary['Precipitation'], color='#ef4444', marker='o', linewidth=2.5, label='Precipitation (mm)')
ax1_twin.set_ylabel('Precipitation (mm)', color='#991b1b', fontweight='bold')
ax1_twin.tick_params(axis='y', labelcolor='#991b1b')
ax1_twin.set_ylim(0, max(date_summary['Precipitation']) * 1.15)
ax1_twin.grid(False)

for bar in bars:
    height = bar.get_height()
    ax1.annotate(f'฿{height:.0f}',
                xy=(bar.get_x() + bar.get_width() / 2, height),
                xytext=(0, 3),
                textcoords="offset points",
                ha='center', va='bottom', fontsize=7, rotation=90)


# --- Chart 2: Net Sales by Branch (Bar Chart) ---
ax2 = fig.add_axes([0.67, 0.46, 0.29, 0.30])
colors_branch = ['#0284c7', '#0d9488', '#6366f1']
bars_b = ax2.bar(branch_summary['Branch_Name'], branch_summary['Net_Sales'], color=colors_branch, width=0.55)
ax2.set_title('Net Sales by Branch', fontsize=12, fontweight='bold', loc='left', pad=10)
ax2.set_ylabel('Net Sales (฿)', fontweight='bold')
ax2.set_ylim(0, max(branch_summary['Net_Sales']) * 1.18)

for bar in bars_b:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, yval + 100, f'฿{yval:,.0f}', ha='center', va='bottom', fontweight='bold', fontsize=9)


# --- Chart 3: Category Share (Donut Chart) ---
ax3 = fig.add_axes([0.04, 0.08, 0.26, 0.30])
colors_cat = ['#f59e0b', '#3b82f6', '#10b981']
wedges, texts, autotexts = ax3.pie(
    category_summary['Net_Sales'], 
    labels=category_summary['Category'], 
    autopct='%1.1f%%',
    startangle=140, 
    colors=colors_cat,
    wedgeprops=dict(width=0.4, edgecolor='white', linewidth=2)
)
plt.setp(autotexts, size=9, weight="bold", color="white")
plt.setp(texts, size=10, weight="bold")
ax3.set_title('Net Sales Share by Category', fontsize=12, fontweight='bold', loc='left', pad=10)


# --- Chart 4: Top Products Performance (Horizontal Bar Chart) ---
ax4 = fig.add_axes([0.36, 0.08, 0.30, 0.30])
y_pos = np.arange(len(product_summary))
bars_p = ax4.barh(y_pos, product_summary['Net_Sales'], color='#8b5cf6', height=0.6)
ax4.set_yticks(y_pos)
ax4.set_yticklabels(product_summary['Product_Name'], fontweight='bold')
ax4.invert_yaxis()
ax4.set_xlabel('Net Sales (฿)', fontweight='bold')
ax4.set_title('Product Sales Performance', fontsize=12, fontweight='bold', loc='left', pad=10)

for bar in bars_p:
    xval = bar.get_width()
    ax4.text(xval + 50, bar.get_y() + bar.get_height()/2, f'฿{xval:,.0f}', ha='left', va='center', fontsize=8, fontweight='bold')
ax4.set_xlim(0, max(product_summary['Net_Sales']) * 1.25)


# --- Chart 5: Weather Condition Impact (Bar Chart) ---
ax5 = fig.add_axes([0.71, 0.08, 0.25, 0.30])
bars_r = ax5.bar(rain_summary['Rain_Status'], rain_summary['Net_Sales'], color=['#0284c7', '#38bdf8'], width=0.45)
ax5.set_title('Net Sales by Rain Condition', fontsize=12, fontweight='bold', loc='left', pad=10)
ax5.set_ylabel('Net Sales (฿)', fontweight='bold')
ax5.set_ylim(0, max(rain_summary['Rain_Status'].map(lambda x: rain_summary[rain_summary['Rain_Status']==x]['Net_Sales'].values[0])) * 1.18)

for bar in bars_r:
    yval = bar.get_height()
    ax5.text(bar.get_x() + bar.get_width()/2, yval + 200, f'฿{yval:,.0f}', ha='center', va='bottom', fontweight='bold', fontsize=9)

# Save figure
plt.savefig('Final_Sales_Weather_Dashboard.png', bbox_inches='tight', facecolor=fig.get_facecolor())
plt.close()
print("Dashboard saved successfully!")