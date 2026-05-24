import sys
import json
import plotly.graph_objects as go

def create_arrow_shape(x_center, y_bottom, color):
    """Helper to create a downward-pointing arrow shape below a header."""
    return go.layout.Shape(
        type="path",
        path=f"M {x_center-0.015} {y_bottom} L {x_center} {y_bottom+0.015} L {x_center+0.015} {y_bottom} Z",
        fillcolor=color,
        line_color=color,
        xref="paper",
        yref="paper"
    )

if len(sys.argv) != 2:
    print("Usage: python <script_name>.py <json_file_path>")
    sys.exit(1)

json_file_path = sys.argv[1]
try:
    with open(json_file_path, 'r', encoding='utf-8') as f:
        chart_info = json.load(f)
except FileNotFoundError:
    print(f"Error: JSON file not found at {json_file_path}")
    sys.exit(1)
except json.JSONDecodeError:
    print(f"Error: Could not decode JSON from {json_file_path}")
    sys.exit(1)

# Extract data from JSON
texts = chart_info['texts']
data = chart_info['chart_data']
colors = chart_info['colors']

# --- Figure Initialization ---
fig = go.Figure()

# --- Top Section ---
# Header: Population
fig.add_shape(type="rect", xref="paper", yref="paper", x0=0.05, y0=0.08, x1=0.26, y1=0.12, fillcolor=colors['population'], line_width=0)
fig.add_annotation(xref="paper", yref="paper", x=0.155, y=0.1, text=texts['section_titles'][0], showarrow=False, font=dict(color="white", size=14, family="Arial"))
fig.add_shape(create_arrow_shape(0.155, 0.12, colors['population']))

# Header: Qualifications
fig.add_shape(type="rect", xref="paper", yref="paper", x0=0.28, y0=0.08, x1=0.58, y1=0.12, fillcolor=colors['qualifications'], line_width=0)
fig.add_annotation(xref="paper", yref="paper", x=0.43, y=0.1, text=texts['section_titles'][1], showarrow=False, font=dict(color="white", size=14, family="Arial"))
fig.add_shape(create_arrow_shape(0.43, 0.12, colors['qualifications']))

# Header: Unemployment
fig.add_shape(type="rect", xref="paper", yref="paper", x0=0.60, y0=0.08, x1=0.83, y1=0.12, fillcolor=colors['unemployment'], line_width=0)
fig.add_annotation(xref="paper", yref="paper", x=0.715, y=0.1, text=texts['section_titles'][2], showarrow=False, font=dict(color="white", size=14, family="Arial"))
fig.add_shape(create_arrow_shape(0.715, 0.12, colors['unemployment']))

# Donut: Population
pop_val = data['population_donut']['value']
fig.add_trace(go.Pie(
    values=[pop_val, 100 - pop_val],
    hole=0.75,
    marker_colors=[colors['population'], colors['donut_secondary']],
    domain={'x': [0.05, 0.26], 'y': [0.15, 0.28]},
    showlegend=False,
    textinfo='none',
    hoverinfo='none',
    sort=False
))
fig.add_annotation(xref="paper", yref="paper", x=0.155, y=0.215, text=texts['population']['donut_center_text'], showarrow=False, font=dict(color=colors['text_main'], size=28, family="Arial"), align="center")
fig.add_annotation(xref="paper", yref="paper", x=0.155, y=0.30, text=texts['population']['value_text'], showarrow=False, font=dict(color=colors['text_main'], size=16, family="Arial"))
fig.add_annotation(xref="paper", yref="paper", x=0.155, y=0.32, text=texts['population']['date_text'], showarrow=False, font=dict(color=colors['text_light'], size=12, family="Arial"))

# Bar Chart: Qualifications
max_qual_val = max(d['value'] for d in data['qualifications_bar'])
for i, item in enumerate(data['qualifications_bar']):
    y_pos = 0.19 + i * 0.05
    bar_len = (item['value'] / max_qual_val) * 0.2
    fig.add_shape(type="rect", xref="paper", yref="paper", x0=0.35, y0=y_pos, x1=0.35 + bar_len, y1=y_pos + 0.03, fillcolor=colors['qualifications'], line_width=0)
    fig.add_annotation(xref="paper", yref="paper", x=0.34, y=y_pos + 0.015, text=item['label'], showarrow=False, font=dict(color=colors['text_main'], size=12, family="Arial"), align="right", xanchor="right")
    fig.add_annotation(xref="paper", yref="paper", x=0.36 + bar_len, y=y_pos + 0.015, text=f"{item['value']}%", showarrow=False, font=dict(color=colors['text_main'], size=12, family="Arial"), align="left", xanchor="left")
fig.add_annotation(xref="paper", yref="paper", x=0.45, y=0.32, text=texts['qualifications']['date_text'], showarrow=False, font=dict(color=colors['text_light'], size=12, family="Arial"))

# Bar Chart: Unemployment
max_unemp_val = max(d['value'] for d in data['unemployment_bar'])
for i, item in enumerate(data['unemployment_bar']):
    x_pos = 0.62 + i * 0.08
    bar_height = (item['value'] / max_unemp_val) * 0.12
    fig.add_shape(type="rect", xref="paper", yref="paper", x0=x_pos, y0=0.31 - bar_height, x1=x_pos + 0.05, y1=0.31, fillcolor=colors['unemployment'], line_width=0)
    fig.add_annotation(xref="paper", yref="paper", x=x_pos + 0.025, y=0.31-bar_height-0.01, text=f"{item['value']}%", showarrow=False, font=dict(color=colors['text_main'], size=12, family="Arial"), yanchor="bottom")
    fig.add_annotation(xref="paper", yref="paper", x=x_pos + 0.025, y=0.32, text=item['label'], showarrow=False, font=dict(color=colors['text_light'], size=11, family="Arial"), align="center")
fig.add_annotation(xref="paper", yref="paper", x=0.74, y=0.35, text=texts['unemployment']['date_text'], showarrow=False, font=dict(color=colors['text_light'], size=12, family="Arial"))

# --- Middle Section ---
# Header: Economic Output
fig.add_shape(type="rect", xref="paper", yref="paper", x0=0.05, y0=0.39, x1=0.30, y1=0.43, fillcolor=colors['economic_output'], line_width=0)
fig.add_annotation(xref="paper", yref="paper", x=0.175, y=0.41, text=texts['section_titles'][3], showarrow=False, font=dict(color="white", size=14, family="Arial"))
fig.add_shape(create_arrow_shape(0.175, 0.43, colors['economic_output']))

# Donut: Economic Output
econ_val = data['economic_output_donut']['value']
fig.add_trace(go.Pie(
    values=[econ_val, 100 - econ_val],
    hole=0.75,
    marker_colors=[colors['economic_output'], colors['donut_secondary']],
    domain={'x': [0.05, 0.26], 'y': [0.46, 0.59]},
    showlegend=False,
    textinfo='none',
    hoverinfo='none',
    sort=False
))
fig.add_annotation(xref="paper", yref="paper", x=0.155, y=0.525, text=texts['economic_output']['donut_center_text'], showarrow=False, font=dict(color=colors['text_main'], size=28, family="Arial"), align="center")
fig.add_annotation(xref="paper", yref="paper", x=0.155, y=0.61, text=texts['economic_output']['value_text'], showarrow=False, font=dict(color=colors['text_main'], size=12, family="Arial"))
fig.add_annotation(xref="paper", yref="paper", x=0.155, y=0.63, text=texts['economic_output']['date_text'], showarrow=False, font=dict(color=colors['text_light'], size=12, family="Arial"))

# --- Bottom Section ---
# Headers
fig.add_shape(type="rect", xref="paper", yref="paper", x0=0.05, y0=0.68, x1=0.28, y1=0.72, fillcolor=colors['weekly_earnings'], line_width=0)
fig.add_annotation(xref="paper", yref="paper", x=0.165, y=0.7, text=texts['section_titles'][4], showarrow=False, font=dict(color="white", size=14, family="Arial"))
fig.add_shape(create_arrow_shape(0.165, 0.72, colors['weekly_earnings']))

fig.add_shape(type="rect", xref="paper", yref="paper", x0=0.30, y0=0.68, x1=0.53, y1=0.72, fillcolor=colors['house_prices'], line_width=0)
fig.add_annotation(xref="paper", yref="paper", x=0.415, y=0.7, text=texts['section_titles'][5], showarrow=False, font=dict(color="white", size=14, family="Arial"))
fig.add_shape(create_arrow_shape(0.415, 0.72, colors['house_prices']))

fig.add_shape(type="rect", xref="paper", yref="paper", x0=0.55, y0=0.68, x1=0.78, y1=0.72, fillcolor=colors['life_expectancy'], line_width=0)
fig.add_annotation(xref="paper", yref="paper", x=0.665, y=0.7, text=texts['section_titles'][6], showarrow=False, font=dict(color="white", size=14, family="Arial"))
fig.add_shape(create_arrow_shape(0.665, 0.72, colors['life_expectancy']))

# Circles: Weekly Earnings
fig.add_shape(type="circle", xref="paper", yref="paper", x0=0.1, y0=0.75, x1=0.23, y1=0.82, fillcolor=colors['weekly_earnings'], line=dict(color=colors['weekly_earnings'], width=4), opacity=0.8)
fig.add_shape(type="circle", xref="paper", yref="paper", x0=0.105, y0=0.755, x1=0.225, y1=0.815, fillcolor="white", line_width=0)
fig.add_annotation(xref="paper", yref="paper", x=0.165, y=0.77, text=data['weekly_earnings'][0]['label'], showarrow=False, font=dict(color=colors['weekly_earnings'], size=11, family="Arial"))
fig.add_annotation(xref="paper", yref="paper", x=0.165, y=0.795, text=data['weekly_earnings'][0]['value'], showarrow=False, font=dict(color=colors['weekly_earnings'], size=20, family="Arial"))

fig.add_shape(type="circle", xref="paper", yref="paper", x0=0.1, y0=0.84, x1=0.23, y1=0.91, fillcolor=colors['weekly_earnings'], line=dict(color=colors['weekly_earnings'], width=4), opacity=0.8)
fig.add_shape(type="circle", xref="paper", yref="paper", x0=0.105, y0=0.845, x1=0.225, y1=0.905, fillcolor="white", line_width=0)
fig.add_annotation(xref="paper", yref="paper", x=0.165, y=0.86, text=data['weekly_earnings'][1]['label'], showarrow=False, font=dict(color=colors['weekly_earnings'], size=11, family="Arial"))
fig.add_annotation(xref="paper", yref="paper", x=0.165, y=0.885, text=data['weekly_earnings'][1]['value'], showarrow=False, font=dict(color=colors['weekly_earnings'], size=20, family="Arial"))
fig.add_annotation(xref="paper", yref="paper", x=0.165, y=0.94, text=texts['weekly_earnings']['caption'], showarrow=False, font=dict(color=colors['text_light'], size=12, family="Arial"), align="center")

# Bar Chart: House Prices
fig.add_annotation(xref="paper", yref="paper", x=0.415, y=0.76, text=texts['house_prices']['caption'], showarrow=False, font=dict(color=colors['text_main'], size=12, family="Arial"), align="center")
baseline_y = 0.88
max_price_val = max(abs(d['value']) for d in data['house_prices_bar'])
bar_scale = 0.1 / max_price_val
# Bar 1 (Y&H)
bar1 = data['house_prices_bar'][0]
fig.add_shape(type="rect", xref="paper", yref="paper", x0=0.34, y0=baseline_y, x1=0.40, y1=baseline_y - bar1['value'] * bar_scale, fillcolor=colors['house_prices'], line_width=0, opacity=0.5)
fig.add_annotation(xref="paper", yref="paper", x=0.37, y=baseline_y - bar1['value'] * bar_scale + 0.01, text=bar1['text'], showarrow=False, font=dict(color=colors['house_prices'], size=12, family="Arial"), align="center")
fig.add_shape(create_arrow_shape(0.37, baseline_y - bar1['value'] * bar_scale, colors['house_prices']))
fig.add_annotation(xref="paper", yref="paper", x=0.37, y=baseline_y + 0.015, text=bar1['label'], showarrow=False, font=dict(color=colors['text_light'], size=11, family="Arial"), yanchor="top")
# Bar 2 (London)
bar2 = data['house_prices_bar'][1]
fig.add_shape(type="rect", xref="paper", yref="paper", x0=0.43, y0=baseline_y - bar2['value'] * bar_scale, x1=0.49, y1=baseline_y, fillcolor=colors['house_prices'], line_width=0, opacity=0.5)
fig.add_annotation(xref="paper", yref="paper", x=0.46, y=baseline_y - bar2['value'] * bar_scale - 0.01, text=bar2['text'], showarrow=False, font=dict(color=colors['house_prices'], size=12, family="Arial"), align="center", yanchor="bottom")
fig.add_annotation(xref="paper", yref="paper", x=0.46, y=baseline_y + 0.015, text=bar2['label'], showarrow=False, font=dict(color=colors['text_light'], size=11, family="Arial"), yanchor="top")


# Text: Life Expectancy
fig.add_annotation(xref="paper", yref="paper", x=0.665, y=0.75, text=f"<b>{texts['life_expectancy']['region1_name']}</b>", showarrow=False, font=dict(color=colors['life_expectancy'], size=14, family="Arial"))
fig.add_annotation(xref="paper", yref="paper", x=0.62, y=0.81, text=f"<span style='font-size: 24px;'>&#9794;</span><br>{data['life_expectancy'][0]['male']}<br>years", showarrow=False, font=dict(color=colors['text_main'], size=14, family="Arial"), align="center")
fig.add_annotation(xref="paper", yref="paper", x=0.71, y=0.81, text=f"<span style='font-size: 24px;'>&#9792;</span><br>{data['life_expectancy'][0]['female']}<br>years", showarrow=False, font=dict(color=colors['text_main'], size=14, family="Arial"), align="center")

fig.add_annotation(xref="paper", yref="paper", x=0.665, y=0.86, text=f"<b>{texts['life_expectancy']['region2_name']}</b>", showarrow=False, font=dict(color=colors['text_main'], size=14, family="Arial"))
fig.add_annotation(xref="paper", yref="paper", x=0.62, y=0.92, text=f"<span style='font-size: 24px;'>&#9794;</span><br>{data['life_expectancy'][1]['male']}<br>years", showarrow=False, font=dict(color=colors['text_main'], size=14, family="Arial"), align="center")
fig.add_annotation(xref="paper", yref="paper", x=0.71, y=0.92, text=f"<span style='font-size: 24px;'>&#9792;</span><br>{data['life_expectancy'][1]['female']}<br>years", showarrow=False, font=dict(color=colors['text_main'], size=14, family="Arial"), align="center")

fig.add_annotation(xref="paper", yref="paper", x=0.665, y=0.97, text=texts['life_expectancy']['caption'], showarrow=False, font=dict(color=colors['text_light'], size=12, family="Arial"), align="center")

# --- Footer ---
fig.add_annotation(xref="paper", yref="paper", x=0.05, y=0.97, text=texts['footer']['url'], showarrow=False, font=dict(color=colors['text_main'], size=14, family="Arial"), xanchor="left")
fig.add_annotation(xref="paper", yref="paper", x=0.05, y=0.99, text=texts['footer']['source'], showarrow=False, font=dict(color=colors['text_light'], size=10, family="Arial"), xanchor="left", yanchor="top", align="left")
fig.add_shape(type="rect", xref="paper", yref="paper", x0=0.70, y0=0.965, x1=0.71, y1=1.0, fillcolor="#777", line_width=0)
fig.add_annotation(xref="paper", yref="paper", x=0.72, y=0.9825, text=texts['footer']['logo_text'], showarrow=False, font=dict(color=colors['text_main'], size=12, family="Arial"), xanchor="left", align="left")


# --- Final Layout Configuration ---
fig.update_layout(
    width=850,
    height=1200,
    title=dict(
        text=f"<b>{texts['title']}</b>",
        y=0.97,
        x=0.05,
        xanchor='left',
        yanchor='top',
        font=dict(size=24, family="Arial", color=colors['text_main'])
    ),
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    showlegend=False,
    xaxis=dict(visible=False, showgrid=False, range=[0, 1]),
    yaxis=dict(visible=False, showgrid=False, range=[0, 1]),
    margin=dict(l=20, r=20, t=100, b=20)
)

# --- Output ---
# Derive output filename from the input JSON path
base_filename = json_file_path[:json_file_path.rfind('.')]
output_image_file = f"{base_filename}.png"

fig.write_image(output_image_file, scale=2)

print(f"Chart saved to {output_image_file}")