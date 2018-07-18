// Copyright (C) 2010-2018 Dzhelil S. Rufat. All Rights Reserved.

void resample(const double* xx, int Nx,  //
              int* idx, double* yy, int Ny) {
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

void resample_s(const double* xx, int Nx,  //
                int* idx, double* ss, int Ns) {
  auto yy = ss;
  resample(xx, Nx, idx, yy, Ns);
  int i;
  for (int j = 0; j < Ns; j++) {
    i = idx[j];
    ss[j] = (yy[j] - xx[i]) / (xx[i + 1] - xx[i]);
  }
}

void resample_endpoints(const double* xx, int Nx,  //
                        int* idx, double* yy, int Ny) {
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

void resample_endpoints_s(const double* xx, int Nx,  //
                          int* idx, double* ss, int Ns) {
  auto yy = ss;
  resample_endpoints(xx, Nx, idx, yy, Ns);
  int i;
  for (int j = 0; j < Ns; j++) {
    i = idx[j];
    ss[j] = (yy[j] - xx[i]) / (xx[i + 1] - xx[i]);
  }
}

#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>

namespace py = pybind11;

using arr_d_t = py::array_t<double, py::array::c_style | py::array::forcecast>;
using arr_i_t = py::array_t<int, py::array::c_style | py::array::forcecast>;

PYBIND11_MODULE(resample, m) {
  m.def("resample", [](arr_d_t f, int N) {
    arr_i_t out(N);
    arr_d_t fout(N);
    resample(f.data(), f.shape(0),  //
             out.mutable_data(), fout.mutable_data(), N);
    return py::make_tuple(out, fout);
  });

  m.def("resample_s", [](arr_d_t f, int N) {
    arr_i_t out(N);
    arr_d_t fout(N);
    resample_s(f.data(), f.shape(0),  //
               out.mutable_data(), fout.mutable_data(), N);
    return py::make_tuple(out, fout);
  });

  m.def("resample_endpoints", [](arr_d_t f, int N) {
    arr_i_t out(N);
    arr_d_t fout(N);
    resample_endpoints(f.data(), f.shape(0),  //
                       out.mutable_data(), fout.mutable_data(), N);
    return py::make_tuple(out, fout);
  });

  m.def("resample_endpoints_s", [](arr_d_t f, int N) {
    arr_i_t out(N);
    arr_d_t fout(N);
    resample_endpoints_s(f.data(), f.shape(0),  //
                         out.mutable_data(), fout.mutable_data(), N);
    return py::make_tuple(out, fout);
  });
}
