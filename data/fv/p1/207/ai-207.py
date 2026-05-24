import sys
import json
import plotly.graph_objects as go
import os

# Check for command-line argument
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)


# Extract data and texts
categories = chart_info['categories']
chart_data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

# Initialize figure
fig = go.Figure()

# Add bar traces
for i, series in enumerate(chart_data):
    fig.add_trace(go.Bar(
        x=categories,
        y=series['data'],
        name=series['name'],
        marker_color=colors[i]
    ))

# Find max value for annotation
first_series_data = chart_data[0]['data']
max_val = max(first_series_data)
max_idx = first_series_data.index(max_val)
max_year = categories[max_idx]

# Add horizontal line for max value
fig.add_shape(
    type="line",
    xref="paper", x0=0, x1=1,
    yref="y", y0=max_val, y1=max_val,
    line=dict(color="red", width=1)
)

# Add annotation for max value
fig.add_annotation(
    x=categories[-1],
    y=max_val,
    text=texts['annotation_text'],
    showarrow=False,
    xanchor='left',
    yanchor='middle',
    xshift=10,
    font=dict(color="red", size=10)
)


# Prepare custom x-axis tick labels
tick_texts = []
for i, year in enumerate(categories):
    value = first_series_data[i]
    if i == max_idx:
        label = f"{year}<br><span style='color:red; font-weight:bold;'>{value}</span>"
    else:
        label = f"{year}<br>{value}"
    tick_texts.append(label)

# Add header for the bottom data row
fig.add_annotation(
    text=f"<b>{texts['bottom_data_header']}</b>",
    align='left',
    showarrow=False,
    xref='paper',
    yref='paper',
    x=-0.06,
    y=-0.15,
    xanchor='left',
    yanchor='top'
)

# Update layout
fig.update_layout(
    barmode='group',
    title_text=f"<b>{texts['title']}</b><br>{texts['subtitle']}",
    title_x=0.05,
    title_xanchor='left',
    font=dict(family="Arial", size=12),
    plot_bgcolor='#E6EBF5',
    xaxis=dict(
        title=texts['x_axis_title'],
        title_standoff=15,
        title_font=dict(size=12),
        tickvals=categories,
        ticktext=tick_texts,
        tickangle=0,
        showgrid=False,
        domain=[0, 0.98] # Make space for Vereine label
    ),
    yaxis=dict(
        title=texts['y_axis_title'],
        range=[0, 150],
        tickvals=[0, 37.5, 75, 112.5, 150],
        gridcolor='white'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.4,
        xanchor="center",
        x=0.5
    ),
    margin=dict(t=80, b=150, l=60, r=60),
    bargap=0.2,
    bargroupgap=0.1
)

# Generate output filename from JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved as {output_filename}")