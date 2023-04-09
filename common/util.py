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
    correct_error = all_angle_errors[correct_angle_booleans].mean()
    return {
        'availability': availability,
        'error_rate': error_rate,
        'attitude_error': correct_error,
    }
