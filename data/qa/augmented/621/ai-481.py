import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# The script requires the path to the JSON file as a command-line argument.
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

# Read and parse the JSON file.
try:
    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Failed to decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data, texts, and colors from the loaded JSON.
chart_data = config.get('chart_data', [])
texts = config.get('texts', {})
colors = config.get('colors', [])

# --- 2. Prepare Data for Plotting ---
# Unpack the chart data into separate lists for Plotly.
categories = [item.get('category') for item in chart_data]
values = [item.get('value') for item in chart_data]

# --- 3. Create and Configure the Chart ---
# Initialize a Figure object.
fig = go.Figure()

# Add the bar trace to the figure.
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    marker_color=colors[0] if colors else None,
    text=values,
    textposition='outside',
    texttemplate='%{text}',
    cliponaxis=False  # Allow text labels to be drawn outside the plotting area.
))

# Update the layout of the figure for a clean, accurate look.
fig.update_layout(
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
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
        range=[0, 1050],  # Extend range slightly for top label padding.
        tickvals=[0, 200, 400, 600, 800, 1000],
        ticktext=['0', '200', '400', '600', '800', '1 000'], # Custom label for '1 000'
        gridcolor='#E0E0E0',
        gridwidth=1,
        griddash='dot',  # Match the dotted grid lines from the original image.
        zeroline=False,
        showline=False,
        tickfont=dict(size=12)
    ),
    margin=dict(l=90, r=40, t=60, b=100), # Adjust margins for titles and source.
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref="paper",
            yref="paper",
            x=0.98,
            y=-0.22,
            xanchor='right',
            yanchor='top',
            font=dict(size=12, color="#7f7f7f")
        )
    ] if texts.get('source') else []
)

# Customize the font for the text on the bars.
fig.update_traces(textfont_size=12, textfont_color='black')

# --- 4. Save the Output ---
# Derive the output filename from the input JSON file's base name.
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG image.
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to '{output_filename}'")