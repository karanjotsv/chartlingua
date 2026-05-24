import sys
import json
import plotly.graph_objects as go
from pathlib import Path

# --- 1. Load Data from JSON ---
# The script expects the JSON file path as the first and only command-line argument.
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = Path(sys.argv[1])
if not json_path.is_file():
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)

with open(json_path, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# --- 2. Prepare Data and Styles ---
chart_data = chart_info["chart_data"]
texts = chart_info["texts"]
colors = chart_info["colors"]

# Extract data into separate lists for Plotly
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]
labels = [item['label'] for item in chart_data]

# Reverse data for correct top-to-bottom display in Plotly horizontal bar charts
categories.reverse()
values.reverse()
labels.reverse()
colors.reverse()

# --- 3. Create the Chart ---
fig = go.Figure()

# Add the single bar trace
fig.add_trace(go.Bar(
    x=values,
    y=categories,
    orientation='h',
    marker=dict(color=colors, line=dict(width=0)),
    text=labels,
    textposition='outside',
    textfont=dict(family='Arial', size=12, color='#333333'),
    hoverinfo='none',
    cliponaxis=False
))

# --- 4. Configure Layout ---
# Combine title and subtitle using HTML for rich formatting
title_text = f"<b>{texts['title']}</b><br><span style='font-size: 15px; color:#5f5f5f;'>{texts['subtitle']}</span>"

fig.update_layout(
    # Title and Fonts
    title=dict(
        text=title_text,
        x=0.01,
        y=0.96,
        xanchor='left',
        yanchor='top'
    ),
    font=dict(family="Arial", size=12, color="black"),
    
    # Plot and Paper Background
    plot_bgcolor='white',
    paper_bgcolor='#f7f7f7',
    
    # Axes
    xaxis=dict(
        showgrid=True,
        gridcolor='#e0e0e0',
        gridwidth=1,
        zeroline=False,
        showline=False,
        showticklabels=True,
        side='bottom',
        tickformat=".2f",
        range=[0, max(values) * 1.15] # Add padding for text labels
    ),
    yaxis=dict(
        showgrid=False,
        showline=False,
        showticklabels=True,
        autorange=True,
        ticks='',
        tickfont=dict(size=14)
    ),
    
    # Legend and Margins
    showlegend=False,
    margin=dict(l=230, r=40, t=110, b=100),
    
    # Annotations for Source and Footer
    annotations=[
        dict(
            xref='paper', yref='paper',
            x=0.0, y=-0.15,
            xanchor='left', yanchor='top',
            text=texts['source_note'],
            showarrow=False,
            align='left',
            font=dict(size=11, color='#5f5f5f')
        ),
        dict(
            xref='paper', yref='paper',
            x=1.0, y=-0.15,
            xanchor='right', yanchor='top',
            text=texts['footer'],
            showarrow=False,
            align='right',
            font=dict(size=11, color='#5f5f5f')
        )
    ]
)

# --- 5. Save Output ---
output_filename = json_path.stem + ".png"
fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")