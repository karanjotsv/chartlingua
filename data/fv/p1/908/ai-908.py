import sys
import json
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

def main():
    # Check for command-line argument
    if len(sys.argv) != 2:
        print("Usage: python create_chart.py <path_to_json_file>")
        sys.exit(1)

    json_path = sys.argv[1]

    # Read data from the specified JSON file
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_config = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}")
        sys.exit(1)

    # Extract data from JSON
    chart_data = chart_config.get('chart_data', [])
    texts = chart_config.get('texts', {})
    colors = chart_config.get('colors', [])

    # Initialize figure with subplots
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.02,
        row_heights=[0.7, 0.3]
    )

    # Add traces to the figure
    color_index = 0
    for series in chart_data:
        show_legend = series.get('type') != 'markers'
        
        if series.get('type') == 'line':
            trace_color = colors[color_index] if color_index < len(colors) else None
            fig.add_trace(go.Scatter(
                x=series['x'],
                y=series['y'],
                name=series['name'],
                mode='lines',
                line=dict(color=trace_color, width=1.5),
                showlegend=show_legend
            ), row=series['subplot'], col=1)
            if show_legend:
                color_index += 1
        elif series.get('type') == 'markers':
            # Markers use the color of the first trace
            marker_color = colors[0] if colors else 'black'
            fig.add_trace(go.Scatter(
                x=series['x'],
                y=series['y'],
                name=series['name'],
                mode='markers',
                marker=dict(
                    symbol='triangle-up',
                    color=marker_color,
                    size=12
                ),
                showlegend=show_legend
            ), row=series['subplot'], col=1)

    # Update layout
    fig.update_layout(
        template='simple_white',
        font=dict(family="Arial", size=12),
        margin=dict(l=50, r=20, t=60, b=50),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="left",
            x=0
        ),
        plot_bgcolor='white',
        paper_bgcolor='white'
    )
    
    # Update y-axes
    fig.update_yaxes(
        range=[790, 1110], 
        dtick=20, 
        row=1, col=1, 
        gridcolor='#D3D3D3', 
        showgrid=True,
        zeroline=False
    )
    fig.update_yaxes(
        range=[0, 105], 
        dtick=20, 
        row=2, col=1, 
        gridcolor='#D3D3D3', 
        showgrid=True,
        zeroline=False
    )

    # Update x-axis
    tick_dates = [f"2003-{str(i).zfill(2)}-01" for i in range(1, 13)] + ["2004-01-01"]
    tick_labels = [
        "Jan<br>2003", "Feb", "Mar", "Apr", "May", "Jun", 
        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "Jan"
    ]
    fig.update_xaxes(
        showgrid=True,
        gridcolor='#D3D3D3',
        tickvals=tick_dates,
        ticktext=tick_labels,
        tickangle=0,
        showline=True,
        linecolor='black',
        mirror=True
    )

    # Generate output filename from JSON path
    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"

    # Save the figure as a PNG image
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()