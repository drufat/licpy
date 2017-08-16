// Copyright (C) 2010-2016 Dzhelil S. Rufat. All Rights Reserved.
#include <pybindcpp/module.h>
#include <pybindcpp/numpy.h>

using namespace pybindcpp;

void resample(                   //
    const double *xx, int Nx,    //
    int *idx, double *yy, int Ny //
    ) {

  auto dy = (xx[Nx - 1] - xx[0]) / Ny;
  auto y = xx[0] + 0.5 * dy;

  int i = 0;
  for (int j = 0; j < Ny; j++) {
    while (xx[i + 1] < y) {
      i++;
    }
    idx[j] = i;
    yy[j] = y;
    y += dy;
  }
}

void resample_s(                 //
    const double *xx, int Nx,    //
    int *idx, double *ss, int Ns //
    ) {
  auto yy = ss;
  resample(xx, Nx, idx, yy, Ns);
  int i;
  for (int j = 0; j < Ns; j++) {
    i = idx[j];
    ss[j] = (yy[j] - xx[i]) / (xx[i + 1] - xx[i]);
  }
}

void resample_endpoints(         //
    const double *xx, int Nx,    //
    int *idx, double *yy, int Ny //
    ) {

  auto dy = (xx[Nx - 1] - xx[0]) / (Ny - 1);
  auto y = xx[0];

  int i = 0;
  for (int j = 0; j < Ny - 1; j++) {
    while (xx[i + 1] < y) {
      i++;
    }
    idx[j] = i;
    yy[j] = y;
    y += dy;
  }
  idx[Ny - 1] = Nx - 2;
  yy[Ny - 1] = xx[Nx - 1];
}

void resample_endpoints_s(       //
    const double *xx, int Nx,    //
    int *idx, double *ss, int Ns //
    ) {
  auto yy = ss;
  resample_endpoints(xx, Nx, idx, yy, Ns);
  int i;
  for (int j = 0; j < Ns; j++) {
    i = idx[j];
    ss[j] = (yy[j] - xx[i]) / (xx[i + 1] - xx[i]);
  }
}

void init(pybindcpp::ExtModule &m) {
  using py_t = py_function<PyObject *(PyObject *)>;
  py_t py("licpy.resample_wrap", "resample_wrap");

  m.add("resample", py(fun2obj(resample)));
  m.add("resample_s", py(fun2obj(resample_s)));

  m.add("resample_endpoints", py(fun2obj(resample_endpoints)));
  m.add("resample_endpoints_s", py(fun2obj(resample_endpoints_s)));
}

PyMODINIT_FUNC PyInit_resample(void) {
  import_array();
  return module_init("resample", init);
}
