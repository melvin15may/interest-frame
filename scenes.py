from subprocess import call

# Save scenes from video
def save_scenes(input_path, output_path='output.mkv', detector="content", threshold=30):
    # Add Python endpoints when more stable version for pyscenedetect is available
    call(["scenedetect", "-i", input_path, "-d", detector, "-t", str(threshold), "-o", output_path])
    return