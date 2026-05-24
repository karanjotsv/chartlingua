import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load Data ---
# The script must be called with the JSON file path as the first argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Derive the output filename base from the input JSON path
filename_base = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{filename_base}.png"

# Load the chart data from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_config = json.load(f)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

# --- 2. Create Figure ---
fig = go.Figure()
fig.update_layout(
    width=900,
    height=1350,
    plot_bgcolor=colors['main_background'],
    paper_bgcolor=colors['main_background'],
    font=dict(family="Arial", color=colors['text']),
    margin=dict(t=100, b=100, l=40, r=40),
    showlegend=False
)

# --- 3. Build Chart Elements ---
# The layout is custom, so we build it piece by piece using absolute positioning
shapes = []
annotations = []
traces = []

# --- Section Headers ---
header_y_top, header_y_bottom = 0.92, 0.89
header_coords = {
    0: [0.05, 0.32],  # Population
    1: [0.35, 0.62],  # Life Expectancy
    2: [0.65, 0.95],  # Qualifications
    3: [0.05, 0.32],  # Economic Output
    4: [0.05, 0.32],  # Unemployment
    5: [0.35, 0.62],  # Weekly Earnings
    6: [0.65, 0.95]   # House Prices
}
y_offsets = {3: -0.3, 4: -0.55, 5: -0.55, 6: -0.55} # y offset for lower rows

for i, item in enumerate(chart_data):
    x0, x1 = header_coords[i]
    y_off = y_offsets.get(i, 0)
    
    # Header rectangle
    shapes.append(dict(type="rect", xref="paper", yref="paper",
                       x0=x0, y0=header_y_bottom + y_off, x1=x1, y1=header_y_top + y_off,
                       fillcolor=colors['header_bg'][i], layer="below", line_width=0))
    # Header text
    annotations.append(dict(xref="paper", yref="paper", x=(x0 + x1) / 2, y=(header_y_top + header_y_bottom) / 2 + y_off,
                            text=f"<b>{item['title']}</b>", showarrow=False, font=dict(color=colors['header_text'], size=12)))
    # Header pointer
    shapes.append(dict(type="path", xref="paper", yref="paper",
                       path=f"M {x0+0.02} {header_y_bottom+y_off} L {x0+0.04} {header_y_bottom+y_off-0.02} L {x0+0.06} {header_y_bottom+y_off} Z",
                       fillcolor=colors['header_bg'][i], layer="below", line_width=0))

# --- Chart-Specific Elements ---

# 1. Population (Donut)
pop_data = chart_data[0]
traces.append(go.Pie(
    values=[pop_data['value'], 100 - pop_data['value']],
    domain={'x': [0.05, 0.32], 'y': [0.7, 0.88]},
    marker=dict(colors=[colors['donut_segment'][0], colors['donut_base']]),
    hole=0.7, textinfo='none', sort=False, direction='clockwise'
))
annotations.append(dict(xref="paper", yref="paper", x=0.185, y=0.79, text=f"<b>{pop_data['center_text']}</b>", showarrow=False, font_size=20, align='center'))
annotations.append(dict(xref="paper", yref="paper", x=0.185, y=0.67, text=pop_data['sub_text'], showarrow=False, align='center'))

# 2. Life Expectancy (Info Block)
le_data = chart_data[1]
male_icon = "&#9794;"  # Unicode for male symbol
female_icon = "&#9792;" # Unicode for female symbol
annotations.extend([
    dict(xref="paper", yref="paper", x=0.485, y=0.83, text=f"<b>{le_data['data'][0]['region']}</b>", showarrow=False, font_size=14, font_color=colors['header_bg'][1]),
    dict(xref="paper", yref="paper", x=0.42, y=0.8, text=f"<span style='font-size: 24px;'>{male_icon}</span> {le_data['data'][0]['male']}<br>years", showarrow=False, align='center', font_size=12),
    dict(xref="paper", yref="paper", x=0.55, y=0.8, text=f"<span style='font-size: 24px;'>{female_icon}</span> {le_data['data'][0]['female']}<br>years", showarrow=False, align='center', font_size=12),
    dict(xref="paper", yref="paper", x=0.485, y=0.75, text=f"<b>{le_data['data'][1]['region']}</b>", showarrow=False, font_size=14),
    dict(xref="paper", yref="paper", x=0.42, y=0.72, text=f"<span style='font-size: 24px;'>{male_icon}</span> {le_data['data'][1]['male']}<br>years", showarrow=False, align='center', font_size=12),
    dict(xref="paper", yref="paper", x=0.55, y=0.72, text=f"<span style='font-size: 24px;'>{female_icon}</span> {le_data['data'][1]['female']}<br>years", showarrow=False, align='center', font_size=12),
    dict(xref="paper", yref="paper", x=0.485, y=0.67, text=le_data['sub_text'], showarrow=False, align='center')
])

# 3. Qualifications (Horizontal Bar)
qual_data = chart_data[2]
traces.append(go.Bar(
    y=qual_data['categories'], x=qual_data['values'], orientation='h',
    text=[f"{v}%" for v in qual_data['values']], textposition='auto', insidetextanchor='end',
    marker_color=colors['qualifications_bar'], xaxis='x2', yaxis='y2'
))
annotations.append(dict(xref="paper", yref="paper", x=0.8, y=0.67, text=qual_data['sub_text'], showarrow=False, align='center'))

# 4. Economic Output (Donut)
econ_data = chart_data[3]
traces.append(go.Pie(
    values=[econ_data['value'], 100 - econ_data['value']],
    domain={'x': [0.05, 0.32], 'y': [0.44, 0.62]},
    marker=dict(colors=[colors['donut_segment'][1], colors['donut_base']]),
    hole=0.7, textinfo='none', sort=False, direction='clockwise'
))
annotations.append(dict(xref="paper", yref="paper", x=0.185, y=0.53, text=f"<b>{econ_data['center_text']}</b>", showarrow=False, font_size=20, align='center'))
annotations.append(dict(xref="paper", yref="paper", x=0.185, y=0.41, text=econ_data['sub_text'], showarrow=False, align='center'))

# 5. Unemployment (Vertical Bar)
unemp_data = chart_data[4]
unemp_colors = [colors['unemployment_bars'][0] if v > 10 else colors['unemployment_bars'][1] for v in unemp_data['values']]
traces.append(go.Bar(
    x=unemp_data['categories'], y=unemp_data['values'],
    text=[f"{v}%" for v in unemp_data['values']], textposition='outside',
    marker_color=unemp_colors, xaxis='x3', yaxis='y3'
))
annotations.append(dict(xref="paper", yref="paper", x=0.185, y=0.1, text=unemp_data['sub_text'], showarrow=False, align='center'))

# 6. Weekly Earnings (Custom Circles)
earn_data = chart_data[5]
traces.append(go.Scatter(
    x=[d['position'][0] for d in earn_data['data']],
    y=[d['position'][1] for d in earn_data['data']],
    mode='markers', marker=dict(color=colors['earnings_circles'], size=90, line=dict(width=4, color='white')),
    xaxis='x4', yaxis='y4'
))
for d in earn_data['data']:
    annotations.append(dict(x=d['position'][0], y=d['position'][1], text=f"<b>{d['value']}</b>", showarrow=False, font_size=18, font_color='white', xref='x4', yref='y4'))
    annotations.append(dict(x=d['position'][0], y=d['position'][1]+0.2, text=f"<b>{d['region']}</b>", showarrow=False, font_color=colors['earnings_circles'], xref='x4', yref='y4'))
annotations.append(dict(xref="paper", yref="paper", x=0.485, y=0.1, text=earn_data['sub_text'], showarrow=False, align='center'))

# 7. House Prices (Vertical Bar with Custom Shape)
hp_data = chart_data[6]
traces.append(go.Bar(
    x=hp_data['categories'], y=hp_data['values'],
    text=[f"<b>{v}%</b><br>{hp_data['value_suffix']}" for v in hp_data['values']], textposition='outside',
    marker_color=colors['house_price_bars'], xaxis='x5', yaxis='y5', textfont_size=12
))
# Add triangle shape for the first bar
bar0_x = hp_data['categories'][0]
bar0_y = hp_data['values'][0]
shapes.append(dict(type="path", xref="x5", yref="y5",
                   path=f"M -0.4 {bar0_y} L 0 {bar0_y + 1} L 0.4 {bar0_y} Z",
                   fillcolor=colors['house_price_bars'][0], line_width=0))
annotations.append(dict(xref="paper", yref="paper", x=0.8, y=0.1, text=hp_data['sub_text'], showarrow=False, align='center'))

# --- 4. Final Layout and Annotations ---
# Main title
annotations.append(dict(xref="paper", yref="paper", x=0.5, y=0.97, text=texts['title'], showarrow=False,
                        font=dict(size=24, color=colors['title_text'])))

# Footer
annotations.append(dict(xref="paper", yref="paper", x=0.05, y=0.05, text=f"<b>{texts['source']}</b>", showarrow=False, xanchor='left', yanchor='bottom', font_size=14))
annotations.append(dict(xref="paper", yref="paper", x=0.05, y=0.03, text=texts['note'], showarrow=False, xanchor='left', yanchor='bottom', font_size=10))

# --- Update Figure with All Elements ---
fig.update_layout(
    shapes=shapes,
    annotations=annotations,
    # Axes for Qualifications Bar Chart
    xaxis2=dict(domain=[0.65, 0.95], anchor='y2', showticklabels=False, showgrid=False, zeroline=False, range=[0, 15]),
    yaxis2=dict(domain=[0.7, 0.88], anchor='x2', autorange="reversed", showticklabels=False, showgrid=False, zeroline=False),
    # Axes for Unemployment Bar Chart
    xaxis3=dict(domain=[0.05, 0.32], anchor='y3', showgrid=False),
    yaxis3=dict(domain=[0.14, 0.32], anchor='x3', showgrid=False, range=[0, 12]),
    # Axes for Weekly Earnings Circles
    xaxis4=dict(domain=[0.35, 0.62], anchor='y4', showticklabels=False, showgrid=False, zeroline=False, range=[0,1]),
    yaxis4=dict(domain=[0.14, 0.32], anchor='x4', showticklabels=False, showgrid=False, zeroline=False, range=[0,1]),
    # Axes for House Prices Bar Chart
    xaxis5=dict(domain=[0.65, 0.95], anchor='y5', showgrid=False),
    yaxis5=dict(domain=[0.14, 0.32], anchor='x5', showgrid=False, range=[0, 10])
)
fig.add_traces(traces)

# --- 5. Save Output ---
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")