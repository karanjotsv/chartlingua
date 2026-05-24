import sys
import json
import os
import plotly.graph_objects as go

def main():
    """
    Main function to generate a chart from a JSON file.
    """
    if len(sys.argv) != 2:
        print(f"Usage: python {os.path.basename(sys.argv[0])} <json_file_path>")
        sys.exit(1)

    json_path = sys.argv[1]

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            chart_info = json.load(f)
    except FileNotFoundError:
        print(f"Error: JSON file not found at '{json_path}'")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from '{json_path}'")
        sys.exit(1)

    # Extract data from the JSON structure
    data = chart_info['chart_data']
    texts = chart_info['texts']
    colors = chart_info['colors']
    
    # Unpack data into lists for plotting
    dates = [d['date'] for d in data]
    edits = [d['Edits'] for d in data]
    total_edits = [d['Total edits'] for d in data]
    avg_per_day = [d['Average per Day'] for d in data]
    
    # The actual cumulative total from data to match the blue line's end point
    cumulative_total_edits = [sum(edits[:i+1]) for i in range(len(edits))]

    # Create the figure object
    fig = go.Figure()

    # Add Edits bar trace (Primary Y-axis)
    fig.add_trace(go.Bar(
        x=dates,
        y=edits,
        name=texts['legend_labels']['Edits'],
        marker_color=colors['Edits'],
        yaxis='y1'
    ))

    # Add Total edits line trace (Secondary Y-axis)
    fig.add_trace(go.Scatter(
        x=dates,
        y=cumulative_total_edits,
        name=texts['legend_labels']['Total edits'],
        mode='lines',
        line=dict(color=colors['Total edits'], width=2),
        yaxis='y2'
    ))

    # Add Average per Day line trace (Primary Y-axis)
    fig.add_trace(go.Scatter(
        x=dates,
        y=avg_per_day,
        name=texts['legend_labels']['Average per Day'],
        mode='lines',
        line=dict(color=colors['Average per Day'], width=2),
        yaxis='y1'
    ))

    # Update layout to match the original chart's appearance
    fig.update_layout(
        title_text=texts['title'],
        title_x=0.5,
        plot_bgcolor='#D3D3D3',
        paper_bgcolor='white',
        font=dict(family="Arial", size=12),
        xaxis=dict(
            title_text=texts.get('x_axis_title'),
            showgrid=False,
            zeroline=False,
            tickformat='%Y-%m-%d',
            nticks=25 # Approximate the number of ticks from the original
        ),
        yaxis=dict(
            title=texts['y_axis_title'],
            side='left',
            range=[0, 140],
            gridcolor='white',
            showgrid=True,
            zeroline=True,
            zerolinecolor='white'
        ),
        yaxis2=dict(
            title=texts['y2_axis_title'],
            overlaying='y',
            side='right',
            range=[0, 2000],
            showgrid=False,
            zeroline=False
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5,
            bgcolor='white',
            bordercolor='black',
            borderwidth=1
        ),
        margin=dict(l=80, r=80, t=80, b=120)
    )

    # Determine output filename and save the image
    base_filename = os.path.splitext(os.path.basename(json_path))[0]
    output_filename = f"{base_filename}.png"

    fig.write_image(output_filename, scale=2)
    print(f"Chart successfully saved to {output_filename}")

if __name__ == "__main__":
    # Wrapping in a main function for better structure, but keeping it script-like.
    # No external function definitions as requested.
    main()