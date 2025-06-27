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
