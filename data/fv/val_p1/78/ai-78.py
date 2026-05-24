import sys
import json
import plotly.graph_objects as go
import os

# --- 1. Load Data from JSON ---
# The script expects the JSON file path as the first command-line argument.
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_path}'")
    sys.exit(1)

# Extract data and text from the loaded JSON
chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', {})

# --- 2. Create the Plotly Figure ---
fig = go.Figure()

# --- 3. Add Bar Trace ---
fig.add_trace(go.Bar(
    x=[item['category'] for item in chart_data],
    y=[item['value'] for item in chart_data],
    text=[f"{item['value']:.1f}" for item in chart_data],
    textposition='auto',
    marker_color=colors.get('bar_color', '#F4A55A'),
    hoverinfo='none'
))

# --- 4. Configure Layout, Titles, and Annotations ---
# Combine title and subtitle using HTML for styling
title_html = (
    f"<span style='background-color:{colors.get('title_background', '#9985B6')}; color:{colors.get('title_font', '#FFFFFF')}; padding: 10px 15px; font-size: 22px;'>"
    f"<b>{texts.get('title', '')}</b></span>"
    f"<br><br><span style='font-size: 16px;'>{texts.get('subtitle', '')}</span>"
)

# Custom annotations for y-axis labels
y_axis_annotations = []
for label_info in texts.get('y_axis_labels', []):
    y_axis_annotations.append(
        go.layout.Annotation(
            text=label_info['text'],
            align='right',
            showarrow=False,
            xref='paper',
            yref='y',
            x=-0.08,
            y=label_info['value'],
            xanchor='right',
            yanchor='middle'
        )
    )

# Annotation for the bottom note and survey source
bottom_annotations = [
    go.layout.Annotation(
        text=texts.get('source_note', ''),
        showarrow=False,
        xref='paper',
        yref='paper',
        x=0.0,
        y=-0.25,
        xanchor='left',
        yanchor='top',
        align='left'
    ),
    go.layout.Annotation(
        text=texts.get('source_survey', ''),
        showarrow=False,
        xref='paper',
        yref='paper',
        x=1.0,
        y=-0.25,
        xanchor='right',
        yanchor='top',
        align='right'
    )
]

fig.update_layout(
    title_text=title_html,
    title_x=0.5,
    title_y=0.95,
    title_font_color=colors.get('text_main', '#000000'),
    font=dict(family="Arial", size=12, color=colors.get('text_main', '#000000')),
    plot_bgcolor='white',
    paper_bgcolor='white',
    showlegend=False,
    margin=dict(l=100, r=40, t=140, b=150),
    xaxis=dict(
        showline=True,
        linewidth=1,
        linecolor='black',
        tickfont=dict(size=11)
    ),
    yaxis=dict(
        range=[0, 5.5],
        tickvals=[1.0, 2.0, 3.0, 4.0, 5.0],
        ticktext=['1.0', '2.0', '3.0', '4.0', '5.0'],
        gridcolor=colors.get('grid', '#D3D3D3'),
        zeroline=False,
        showline=True,
        linewidth=1,
        linecolor='black'
    ),
    annotations=y_axis_annotations + bottom_annotations,
    shapes=[
        go.layout.Shape(
            type="rect",
            xref="x",
            yref="y",
            x0=len(chart_data) - 1.5,
            y0=0,
            x1=len(chart_data) - 0.5,
            y1=5.0,
            line=dict(
                color="Black",
                width=2,
            )
        )
    ]
)

fig.update_traces(
    texttemplate='%{text}', 
    textfont_size=12,
    insidetextanchor='end',
    textangle=0
)

# --- 5. Output the Image ---
# Derive the output filename from the input JSON path
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2, width=800, height=600)

print(f"Chart successfully generated and saved to '{output_filename}'")