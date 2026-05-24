import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)


data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

categories = [d['category'] for d in data]
values_left = [-d['values'][0] for d in data]
values_right = [d['values'][1] for d in data]
text_left = [d['values'][0] for d in data]
text_right = [d['values'][1] for d in data]

# Reverse data for top-to-bottom display in Plotly
categories.reverse()
values_left.reverse()
values_right.reverse()
text_left.reverse()
text_right.reverse()

fig = go.Figure()

# Left side bars (negative values)
fig.add_trace(go.Bar(
    y=categories,
    x=values_left,
    orientation='h',
    text=text_left,
    textposition='inside',
    insidetextanchor='middle',
    marker=dict(color=colors[0], line=dict(width=0)),
    hoverinfo='none',
    showlegend=False,
    textfont=dict(color='black', size=12, family='Arial')
))

# Right side bars (positive values)
fig.add_trace(go.Bar(
    y=categories,
    x=values_right,
    orientation='h',
    text=text_right,
    textposition='inside',
    insidetextanchor='middle',
    marker=dict(color=colors[1], line=dict(width=0)),
    hoverinfo='none',
    showlegend=False,
    textfont=dict(color='white', size=12, family='Arial')
))

title_text = f"<b>{texts['title']}</b><br><span style='font-size:14px;color:grey;'>{texts['subtitle']}</span>"

fig.update_layout(
    barmode='relative',
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color="black"),
    title=dict(
        text=title_text,
        y=0.98,
        x=0.01,
        xanchor='left',
        yanchor='top',
        font=dict(size=18)
    ),
    margin=dict(l=150, r=20, t=140, b=100, pad=5),
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        showticklabels=False,
        title_text='',
        range=[-90, 90]
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        title_text='',
        tickmode='array',
        tickvals=categories,
        ticktext=[cat for cat in categories],
        ticks='',
        domain=[0, 0.9]
    ),
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=0.48, y=0.90,
            xanchor='right', yanchor='bottom',
            text=texts['series_labels'][0],
            font=dict(family='Arial', size=12, color=colors[0]),
            align='right',
            showarrow=False
        ),
        dict(
            xref='paper', yref='paper',
            x=0.52, y=0.90,
            xanchor='left', yanchor='bottom',
            text=texts['series_labels'][1],
            font=dict(family='Arial', size=12, color=colors[1]),
            align='left',
            showarrow=False
        ),
        dict(
            xref='paper', yref='paper',
            x=0.0, y=-0.15,
            xanchor='left', yanchor='top',
            text=texts['source'],
            font=dict(family='Arial', size=10, color='grey'),
            align='left',
            showarrow=False
        )
    ],
    shapes=[
        dict(
            type='line',
            xref='x', yref='paper',
            x0=0, y0=0,
            x1=0, y1=0.9,
            line=dict(color='grey', width=1)
        )
    ]
)

base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2, width=600, height=650)
print(f"Chart saved as {output_filename}")