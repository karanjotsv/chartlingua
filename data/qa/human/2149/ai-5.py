import sys
import json
import plotly.graph_objects as go

# Ensure a JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: The file '{json_path}' was not found.")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: The file '{json_path}' contains invalid JSON.")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# Prepare data for Plotly traces
categories = [item['category'] for item in chart_data]
num_series = len(texts.get('legend_labels', []))
series_data = [[item['values'][i] for item in chart_data] for i in range(num_series)]

# Initialize the figure
fig = go.Figure()

# Add a bar trace for each series defined in the JSON
for i in range(num_series):
    fig.add_trace(go.Bar(
        x=categories,
        y=series_data[i],
        name=texts['legend_labels'][i],
        marker_color=colors[i],
        text=[f"{val}%" for val in series_data[i]],
        textposition='outside',
        cliponaxis=False
    ))

# Construct the title string from title and subtitle
title_text = ""
if texts.get('title'):
    title_text += f"<b>{texts['title']}</b>"
if texts.get('subtitle'):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Configure the chart layout
fig.update_layout(
    barmode='group',
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    title=dict(text=title_text, x=0.05),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        categoryorder='array',
        categoryarray=categories,
        showline=True,
        linecolor='black',
        ticks='outside'
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 70],
        tickvals=[0, 10, 20, 30, 40, 50, 60, 70],
        ticktext=[f'{i}%' for i in range(0, 71, 10)],
        gridcolor='#EAEAEA',
        zeroline=False
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.3,
        xanchor="center",
        x=0.5
    ),
    margin=dict(l=80, r=40, b=150, t=60),
    annotations=[
        dict(
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.38,
            xanchor='right',
            yanchor='bottom',
            text=texts.get('source', ''),
            font=dict(size=10, color='grey')
        )
    ]
)

# Determine the output filename and save the chart as a PNG image
base_filename = json_path.rsplit('.', 1)[0]
output_filename = f"{base_filename}.png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")