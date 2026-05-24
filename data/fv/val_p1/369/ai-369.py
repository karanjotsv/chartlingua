import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_path = pathlib.Path(sys.argv[1])

# Read and parse the JSON file
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    print(f"Error reading or parsing JSON file: {e}")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_info.get('chart_data', [])
texts = chart_info.get('texts', {})
colors = chart_info.get('colors', [])

# --- 2. Create the Chart ---
# Initialize a Figure object
fig = go.Figure()

# Add a bar trace for each data series specified in the JSON
for i, series in enumerate(chart_data):
    color = colors[i % len(colors)] # Cycle through colors if not enough are provided
    fig.add_trace(go.Bar(
        name=series.get('name'),
        x=[series.get('name')],  # Use the series name as the x-axis category
        y=series.get('y'),
        marker_color=color,
        text=series.get('text'),
        textfont=dict(
            color=series.get('text_color', 'black'),
            family="Arial"
        ),
        error_y=dict(
            type='data',
            array=series.get('error_y', {}).get('plus'),
            arrayminus=series.get('error_y', {}).get('minus'),
            visible=True,
            color='dimgray',
            thickness=1.5
        )
    ))

# Set the text position to be inside the bars
fig.update_traces(textposition='inside', insidetextanchor='middle')


# --- 3. Configure Layout and Styling ---
# Combine title and subtitle if they exist
title_parts = []
if texts.get('title'):
    title_parts.append(texts['title'])
if texts.get('subtitle'):
    # Make subtitle smaller
    title_parts.append(f'<br><span style="font-size:0.8em; color:gray;">{texts["subtitle"]}</span>')
final_title = "<br>".join(title_parts)

# Update the layout of the figure
fig.update_layout(
    title_text=final_title,
    xaxis_title=texts.get('x_axis_title'),
    yaxis_title=texts.get('y_axis_title'),
    font=dict(family="Arial", size=12, color="black"),
    plot_bgcolor='white',
    paper_bgcolor='white',
    legend=dict(
        orientation='h',
        yanchor='bottom',
        y=1.02,
        xanchor='left',
        x=0,
        traceorder='normal'
    ),
    yaxis=dict(
        showgrid=True,
        gridcolor='#dddddd',
        zeroline=True,
        zerolinecolor='black',
        zerolinewidth=1,
        range=[-250, 650] # Set range to provide padding
    ),
    xaxis=dict(
        showgrid=False,
        showline=False,
        zeroline=False
    ),
    margin=dict(l=60, r=40, b=80, t=80) # Adjust margins to prevent clipping
)

# --- 4. Output the Chart ---
# Derive the output filename from the input JSON filename
output_filename = json_path.stem + ".png"

# Save the figure as a PNG image
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")