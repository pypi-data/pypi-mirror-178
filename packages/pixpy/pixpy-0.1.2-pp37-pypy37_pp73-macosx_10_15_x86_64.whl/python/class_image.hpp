#pragma once

#include "../vec2.hpp"

#include "../gl/texture.hpp"

#include <pybind11/detail/common.h>
#include <pybind11/pybind11.h>

#include <memory>
#include <string>
#include <tuple>

namespace py = pybind11;
namespace gl = gl_wrap;

inline std::vector<gl::TexRef> split_wh(gl::TexRef img, int cols, int rows,
                                        int w, int h)
{
    if (cols < 0) { cols = static_cast<int>(img.width() / w); }
    if (rows < 0) { rows = static_cast<int>(img.height() / h); }
    return img.split(cols, rows);
}

inline std::vector<gl::TexRef> split_size(gl::TexRef img, Vec2f const& size)
{
    auto cols = img.width() / size.x;
    auto rows = img.height() / size.y;
    return img.split(static_cast<int>(cols), static_cast<int>(rows));
}

inline gl::TexRef image_from_vec2(Vec2f const& v)
{
    return {static_cast<int>(v.x), static_cast<int>(v.y)};
}

inline auto add_image_class(py::module_ const& mod)
{
    // Image
    return py::class_<gl_wrap::TexRef>(mod, "Image")
        .def(py::init<int32_t, int32_t>(), py::arg("width"), py::arg("height"))
        .def(py::init<>(&image_from_vec2), py::arg("size"))
        .def("split", &split_wh, py::arg("cols") = -1, py::arg("rows") = -1,
             py::arg("width") = 8, py::arg("height") = 8)
        .def("split", &split_size, py::arg("size"))
        .def("bind", &gl::TexRef::bind, py::arg("unit") = 0)
        .def("copy_from", &gl::TexRef::copy_from, py::arg("image"))
        .def("copy_to", &gl::TexRef::copy_to, py::arg("image"))
        .def("set_as_target", &gl::TexRef::set_target)
        .def_property_readonly(
            "pos", [](gl::TexRef const& t) { return Vec2f(t.x(), t.y()); })
        .def_property_readonly(
            "size",
            [](gl::TexRef const& t) { return Vec2f(t.width(), t.height()); })
        .def_property_readonly("width", &gl_wrap::TexRef::width)
        .def_property_readonly("height", &gl_wrap::TexRef::height);
}
