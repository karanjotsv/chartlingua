import sys
import json
import plotly.graph_objects as go
import pathlib

# --- 1. Load data from JSON file ---
# Check if a command-line argument is provided
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

# Get the JSON file path from the command-line argument
json_file_path = pathlib.Path(sys.argv[1])

# Check if the JSON file exists
if not json_file_path.is_file():
    print(f"Error: File not found at {json_file_path}")
    sys.exit(1)

# Construct the output image filename from the JSON filename
output_filename = json_file_path.with_suffix('.png').name

# Read the JSON data
with open(json_file_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# Extract data, texts, and colors from the loaded JSON
chart_data = chart_info.get("chart_data", [])
texts = chart_info.get("texts", {})
colors = chart_info.get("colors", [])

# --- 2. Prepare data for Plotly ---
# Extract categories and values from chart_data, preserving order
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# Format bar text with a space as a thousand separator and bold tag
bar_text = [f"<b>{v:,}</b>".replace(',', ' ') for v in values]

# --- 3. Create the Plotly figure ---
# Initialize the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=categories,
    y=values,
    text=bar_text,
    textposition='auto',
    marker_color=colors[0],
    insidetextanchor='end'
))

# --- 4. Configure layout and styling ---
# Define y-axis tick values and format their labels
y_axis_ticks_values = [0, 2500, 5000, 7500, 10000, 12500, 15000]
y_axis_ticks_text = [f"{v:,}".replace(',', ' ') for v in y_axis_ticks_values]

fig.update_layout(
    # Chart titles (not present in this chart)
    title_text=texts.get("title"),
    title_x=0.05,

    # General styling
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    font=dict(family="Arial", size=12, color='black'),
    
    # X-axis styling
    xaxis=dict(
        title_text=texts.get("x_axis_title"),
        showgrid=False,
        showline=True,
        linecolor='black',
        linewidth=1,
        tickfont=dict(size=12)
    ),

    # Y-axis styling
    yaxis=dict(
        title_text=texts.get("y_axis_title"),
        showgrid=True,
        gridcolor='#E0E0E0',
        gridwidth=1,
        showline=False,
        range=[0, 15000],
        tickvals=y_axis_ticks_values,
        ticktext=y_axis_ticks_text,
        tickfont=dict(size=12)
    ),

    # Margins to prevent labels/annotations from being cut off
    margin=dict(l=90, r=40, b=100, t=50),

    # Annotations for source text
    annotations=[
        dict(
            text=texts.get("source"),
            showarrow=False,
            xref="paper", yref="paper",
            x=1.0, y=-0.15,
            xanchor='right', yanchor='top',
            font=dict(size=11, color='#555555')
        )
    ]
)

# Update trace-specific styling for text on bars
fig.update_traces(textfont_size=12, textfont_color='black')


# --- 5. Output the chart as a PNG image ---
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved as {output_filename}")