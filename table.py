import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

def draw_table_frame(speeds, shot_classif, player_info, frame_idx, fps=25,
                     last_max_state=None, max_fade_tracker=None,
                     last_shot_state=None, fade_duration=10):
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

    fig, ax = plt.subplots(figsize=(5.2, 2.2))
    ax.axis('off')

    players = sorted(player_info.keys())
    col_labels = ["Player", "Avg Speed (1s)", "Max Speed", "Avg Shot", "Max Shot"]
    table_data = []
    cell_colors = []
    cell_text_props = {}

    new_max_state = {}
    new_shot_state = {}
    new_fade_tracker = {} if max_fade_tracker is None else max_fade_tracker.copy()

    for row_idx, player in enumerate(players, start=1):
        name = player_info[player]['name']
        frame_keys = sorted([f for f in speeds[player] if f <= frame_idx])

        # --- AVG Speed over last 1s
        if len(frame_keys) >= 1:
            recent_frames = [f for f in frame_keys if f >= frame_idx - fps]
            avg_speed = np.mean([speeds[player][f] for f in recent_frames]) if recent_frames else 0
            max_speed = np.max([speeds[player][f] for f in frame_keys])
        else:
            avg_speed = 0
            max_speed = 0

        # --- Shots
        player_shots = [s for s in shot_classif if s['player'] == player and s['frame'] <= frame_idx]
        shot_dists = [s['distance'] for s in player_shots]
        avg_shot = np.mean(shot_dists) if shot_dists else 0
        max_shot = np.max(shot_dists) if shot_dists else 0

        new_max_state[player] = {"max_speed": max_speed, "max_shot": max_shot}

        # --- Build row
        row = [
            name,
            f"{avg_speed:.1f}",
            f"{max_speed:.1f}",
            f"{avg_shot:.1f}",
            f"{max_shot:.1f}"
        ]
        table_data.append(row)
        cell_colors.append(['white'] * len(col_labels))  # no background coloring

        # --- Bold fading logic
        prev = last_max_state.get(player, {}) if last_max_state else {}

        for col_idx, metric in zip([2, 4], ["max_speed", "max_shot"]):
            prev_val = prev.get(metric, -1)
            cur_val = new_max_state[player][metric]

            key = (player, metric)

            if cur_val > prev_val:
                new_fade_tracker[key] = fade_duration  # reset fade
            elif key in new_fade_tracker:
                new_fade_tracker[key] = max(0, new_fade_tracker[key] - 1)

            fade_value = new_fade_tracker.get(key, 0)
            if fade_value > 0:
                font_size = 8 + int(2 * fade_value / fade_duration)  # fade out size
                weight = 'bold'
            else:
                font_size = 8
                weight = 'normal'

            cell_text_props[(row_idx, col_idx)] = {'weight': weight, 'size': font_size, 'color': 'black'}

    # --- Draw table
    table = ax.table(cellText=table_data,
                     colLabels=col_labels,
                     cellLoc='center',
                     cellColours=cell_colors,
                     loc='center')

    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1.3, 1.4)

    for (row, col), cell in table.get_celld().items():
        if row == 0:
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor('#444444')
        elif (row, col) in cell_text_props:
            props = cell_text_props[(row, col)]
            cell.set_text_props(weight=props['weight'],
                                size=props['size'],
                                color=props['color'])

    # Render
    canvas = FigureCanvas(fig)
    canvas.draw()
    img = np.asarray(canvas.get_renderer().buffer_rgba())[..., :3].copy()
    plt.close(fig)

    return img, new_max_state, new_shot_state, new_fade_tracker



def create_table_video(bbox_dico, shot_classif, player_info, output_path="table_stats_styled.mp4", fps=25):
    speeds = compute_speeds(bbox_dico, fps)
    all_frames = sorted(set.intersection(*(set(speeds[p].keys()) for p in player_info)))

    last_max_state = {}
    last_shot_state = {}
    max_fade_tracker = {}

    # First frame
    sample_img, _, _, _ = draw_table_frame(
        speeds, shot_classif, player_info, all_frames[0], fps,
        last_max_state, max_fade_tracker, last_shot_state
    )
    h, w, _ = sample_img.shape
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (w, h))

    for frame in all_frames:
        frame_img, last_max_state, last_shot_state, max_fade_tracker = draw_table_frame(
            speeds, shot_classif, player_info, frame, fps,
            last_max_state=last_max_state,
            max_fade_tracker=max_fade_tracker,
            last_shot_state=last_shot_state
        )

        frame_bgr = cv2.cvtColor(frame_img, cv2.COLOR_RGB2BGR)
        out.write(frame_bgr)

    out.release()
    print(f"Saved with max transitions: {output_path}")
