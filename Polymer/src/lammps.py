import sys
import traceback
from ctypes import *


# TODO ???
class Lammps:

    def __init__(self, name="", cmdargs=None):
        try:
            if not name:
                self.lib = CDLL("liblammps.so", RTLD_GLOBAL)
            else:
                self.lib = CDLL("liblammps_%s.so" % name, RTLD_GLOBAL)
        except:
            type, value, tb = sys.exc_info()
            traceback.print_exception(type, value, tb)
            raise OSError("Could not load LAMMPS dynamic library")

        if cmdargs:
            cmdargs.insert(0, "lammps.py")
            narg = len(cmdargs)
            cargs = (c_char_p * narg)(*cmdargs)
            self.lmp = c_void_p()
            self.lib.lammps_open_no_mpi(narg, cargs, byref(self.lmp))
        else:
            self.lmp = c_void_p()
            self.lib.lammps_open_no_mpi(0, None, byref(self.lmp))

    def __del__(self):
        if self.lmp: self.lib.lammps_close(self.lmp)

    def close(self):
        self.lib.lammps_close(self.lmp)
        self.lmp = None

    def file(self, file):
        self.lib.lammps_file(self.lmp, file)

    def command(self, cmd):
        self.lib.lammps_command(self.lmp, cmd)

    def extract_global(self, name, type):
        if type == 0:
            self.lib.lammps_extract_global.restype = POINTER(c_int)
        elif type == 1:
            self.lib.lammps_extract_global.restype = POINTER(c_double)
        else:
            return None
        ptr = self.lib.lammps_extract_global(self.lmp, name)
        return ptr[0]

    def extract_atom(self, name, type):
        if type == 0:
            self.lib.lammps_extract_atom.restype = POINTER(c_int)
        elif type == 1:
            self.lib.lammps_extract_atom.restype = POINTER(POINTER(c_int))
        elif type == 2:
            self.lib.lammps_extract_atom.restype = POINTER(c_double)
        elif type == 3:
            self.lib.lammps_extract_atom.restype = POINTER(POINTER(c_double))
        else:
            return None
        ptr = self.lib.lammps_extract_atom(self.lmp, name)
        return ptr

    def extract_compute(self, id, style, type):
        if type == 0:
            if style > 0: return None
            self.lib.lammps_extract_compute.restype = POINTER(c_double)
            ptr = self.lib.lammps_extract_compute(self.lmp, id, style, type)
            return ptr[0]
        if type == 1:
            self.lib.lammps_extract_compute.restype = POINTER(c_double)
            ptr = self.lib.lammps_extract_compute(self.lmp, id, style, type)
            return ptr
        if type == 2:
            self.lib.lammps_extract_compute.restype = POINTER(POINTER(c_double))
            ptr = self.lib.lammps_extract_compute(self.lmp, id, style, type)
            return ptr
        return None

    def extract_fix(self, id, style, type, i=0, j=0):
        if type == 0:
            if style > 0:
                return None

            self.lib.lammps_extract_fix.restype = POINTER(c_double)
            ptr = self.lib.lammps_extract_fix(self.lmp, id, style, type, i, j)
            result = ptr[0]
            self.lib.lammps_free(ptr)
            return result
        if type == 1:
            self.lib.lammps_extract_fix.restype = POINTER(c_double)
            ptr = self.lib.lammps_extract_fix(self.lmp, id, style, type, i, j)
            return ptr
        if type == 2:
            self.lib.lammps_extract_fix.restype = POINTER(POINTER(c_double))
            ptr = self.lib.lammps_extract_fix(self.lmp, id, style, type, i, j)
            return ptr
        return None

    def extract_variable(self, name, group, type):
        if type == 0:
            self.lib.lammps_extract_variable.restype = POINTER(c_double)
            ptr = self.lib.lammps_extract_variable(self.lmp, name, group)
            result = ptr[0]
            self.lib.lammps_free(ptr)
            return result
        if type == 1:
            self.lib.lammps_extract_global.restype = POINTER(c_int)
            nlocalptr = self.lib.lammps_extract_global(self.lmp, "nlocal")
            nlocal = nlocalptr[0]
            result = (c_double * nlocal)()
            self.lib.lammps_extract_variable.restype = POINTER(c_double)
            ptr = self.lib.lammps_extract_variable(self.lmp, name, group)
            for i in range(0, nlocal): result[i] = ptr[i]
            self.lib.lammps_free(ptr)
            return result
        return None

    def get_natoms(self):
        return self.lib.lammps_get_natoms(self.lmp)

    def gather_atoms(self, name, type, count):
        natoms = self.lib.lammps_get_natoms(self.lmp)
        if type == 0:
            data = ((count * natoms) * c_int)()
            self.lib.lammps_gather_atoms(self.lmp, name, type, count, data)
        elif type == 1:
            data = ((count * natoms) * c_double)()
            self.lib.lammps_gather_atoms(self.lmp, name, type, count, data)
        else:
            return None
        return data

    def scatter_atoms(self, name, type, count, data):
        self.lib.lammps_scatter_atoms(self.lmp, name, type, count, data)
