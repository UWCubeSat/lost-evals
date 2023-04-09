import os
import numpy as np
import quaternion

import common.params as params

def smallest_angle(quat):
    raw_angle = quat.normalized().angle()
    return (raw_angle if raw_angle < np.pi else 2*np.pi-raw_angle)

def compare_attitudes(actual, expected):
    """Return dict with availability, error rate, and average error for each correctly identified. It is important to pass arguments in the correct order, because expected shouldn't have any Nones in it, but actual can."""
    assert len(actual) == len(expected)
    actual = np.array(actual)
    expected = np.array(expected)
    known_booleans = np.array([a is not None for a in actual])
    actual_known = actual[known_booleans]
    expected_known = expected[known_booleans]
    quat_differences = actual_known*expected_known.conjugate()
    all_angle_errors = np.array(list(map(smallest_angle, quat_differences)))
    correct_angle_booleans = all_angle_errors < params.comprehensive_attitude_tolerance
    availability = correct_angle_booleans.sum() / len(actual)
    error_rate = (len(correct_angle_booleans) - correct_angle_booleans.sum()) / len(actual)
    correct_error = all_angle_errors[correct_angle_booleans].mean() if len(all_angle_errors[correct_angle_booleans]) > 0 else np.inf
    return {
        'availability': availability,
        'error_rate': error_rate,
        'attitude_error': correct_error,
    }

def quaternion_from_celestial_euler_angles(ra, de, roll):
    """Follows the same conventions as in LOST. Roll has a 50-50 chance of being flipped when comparing against third-party software"""
    # The exponential of a quaternion is morally similar to the exponential of an imaginary number.
    # The exponential of an imaginary number takes the (scalar logarithbm of) real part as the magnitude, and the imaginary part (in radians) as the rotation.
    # The exponential of a quaternion takes the (scalar logarithm of) real part a a magnitude also, the direction of the imaginary vector as the axis of rotation, and the magnitude of the imaginary vector (in radians) as the angle of rotation.
    return (ra*quaternion.z/2).exp() * (-de*quaternion.y/2).exp() * (-roll*quaternion.x/2).exp()

# This could just be a variable, but I don't want it throwing errors in scripts that don't need ost
def get_openstartracker_dir():
    if not 'OPENSTARTRACKER_DIR' in os.environ:
        raise Exception('OPENSTARTRACKER_DIR not set in environment')
    return os.environ['OPENSTARTRACKER_DIR']
