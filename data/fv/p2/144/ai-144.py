import sys
import json
import plotly.graph_objects as go

def main():
    # Check for command-line argument
    if len(sys.argv) != 2:
        print(f"Usage: python {sys.argv[0]} <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]

    # Read and parse the JSON file
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_config = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at {json_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {json_path}")
        sys.exit(1)

    # Extract data from the JSON structure
    chart_data = chart_config['chart_data']
    texts = chart_config['texts']
    colors = chart_config['colors']

    # Prepare data for Plotly
    values = [d['percentage'] for d in chart_data]
    
    # Create the figure
    fig = go.Figure()

    # Add the pie chart trace
    fig.add_trace(go.Pie(
        values=values,
        labels=[d['label'] for d in chart_data],
        marker=dict(
            colors=colors,
            line=dict(color='black', width=1)
        ),
        sort=False,
        direction='clockwise',
        rotation=74, # Rotates the pie to place the 9% slice at the top
        textinfo='none',
        hoverinfo='none',
        domain={'x': [0.05, 0.95], 'y': [0.05, 0.95]} # Contract pie slightly to prevent clipping
    ))

    # Add annotations for the pie slices
    # Annotation for 56% slice (Contractors)
    data_56 = chart_data[2]
    fig.add_annotation(
        text=f"<span style='font-size:18px;'><b>{data_56['percentage']}%</b></span><br>{data_56['label']} ({data_56['value']:,})",
        xref="paper", yref="paper",
        x=0.25, y=0.5,
        showarrow=False,
        align="center",
        font=dict(family="Arial", size=14)
    )

    # Annotation for 35% slice (Civilians)
    data_35 = chart_data[1]
    fig.add_annotation(
        text=f"<span style='font-size:18px;'><b>{data_35['percentage']}%</b></span><br>{data_35['label']} ({data_35['value']:,})",
        xref="paper", yref="paper",
        x=0.7, y=0.35,
        showarrow=False,
        align="center",
        font=dict(family="Arial", size=14)
    )

    # Annotation and lines for 9% slice (Military)
    data_9 = chart_data[0]
    # Dot inside the slice
    fig.add_shape(type="circle",
        xref="paper", yref="paper",
        x0=0.495, y0=0.795, x1=0.505, y1=0.805,
        fillcolor="black",
        line_color="black"
    )
    # Vertical line
    fig.add_shape(type="line",
        xref="paper", yref="paper",
        x0=0.5, y0=0.8, x1=0.5, y1=0.9,
        line=dict(color="black", width=1)
    )
    # Horizontal line
    fig.add_shape(type="line",
        xref="paper", yref="paper",
        x0=0.5, y0=0.9, x1=0.68, y1=0.9,
        line=dict(color="black", width=1)
    )
    fig.add_annotation(
        text=f"<span style='font-size:18px;'><b>{data_9['percentage']}%</b></span><br>{data_9['label']} ({data_9['value']:,})",
        xref="paper", yref="paper",
        x=0.69, y=0.9,
        showarrow=False,
        xanchor='left',
        yanchor='bottom',
        align="left",
        font=dict(family="Arial", size=14)
    )
    
    # Add source text
    if texts.get('source'):
        fig.add_annotation(
            text=texts['source'],
            xref="paper", yref="paper",
            x=0, y=0.01,
            xanchor='left', yanchor='bottom',
            showarrow=False,
            align="left",
            font=dict(family="Arial", size=10)
        )

    # Update layout
    fig.update_layout(
        showlegend=False,
        paper_bgcolor='white',
        plot_bgcolor='white',
        margin=dict(l=20, r=20, t=20, b=50),
        font=dict(family="Arial")
    )

    # Derive output filename and save the image
    base_filename = json_path.split('/')[-1].split('\\')[-1].rsplit('.', 1)[0]
    output_filename = f"{base_filename}.png"

    fig.write_image(output_filename, scale=2)
    print(f"Image saved to {output_filename}")

if __name__ == "__main__":
    main()