import sys
import json
import os
import plotly.graph_objects as go

# Check for command-line argument
if len(sys.argv) != 2:
    print(f"Usage: python {os.path.basename(__file__)} <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read data from the specified JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_file_path}'")
    sys.exit(1)

# Extract data and texts from the JSON structure
categories = [item['category'] for item in chart_data['chart_data']]
series_names = chart_data['series_names']
texts = chart_data['texts']
colors = chart_data['colors']

# Create the figure object
fig = go.Figure()

# Add a bar trace for each data series
for i, series_name in enumerate(series_names):
    y_values = [item['values'][i] for item in chart_data['chart_data']]
    fig.add_trace(go.Bar(
        x=categories,
        y=y_values,
        name=series_name,
        marker_color=colors[i],
        text=y_values,
        textposition='outside',
        textfont=dict(
            family="Arial",
            size=12,
            color='black'
        ),
        cliponaxis=False # Allows text to render outside the plot area
    ))

# Combine title and subtitle if they exist
title_text = ""
if texts.get("title"):
    title_text += texts["title"]
if texts.get("subtitle"):
    title_text += f"<br><sub>{texts['subtitle']}</sub>"

# Update layout for a professional appearance
fig.update_layout(
    barmode='group',
    title=dict(
        text=title_text if title_text else None
    ),
    xaxis=dict(
        title_text=texts.get('x_axis_title'),
        tickangle=-45,
        automargin=True
    ),
    yaxis=dict(
        title_text=texts.get('y_axis_title'),
        range=[0, 250],
        showgrid=True,
        gridcolor='#e5e5e5'
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.4, # Position legend below x-axis labels
        xanchor="center",
        x=0.5
    ),
    font=dict(
        family="Arial",
        size=12,
        color="black"
    ),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=60, r=40, t=40, b=150), # Increased bottom margin for legend and labels
    annotations=[
        dict(
            showarrow=False,
            text=texts.get('source', ''),
            xref="paper",
            yref="paper",
            x=1.0,
            y=-0.38, # Position source below legend
            xanchor='right',
            yanchor='bottom',
            font=dict(
                size=12
            )
        )
    ]
)

# Determine the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure to a high-resolution PNG file
fig.write_image(output_filename, scale=2)

print(f"Chart successfully generated and saved to '{output_filename}'")