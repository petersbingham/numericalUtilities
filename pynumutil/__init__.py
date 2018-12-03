from pynumutil.release import __version__

precision = 8
min = pow(10,-precision)

absolute = 0
relative = 1
class NearlyEqual:
    def __init__(self, *args):
        if len(args) == 0:
            self.real_type = absolute
            self.real_val = min
            self.imag_type = absolute
            self.imag_val = min
        if len(args) == 1:
            self.real_type = absolute
            self.real_val = args[0]
            self.imag_type = absolute
            self.imag_val = args[0]
        elif len(args) == 2:
            self.real_type = args[0]
            self.real_val = args[1]
            self.imag_type = args[0]
            self.imag_val = args[1]
        elif len(args) == 4:
            self.real_type = args[0]
            self.real_val = args[1]
            self.imag_type = args[2]
            self.imag_val = args[3]

    def float_compare(self, f1, f2, complex=False):
        if complex:
            return self._compare(f1, f2, self.imag_type, self.imag_val)
        else:
            return self._compare(f1, f2, self.real_type, self.real_val)

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
    def __init__(self, rtol=None, ztol=0.0):
        self.rtol = rtol
        self.ztol = ztol

    def set_rtol(self, rtol):
        self.rtol = rtol

    def is_close(self, cval1, cval2, rtol=None):
        diff = self.get_complex_diff(cval1, cval2)
        return self.check_complex_diff(diff, rtol)

    def get_complex_diff(self, cval1, cval2):
        realdiff = self._get_diff(cval2.real, cval1.real)
        imagdiff = self._get_diff(cval2.imag, cval1.imag)
        return realdiff + 1.0j*imagdiff

    def check_complex_diff(self, cdiff, rtol=None):
        if rtol is None:
            rtol = self.rtol
        return cdiff.imag<rtol and cdiff.real<rtol

    def _get_diff(self, val1, val2):
        abs_val1 = abs(val1)
        abs_val2 = abs(val2)
        if abs_val1<=self.ztol and abs_val2<=self.ztol:
            return 0.0
        elif abs_val1>self.ztol and abs_val2>self.ztol:
            return self._cal_diff(val1, val2)
        elif abs_val1 > self.ztol:
            return self._cal_diff(val1, self.ztol)
        else:
            return self._cal_diff(self.ztol, val2)

    #https://en.wikipedia.org/wiki/Relative_change_and_difference
    def _cal_diff(self, val1, val2):
        abs_val1 = abs(val1)
        abs_val2 = abs(val2)
        valMax = abs_val2 if (abs_val1 < abs_val2) else abs_val1
        return abs(val2-val1) / valMax


def abs_diff(c1, c2):
    return abs(c1-c2)

def complex_diff(c1, c2):
    return c1-c2

def truncate_float(dps, val):
    return float(("{0:."+str(dps)+"f}").format(val))

def truncate_complex(dps, val):
    return truncate_float(dps,val.real) + truncate_float(dps,val.imag)*1.0j

def get_permutations(poss_vals, num_of):
    if num_of == 1:
        perms = [[x] for x in possVals]
    else:
        perms = []
        nextPerms = get_permutations(poss_vals, num_of-1)
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
        i_start = 0
        while i_start<len(lst)-1:
            com_val = _getVal(lst,i_start,accessor)
            for i in range(i_start+1, len(lst)):
                if comparator.complex_compare(com_val,_getVal(lst,i,accessor)):
                    lst.pop(i)
                    break
                elif i == len(lst)-1:
                    i_start += 1

# Remove trailing zero from scientific notation string.
def sci_str(n):
    a = '%e' % n
    return a.split('e')[0].rstrip('0').rstrip('.') + 'e' + a.split('e')[1]

def find_closest(target, shots):
  closest_shot = None
  for shot in shots:
    if closest_shot is None or abs(float(shot)-target) < abs(float(closest_shot)-target):
      closest_shot = float(shot)
  return closest_shot

def _lock_closest_(targets, equal_grp):
  smallest_delta = None
  smallest_index = None
  for i in equal_grp:
    delta = abs(targets[i][0] - targets[i][1])
    if smallest_delta is None or smallest_delta > delta:
      smallest_delta = delta
      smallest_index = i
  targets[smallest_index][2] = True

def _lock_closest(targets, equal_grps):
  for equal_grp in equal_grps.values():
    _lock_closest_(targets, equal_grp)

def match_closest(targets, shots):
  if isinstance(targets[0], float) or isinstance(targets[0], int):
    targets = [[target,None,False] for target in targets]
  for target in targets:
    if not target[2]:
      target[1] = find_closest(target[0], shots)
  equal_grps = {}
  for i,target in enumerate(targets):    
    if not target[2]:
      if target[1] not in equal_grps:
        equal_grps[target[1]] = [i]
      else:
        equal_grps[target[1]].append(i)
  _lock_closest(targets, equal_grps)    

  all_locked = True
  for target in targets:
    if target[2]:
      try:
        shots.discard(target[1])
      except AttributeError:
        try:
          shots.remove(target[1])
        except ValueError:
          pass
    else:
      all_locked = False

  if not all_locked:
    return match_closest(targets, shots)
  else:
    return [[target[0], target[1]] for target in targets]
