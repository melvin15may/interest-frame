from subprocess import check_output


# Save scenes from video
def save_scenes(input_path, output_path='output.mkv', detector="content", threshold=30):
    # Add Python endpoints when more stable version for pyscenedetect is
    # available
    check_output(["scenedetect", "-i", input_path, "-d",
                  detector, "-t", str(threshold), "-o", output_path])
    return
