import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data_json = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)


data = chart_data_json['chart_data']
texts = chart_data_json['texts']
colors = chart_data_json['colors']

categories = [item['category'] for item in data]
values = [item['value'] for item in data]

# Reverse data for Plotly's horizontal bar chart rendering (top-to-bottom)
categories.reverse()
values.reverse()
colors.reverse()

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker_color=colors,
    text=values,
    texttemplate='%{text:.2f}',
    textposition='outside',
    hoverinfo='none',
    cliponaxis=False 
))

fig.update_layout(
    title=dict(
        text=texts['title'],
        font=dict(family="Arial", size=22, color='black'),
        x=0.01,
        y=0.95,
        xanchor='left',
        yanchor='top'
    ),
    font=dict(family="Arial", size=12, color='#333333'),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=150, r=50, t=100, b=80),
    xaxis=dict(
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        griddash='dash',
        zeroline=False,
        showline=False,
        ticks='outside',
        tickfont=dict(size=14),
        range=[0, 4],
        tick0=0,
        dtick=0.5
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        ticks='',
        tickfont=dict(size=14)
    ),
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.12,
            xanchor='left',
            yanchor='top',
            font=dict(family="Arial", size=12, color='#555555')
        ),
        dict(
            text=texts['note'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.12,
            xanchor='right',
            yanchor='top',
            font=dict(family="Arial", size=12, color='#555555')
        )
    ]
)

fig.update_traces(textfont_size=12, textfont_color='black')

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)