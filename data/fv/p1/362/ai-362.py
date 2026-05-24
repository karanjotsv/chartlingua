import sys
import json
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read data from the specified JSON file
with open(json_file_path, 'r', encoding='utf-8') as f:
    config = json.load(f)

# Extract data for plotting
chart_data = config['chart_data']
texts = config['texts']
colors = config['colors']
categories = chart_data['categories']
series_list = chart_data['series']

# Initialize the figure
fig = go.Figure()

# Add a trace for each data series
for i, series in enumerate(series_list):
    fig.add_trace(go.Scatter(
        x=categories,
        y=series['values'],
        name=series['name'],
        mode='lines',
        line=dict(color=colors[i], width=2)
    ))

# Combine title and subtitle if both exist
title_text = texts['title']
if texts.get('subtitle'):
    title_text = f"<b>{texts['title']}</b><br><sub>{texts['subtitle']}</sub>"
else:
    title_text = f"<b>{texts['title']}</b>"


# Update the layout of the chart
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.95,
        x=0.5,
        xanchor='center',
        yanchor='top',
        font=dict(size=18)
    ),
    xaxis_title=texts['x_axis_label'],
    yaxis_title=texts['y_axis_label'],
    font=dict(
        family="Arial",
        size=12
    ),
    template="plotly_white",
    xaxis=dict(
        showgrid=False,
        tickmode='array',
        tickvals=categories,
        ticktext=[str(year) for year in categories]
    ),
    yaxis=dict(
        range=[-14000, 4000],
        dtick=2000,
        showgrid=True,
        gridcolor='lightgray',
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1
    ),
    legend=dict(
        orientation="v",
        yanchor="top",
        y=0.8,
        xanchor="left",
        x=1.01,
        bgcolor='rgba(0,0,0,0)'
    ),
    margin=dict(l=80, r=80, t=80, b=50),
    plot_bgcolor='white',
    width=700,
    height=500
)

# Determine the output filename from the input JSON path
base_filename = json_file_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"

# Save the figure to a PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")