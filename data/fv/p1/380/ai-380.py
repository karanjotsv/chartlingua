import sys
import json
import pathlib
import plotly.graph_objects as go

def create_header(fig, x, y, width, height, text, color):
    """Helper function to create a section header."""
    fig.add_shape(
        type="rect",
        x0=x, y0=y, x1=x + width, y1=y + height,
        xref="paper", yref="paper",
        fillcolor=color,
        line_color=color,
        layer="below"
    )
    fig.add_annotation(
        x=x + width / 2, y=y + height / 2,
        xref="paper", yref="paper",
        text=text,
        showarrow=False,
        font=dict(family="Arial", size=14, color="white"),
        align="center",
        valign="middle"
    )
    # Add triangle pointer
    triangle_x_center = x + width / 2
    triangle_y_top = y
    triangle_size = 0.015
    fig.add_shape(
        type="path",
        path=f"M {triangle_x_center - triangle_size},{triangle_y_top} L {triangle_x_center},{triangle_y_top - triangle_size} L {triangle_x_center + triangle_size},{triangle_y_top} Z",
        xref="paper", yref="paper",
        fillcolor=color,
        line_color=color,
        layer="below"
    )

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Usage: python {pathlib.Path(__file__).name} <path_to_json_file>")
        sys.exit(1)

    json_path = pathlib.Path(sys.argv[1])
    if not json_path.is_file():
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)

    output_filename = json_path.with_suffix(".png")

    with open(json_path, 'r', encoding='utf-8') as f:
        config = json.load(f)

    texts = config["texts"]
    colors = config["colors"]
    chart_data = config["chart_data"]

    fig = go.Figure()

    # --- Section Headers ---
    header_y = 0.9
    header_h = 0.04
    create_header(fig, 0.05, header_y, 0.2, header_h, texts["section_population"], colors["population"])
    create_header(fig, 0.3, header_y, 0.2, header_h, texts["section_median_age"], colors["median_age"])
    create_header(fig, 0.55, header_y, 0.2, header_h, texts["section_unemployment"], colors["unemployment"])
    
    header_y = 0.6
    create_header(fig, 0.05, header_y, 0.2, header_h, texts["section_economic_output"], colors["economic_output"])

    header_y = 0.35
    create_header(fig, 0.05, header_y, 0.2, header_h, texts["section_weekly_earnings"], colors["weekly_earnings"])
    create_header(fig, 0.3, header_y, 0.2, header_h, texts["section_house_prices"], colors["house_prices"])
    create_header(fig, 0.55, header_y, 0.2, header_h, texts["section_crime"], colors["crime"])

    # --- Population ---
    pop_data = chart_data["population"]
    fig.add_trace(go.Pie(
        values=[pop_data['value'], 100 - pop_data['value']],
        hole=0.75,
        domain={'x': [0.05, 0.25], 'y': [0.67, 0.87]},
        marker={'colors': [colors['population'], colors['donut_secondary']]},
        showlegend=False, hoverinfo='none', textinfo='none', sort=False
    ))
    fig.add_annotation(x=0.15, y=0.79, text=texts['population_value'], font=dict(size=36, color=colors['text_dark']), showarrow=False)
    fig.add_annotation(x=0.15, y=0.75, text=texts['population_sub_label'], font=dict(size=12, color=colors['text_dark']), showarrow=False)
    fig.add_annotation(x=0.15, y=0.69, text=texts['population_extra_1'], font=dict(size=18, color=colors['text_dark']), showarrow=False)
    fig.add_annotation(x=0.15, y=0.64, text=texts['population_extra_2'], font=dict(size=11, color=colors['text_medium']), showarrow=False, align="center")

    # --- Median Age ---
    age_data = chart_data["median_age"]["series"]
    fig.add_annotation(x=0.32, y=0.82, text=age_data[0]['name'], font=dict(size=12, color=colors['text_medium']), showarrow=False, align="left")
    fig.add_annotation(x=0.42, y=0.82, text=f"<b>{age_data[0]['value']}</b><span style='font-size:12px'> years</span>", font=dict(size=24, color=colors['text_dark']), showarrow=False, align="left")
    fig.add_annotation(x=0.32, y=0.77, text=age_data[1]['name'], font=dict(size=12, color=colors['median_age']), showarrow=False, align="left")
    fig.add_annotation(x=0.42, y=0.77, text=f"<b>{age_data[1]['value']}</b><span style='font-size:12px'> years</span>", font=dict(size=24, color=colors['median_age']), showarrow=False, align="left")
    fig.add_annotation(x=0.32, y=0.72, text=age_data[2]['name'], font=dict(size=12, color=colors['text_medium']), showarrow=False, align="left")
    fig.add_annotation(x=0.42, y=0.72, text=f"<b>{age_data[2]['value']}</b><span style='font-size:12px'> years</span>", font=dict(size=24, color=colors['text_dark']), showarrow=False, align="left")
    fig.add_annotation(x=0.4, y=0.64, text=texts['median_age_note'], font=dict(size=11, color=colors['text_medium']), showarrow=False, align="center")

    # --- Unemployment ---
    unemp_data = chart_data["unemployment"]
    fig.add_trace(go.Bar(
        x=unemp_data['categories'], y=unemp_data['values'],
        marker_color=colors['unemployment'], showlegend=False, hoverinfo='none',
        text=[f"{v}%" for v in unemp_data['values']], textposition='outside',
        textfont=dict(size=11, color=colors['text_dark']),
        xaxis='x2', yaxis='y2'
    ))
    fig.add_annotation(x=0.675, y=0.64, text=texts['unemployment_note'], font=dict(size=11, color=colors['text_medium']), showarrow=False, align="center")

    # --- Economic Output ---
    econ_data = chart_data["economic_output"]
    fig.add_trace(go.Pie(
        values=[econ_data['value'], 100 - econ_data['value']],
        hole=0.75,
        domain={'x': [0.05, 0.25], 'y': [0.38, 0.58]},
        marker={'colors': [colors['economic_output'], colors['donut_secondary']]},
        showlegend=False, hoverinfo='none', textinfo='none', sort=False
    ))
    fig.add_annotation(x=0.15, y=0.5, text=texts['economic_output_value'], font=dict(size=36, color=colors['text_dark']), showarrow=False)
    fig.add_annotation(x=0.15, y=0.46, text=texts['economic_output_sub_label'], font=dict(size=12, color=colors['text_dark']), showarrow=False)
    fig.add_annotation(x=0.15, y=0.35, text=texts['economic_output_note'], font=dict(size=11, color=colors['text_medium']), showarrow=False, align="center")

    # --- Map ---
    fig.add_shape(type="path",
        path="M 0.48,0.79 L 0.53,0.78 L 0.55,0.7 L 0.56,0.6 L 0.52,0.58 L 0.56,0.5 L 0.52,0.45 L 0.47,0.46 L 0.44,0.55 L 0.45,0.65 Z",
        xref="paper", yref="paper", fillcolor=colors['map_fill'], line_color=colors['map_fill'], layer="below")
    for city in chart_data['map_cities']:
        fig.add_annotation(x=city['x'], y=city['y'], text=f"● <span style='font-size:11px'>{city['name']}</span>",
                           font=dict(color=colors['map_points'], size=14), showarrow=False, align="left", xanchor="left")
    
    # --- Weekly Earnings ---
    earn_data = chart_data["weekly_earnings"]["series"]
    circle_y_positions = [0.25, 0.12]
    for i, series in enumerate(earn_data):
        fig.add_shape(type="circle", x0=0.08, y0=circle_y_positions[i], x1=0.22, y1=circle_y_positions[i]+0.1, fillcolor=colors['weekly_earnings'], line_color=colors['weekly_earnings'])
        fig.add_annotation(x=0.15, y=circle_y_positions[i]+0.065, text=series['name'], font=dict(size=11, color=colors['text_light']), showarrow=False)
        fig.add_annotation(x=0.15, y=circle_y_positions[i]+0.035, text=f"£{series['value']}", font=dict(size=24, color=colors['text_light']), showarrow=False)
    fig.add_annotation(x=0.15, y=0.04, text=texts['weekly_earnings_note'], font=dict(size=11, color=colors['text_medium']), showarrow=False, align="center")

    # --- House Prices ---
    price_data = chart_data["house_prices"]["series"]
    fig.add_trace(go.Bar(
        x=[p['name'] for p in price_data], y=[p['value'] for p in price_data],
        marker_color=colors['house_prices'], showlegend=False, hoverinfo='none',
        text=[f"£{p['value']:,}" for p in price_data], textposition='outside',
        textfont=dict(size=14, color=colors['text_dark']),
        width=0.4,
        xaxis='x3', yaxis='y3'
    ))
    fig.add_annotation(x=0.4, y=0.04, text=texts['house_prices_note'], font=dict(size=11, color=colors['text_medium']), showarrow=False, align="center")

    # --- Crime ---
    crime_data = chart_data["crime"]["series"]
    fig.add_shape(type="rect", x0=0.6, y0=0.26, x1=0.6+crime_data[0]['value']/100, y1=0.3, fillcolor=colors['crime'], line_width=0)
    fig.add_annotation(x=0.59, y=0.28, text=crime_data[0]['name'], font=dict(size=12, color=colors['text_dark']), showarrow=False, align="right", xanchor="right")
    fig.add_annotation(x=0.62, y=0.28, text=f"<b>{crime_data[0]['value']}</b>", font=dict(size=18, color=colors['text_light']), showarrow=False, align="left", xanchor="left")
    fig.add_shape(type="rect", x0=0.6, y0=0.2, x1=0.6+crime_data[1]['value']/100, y1=0.24, fillcolor=colors['bar_secondary'], line_width=0)
    fig.add_annotation(x=0.59, y=0.22, text=crime_data[1]['name'], font=dict(size=12, color=colors['text_dark']), showarrow=False, align="right", xanchor="right")
    fig.add_annotation(x=0.62, y=0.22, text=f"<b>{crime_data[1]['value']}</b>", font=dict(size=18, color=colors['text_light']), showarrow=False, align="left", xanchor="left")
    fig.add_annotation(x=0.675, y=0.14, text=texts['crime_note'], font=dict(size=11, color=colors['text_medium']), showarrow=False, align="center")

    # --- General Layout ---
    fig.update_layout(
        width=800, height=1100,
        margin=dict(l=20, r=20, t=80, b=80),
        paper_bgcolor=colors['background'],
        plot_bgcolor=colors['background'],
        font=dict(family="Arial"),
        title=dict(
            text=f"<b>{texts['title']}</b>",
            font=dict(size=28, color=colors['unemployment']),
            x=0.05, y=0.98, xanchor='left', yanchor='top'
        ),
        xaxis=dict(visible=False, range=[0, 1]),
        yaxis=dict(visible=False, range=[0, 1]),
        xaxis2=dict(domain=[0.55, 0.79], anchor='y2', visible=False),
        yaxis2=dict(domain=[0.67, 0.87], anchor='x2', range=[0, 12], visible=False),
        xaxis3=dict(domain=[0.3, 0.5], anchor='y3', visible=False),
        yaxis3=dict(domain=[0.14, 0.32], anchor='x3', range=[0, 500000], visible=False),
        showlegend=False,
    )

    # --- Footers ---
    fig.add_annotation(x=0, y=0.01, xref="paper", yref="paper",
                       text=texts['footer_left'], showarrow=False, xanchor="left", yanchor="bottom",
                       font=dict(size=12, color=colors['text_dark']))
    fig.add_annotation(x=0.5, y=0.01, xref="paper", yref="paper",
                       text=texts['footer_middle'], showarrow=False, xanchor="center", yanchor="bottom",
                       font=dict(size=9, color=colors['text_medium']), align="center")

    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")