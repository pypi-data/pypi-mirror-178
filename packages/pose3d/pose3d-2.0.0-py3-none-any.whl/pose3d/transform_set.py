import toml
import numpy as np

from .transform import Transform


class TransformSet:
    def __init__(self, cfg_file: str) -> None:

        self.frame_data = toml.load(cfg_file)

        # Save names of transforms
        self.frame_names = []
        for frame_name in self.frame_data.keys():
            self.frame_names.append(frame_name)

        if 'base' not in self.frame_names:
            raise ValueError(f"TransformSet - No frame is marked as base frame. Please mark one of the frames as 'base'.")

        # Convert dictionary parameters to a list of transformations
        self.transformations = []
        valid_rotation_types = ['euler', 'quaternion', 'angle-axis', 'matrix', 'rodrigues']
        for frame_name in self.frame_data.keys():
            new_transf = Transform(name=frame_name, orig='base', dest=frame_name)
            new_transf.translation = self.frame_data[frame_name]['translation']

            degree_opt = 'degree' in self.frame_data[frame_name]['orientation_units']
            orientation_type = self.frame_data[frame_name]['orientation_type']
            orientation_value = self.frame_data[frame_name]['orientation']

            if orientation_type not in valid_rotation_types:
                raise ValueError(f'TransformSet - Invalid rotation type: {orientation_type}. Rotation type must be: {valid_rotation_types}')
            elif orientation_type == 'euler':
                new_transf.rotation.from_euler('xyz', orientation_value, degrees=degree_opt)
            elif orientation_type == 'quaternion':
                new_transf.rotation.from_quat(orientation_value)
            elif orientation_type == 'angle-axis':
                new_transf.rotation.from_angle_axis(orientation_value)
            elif orientation_type == 'matrix':
                new_transf.rotation.from_matrix(orientation_value)

            self.transformations.append(new_transf)


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
        full_transf = self.__create_compound_transf(from_frame, to_frame)

        return full_transf.apply(input)


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
        full_transf = self.__create_compound_transf(from_frame, to_frame)

        # Transform wrench
        force_at_orig = wrench[:3]
        torque_at_orig = wrench[3:]

        torque_at_dest = full_transf.rotation.apply(np.cross(force_at_orig, full_transf.translation) + torque_at_orig)
        force_at_dest = full_transf.rotation.apply(force_at_orig)

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
            from_frame (str): _description_
            to_frame (str): _description_

        Returns:
            Transform: _description_
        '''
        # Verify frame names
        if from_frame not in self.frame_names or to_frame not in self.frame_names:
            raise ValueError(f"TransformSet - Invalid frame name, names must be: {self.frame_names}")

        # Create transform to base frame from orig_frame
        if from_frame == 'base':
            transf_to_base = Transform(name="orig_is_base", orig='base', dest='base')
        else:
            orig_transf = self.transformations[self.frame_names.index(from_frame)]
            transf_to_base = orig_transf.inv()

        # Create transform from base frame from dest_frame
        if to_frame == 'base':
            transf_to_dest = Transform(name="dest_is_base", orig='base', dest='base')
        else:
            transf_to_dest = self.transformations[self.frame_names.index(to_frame)]

        # Create compound transformation
        full_transformation = Transform(name=f"{from_frame}2{to_frame}", orig=from_frame, dest=to_frame)
        full_transformation.translation = transf_to_base.rotation.apply(transf_to_dest.translation) + transf_to_base.translation
        full_transformation.rotation.from_matrix(np.matmul(transf_to_base.rotation.as_matrix(), transf_to_dest.rotation.as_matrix()))

        return full_transformation
