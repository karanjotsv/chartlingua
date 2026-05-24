import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load data from JSON file ---
if len(sys.argv) != 2:
    print("Usage: python script.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]
if not os.path.exists(json_path):
    print(f"Error: File not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

base_filename = os.path.splitext(os.path.basename(json_path))[0]

# --- 2. Extract data and settings from the loaded JSON ---
data_series = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']
categories = texts['categories']

# --- 3. Create the Plotly figure ---
fig = go.Figure()

# --- 4. Add bar traces for each data series ---
for i, series in enumerate(data_series):
    fig.add_trace(go.Bar(
        y=categories,
        x=series['values'],
        name=series['name'],
        orientation='h',
        marker=dict(
            color=colors['bar_colors'][i],
            line=dict(color='white', width=0)
        ),
        text=[f"{val}" for val in series['values']],
        textposition='inside',
        insidetextanchor='middle',
        textfont=dict(
            family='Arial',
            size=18,
            color=colors['text_colors'][i]
        ),
        hoverinfo='none'
    ))

# --- 5. Configure the layout ---
title_text = f"<b>{texts['title']}</b>"
subtitle_text = f"<span style='font-size: 18px; color: #555555;'><i>{texts['subtitle']}</i></span>"

fig.update_layout(
    barmode='stack',
    title=dict(
        text=f"{title_text}<br>{subtitle_text}",
        y=0.95,
        x=0.01,
        xanchor='left',
        yanchor='top',
        font=dict(family='Arial', size=26, color='black')
    ),
    xaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=False,
        zeroline=False,
        range=[0, sum(s['values'][2] for s in data_series) + 5] # Dynamically set range based on 'Total'
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=False,
        zeroline=False,
        domain=[0, 0.7] # Create space at the top for annotations
    ),
    showlegend=False,
    paper_bgcolor='white',
    plot_bgcolor='white',
    margin=dict(l=150, r=40, t=180, b=120),
    font=dict(family='Arial')
)

# --- 6. Add custom annotations ---
# Series labels above the chart
total_val1 = data_series[0]['values'][categories.index('Total')]
total_val2 = data_series[1]['values'][categories.index('Total')]
x_pos1 = total_val1 / 2
x_pos2 = total_val1 + (total_val2 / 2)

fig.add_annotation(
    xref='x', yref='paper',
    x=x_pos1, y=0.85,
    text=f"<b>{data_series[0]['name']}</b>",
    showarrow=False,
    font=dict(family='Arial', size=14, color=colors['bar_colors'][0]),
    align='center', xanchor='center', yanchor='middle'
)

fig.add_annotation(
    xref='x', yref='paper',
    x=x_pos2, y=0.85,
    text=f"<b>{data_series[1]['name']}</b>",
    showarrow=False,
    font=dict(family='Arial', size=14, color=colors['bar_colors'][1]),
    align='center', xanchor='center', yanchor='middle'
)

# A small vertical separator between top annotations
fig.add_shape(type="line",
    xref="x", yref="paper",
    x0=total_val1, y0=0.8, x1=total_val1, y1=0.9,
    line=dict(color="lightgrey", width=1)
)

# Category labels on the left
for i, category in enumerate(categories):
    fig.add_annotation(
        xref='paper', yref='y',
        x=-0.01, y=category,
        text=f"<b>{category}</b>",
        showarrow=False,
        xanchor='right',
        yanchor='middle',
        align='right',
        font=dict(family='Arial', size=16, color='black')
    )

# Source and logo text at the bottom
source_logo_text = f"{texts['source']}<br><b>{texts['logo']}</b>"
fig.add_annotation(
    xref='paper', yref='paper',
    x=0, y=-0.1,
    text=source_logo_text,
    showarrow=False,
    xanchor='left',
    yanchor='top',
    align='left',
    font=dict(family='Arial', size=12, color='#555555')
)

# --- 7. Write the output image ---
fig.write_image(f"{base_filename}.png", scale=2, width=800, height=600)

print(f"Chart saved to {base_filename}.png")