import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at '{json_file_path}'")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from '{json_file_path}'")
    sys.exit(1)

chart_data = chart_config.get('chart_data', [])
texts = chart_config.get('texts', {})
colors = chart_config.get('colors', [])

# --- 2. Prepare Data for Plotting ---
categories = [item['category'] for item in chart_data]
values = [item['value'] for item in chart_data]

# --- 3. Create the Chart Figure ---
fig = go.Figure()

# --- 4. Add Bar Trace ---
fig.add_trace(go.Bar(
    y=categories,
    x=values,
    orientation='h',
    marker=dict(color=colors[0]),
    text=values,
    textposition='outside',
    texttemplate='%{text:.2f}',
    cliponaxis=False # Ensures text outside the bar is not clipped
))

# --- 5. Configure Layout ---
fig.update_layout(
    # Set global font properties
    font=dict(family="Arial", size=12, color="black"),
    
    # Title and Subtitle (handled by annotations if complex, or title attribute)
    title=dict(text=texts.get('title'), x=0.05, xanchor='left'),

    # X-Axis styling
    xaxis=dict(
        title=texts.get('x_axis_title'),
        showgrid=True,
        gridcolor='#E0E0E0',
        griddash='dot',
        zeroline=False,
        showline=False,
        range=[0, max(values) * 1.15] # Add padding for text labels
    ),
    
    # Y-Axis styling
    yaxis=dict(
        title=texts.get('y_axis_title'),
        showgrid=False,
        showline=True,
        linewidth=1,
        linecolor='black',
        # Enforce the order from the JSON data
        categoryorder='array',
        categoryarray=categories
    ),
    
    # General layout styling
    plot_bgcolor='white',
    showlegend=False,
    
    # Margins to prevent clipping of labels
    margin=dict(l=150, r=50, t=50, b=80),
    
    # Annotations for source text
    annotations=[
        dict(
            text=texts.get('source'),
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.15,
            xanchor='right',
            yanchor='top',
            font=dict(size=11)
        )
    ]
)

# Update text font for the bar labels
fig.update_traces(textfont_size=12, textfont_color='black')


# --- 6. Output the Image ---
base_filename = os.path.splitext(os.path.basename(json_file_path))[0]
output_image_path = f"{base_filename}.png"

fig.write_image(output_image_path, scale=2)

print(f"Chart saved to {output_image_path}")