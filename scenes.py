import scenedetect
from subprocess import check_output


class PySceneDetectArgs(object):

    def __init__(self, input, type='content', threshold=30):
        self.input = input
        self.detection_method = type
        self.threshold = threshold
        self.min_percent = None
        self.min_scene_len = None
        self.block_size = None
        self.fade_bias = None
        self.downscale_factor = None
        self.frame_skip = None
        self.save_images = False
        self.start_time = None
        self.end_time = None
        self.duration = None
        self.quiet_mode = False
        self.stats_file = None


# Get frames of different scenes from video
def get_frames(input_file_name, output_file_name="output.avi", output_directory_name="data", detector="content", threshold=30):

    # Scenedetect Python endpoints are not stable
    scene_detectors = scenedetect.detectors.get_available()

    smgr_content = scenedetect.manager.SceneManager(
        PySceneDetectArgs(input=input_file_name, type=detector, threshold=threshold), scene_detectors)

    video_fps, frames_read, frames_processed = scenedetect.detect_scenes_file(
        path=input_file_name, scene_manager=smgr_content)

    # Frames where next scene starts
    detected_frames = smgr_content.scene_list
    # Time in millisec where next scene starts
    scene_list_msec = [(1000.0 * x) / float(video_fps)
                       for x in detected_frames]

    # Write output
    if output_file_name is not None and len(detected_frames) > 0:
        create_directory(output_directory_name)
        timecode_list_str = ','.join(
            [scenedetect.timecodes.get_string(x) for x in scene_list_msec])
        scenedetect.split_input_video(
            input_file_name, output_directory_name + "/" + output_file_name, timecode_list_str)

    return {
        "frames": detected_frames,
        "start_times": scene_list_msec,
        "fps": video_fps
    }


# Store scenes is a directory
def create_directory(name="data"):
    #check_output(["rm", "-rf", name])
    #check_output(["mkdir", name])
    return
