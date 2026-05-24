import sys
import json
import plotly.graph_objects as go

def main():
    if len(sys.argv) != 2:
        print("Usage: python <script_name>.py <json_file_path>")
        sys.exit(1)

    json_file_path = sys.argv[1]
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            chart_data = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_file_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_file_path}")
        sys.exit(1)

    base_filename = json_file_path.split('/')[-1].split('.')[0]

    fig = go.Figure()

    # Add traces from JSON data
    for i, series in enumerate(chart_data.get("chart_data", [])):
        fig.add_trace(go.Scatter(
            x=series.get("x"),
            y=series.get("y"),
            mode='lines',
            name=series.get("name"),
            line=dict(color=chart_data["colors"]["series"][i], width=2.5)
        ))

    # Apply layout settings from JSON
    layout = {
        "plot_bgcolor": chart_data["colors"]["background"],
        "paper_bgcolor": chart_data["colors"]["background"],
        "showlegend": False,
        "font": {
            "family": "Arial",
            "size": 16,
            "color": chart_data["colors"]["text"]
        },
        "margin": dict(l=50, r=50, t=50, b=50),
        "xaxis": {
            "showgrid": False,
            "zeroline": False,
            "showticklabels": False,
            "visible": False,
            "range": [-3, 5]
        },
        "yaxis": {
            "showgrid": False,
            "zeroline": False,
            "showticklabels": False,
            "visible": False,
            "range": [-3, 5]
        }
    }
    fig.update_layout(**layout)
    
    # Add shapes from JSON
    shapes = []
    for shape_config in chart_data.get("shapes", []):
        shape_config['line']['color'] = chart_data['colors']['axes_and_shapes']
        shapes.append(shape_config)
    fig.update_layout(shapes=shapes)

    # Add annotations from JSON
    annotations = []
    for anno_config in chart_data["texts"].get("annotations", []):
        annotations.append(go.layout.Annotation(
            text=anno_config["text"],
            x=anno_config["x"],
            y=anno_config["y"],
            xanchor=anno_config.get("xanchor", "center"),
            yanchor=anno_config.get("yanchor", "middle"),
            showarrow=anno_config["showarrow"],
            font=dict(
                family="Arial",
                size=16,
                color=chart_data["colors"]["text"]
            )
        ))
    fig.update_layout(annotations=annotations)

    # Generate the output image
    output_filename = f"{base_filename}.png"
    fig.write_image(output_filename, scale=2)
    print(f"Chart saved to {output_filename}")

if __name__ == "__main__":
    main()