import sys
import json
import plotly.graph_objects as go
import pathlib

# Check if a command-line argument is provided
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read data from the JSON file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data, texts, and colors from the JSON structure
data_entries = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

# Reverse the data and colors to match Plotly's bottom-up rendering for horizontal bars
data_entries.reverse()
colors.reverse()

# Prepare data for Plotly trace
y_categories = [d['category'] for d in data_entries]
x_values = [d['value'] for d in data_entries]
bar_labels = [d['label'] for d in data_entries]

# Create the figure
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=y_categories,
    x=x_values,
    orientation='h',
    marker=dict(color=colors),
    text=bar_labels,
    textposition='outside',
    cliponaxis=False,
    textfont=dict(family="Arial", size=12, color='black')
))

# Combine title and subtitle using HTML for rich text formatting
title_text = f"<b>{texts['title']}</b><br><span style='font-size:14px;color:#555555;'>{texts['subtitle']}</span>"

# Update layout for a clean and accurate presentation
fig.update_layout(
    title=dict(
        text=title_text,
        y=0.98,
        x=0.01,
        xanchor='left',
        yanchor='top',
        font=dict(size=22)
    ),
    xaxis=dict(
        showgrid=True,
        gridcolor='#E5E5E5',
        gridwidth=1,
        griddash='dash',
        zeroline=False,
        ticks='outside',
        tickformat='%g%%',
        range=[0, 85],  # Extend range to fit outside text labels
        showline=False
    ),
    yaxis=dict(
        showgrid=False,
        ticks='',
        showline=False,
        categoryorder='array',
        categoryarray=y_categories, # Explicitly set category order
        tickfont=dict(size=14)
    ),
    font=dict(
        family="Arial"
    ),
    plot_bgcolor='white',
    showlegend=False,
    margin=dict(l=100, r=40, t=140, b=80),
    annotations=[
        dict(
            text=texts['source'],
            xref="paper", yref="paper",
            x=0, y=-0.1,
            xanchor='left', yanchor='top',
            showarrow=False,
            font=dict(size=12, color='#555555')
        ),
        dict(
            text=texts['cc_by'],
            xref="paper", yref="paper",
            x=1, y=-0.1,
            xanchor='right', yanchor='top',
            showarrow=False,
            font=dict(size=12, color='#555555')
        )
    ]
)

# Derive output filename from the input JSON filename
output_path = pathlib.Path(json_file_path).with_suffix('.png')

# Save the figure as a high-resolution PNG image
fig.write_image(str(output_path), scale=2)

print(f"Chart successfully generated and saved to {output_path}")