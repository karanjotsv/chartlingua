import sys
import json
import plotly.graph_objects as go
import os

# --- 1. Load Data from JSON ---
# The script expects the JSON file path as the first and only command-line argument.
if len(sys.argv) != 2:
    print("Usage: python create_chart.py <path_to_json_file>")
    sys.exit(1)

json_path = sys.argv[1]

try:
    with open(json_path, 'r', encoding='utf-8') as f:
        chart_data = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_path}")
    sys.exit(1)

# --- 2. Extract Data and Texts ---
data_left = chart_data["chart_data"][0]
data_right = chart_data["chart_data"][1]
texts = chart_data["texts"]
colors = chart_data["colors"]

# --- 3. Create Figure and Traces ---
fig = go.Figure()

# Left chart trace (Key Elements)
fig.add_trace(go.Bar(
    x=data_left['categories'],
    y=data_left['values'],
    text=data_left['text_labels'],
    textposition='outside',
    marker_color=colors[0],
    name=data_left['name'],
    cliponaxis=False,
    textfont=dict(family="Arial", size=14, color='black')
))

# Right chart trace (Trace Elements)
fig.add_trace(go.Bar(
    x=data_right['categories'],
    y=data_right['values'],
    marker_color=colors[1],
    name=data_right['name'],
    xaxis='x2',
    yaxis='y2'
))


# --- 4. Configure Layout ---
fig.update_layout(
    # General styling
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(family="Arial", size=12, color='black'),
    
    # Main title
    title=dict(
        text=texts['main_title'],
        x=0.5,
        y=0.95,
        font=dict(size=20, weight='bold')
    ),
    
    # Margins to prevent clipping
    margin=dict(l=60, r=40, t=100, b=100),
    
    # Left chart axes
    xaxis=dict(
        domain=[0.0, 0.28],
        showgrid=False,
        zeroline=False,
        showline=False,
        tickfont=dict(size=14)
    ),
    yaxis=dict(
        domain=[0.0, 0.7],
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=False,
        range=[0, 105]
    ),
    
    # Right chart axes
    xaxis2=dict(
        domain=[0.45, 1.0],
        anchor='y2',
        showgrid=False,
        zeroline=False,
        showline=False,
        tickfont=dict(size=14)
    ),
    yaxis2=dict(
        domain=[0.0, 0.7],
        anchor='x2',
        title=dict(
            text=data_right['y_axis_title'],
            standoff=5,
            font=dict(size=14)
        ),
        gridcolor='#e0e0e0',
        range=[0, 160],
        tickfont=dict(size=14)
    ),
    
    # Annotations for subplot titles and pointer
    annotations=[
        # Left chart title
        dict(
            text=f"<b>{data_left['name']}</b>",
            x=0.14, y=0.82,
            xref='paper', yref='paper',
            showarrow=False,
            font=dict(size=16)
        ),
        # Right chart title
        dict(
            text=f"<b>{data_right['name']}</b>",
            x=0.725, y=0.82,
            xref='paper', yref='paper',
            showarrow=False,
            font=dict(size=16)
        ),
        # "Trace" text
        dict(
            text=texts['annotation_text_1'],
            x=0.36, y=0.18,
            xref='paper', yref='paper',
            showarrow=False,
            font=dict(size=14)
        ),
        # "See Right" text
        dict(
            text=texts['annotation_text_2'],
            x=0.36, y=0.1,
            xref='paper', yref='paper',
            showarrow=False,
            font=dict(size=14),
            align='center'
        ),
        # Arrow pointing right
        dict(
            x=0.43, y=0.12,
            xref='paper', yref='paper',
            showarrow=True,
            arrowhead=2,
            arrowsize=1.5,
            arrowwidth=2,
            arrowcolor=colors[1],
            ax=-50, ay=0, # Arrow starts 50 pixels to the left of the x,y point
            text="" # No text for the arrow itself
        )
    ]
)

# --- 5. Output Image ---
# Derive the output filename from the input JSON filename
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

# Save the figure as a high-resolution PNG file
fig.write_image(output_filename, scale=2, width=900, height=500)

print(f"Chart saved to {output_filename}")