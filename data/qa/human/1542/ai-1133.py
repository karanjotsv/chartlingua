import sys
import json
import plotly.graph_objects as go
import os

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_details = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

chart_data = chart_details['chart_data']
texts = chart_details['texts']
colors = chart_details['colors']

categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Reverse data to display from top to bottom in the same order as the JSON
categories.reverse()
values.reverse()
colors.reverse()

fig = go.Figure()

fig.add_trace(go.Bar(
    x=values,
    y=categories,
    orientation='h',
    marker=dict(color=colors),
    text=[f'{v} t' for v in values],
    textposition='outside',
    textfont=dict(family='Arial', size=12, color='#333333'),
    hoverinfo='none',
    cliponaxis=False
))

title_text = f"<b>{texts['title']}</b><br><span style='font-size:15px;color:#555555;'>{texts['subtitle']}</span>"

fig.update_layout(
    title=dict(
        text=title_text,
        x=0.02,
        y=0.96,
        xanchor='left',
        yanchor='top',
        font=dict(size=24)
    ),
    font=dict(family="Arial", size=12, color='#333333'),
    xaxis=dict(
        showgrid=True,
        gridcolor='#EAEAEA',
        zeroline=False,
        showline=False,
        ticks='outside',
        tickfont=dict(size=14),
        ticksuffix=' t',
        range=[0, max(values) * 1.15],
        dtick=2
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        tickfont=dict(size=14),
        automargin=True
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=10, r=50, t=100, b=80),
    showlegend=False,
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
            font=dict(size=12, color='#888888')
        ),
        dict(
            text=texts['credit'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1,
            y=-0.12,
            xanchor='right',
            yanchor='top',
            font=dict(size=12, color='#888888')
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2, width=900, height=600)

print(f"Chart saved to {output_filename}")