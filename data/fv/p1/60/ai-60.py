import sys
import json
import plotly.graph_objects as go
import os

def main():
    if len(sys.argv) != 2:
        print("Usage: python <script_name>.py <json_file_path>")
        sys.exit(1)

    json_filepath = sys.argv[1]

    try:
        with open(json_filepath, 'r', encoding='utf-8') as f:
            chart_info = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_filepath}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_filepath}")
        sys.exit(1)

    fig = go.Figure()

    # Create a mapping from legend labels to colors
    color_map = {label: color for label, color in zip(chart_info['texts']['legend_labels'], chart_info['colors'])}
    
    # Add scatter traces
    for series in chart_info['chart_data']:
        if series['type'] == 'scatter':
            fig.add_trace(go.Scatter(
                x=series['x'],
                y=series['y'],
                mode='markers',
                name=series['name'],
                marker=dict(
                    color=color_map.get(series['name']),
                    size=8
                )
            ))
            
    # Add line traces
    for series in chart_info['chart_data']:
        if series['type'] == 'line':
            # Associate trendline with its data series color
            series_name_key = series['name'].split(' ')[0] + ' Data'
            line_color = color_map.get(series_name_key)
            
            fig.add_trace(go.Scatter(
                x=series['x'],
                y=series['y'],
                mode='lines',
                name=series['name'],
                line=dict(
                    color=line_color,
                    width=3
                ),
                showlegend=False
            ))

    # Update layout
    fig.update_layout(
        font=dict(family="Arial", size=18, color="black"),
        xaxis=dict(
            title=chart_info['texts']['x_axis_title'],
            range=[-16.5, -25.5],  # For reversed axis, range is [max, min]
            tickmode='array',
            tickvals=[-18, -20, -22, -24],
            showline=True,
            linewidth=2,
            linecolor='black',
            mirror=True,
            ticks='inside',
            tickwidth=1,
            ticklen=6,
            gridcolor='white'
        ),
        yaxis=dict(
            title=chart_info['texts']['y_axis_title'],
            range=[1.55, 2.85],
            tickmode='array',
            tickvals=[1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8],
            showline=True,
            linewidth=2,
            linecolor='black',
            mirror=True,
            ticks='inside',
            tickwidth=1,
            ticklen=6,
            gridcolor='white'
        ),
        legend=dict(
            x=0.98,
            y=0.02,
            xanchor='right',
            yanchor='bottom',
            bgcolor='white',
            itemsizing='constant'
        ),
        plot_bgcolor='white',
        margin=dict(l=80, r=40, t=40, b=80),
        width=800,
        height=600
    )

    # Determine output filename
    base_filename = os.path.splitext(os.path.basename(json_filepath))[0]
    output_filename = f"{base_filename}.png"

    # Save the figure
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()