import t_application_lifecycle as al
import pytest


def test_correct_expression_is_ok():
    forced_headers_str = "['h1', 'h2', 'h3', 'h4']"
    result = al.eval_forced_headers(forced_headers_str)
    expected = ['h1', 'h2', 'h3', 'h4']
    assert result == expected


def test_wrong_expression_throws_exception():
    forced_headers_str = "['h1', 'h2', 'h3', 'h4]"
    with pytest.raises(SyntaxError) as e_info:
        al.eval_forced_headers(forced_headers_str)

# More tests that could be done here:
# test_not_list_of_strings - This would check the case of a valid expression, but that is not a list of strings.
#                            Not going to implement it as it would also require changes to the method and might also
#                            make it less readable.
