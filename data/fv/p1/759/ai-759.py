import sys
import json
import os
import plotly.graph_objects as go

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

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
xaxis_ticks = chart_data['xaxis_ticks']

fig = go.Figure()

# Add the main line and markers trace
fig.add_trace(go.Scatter(
    x=[d['x'] for d in data],
    y=[d['y'] for d in data],
    mode='lines+markers',
    line=dict(color=colors['line'], width=2),
    marker=dict(
        color=colors['marker_fill'],
        size=8,
        line=dict(color=colors['marker_line'], width=1)
    ),
    showlegend=False
))

# Prepare annotations for each data point
annotations = []
for point in data:
    anno_details = point['annotation']
    annotations.append(
        dict(
            x=point['x'],
            y=point['y'],
            text=point['label'],
            showarrow=False,
            font=dict(family="Arial", size=12, color=colors['annotation_font']),
            textangle=anno_details['angle'],
            xanchor=anno_details['xanchor'],
            yanchor=anno_details['yanchor'],
            xshift=anno_details['xshift'],
            yshift=anno_details['yshift'],
        )
    )

# Add the special 'Linear plot' annotation
annotations.append(
    dict(
        text=texts['annotation_label'],
        align='center',
        showarrow=False,
        xref='x',
        yref='paper',
        x=2.5e9,
        y=1.07,
        bgcolor=colors['annotation_background'],
        bordercolor=colors['annotation_border'],
        borderwidth=1,
        borderpad=4
    )
)

fig.update_layout(
    title=dict(
        text=texts['title'],
        font=dict(
            family="Arial",
            size=20,
            color=colors['title_font']
        ),
        x=0.05,
        y=0.95,
        xanchor='left',
        yanchor='top'
    ),
    xaxis=dict(
        title=texts['x_axis_title'],
        autorange='reversed',
        tickvals=xaxis_ticks['values'],
        ticktext=xaxis_ticks['text'],
        gridcolor=colors['grid'],
        zeroline=False,
        title_font=dict(size=14),
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        type='log',
        exponentformat='power',
        gridcolor=colors['grid'],
        zeroline=False,
        title_font=dict(size=14),
        tickfont=dict(size=12)
    ),
    font=dict(
        family="Arial",
        color=colors['axis_font']
    ),
    plot_bgcolor=colors['plot_background'],
    paper_bgcolor=colors['background'],
    margin=dict(l=100, r=50, t=100, b=80),
    annotations=annotations
)

fig.write_image(output_filename, scale=2)
print(f"Chart saved to {output_filename}")