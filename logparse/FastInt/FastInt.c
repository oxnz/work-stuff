/*
 * Filename:	fast_int.c
 *
 * Author:		Oxnz
 * Email:		yunxinyi@gmail.com
 * Created:		2015-12-23 19:57:31 CST
 * Last-update:	2015-12-23 19:57:31 CST
 * Description: anchor
 *
 * Version:		0.0.1
 * Revision:	[NONE]
 * Revision history:	[NONE]
 * Date Author Remarks:	[NONE]
 *
 * License:
 * Copyright (c) 2015 Oxnz
 *
 * Distributed under terms of the [LICENSE] license.
 * [license]
 *
 */

#include <Python.h>

static PyObject *FastIntError;

/* convert string to integer */
static PyObject*
atoi_(PyObject *self, PyObject *args) {
	const char *s;
	int i;

	if (!PyArg_ParseTuple(args, "s", &s))
		return NULL;
	i = atoi(s);
	return Py_BuildValue("i", i);
}

static PyObject*
toInt(PyObject *self, PyObject *args) {
	const char *s;
	int i = 0;

	if (!PyArg_ParseTuple(args, "s", &s))
		return 0;
	while (*s) {
		i = i * 10 + *s - '0';
		++s;
	}
	return Py_BuildValue("i", i);
}

static PyObject*
toLong(PyObject *self, PyObject *args) {
	const char *s;
	long l = 0;

	if (!PyArg_ParseTuple(args, "s", &s))
		return 0;
	l = strtol(s, 0, 10);
	return Py_BuildValue("l", l);
}

static PyObject*
add(PyObject *self, PyObject *args) {
	const char *s;
	int iv, i = 0;

	if (!PyArg_ParseTuple(args, "is", &iv, &s))
		return 0;
	while (*s) {
		i = i * 10 + *s - '0';
		++s;
	}
	return Py_BuildValue("i", i + iv);
}

static PyObject*
addArray(PyObject *self, PyObject *args) {
	const char *s;
	int iv, i = 0;
	if (!PyArg_ParseTuple(args, "Os", &iv, &s))
		return 0;
	while (*s) {
		i = i * 10 + *s - '0';
		++s;
	}
	return Py_BuildValue("i", i + iv);
}

static PyMethodDef FastIntMethods[] =
{
	{"atoi", atoi_, METH_VARARGS, "string to int"},
	{"toInt", toInt, METH_VARARGS, "string to int"},
	{"toLong", toLong, METH_VARARGS, "string to long"},
	{"add", add, METH_VARARGS, "add(i, s) { return i + atoi(s); }"},
	{NULL, NULL, 0, NULL} /* sentinel */
};

PyMODINIT_FUNC
initFastInt(void)
{
	PyObject *m = Py_InitModule("FastInt", FastIntMethods);
	if (m == 0)
		return;
	FastIntError = PyErr_NewException("FastInt.error", NULL, NULL);
	Py_INCREF(FastIntError);
	PyModule_AddObject(m, "error", FastIntError);
}
