// convert between python and C file handle
%typemap(in) FILE * {
  if (PyFile_Check($input)) /* check for undef */
        $1 = PyFile_AsFile($input);
  else  $1 = NULL;
}

%typemap(typecheck) FILE * {
  if (PyFile_Check($input)) /* check for undef */
    $1 = PyFile_AsFile($input) ? 1 : 0;
}

%typemap(out) float [ANY] {
  int i;
  $result = PyList_New($1_dim0);
  for (i = 0; i < $1_dim0; i++) {
    PyObject *o = PyFloat_FromDouble((double) $1[i]);
    PyList_SetItem($result,i,o);
  }
}

%typemap(out) int [ANY] {
  int i;
  $result = PyList_New($1_dim0);
  for (i = 0; i < $1_dim0; i++) {
    PyObject *o = PyLong_FromLong((long) $1[i]);
    PyList_SetItem($result,i,o);
  }
}

// This tells SWIG to treat char ** as a special case
%typemap(in) char ** {
  /* Check if is a list */
  if (PyList_Check($input)) {
    int size = PyList_Size($input);
    int i = 0;
    $1 = (char **) malloc((size+1)*sizeof(char *));
    for (i = 0; i < size; i++) {
      PyObject *o = PyList_GetItem($input,i);
      if (PyString_Check(o))
        $1[i] = PyString_AsString(PyList_GetItem($input,i));
      else {
        PyErr_SetString(PyExc_TypeError,"list must contain strings");
        free($1);
        return NULL;
      }
    }
    $1[i] = 0;
  } else {
    PyErr_SetString(PyExc_TypeError,"not a list");
    return NULL;
  }
}

// This tells SWIG to treat char *[], const char **, and const char *[] the same as char **
%apply char ** { char *[], const char **, const char *[] };

%typemap(in) PyObject *PyFunc {
  if (!PyCallable_Check($input)) {
      PyErr_SetString(PyExc_TypeError, "Need a callable object!");
      return NULL;
  }
  $1 = $input;
}

%typemap(in) PyObject *PyFuncOrNone {
  if($input != Py_None){
    if (!PyCallable_Check($input)) {
        PyErr_SetString(PyExc_TypeError, "Need a callable object!");
        return NULL;
    }
  }
  $1 = $input;
}

%typemap(in) PyObject *data {
  $1 = $input;
}
