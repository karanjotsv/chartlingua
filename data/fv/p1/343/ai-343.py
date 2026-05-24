import sys
import json
import plotly.graph_objects as go

def create_chart(json_path):
    """
    Reads chart data from a JSON file and generates a Plotly chart image.

    Args:
        json_path (str): The file path for the JSON data source.
    """
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_config = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{json_path}'")
        sys.exit(1)

    chart_data = chart_config['chart_data']
    texts = chart_config['texts']
    colors = chart_config['colors']
    
    fig = go.Figure()

    # Add background shapes for different zones
    fig.add_shape(
        type="rect",
        xref="paper", yref="y",
        x0=0, y0=0.5, x1=1, y1=8.5,
        fillcolor=colors['backgrounds']['playoff_zone'],
        layer="below", line_width=0,
    )
    fig.add_shape(
        type="rect",
        xref="paper", yref="y",
        x0=0, y0=8.5, x1=1, y1=14.5,
        fillcolor=colors['backgrounds']['lower_zone'],
        layer="below", line_width=0,
    )

    # Add a trace for each series
    for i, series in enumerate(chart_data['series']):
        line_color = colors['lines'][i]
        fig.add_trace(go.Scatter(
            x=chart_data['categories'],
            y=series['y'],
            name=series['name'],
            mode='lines+markers',
            line=dict(color=line_color, width=1.5),
            marker=dict(
                symbol=series['marker_symbol'],
                color=line_color,
                size=6
            )
        ))

    # Update layout
    title_text = f"<b>{texts['title']}</b><br><span style='font-size: 14px; color: blue;'>{texts['subtitle']}</span>"

    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.5,
            y=0.95,
            xanchor='center',
            yanchor='top'
        ),
        xaxis_title=texts['x_axis_title'],
        yaxis_title=texts['y_axis_title'],
        yaxis=dict(
            autorange='reversed',
            range=[14.5, 0.5],
            tickmode='linear',
            tick0=1,
            dtick=1,
            gridcolor='white',
            zeroline=False
        ),
        xaxis=dict(
            showgrid=False,
            tickfont=dict(size=10)
        ),
        font=dict(
            family="Arial",
            size=12
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.5,
            xanchor="center",
            x=0.5,
            traceorder='normal'
        ),
        margin=dict(l=60, r=20, t=80, b=180),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='white',
        width=800,
        height=650
    )

    # Generate output filename and save the image
    base_filename = json_path.rsplit('.', 1)[0]
    output_filename = f"{base_filename}.png"
    
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python script.py <path_to_json_file>")
        sys.exit(1)
    
    json_file_path = sys.argv[1]
    # Encapsulate the script logic in a function to improve structure and readability
    create_chart(json_file_path)