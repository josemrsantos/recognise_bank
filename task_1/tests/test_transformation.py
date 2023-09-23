import t_application_lifecycle as al
import pytest


def test_correct_read_sets_correct_values():
    in_file_name = 'tests/test_input_ok.csv'
    transformation = al.TransformApplicationLifecycle(in_file_name=in_file_name)
    transformation.fetch_data()
    expected_headers = ['UniqueID', 'REGISTERED_0', 'INITIATED_0', 'APPOINTMENT_SCHEDULED_0', 'CLOSED_0',
                        'ACKNOWLEDGED_0', 'APPROVED_0', 'ON_HOLD_0', 'APPROVED_1']
    expected_data_1 = {'UniqueID': '15572956', 'REGISTERED_0': 'May 01 2019, 13:48:28',
                       'INITIATED_0': 'May 01 2019, 13:51:18', 'APPOINTMENT_SCHEDULED_0': 'May 01 2019, 13:56:49',
                       'ACKNOWLEDGED_0': 'May 07 2019, 04:09:47', 'APPROVED_0': 'May 08 2019, 02:24:18',
                       'ON_HOLD_0': 'Feb 16 2020, 15:45:09', 'APPROVED_1': 'Feb 19 2020, 10:30:23'}
    assert transformation.headers == expected_headers
    assert transformation.data[1] == expected_data_1


def test_wrong_filename_throws_exception():
    in_file_name = 'no_such_file.csv'
    transformation = al.TransformApplicationLifecycle(in_file_name=in_file_name)
    with pytest.raises(FileNotFoundError) as e_info:
        transformation.fetch_data()


def test_different_input_format_throws_exception():
    in_file_name = 'tests/test_input_eval_error.csv'
    transformation = al.TransformApplicationLifecycle(in_file_name=in_file_name)
    # Should have created an Exception for this case and throw it from the list comprehension
    with pytest.raises(IndexError) as e_info:
        transformation.fetch_data()


def test_different_timestamp_format_throws_exception():
    in_file_name = 'tests/test_input_timestamp_error.csv'
    transformation = al.TransformApplicationLifecycle(in_file_name=in_file_name)
    # Should have created an Exception for this case and throw it from the list comprehension
    with pytest.raises(ValueError) as e_info:
        transformation.fetch_data()
        assert 'does not match format' in e_info


def test_correct_read_and_transformation_sets_correct_values():
    in_file_name = 'tests/test_input_ok.csv'
    transformation = al.TransformApplicationLifecycle(in_file_name=in_file_name)
    transformation.fetch_data()
    transformation.transform()
    expected_result = [['UniqueID', 'REGISTERED_0', 'INITIATED_0', 'APPOINTMENT_SCHEDULED_0', 'CLOSED_0',
                        'ACKNOWLEDGED_0', 'APPROVED_0', 'ON_HOLD_0', 'APPROVED_1'],
                       ['15569264', 'Aug 08 2019, 04:12:53', 'Aug 09 2019, 05:20:06', 'Aug 09 2019, 05:49:25',
                        'Dec 13 2019, 08:08:35', '', '', '', ''],
                       ['15572956', 'May 01 2019, 13:48:28', 'May 01 2019, 13:51:18', 'May 01 2019, 13:56:49', '',
                        'May 07 2019, 04:09:47', 'May 08 2019, 02:24:18', 'Feb 16 2020, 15:45:09',
                        'Feb 19 2020, 10:30:23']
                       ]
    assert transformation.result == expected_result


def test_forced_headers_correct_read_and_transformation_sets_correct_values():
    in_file_name = 'tests/test_input_ok.csv'
    forced_headers = ['UniqueID', 'APPROVED_0', 'REGISTERED_0', 'INITIATED_0', 'APPOINTMENT_SCHEDULED_0', 'CLOSED_0',
                      'ACKNOWLEDGED_0', 'ON_HOLD_0', 'APPROVED_1']
    transformation = al.TransformApplicationLifecycle(in_file_name=in_file_name, forced_headers=forced_headers)
    transformation.fetch_data()
    transformation.transform()
    expected_result = [['UniqueID', 'APPROVED_0', 'REGISTERED_0', 'INITIATED_0', 'APPOINTMENT_SCHEDULED_0', 'CLOSED_0',
                        'ACKNOWLEDGED_0', 'ON_HOLD_0', 'APPROVED_1'],
                       ['15569264', '', 'Aug 08 2019, 04:12:53', 'Aug 09 2019, 05:20:06', 'Aug 09 2019, 05:49:25',
                        'Dec 13 2019, 08:08:35', '', '', ''],
                       ['15572956', 'May 08 2019, 02:24:18', 'May 01 2019, 13:48:28', 'May 01 2019, 13:51:18',
                        'May 01 2019, 13:56:49', '', 'May 07 2019, 04:09:47', 'Feb 16 2020, 15:45:09',
                        'Feb 19 2020, 10:30:23']]
    assert transformation.result == expected_result


def test_invalid_forced_header_throws_exception():
    in_file_name = 'tests/test_input_ok.csv'
    forced_headers = ['UniqueID', 'NoSuchHeader', 'REGISTERED_0', 'INITIATED_0', 'APPOINTMENT_SCHEDULED_0', 'CLOSED_0',
                      'ACKNOWLEDGED_0', 'ON_HOLD_0', 'APPROVED_1']
    transformation = al.TransformApplicationLifecycle(in_file_name=in_file_name, forced_headers=forced_headers)
    transformation.fetch_data()
    with pytest.raises(Exception) as e_info:
        transformation.fetch_data()
        assert e_info == 'Forced headers are not the same as the headers found on the data.'


def test_unique_column_name_returns_ok():
    transformation = al.TransformApplicationLifecycle()
    columns = {'test1':0}
    name = 'test1'
    result = transformation.unique_column_name(columns, name)
    assert result == 'test1_1'
    assert columns == {'test1':1}


def test_unique_columns_empty_name_returns_ok():
    transformation = al.TransformApplicationLifecycle()
    columns = {}
    name = 'test1'
    result = transformation.unique_column_name(columns, name)
    assert result == 'test1_0'
    assert columns == {'test1':0}


def test_unique_column_name_wrong_columns_type_throws_exception():
    transformation = al.TransformApplicationLifecycle()
    columns = 'this should be a dictionary'
    name = 'test1'
    with pytest.raises(AttributeError) as e_info:
        transformation.unique_column_name(columns, name)
        assert "object has no attribute 'get'" in e_info
