import sys
import json
import pathlib
import plotly.graph_objects as go

# Check if the JSON file path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python generate_chart.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]

# Read the JSON data from the file
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_config = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data from the loaded JSON
chart_data = chart_config['chart_data']
texts = chart_config['texts']
colors = chart_config['colors']

main_data = chart_data[0]
secondary_data = chart_data[1]

fig = go.Figure()

# Define domains for the two subplots
domain_x1 = [0.0, 0.55]
domain_y1 = [0.05, 0.95]
domain_x2 = [0.68, 0.98]
domain_y2 = [0.25, 0.8]

# --- Main Chart (Left) ---
fig.add_trace(go.Bar(
    y=main_data['categories'][::-1],
    x=main_data['values'][::-1],
    orientation='h',
    name=main_data['name'],
    marker=dict(
        color=colors[0],
        line=dict(color='#A01C20', width=1)
    ),
    text=[f'{v}%' for v in main_data['values'][::-1]],
    textposition='inside',
    insidetextanchor='middle',
    insidetextfont=dict(color='white', size=12),
    hoverinfo='none'
))

# --- Secondary Chart (Right) ---
fig.add_trace(go.Bar(
    y=secondary_data['categories'][::-1],
    x=secondary_data['values'][::-1],
    orientation='h',
    name=secondary_data['name'],
    marker=dict(
        color=colors[0],
        line=dict(color='#A01C20', width=1)
    ),
    text=[f'{v}%' for v in secondary_data['values'][::-1]],
    textposition='auto',
    insidetextanchor='end',
    textfont=dict(color='black', size=11),
    hoverinfo='none',
    xaxis='x2',
    yaxis='y2'
))

# --- Layout and Styling ---
title_text = f"<b>{texts['title']}</b><br><span style='color:grey; font-size:0.9em;'>{texts['subtitle']}</span>"

# Add background box and connector lines for the secondary chart
# Box coordinates in paper reference
box_x0, box_x1 = 0.61, 1.0
box_y0, box_y1 = 0.22, 0.83

# Source point calculation (from the end of the 'Corporate real estate...' bar)
source_category_index = main_data['categories'].index('Corporate real estate management &<br>property operators')
num_categories_main = len(main_data['categories'])
source_value = main_data['values'][source_category_index]
max_value_main = max(main_data['values']) * 1.1

# Calculate paper coordinates for the source bar
y_source_paper = domain_y1[0] + ((num_categories_main - 1 - source_category_index + 0.5) / num_categories_main) * (domain_y1[1] - domain_y1[0])
x_source_paper = domain_x1[0] + (source_value / max_value_main) * (domain_x1[1] - domain_x1[0])

fig.add_shape(type="rect",
    xref="paper", yref="paper",
    x0=box_x0, y0=box_y0, x1=box_x1, y1=box_y1,
    line=dict(color="lightgrey", width=1),
    fillcolor="rgba(245, 245, 245, 0.6)"
)

fig.add_shape(type="path",
    path=f"M {x_source_paper} {y_source_paper} L {box_x0} {box_y1}",
    xref="paper", yref="paper",
    line=dict(color="lightgrey", width=1)
)

fig.add_shape(type="path",
    path=f"M {x_source_paper} {y_source_paper} L {box_x0} {box_y0}",
    xref="paper", yref="paper",
    line=dict(color="lightgrey", width=1)
)

fig.update_layout(
    title=dict(text=title_text, x=0.01, y=0.98, xanchor='left', yanchor='top'),
    font=dict(family="Arial", size=12),
    showlegend=False,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(l=280, r=40, t=80, b=50),

    # Main axes configuration
    xaxis=dict(
        domain=domain_x1,
        showticklabels=False,
        showgrid=True,
        gridcolor='#F0F0F0',
        range=[0, max(main_data['values'])*1.1]
    ),
    yaxis=dict(
        domain=domain_y1,
        showgrid=False,
        showline=False,
        showticklabels=True,
        tickfont=dict(size=12)
    ),

    # Secondary axes configuration
    xaxis2=dict(
        domain=domain_x2,
        anchor='y2',
        showticklabels=False,
        showgrid=True,
        gridcolor='#F0F0F0',
        range=[0, max(secondary_data['values']) * 1.25]
    ),
    yaxis2=dict(
        domain=domain_y2,
        anchor='x2',
        showgrid=False,
        showline=False,
        showticklabels=True,
        side='right',
        tickfont=dict(size=12)
    ),

    # Annotations for titles and source/note
    annotations=[
        dict(
            text=texts['secondary_chart_title'],
            xref="paper", yref="paper",
            x=box_x0 + 0.02, y=box_y1,
            xanchor='left', yanchor='bottom',
            showarrow=False,
            font=dict(size=14)
        ),
        dict(
            text=texts['note'],
            xref="paper", yref="paper",
            x=0, y=-0.08,
            xanchor='left', yanchor='top',
            showarrow=False,
            font=dict(size=11, color='grey')
        ),
        dict(
            text=texts['source'],
            xref="paper", yref="paper",
            x=1, y=-0.08,
            xanchor='right', yanchor='top',
            showarrow=False,
            font=dict(size=11, color='grey')
        )
    ]
)

# Generate the output image file
filename_base = pathlib.Path(json_file_path).stem
output_filename = f"{filename_base}.png"
fig.write_image(output_filename, scale=2, width=800, height=600)

print(f"Chart generated and saved as {output_filename}")