import toml
import numpy as np
from pathlib import Path

from .utils import VALID_ROTATION_TYPES
from .pose import Pose
from .transform import Transform


class TransformSet:
    def __init__(self, transf_set: str|Path|dict) -> None:

        self.frames = dict()
        if isinstance(transf_set, str) or isinstance(transf_set, Path):
            self.__frame_data = toml.load(transf_set)
        elif isinstance(transf_set, dict):
            self.__frame_data = transf_set

        # Create dictionary of frames (from which we can create transformations)
        for frame_name, frame_data in self.__frame_data.items():
            self.add_frame(frame_name=frame_name, frame_data=frame_data)

        # Add base frame if not present
        if 'base' not in self.frame_names():
            base_frame = Pose(name='base')
            base_frame.position.zero()
            base_frame.orientation.identity()
            self.frames['base'] = base_frame
        

    # Setter functions
    def add_frame(self, frame_name: str, frame_data: dict) -> None:
        new_frame = Pose(name=frame_name)

        # Extract position
        new_frame.position.from_vector(frame_data['position'])

        # Extract orientation
        orientation_value = frame_data['orientation']
        orientation_type = frame_data['orientation_type'].lower()
        degrees = 'degree' in frame_data['orientation_untis'].lower()

        if orientation_type == 'euler':
            new_frame.orientation.from_euler('xyz', orientation_value, degrees=degrees)
        elif orientation_type == 'quaternion':
            new_frame.rotation.from_quat(orientation_value)
        elif orientation_type == 'angle-axis':
            new_frame.rotation.from_angle_axis(orientation_value)
        elif orientation_type == 'matrix':
            new_frame.rotation.from_matrix(orientation_value)
        else:
            raise ValueError(f'TransformSet - Invalid rotation type: {orientation_type}. Rotation type must be: {VALID_ROTATION_TYPES}')

        # Save new frame to self.frames
        self.frames[frame_name] = new_frame


    # Getter functions
    def frame_names(self) -> list:
        return self.frames.keys()


    def change_frame(self, input, from_frame: str, to_frame: str) -> np.ndarray:
        '''
        Coordinate transformation of a pose (6D vector) from origin frame to target frame.

        A compund transformation from origin frame (defined in `from_frame` argument) to
        the target frame (defined in `to_frame` argument) is computed and applied to the
        input pose.

        Args:
            input (np.ndarray): Input pose
            from_frame (str): Name of origin frame
            to_frame (str): Name of target frame

        Returns:
            np.ndarray: Transformed pose in target frame.
        '''
        # Create compound transformation
        transformation = self.__create_compound_transf(from_frame=from_frame, to_frame=to_frame)

        return transformation.apply(input)


    def wrench_change_frame(self, wrench: np.ndarray, from_frame: str, to_frame: str) -> np.ndarray:
        '''
        Function to change frame of wrench vector.

        Function will perform simple rotation on forces (first three elements), and
        will rotate the total moments on the origin frame.

        Args:
            wrench (np.ndarray): Input wrench array
            from_frame (str): Name of origin frame
            to_frame (str): Name of target frame

        Returns:
            np.ndarray: Transformed wrench array
        '''
        # Verify input
        if not np.array(wrench).shape == (6,):
            raise ValueError(f"TransformSet - Invalid wrench input. Shape must be (6,)")

        # Create compound transformation
        transformation = self.__create_compound_transf(from_frame=from_frame, to_frame=to_frame)

        # Transform wrench
        force_at_orig = wrench[:3]
        torque_at_orig = wrench[3:]

        torque_at_dest = transformation.rotation.apply(np.cross(force_at_orig, transformation.translation) + torque_at_orig)
        force_at_dest = transformation.rotation.apply(force_at_orig)

        return np.hstack([force_at_dest, torque_at_dest])


    def transform_matrix(self, from_frame: str, to_frame: str, homogeneous: bool = True) -> np.ndarray:
        '''
        Return the transformation matrix to transform poses from origin
        frame to destination frame.

        Function will call the `__create_compound_transf()` function. Note that such a matrix
        can only be directly used for poses. Other calculations are required for wrench
        transformations.

        Args:
            from_frame (str): Name of origin frame
            to_frame (str): Name of target frame
            homogeneous (bool, optional): Option if matrix should be homogenous or not (3x4 or 4x4). Defaults to True.

        Returns:
            np.ndarray: Numpy matrix
        '''
        # Create compound transformation
        full_transf = self.__create_compound_transf(from_frame, to_frame)

        return full_transf.matrix(homogeneous=homogeneous)


    def __create_compound_transf(self, from_frame: str, to_frame: str) -> Transform:
        '''
        Function to create compound transform between two frames.

        The function will create a transformation from one frame to another by 

        Args:
            from_frame (str): Name of origin frame
            to_frame (str): Name of destination frame

        Returns:
            Transform: Transform object
        '''
        transformation = Transform(name=f'{from_frame}2{to_frame}', orig=from_frame, dest=to_frame)
        transformation.between_poses(pose_1=self.frames[from_frame], pose_2=self.frames[to_frame])

        return transformation
