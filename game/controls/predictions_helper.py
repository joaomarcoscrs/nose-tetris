# Predictions helper functions
def get_class_prediction(predictions, class_name):
    if predictions is None:
        return None
    
    for prediction in predictions:
        if prediction['class'] == class_name:
            return prediction
    return None

def get_nose_prediction(predictions):
    return get_class_prediction(predictions, 'nose-axis')

def get_eye_prediction(predictions):
    return get_class_prediction(predictions, 'eye-axis')

# Keypoints helper functions

def get_keypoint(keypoints, keypoint_name):
    for keypoint in keypoints:
        if keypoint['class_name'] == keypoint_name:
            return keypoint
    return None

def get_nose_top(predictions):
    nose_prediction = get_nose_prediction(predictions)
    if nose_prediction is None:
        return None
    
    return get_keypoint(nose_prediction['keypoints'], 'top')

def get_nose_bottom(predictions):
    nose_prediction = get_nose_prediction(predictions)
    if nose_prediction is None:
        return None
    
    return get_keypoint(nose_prediction['keypoints'], 'bottom')

def get_nose_tip(predictions):
    nose_prediction = get_nose_prediction(predictions)
    if nose_prediction is None:
        return None
    
    return get_keypoint(nose_prediction['keypoints'], 'tip')

def get_left_eye(predictions):
    eye_prediction = get_eye_prediction(predictions)
    if eye_prediction is None:
        return None
    
    return get_keypoint(eye_prediction['keypoints'], 'left')

def get_right_eye(predictions):
    eye_prediction = get_eye_prediction(predictions)
    if eye_prediction is None:
        return None
    
    return get_keypoint(eye_prediction['keypoints'], 'right')