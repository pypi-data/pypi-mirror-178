#pragma once

#include "../vec2.hpp"

#include <pybind11/detail/common.h>
#include <pybind11/pybind11.h>

#include <tuple>

namespace py = pybind11;

static inline Vec2f vec2_one{1, 1};
static inline Vec2f vec2_zero{0, 0};

template <typename T>
inline auto add_vec2_class(py::module_& mod, std::string const& name)
{
    using Vec = Vec2<T>;
    auto rc =
        py::class_<Vec>(mod, name.c_str())
            .def(py::init<T, T>(), py::arg("x") = 0, py::arg("y") = 0)
            .def(py::init<std::pair<T, T>>())
            .def("__len__", &Vec::len)
            .def_static("from_angle", &Vec::from_angle, "From angle")
            .def("clamp", &Vec::clamp, py::arg("low"), py::arg("high"))
            .def("clip", &Vec::clip, py::arg("low"), py::arg("high"))
            .def("mag", &Vec::mag, "Get magnitude (length) of vector")
            .def("mag2", &Vec::mag2, "Get the squared magnitude")
            .def("norm", &Vec::norm)
            .def("angle", &Vec::angle)
            .def("sign", &Vec::sign)
            .def("cossin", &Vec::cossin)
            .def_readonly_static("ONE", &vec2_one)
            .def_readonly_static("ZERO", &vec2_zero)
            .def_readonly("x", &Vec::x)
            .def_readonly("y", &Vec::y)
            .def("__eq__", [](const Vec& a, Vec const& b) { return a == b; })
            .def("__ne__", [](const Vec& a, Vec const& b) { return a != b; })
            .def("__getitem__",
                 [](Vec const& v, size_t i) {
                     if (i > 1) { throw pybind11::index_error(); }
                     return v[i];
                 })
            .def(
                "__iter__",
                [](Vec const& v) { return py::make_iterator(&v.x, &v.y + 1); },
                py::keep_alive<0, 1>())
            .def("__repr__", &Vec::repr)
            .def("__truediv__", &Vec::div)
            .def("__truediv__", &Vec::divs)
            .def("__floordiv__", &Vec::fdiv)
            .def("__floordiv__", &Vec::fdivs)
            .def("__mul__", &Vec::mul)
            .def("__mul__", &Vec::muls)
            .def("__add__", &Vec::add)
            .def("__add__", &Vec::adds)
            .def("__sub__", &Vec::sub)
            .def("__sub__", &Vec::subs);

    pybind11::implicitly_convertible<std::tuple<int, int>, Vec2f>();
    pybind11::implicitly_convertible<std::tuple<double, double>, Vec2f>();
    pybind11::implicitly_convertible<std::tuple<double, int>, Vec2f>();
    pybind11::implicitly_convertible<std::tuple<int, double>, Vec2f>();

    return rc;
}

