import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
# The script expects the path to the JSON file as the first command-line argument.
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_file_path = sys.argv[1]

try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# --- 2. Extract Data and Texts ---
chart_data = chart_config.get('chart_data', {})
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])
categories = chart_data.get('categories', [])
series = chart_data.get('series', [])

# --- 3. Create the Chart Figure ---
fig = go.Figure()

# Add traces (bars) by iterating through the series data
for i, s in enumerate(series):
    fig.add_trace(go.Bar(
        x=categories,
        y=s.get('data', []),
        name=s.get('name', ''),
        marker_color=colors[i % len(colors)],
        text=s.get('data', []),
        textposition='inside',
        textfont=dict(
            family='Arial',
            size=12,
            color=s.get('text_color', 'black'),
            weight='bold'
        ),
        texttemplate='%{text}',
        hoverinfo='skip'
    ))

# --- 4. Configure Layout and Styling ---
# Build annotations for footer text
annotations = []
if texts.get('footer_left'):
    annotations.append(
        go.layout.Annotation(
            text=texts['footer_left'],
            align='left',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.3,
            xanchor='left',
            yanchor='bottom'
        )
    )

source_parts = [texts.get('source'), texts.get('note')]
source_text = "<br>".join(filter(None, source_parts))
if source_text:
    annotations.append(
        go.layout.Annotation(
            text=source_text,
            align='right',
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.3,
            xanchor='right',
            yanchor='bottom'
        )
    )

fig.update_layout(
    barmode='stack',
    font=dict(family="Arial", size=12),
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=80, r=40, t=50, b=150),
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
        range=[0, 120],
        tickvals=[0, 20, 40, 60, 80, 100, 120],
        showgrid=True,
        gridcolor='#E5E5E5',
        griddash='dot',
        tickfont=dict(size=12)
    ),
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    ),
    annotations=annotations,
    showlegend=True
)

# --- 5. Output the Image ---
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_filename = f"{base_filename}.png"

try:
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")
except ValueError as e:
    if "requires the kaleido package" in str(e):
        print("Error: The 'kaleido' package is required to save images.")
        print("Please install it using: pip install kaleido")
    else:
        print(f"An error occurred while saving the image: {e}")
    sys.exit(1)