import pytest
from ..main import str_len, concatenated_str

def test_str_len() -> None: 
   assert str_len("hello") == 5

def test_conc_str() -> None:
   """Verify that the concatenated_str function returns the correct result."""
        
   assert concatenated_str("Py", "thon") == "Python"

   with pytest.raises(TypeError):
      concatenated_str(" ", 4)

# (set_up_venv) kilimovaann@MacBook-Air-Kilimova set_up_venv % pytest HW_1/str_data/py_tests/test_strings_1_param.py -v