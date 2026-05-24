import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load Data ---
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json>")
    sys.exit(1)

json_path = pathlib.Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

texts = chart_info['texts']
colors = chart_info['colors']
data = chart_info['chart_data']

# --- 2. Create Figure ---
fig = go.Figure()

# --- 3. Add Traces for each subplot ---

# Population (Donut)
pop_val = data['population']['value']
fig.add_trace(go.Pie(
    values=[pop_val, 100 - pop_val],
    labels=['Y&H', 'Rest of UK'],
    hole=0.7,
    marker_colors=[colors['population'], colors['donut_secondary']],
    textinfo='none',
    hoverinfo='none',
    sort=False,
    domain={'x': [0.0, 0.28], 'y': [0.65, 0.95]}
))

# Qualifications (Horizontal Bar)
qual_data = data['qualifications']
fig.add_trace(go.Bar(
    y=[d['category'] for d in qual_data],
    x=[d['value'] for d in qual_data],
    orientation='h',
    marker_color=colors['qualifications'],
    hoverinfo='none',
    text=[f"{d['value']}%" for d in qual_data],
    textposition='auto',
    insidetextanchor='start',
    xaxis='x2',
    yaxis='y2'
))

# Unemployment (Vertical Bar)
unemp_data = data['unemployment']
fig.add_trace(go.Bar(
    x=[d['category'] for d in unemp_data],
    y=[d['value'] for d in unemp_data],
    marker_color=colors['unemployment'],
    hoverinfo='none',
    text=[f"{d['value']}%" for d in unemp_data],
    textposition='outside',
    xaxis='x3',
    yaxis='y3'
))

# Economic Output (Donut)
econ_val = data['economic_output']['value']
fig.add_trace(go.Pie(
    values=[econ_val, 100 - econ_val],
    labels=['Y&H', 'Rest of UK'],
    hole=0.7,
    marker_colors=[colors['economic_output'], colors['donut_secondary']],
    textinfo='none',
    hoverinfo='none',
    sort=False,
    domain={'x': [0.0, 0.28], 'y': [0.3, 0.6]}
))

# Weekly Earnings (Scatter for circles)
fig.add_trace(go.Scatter(
    x=[0.5, 0.5],
    y=[0.75, 0.25],
    mode='markers',
    marker=dict(
        color=colors['weekly_earnings'],
        size=85,
        line=dict(width=3, color='#FFFFFF')
    ),
    hoverinfo='none',
    xaxis='x4',
    yaxis='y4'
))

# House Prices (Vertical Bar)
hp_data = data['house_prices']
fig.add_trace(go.Bar(
    x=[d['category'] for d in hp_data],
    y=[d['value'] for d in hp_data],
    marker_color=colors['house_prices'],
    hoverinfo='none',
    xaxis='x5',
    yaxis='y5'
))

# --- 4. Configure Layout, Axes, and Annotations ---
annotations = []

# --- Section Titles with Arrows ---
title_font = dict(family="Arial", size=14, color='white')
arrow_props = dict(showarrow=True, arrowhead=6, arrowwidth=1, ax=0, ay=-25)

annotations.extend([
    dict(x=0.14, y=0.98, text=f"<b>{texts['section_titles']['population']}</b>", bgcolor=colors['population'], font=title_font, **arrow_props),
    dict(x=0.46, y=0.98, text=f"<b>{texts['section_titles']['qualifications']}</b>", bgcolor=colors['qualifications'], font=title_font, **arrow_props),
    dict(x=0.825, y=0.98, text=f"<b>{texts['section_titles']['unemployment']}</b>", bgcolor=colors['unemployment'], font=title_font, **arrow_props),
    dict(x=0.14, y=0.63, text=f"<b>{texts['section_titles']['economic_output']}</b>", bgcolor=colors['economic_output'], font=title_font, **arrow_props),
    dict(x=0.14, y=0.33, text=f"<b>{texts['section_titles']['weekly_earnings']}</b>", bgcolor=colors['weekly_earnings'], font=title_font, **arrow_props),
    dict(x=0.46, y=0.33, text=f"<b>{texts['section_titles']['house_prices']}</b>", bgcolor=colors['house_prices'], font=title_font, **arrow_props),
    dict(x=0.825, y=0.33, text=f"<b>{texts['section_titles']['life_expectancy']}</b>", bgcolor=colors['life_expectancy'], font=title_font, **arrow_props),
])

# --- Chart Specific Annotations ---
# Population
annotations.extend([
    dict(x=0.14, y=0.81, text=f"<span style='font-size: 28px;'><b>{texts['population']['center_value']}</b></span><br>{texts['population']['center_label']}", showarrow=False),
    dict(x=0.14, y=0.68, text=f"<b>{texts['population']['bottom_value']}</b><br><span style='font-size: 11px;'>{texts['population']['bottom_label']}</span>", showarrow=False),
])
# Qualifications
annotations.append(dict(x=0.95, y=-0.2, text=texts['qualifications']['source_date'], showarrow=False, xref='x2 domain', yref='y2 domain', xanchor='right'))
# Unemployment
annotations.append(dict(x=1, y=-0.2, text=texts['unemployment']['source_date'], showarrow=False, xref='x3 domain', yref='y3 domain', xanchor='right'))
# Economic Output
annotations.extend([
    dict(x=0.14, y=0.46, text=f"<span style='font-size: 28px;'><b>{texts['economic_output']['center_value']}</b></span><br>{texts['economic_output']['center_label']}", showarrow=False),
    dict(x=0.14, y=0.32, text=f"<b>{texts['economic_output']['bottom_value']}</b><br><span style='font-size: 11px;'>{texts['economic_output']['bottom_label']}</span>", showarrow=False),
])
# Weekly Earnings
earnings_data = data['weekly_earnings']
annotations.extend([
    dict(x=0.5, y=0.75, xref='x4', yref='y4', text=f"<span style='font-size: 11px;'>{earnings_data[0]['category']}</span><br><b style='font-size: 20px;'>{earnings_data[0]['prefix']}{earnings_data[0]['value']}</b>", font=dict(color='white'), showarrow=False),
    dict(x=0.5, y=0.25, xref='x4', yref='y4', text=f"<span style='font-size: 11px;'>{earnings_data[1]['category']}</span><br><b style='font-size: 20px;'>{earnings_data[1]['prefix']}{earnings_data[1]['value']}</b>", font=dict(color='white'), showarrow=False),
    dict(x=0.5, y=-0.2, xref='x4 domain', yref='y4 domain', text=texts['weekly_earnings']['source_note'], showarrow=False),
])
# House Prices
hp_note = texts['house_prices']['note']
annotations.extend([
    dict(x=0.5, y=1.2, xref='x5 domain', yref='y5 domain', text=hp_note, align='center', showarrow=False),
    dict(x=hp_data[0]['category'], y=hp_data[0]['value'], xref='x5', yref='y5', text=hp_data[0]['label'], showarrow=True, arrowhead=6, ax=0, ay=30),
    dict(x=hp_data[1]['category'], y=hp_data[1]['value'], xref='x5', yref='y5', text=hp_data[1]['label'], showarrow=True, arrowhead=6, ax=0, ay=-30),
])
# Life Expectancy
le_data = data['life_expectancy']
annotations.extend([
    dict(x=0.825, y=0.25, text=f"<b>{le_data[0]['category']}</b>", showarrow=False),
    dict(x=0.77, y=0.19, text=f"<span style='font-size: 24px; color: {colors['life_expectancy']}'>&#9794;</span> <b>{le_data[0]['male']}</b><br>years", showarrow=False),
    dict(x=0.88, y=0.19, text=f"<span style='font-size: 24px; color: {colors['life_expectancy']}'>&#9792;</span> <b>{le_data[0]['female']}</b><br>years", showarrow=False),
    dict(x=0.825, y=0.12, text=f"<b>{le_data[1]['category']}</b>", showarrow=False),
    dict(x=0.77, y=0.06, text=f"<span style='font-size: 24px; color: {colors['life_expectancy']}'>&#9794;</span> <b>{le_data[1]['male']}</b><br>years", showarrow=False),
    dict(x=0.88, y=0.06, text=f"<span style='font-size: 24px; color: {colors['life_expectancy']}'>&#9792;</span> <b>{le_data[1]['female']}</b><br>years", showarrow=False),
    dict(x=0.825, y=-0.05, text=texts['life_expectancy']['note'], showarrow=False),
])
# Footer
annotations.extend([
    dict(x=0.01, y=-0.12, xref='paper', yref='paper', text=f"<b>{texts['source']}</b>", showarrow=False, xanchor='left', yanchor='bottom', align='left'),
    dict(x=0.01, y=-0.16, xref='paper', yref='paper', text=texts['credits'], showarrow=False, xanchor='left', yanchor='top', align='left', font=dict(size=9)),
])

# --- Final Layout Update ---
fig.update_layout(
    # Sizing and Spacing
    width=800,
    height=1100,
    margin=dict(t=80, b=120, l=40, r=40),
    paper_bgcolor=colors['background'],
    plot_bgcolor=colors['background'],

    # Title
    title=dict(text=f"<b>{texts['title']}</b>", font_size=24, y=0.99, x=0.5, xanchor='center', yanchor='top'),

    # Fonts and Legends
    font=dict(family="Arial", size=12, color='#333333'),
    showlegend=False,

    # Axis Definitions
    xaxis2=dict(domain=[0.32, 0.62], visible=False),
    yaxis2=dict(domain=[0.65, 0.90], autorange='reversed', visible=False, fixedrange=True),
    xaxis3=dict(domain=[0.68, 0.98], showgrid=False, zeroline=False, tickfont=dict(size=10)),
    yaxis3=dict(domain=[0.65, 0.90], visible=False, range=[0, 12]),
    xaxis4=dict(domain=[0.0, 0.28], visible=False, range=[0, 1]),
    yaxis4=dict(domain=[0.0, 0.3], visible=False, range=[0, 1]),
    xaxis5=dict(domain=[0.36, 0.56], visible=False),
    yaxis5=dict(domain=[0.0, 0.2], visible=False, range=[-2, 10]),
    
    # Hide ticks and labels for the bar charts' categorical axes
    xaxis3_tickangle=0,
    yaxis2_showticklabels=True,
    xaxis3_showticklabels=True,
    xaxis2_zeroline=False,
    yaxis3_zeroline=False,

    # Apply all annotations
    annotations=annotations
)

# --- 5. Output ---
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")