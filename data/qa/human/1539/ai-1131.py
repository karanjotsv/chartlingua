import sys
import os
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json>")
    sys.exit(1)

json_path = sys.argv[1]

if not os.path.exists(json_path):
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for Plotly's bottom-up plotting order
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
labels = [item['label'] for item in chart_data]

categories.reverse()
values.reverse()
labels.reverse()
colors.reverse()

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(
        color=colors,
        line=dict(width=0)
    ),
    text=labels,
    textposition='outside',
    textfont=dict(
        family='Arial',
        size=12,
        color='black'
    ),
    cliponaxis=False
))

# Combine title and subtitle using HTML
title_text = f"<b>{texts['title']}</b><br><span style='font-size: 14px; color: #555555;'>{texts['subtitle']}</span>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.01,
        y=0.95,
        xanchor='left',
        yanchor='top',
        font=dict(
            family='Arial',
            size=24,
            color='#333333'
        )
    ),
    xaxis=dict(
        showgrid=True,
        gridwidth=1,
        gridcolor='#E5E5E5',
        griddash='dot',
        zeroline=False,
        showline=False,
        showticklabels=True,
        ticks='outside',
        tickfont=dict(
            family='Arial',
            size=14,
            color='#333333'
        ),
        ticksuffix=' m³',
        range=[0, max(values) * 1.15] 
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        ticks='',
        tickfont=dict(
            family='Arial',
            size=14,
            color='#333333'
        ),
        categoryorder='array',
        categoryarray=categories
    ),
    margin=dict(l=150, r=80, t=120, b=80),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    font=dict(family="Arial"),
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=0, y=-0.12,
            xanchor='left', yanchor='top',
            text=texts['source'],
            showarrow=False,
            font=dict(family="Arial", size=12, color="#666666")
        ),
        dict(
            xref='paper', yref='paper',
            x=1, y=-0.12,
            xanchor='right', yanchor='top',
            text=texts['footer'],
            showarrow=False,
            font=dict(family="Arial", size=12, color="#666666")
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")