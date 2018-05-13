# pynumutil
Simple Numerical Utilities. In particular some objects for comparing and calculating difference between complex numbers.

## Installation

Clone the repository and install with the following commands:

    git clone https://github.com/petersbingham/pynumutil.git
    cd pynumutil
    python setup.py install
    
## Dependencies
None
    
## Usage
Reader is referred to the pynumutil/\_\_init\_\_.py file for details.
There are two comparison classes `NearlyEqual` and `RationalCompare1`. More are planned for later.

### `nearlyEqual`
`NearlyEqual` returns a boolean from it's functions (see \_\_init\_\_.py file) if two numbers are deemed to be nearly equal to one another. If the numbers are complex then the test is performed separately on the real and imaginary components. The type of test is determined by the number of and values of the parameters supplied to the constructor, according to the following:
 - 0 parameters: The test is an absolute comparison and tests positive if the absolute of the difference is less than or equal to 10^-8.
 - 1 parameter: This specifies the threshold for comparison (ie replaces the 10^-8). The test type is absolute.
 - 2 parameters: The first parameter specifies the test type, the second the threshold for comparison. The test type can be specified using the enum in the package scope, either `absolute` or `percent`.
 - 4 parameters: As for 2 parameters except applied separately to both the real and imaginary components separately.

### `RationalCompare1`
This applies the formula |x-y| / max(|x|,|y|) separately to the real and imaginary components of two complex numbers x and y if both |x| and |y| are greater than some minimum value (`zeroValue`). If either |x| or |y| exclusively are less than or equal to `zeroValue` then the formula is applied using the minimum value for the smallest of |x| and |y|. If both |x| and |y| are less than or equal to `zeroValue` then zero is returned. `zeroValue` is optionally specified in the constructor of `rationalCompare1`, along with `distThres`, which specifies a value equal to or above which the numbers are deemed distinct.
