from inference import InferencePipeline
from inference.core.interfaces.camera.entities import VideoFrame

# import opencv to display our annotated images
import cv2
# import supervision to help visualize our predictions
import supervision as sv

# create a bounding box annotator and label annotator to use in our custom sink
label_annotator = sv.LabelAnnotator()
box_annotator = sv.BoundingBoxAnnotator()

def annotate_keypoints(image, predictions):
    for prediction in predictions:
        keypoints = prediction['keypoints']
        
        # Draw lines between keypoints
        for i in range(len(keypoints) - 1):
            start_point = (int(keypoints[i]['x']), int(keypoints[i]['y']))
            end_point = (int(keypoints[i + 1]['x']), int(keypoints[i + 1]['y']))
            color = (0, 0, 0) # black color for lines
            thickness = 1
            cv2.line(image, start_point, end_point, color, thickness)
        
        # Optionally, you can also draw the keypoints themselves
        for keypoint in keypoints:
            center = (int(keypoint['x']), int(keypoint['y']))
            radius = 2
            color = (0, 0, 0)  # Black color for keypoints
            thickness = -1  # Solid circle
            cv2.circle(image, center, radius, color, thickness)

    return image

def render_annotated_image(predictions: dict, video_frame: VideoFrame):
    # get the text labels for each prediction
    labels = [p["class"] for p in predictions["predictions"]]
    # load our predictions into the Supervision Detections api
    detections = sv.Detections.from_inference(predictions)
    # annotate the frame using our supervision annotator, the video_frame, the predictions (as supervision Detections), and the prediction labels
    image = label_annotator.annotate(
        scene=video_frame.image.copy(), detections=detections, labels=labels
    )
    image = box_annotator.annotate(image, detections=detections)
    
    image = annotate_keypoints(image, predictions["predictions"])
  
    # display the annotated image
    cv2.imshow("Predictions", image)
    cv2.waitKey(1)

# initialize a pipeline object
pipeline = InferencePipeline.init(
    model_id="facial-features-keypoints/1", # Roboflow model to use
    video_reference=0, # Path to video, device id (int, usually 0 for built in webcams), or RTSP stream url
    on_prediction=render_annotated_image, # Function to run after each prediction
    max_fps=30, # Maximum frames per second to process
)
pipeline.start()
pipeline.join()