#pragma once

#include "../console_font.hpp"
#include "../machine.hpp"
#include "../vec2.hpp"

#include <pybind11/detail/common.h>
#include <pybind11/pybind11.h>

#include <filesystem>
#include <memory>
#include <string>
#include <tuple>

namespace py = pybind11;
using namespace pybind11::literals;
namespace fs = std::filesystem;

inline std::shared_ptr<ConsoleFont> make_tileset(std::string const& font_file,
                                                 int size)
{
    return std::make_shared<ConsoleFont>(font_file, size);
}

inline std::shared_ptr<ConsoleFont> make_tileset2(Vec2f size)
{
    return std::make_shared<ConsoleFont>(std::pair{size.x, size.y});
}
inline void add_tileset_class(py::module_ const& mod)
{
    // Console
    py::class_<ConsoleFont, std::shared_ptr<ConsoleFont>>(mod, "TileSet")
        .def(py::init<>(&make_tileset), "font_file"_a, "size"_a)
        .def(py::init<>(&make_tileset2), "tile_size"_a)
        .def("get_image_for", &ConsoleFont::get_texture_for_char, "");
}
