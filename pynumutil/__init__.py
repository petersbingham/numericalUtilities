precision = 8
min = pow(10,-precision)

absolute = 0
percent = 1
class NearlyEqual:
    def __init__(self, *args):
        if len(args) == 0:
            self.realType = absolute
            self.realVal = min
            self.imagType = absolute
            self.imagVal = min
        if len(args) == 1:
            self.realType = absolute
            self.realVal = args[0]
            self.imagType = absolute
            self.imagVal = args[0]
        elif len(args) == 2:
            self.realType = args[0]
            self.realVal = args[1]
            self.imagType = args[0]
            self.imagVal = args[1]
        elif len(args) == 4:
            self.realType = args[0]
            self.realVal = args[1]
            self.imagType = args[2]
            self.imagVal = args[3]

    def float_compare(self, f1, f2, complex=False):
        if complex:
            return self._compare(f1, f2, self.imagType, self.imagVal)
        else:
            return self._compare(f1, f2, self.realType, self.realVal)

    def complex_compare(self, c1, c2):
        if not self.float_compare(complex(c1).real, complex(c2).real, False):
            return False
        if not self.float_compare(complex(c1).imag, complex(c2).imag, True):
            return False
        return True

    def _compare(self, f1, f2, type, val):
        if type == absolute:
            return self._absCmp(f1, f2, val)
        else:
            return self._relCmp(f1, f2, val)

    def _absCmp(self, f1, f2, cmpVal):
        if abs(f1-f2) > cmpVal:
            return False
        return True

    def _relCmp(self, f1, f2, cmpVal):
        if abs(f1-f2)/f1*100 > cmpVal:
            return False
        return True


class RationalCompare1:
    def __init__(self, zero_value=0.0, dist_thres=None):
        self.dist_thres = dist_thres
        self.zero_value = zero_value

    def is_close(self, cval1, cval2, dist_thres=None):
        diff = self.get_complex_diff(cval1, cval2)
        return self.check_complex_diff(diff, dist_thres)

    def get_complex_diff(self, cval1, cval2):
        realdiff = self._get_diff(cval2.real, cval1.real)
        imagdiff = self._get_diff(cval2.imag, cval1.imag)
        return realdiff + 1.0j*imagdiff

    def check_complex_diff(self, cdiff, dist_thres=None):
        if dist_thres is None:
            dist_thres = self.dist_thres
        return cdiff.imag<dist_thres and cdiff.real<dist_thres

    def _get_diff(self, val1, val2):
        absVal1 = abs(val1)
        absVal2 = abs(val2)
        if absVal1<=self.zero_value and absVal2<=self.zero_value:
            return 0.0
        elif absVal1>self.zero_value and absVal2>self.zero_value:
            return self._cal_diff(val1, val2)
        elif absVal1 > self.zero_value:
            return self._cal_diff(val1, self.zero_value)
        else:
            return self._cal_diff(self.zero_value, val2)

    #https://en.wikipedia.org/wiki/Relative_change_and_difference
    def _cal_diff(self, val1, val2):
        absVal1 = abs(val1)
        absVal2 = abs(val2)
        valMax = absVal2 if (absVal1 < absVal2) else absVal1
        return abs(val2-val1) / valMax


def abs_diff(c1, c2):
    return abs(c1-c2)

def complex_diff(c1, c2):
    return c1-c2

def truncate_float(dps, val):
    return float(("{0:."+str(dps)+"f}").format(val))

def truncate_complex(dps, val):
    return truncate_float(dps,val.real) + truncate_float(dps,val.imag)*1.0j

def get_permutations(poss_vals, numOf):
    if numOf == 1:
        perms = [[x] for x in possVals]
    else:
        perms = []
        nextPerms = get_permutations(poss_vals, numOf-1)
        for val in poss_vals:
            for nextPerm in nextPerms:
                perms.append([val]+nextPerm)
    return perms

def remove_duplicate_floats(lst, comparator, accessor=None):
    def _getVal(lst,i,accessor):
        if accessor:
            return accessor(lst[i])
        else:
            return lst[i]

    if len(lst) > 0:
        iStart = 0
        while iStart<len(lst)-1:
            comVal = _getVal(lst,iStart,accessor)
            for i in range(iStart+1, len(lst)):
                if comparator.complex_compare(comVal,_getVal(lst,i,accessor)):
                    lst.pop(i)
                    break
                elif i == len(lst)-1:
                    iStart += 1

def sci_str(n):
    a = '%e' % n
    return a.split('e')[0].rstrip('0').rstrip('.') + 'e' + a.split('e')[1]
