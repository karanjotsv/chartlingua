import sys
import json
import pathlib
import plotly.graph_objects as go

# --- 1. Load data from JSON file provided as a command-line argument ---
if len(sys.argv) < 2:
    print("Usage: python generate_chart.py <path_to_json_file>")
    sys.exit(1)

json_filepath = pathlib.Path(sys.argv[1])
if not json_filepath.is_file():
    print(f"Error: File not found at {json_filepath}")
    sys.exit(1)

with open(json_filepath, 'r', encoding='utf-8') as f:
    chart_info = json.load(f)

# --- 2. Extract data and text for plotting ---
data = chart_info['chart_data']
texts = chart_info['texts']
colors = chart_info['colors']

categories = [d['category'] for d in data]
values = [d['value'] for d in data]
text_labels = [f'{v}%' for v in values]

# --- 3. Create the Plotly figure ---
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors),
    text=text_labels,
    textposition='outside',
    cliponaxis=False  # Allows text to be drawn outside the plotting area
))

# --- 4. Configure the layout and styling ---
fig.update_layout(
    # Set global font properties
    font=dict(family="Arial", size=14, color='#333333'),

    # Title configuration
    title=dict(
        text=texts['title'],
        font=dict(size=22),
        x=0.01,
        y=0.98,
        xanchor='left',
        yanchor='top'
    ),

    # X-Axis configuration
    xaxis=dict(
        range=[0, max(values) * 1.1],  # Set range to give space for text labels
        showgrid=True,
        gridcolor='#e0e0e0',
        zeroline=False,
        showline=False,
        showticklabels=True,
        ticksuffix='%'
    ),

    # Y-Axis configuration
    yaxis=dict(
        autorange='reversed',  # Ensures the order matches the original chart (top to bottom)
        showgrid=False,
        showline=False,
        ticks='',
        tickfont=dict(size=14)
    ),

    # General plot aesthetics
    plot_bgcolor='white',
    paper_bgcolor='white',
    bargap=0.35,

    # Margins to prevent clipping of titles, labels, and source note
    margin=dict(l=120, r=60, t=100, b=140),

    # Add source and note as a single annotation at the bottom
    annotations=[
        dict(
            text=texts['source_note'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=0,
            y=-0.18,  # Position below the x-axis
            xanchor='left',
            yanchor='top',
            align='left',
            font=dict(size=12, color='#666666')
        )
    ],
    
    # Disable the legend as it's not needed
    showlegend=False
)

# --- 5. Save the figure to a PNG file ---
output_filename = json_filepath.with_suffix('.png')
fig.write_image(output_filename, scale=2, width=800, height=600)

print(f"Chart saved to {output_filename}")