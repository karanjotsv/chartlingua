import sys
import json
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and decode the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# Extract data, texts, and colors from the JSON object
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Prepare data for Plotly: extract categories and transpose values
categories = [item['category'] for item in chart_data]
values_by_series = list(zip(*[item['values'] for item in chart_data]))

# Initialize a Figure object
fig = go.Figure()

# Add a bar trace for each data series
for i, series_values in enumerate(values_by_series):
    fig.add_trace(go.Bar(
        x=categories,
        y=list(series_values),
        name=texts['legend_labels'][i],
        marker_color=colors[i],
        text=[f'<b>{v}%</b>' for v in series_values],
        textposition='outside',
        textfont=dict(family='Arial', size=12, color='black'),
        cliponaxis=False
    ))

# Combine title and subtitle using HTML for rich text formatting
title_text = texts.get('title')
subtitle_text = texts.get('subtitle')
if title_text and subtitle_text:
    full_title = f"<b>{title_text}</b><br>{subtitle_text}"
elif title_text:
    full_title = f"<b>{title_text}</b>"
else:
    full_title = None

# Update the figure layout for a polished and accurate appearance
fig.update_layout(
    barmode='group',
    plot_bgcolor='white',
    font=dict(family="Arial", size=12),
    title=dict(
        text=full_title,
        x=0.05,
        xanchor='left'
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=12)
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        showgrid=True,
        gridcolor='#e5e5e5',
        ticksuffix='%',
        range=[0, max(max(v for v in s) for s in values_by_series) * 1.15] # Auto-range with 15% padding
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=80, r=40, t=50, b=150),
    annotations=[
        dict(
            showarrow=False,
            text=texts.get('source', ''),
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.38,
            xanchor='right',
            yanchor='bottom',
            align='right',
            font=dict(size=10)
        )
    ]
)

# Derive the output filename from the input JSON path
base_filename = json_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")