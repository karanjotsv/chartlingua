import sys
import json
import os
import plotly.graph_objects as go

# --- 1. Load Data from JSON ---
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
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

# --- 2. Extract Data for Plotting ---
data = chart_data['chart_data']
texts = chart_data['texts']
colors = chart_data['colors']

x_values = [item['x'] for item in data]
y_values = [item['y'] for item in data]

# --- 3. Create the Chart Figure ---
fig = go.Figure()

# Add the bar trace
fig.add_trace(go.Bar(
    x=x_values,
    y=y_values,
    marker_color=colors[0],
    text=y_values,
    textposition='outside',
    texttemplate='%{y:,.0f}',
    textfont=dict(
        family="Arial",
        size=12,
        color='black'
    ),
    cliponaxis=False  # Prevents text labels from being clipped at the top
))

# --- 4. Configure Layout and Styling ---
fig.update_layout(
    font=dict(
        family="Arial",
        size=12,
        color="#444444"
    ),
    title_text=texts['title'] if texts.get('title') else None,
    plot_bgcolor='white',
    paper_bgcolor='#F8F9FA',
    showlegend=False,
    margin=dict(l=80, r=40, t=50, b=100),
    separators='., ',  # Use dot for decimal, space for thousands

    # X-Axis Configuration
    xaxis=dict(
        title_text=texts['x_axis_title'],
        showgrid=False,
        tickfont=dict(size=12)
    ),

    # Y-Axis Configuration
    yaxis=dict(
        title_text=texts['y_axis_title'],
        range=[0, 25000],
        dtick=5000,
        showgrid=True,
        gridcolor='#E0E0E0',
        griddash='dot',
        tickfont=dict(size=12),
        tickformat=',.0f'
    ),

    # Annotations for Source/Note
    annotations=[
        dict(
            text=texts['source'],
            showarrow=False,
            xref='paper',
            yref='paper',
            x=1.0,
            y=-0.2,
            xanchor='right',
            yanchor='top',
            font=dict(size=11)
        )
    ]
)

# --- 5. Output the Chart to a PNG File ---
base_filename = os.path.splitext(os.path.basename(json_path))[0]
output_filename = f"{base_filename}.png"

fig.write_image(output_filename, scale=2)

print(f"Chart saved to {output_filename}")