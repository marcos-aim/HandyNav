import json
import pandas as pd


class Gesture:
    fingers: list
    shape: str
    movement: list
    action: list

    def __init__(self, fingers, shape, movement, action):
        self.fingers = fingers
        self.shape = shape
        self.movement = movement
        self.action = action

    def __str__(self):
        return (f"Lifted Fingers: {self.fingers},"
                f" Shape: {self.shape},"
                f" Movement Bounds: {self.movement},"
                f" Action: {self.action}")

    def to_json(self):
        # Convert the Gesture instance to a dictionary
        gesture_dict = {
            "fingers": self.fingers,
            "shape": self.shape,
            "movement": self.movement,
            "action": self.action
        }
        # Convert the dictionary to a JSON string
        return json.dumps(gesture_dict)


class InputGesture(Gesture):

    def __init__(self, fingers, shape, movement):
        super().__init__(fingers, shape, movement, action=[])

    def __str__(self):
        return (f"Lifted Fingers: {self.fingers},"
                f" Shape: {self.shape},"
                f" Movement Bounds: {self.movement}")


def json_to_dataframe(json_data):
    gestures = []
    for gesture_json in json_data:
        gesture_dict = json.loads(gesture_json)
        # Ensure that 'action' is a list
        if not isinstance(gesture_dict['action'], list):
            gesture_dict['action'] = [gesture_dict['action']]
        gesture = Gesture(gesture_dict['fingers'], gesture_dict['shape'], gesture_dict['movement'],
                          gesture_dict['action'])
        gestures.append(gesture)

    # Create a DataFrame from the list of gestures
    df = pd.DataFrame([vars(gesture) for gesture in gestures])

    return df


def find_matching_action(input_gesture, gestures_df):
    # Check if there are any matching gestures in the DataFrame
    matching_gestures = gestures_df[
        (gestures_df['fingers'] == input_gesture.fingers) &
        (gestures_df['shape'] == input_gesture.shape)
        ]

    if not matching_gestures.empty:
        # If there are matching gestures, return the action from the first one
        return matching_gestures.iloc[0]['action']
    else:
        # If no matching gestures are found, return an error code
        return "No matching gesture found"
