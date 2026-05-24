import sys
import json
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Data is ordered top-to-bottom in JSON, but Plotly plots bottom-to-top.
# Reverse all data lists to maintain the original visual order.
categories = [d['category'] for d in chart_data][::-1]
values = [d['value'] for d in chart_data][::-1]
reversed_colors = colors[::-1]

fig = go.Figure()

fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker_color=reversed_colors,
    text=[f"{v:.2f}" for v in values],
    textposition='outside',
    textfont=dict(family="Arial", size=12, color='black'),
    cliponaxis=False,
    showlegend=False
))

# Combine title and subtitle using HTML
title_text = f"<b>{texts['title']}</b><br><span style='font-size:15px;color:#555555;'>{texts['subtitle']}</span>"

fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.01,
        xanchor='left',
        yanchor='top'
    ),
    font=dict(
        family="Arial",
        size=14
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=90, r=40, t=140, b=80),
    xaxis=dict(
        showgrid=True,
        gridcolor='#e9e9e9',
        gridwidth=1,
        zeroline=False,
        showline=False,
        ticks='outside',
        tickcolor='lightgrey',
        range=[0, max(values) * 1.08] # Give extra space for text labels
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        ticks='',
        categoryorder='array',
        categoryarray=categories
    ),
    annotations=[
        dict(
            text=texts['source_note'],
            align='left',
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
            text=texts['right_note'],
            align='right',
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

# Derive output filename from JSON path
base_filename = json_file_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")