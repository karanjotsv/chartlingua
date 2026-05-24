import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    sys.exit("Usage: python <script_name>.py <json_file_path>")

json_file_path = sys.argv[1]

with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

labels = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Create the main pie chart trace for the colored slices and inner percentage text.
# The domain is slightly reduced to prevent the outside labels from overlapping the slices.
pie_slices = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=colors, line=dict(color='white', width=3)),
    textinfo='percent',
    texttemplate='<b>%{percent}</b>',
    textposition='inside',
    insidetextfont=dict(family='Arial', size=20, color='white'),
    hoverinfo='label+percent',
    sort=False,
    direction='clockwise',
    startangle=25,
    domain=dict(x=[0.1, 0.9], y=[0.1, 0.9])
)

# Create a second, invisible pie trace to place the category labels outside.
# This is a robust method to have different text elements inside and outside the pie.
pie_labels = go.Pie(
    labels=labels,
    values=values,
    marker=dict(colors=['rgba(0,0,0,0)'] * len(values), line=dict(color='rgba(0,0,0,0)', width=1)),
    textinfo='label',
    textposition='outside',
    textfont=dict(family='Arial', size=16, color=colors),
    hoverinfo='none',
    showlegend=False,
    sort=False,
    direction='clockwise',
    startangle=25
)

fig = go.Figure(data=[pie_slices, pie_labels])

# Combine title and subtitle using HTML for better formatting.
title_text = f"<b>{texts['title']}</b><br><sub>{texts['subtitle']}</sub>"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top'
    ),
    title_font=dict(family='Arial', size=18, color='white'),
    showlegend=False,
    plot_bgcolor='black',
    paper_bgcolor='black',
    font=dict(family='Arial'),
    margin=dict(l=80, r=80, t=120, b=80)
)

# Derive output filename from the input JSON file path's base name.
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)