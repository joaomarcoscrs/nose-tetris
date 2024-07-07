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
        
        # Set the line color based on the class
        if prediction['class'] == 'eye-axis':
            line_color = (0, 0, 0)  # Black color for eye-axis
        elif prediction['class'] == 'nose-axis':
            line_color = (128, 0, 128)  # Purple color for nose-axis
        else:
            line_color = (0, 255, 0)  # Default to green if class is not recognized
        
        # Draw lines between keypoints
        for i in range(len(keypoints) - 1):
            start_point = (int(keypoints[i]['x']), int(keypoints[i]['y']))
            end_point = (int(keypoints[i + 1]['x']), int(keypoints[i + 1]['y']))
            thickness = 2
            cv2.line(image, start_point, end_point, line_color, thickness)
        
        # Draw the keypoints and their labels
        for keypoint in keypoints:
            center = (int(keypoint['x']), int(keypoint['y']))
            radius = 3
            point_color = line_color
            thickness = -1  # Solid circle
            cv2.circle(image, center, radius, point_color, thickness)
            
            # Draw the label next to the keypoint
            label = keypoint['class_name']
            label_position = (center[0] + 5, center[1] - 5)  # Offset the label position slightly
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.5
            font_color = (255, 255, 255)  # White color for text
            font_thickness = 1
            cv2.putText(image, label, label_position, font, font_scale, font_color, font_thickness, cv2.LINE_AA)

    return image

def render_annotated_image(predictions: dict, video_frame: VideoFrame):
    # get the text labels for each prediction
    labels = [p["class"] for p in predictions["predictions"]]
    # load our predictions into the Supervision Detections api
    detections = sv.Detections.from_inference(predictions)
    # annotate the frame using our supervision annotator, the video_frame, the predictions (as supervision Detections), and the prediction labels
    # image = label_annotator.annotate(
    #     scene=video_frame.image.copy(), detections=detections, labels=labels
    # )
    # image = box_annotator.annotate(image, detections=detections)
    
    image = annotate_keypoints(video_frame.image.copy(), predictions["predictions"])
  
    # display the annotated image
    cv2.imshow("Predictions", image)
    cv2.waitKey(1)

# initialize a pipeline object
pipeline = InferencePipeline.init(
    model_id="facial-features-keypoints/1", # Roboflow model to use
    video_reference=0, # Path to video, device id (int, usually 0 for built in webcams), or RTSP stream url
    on_prediction=render_annotated_image, # Function to run after each prediction
    max_fps=10, # Maximum frames per second to process
)
pipeline.start()
pipeline.join()