#pragma once

#include "class_context.hpp"

#include "../full_console.hpp"
#include "../machine.hpp"
#include "../vec2.hpp"

#include <pybind11/detail/common.h>
#include <pybind11/pybind11.h>

#include <filesystem>
#include <memory>
#include <string>
#include <tuple>

namespace py = pybind11;
namespace fs = std::filesystem;

inline std::shared_ptr<FullConsole> make_console(int32_t cols, int32_t rows,
                                                 std::string const& font_file,
                                                 Vec2f const& tile_size,
                                                 int font_size)
{
    fs::path p{font_file};

    auto ts = std::pair<int, int>{tile_size.x, tile_size.y};
    auto font = font_file.empty()
                    ? std::make_shared<ConsoleFont>(FreetypeFont::unscii, ts)
                    : std::make_shared<ConsoleFont>(p.string(), font_size, ts);

    auto con = std::make_shared<PixConsole>(cols, rows, font);
    auto fcon = std::make_shared<FullConsole>(con, Machine::get_instance().sys);

    return fcon;
}

inline void add_console_class(py::module_ const& mod)
{
    // Console
    py::class_<FullConsole, std::shared_ptr<FullConsole>>(mod, "Console")
        .def(py::init<>(&make_console), py::arg("cols") = 80,
             py::arg("rows") = 50, py::arg("font_file") = "",
             py::arg("tile_size") = Vec2f{0, 0}, py::arg("font_size") = 16)
        .def("render", &FullConsole::render, py::arg("context"),
             py::arg("pos") = Vec2f(0, 0), py::arg("size") = Vec2f(-1, -1),
             "Render the console to the display")
        .def(
            "put",
            [](std::shared_ptr<FullConsole> const& thiz, float x, float y,
               uint32_t c) { thiz->put(x, y, c); },
            "Put char at position")
        .def(
            "put",
            [](std::shared_ptr<FullConsole> const& thiz, float x, float y,
               std::string const& t) { thiz->text(x, y, t); },
            "Put char at position")
        .def(
            "put",
            [](std::shared_ptr<FullConsole> const& thiz, Vec2f pos,
               std::string const& t) { thiz->text(pos.x, pos.y, t); },
            "Put char at position")
        .def("get", &FullConsole::get, "Get char at position")
        .def(
            "get",
            [](FullConsole const& con, Vec2f const& pos) {
                return con.get(pos.x, pos.y);
            },
            "Get char at position")
        .def_readwrite("cursor_on", &FullConsole::cursor_on)
        .def_property("cursor_pos", [](FullConsole& thiz) {
            return Vec2f(thiz.get_cursor());
            }, [](FullConsole& thiz, Vec2f const& v) {
                thiz.set_cursor(v.x, v.y);
            })
        .def("get_tiles", &FullConsole::get_tiles)
        .def("set_tiles", &FullConsole::set_tiles)
        .def("clear", &FullConsole::clear)
        .def("set_color", &FullConsole::set_color)
        .def_property_readonly("grid_size", &FullConsole::get_size,
                               "Get number cols and rows")
        .def_property_readonly("tile_size", &FullConsole::get_tile_size,
                               "Get size of a single tile")
        .def("get_line", &FullConsole::read_line, "Enter line edit mode")
        .def("read_line", &FullConsole::read_line, "Enter line edit mode")
        .def("cancel_line", &FullConsole::stop_line, "Stop line edit mode")
        .def("set_line", &FullConsole::set_line, "Change the edited line")
        .def("get_font_image", &FullConsole::get_font_texture)
        .def("get_image_for", &FullConsole::get_texture_for_char, "")
        .def("write", [](FullConsole& con, std::vector<char32_t> const& data) {
            con.write(utf8::utf8_encode(data));
            })
        .def("write", static_cast<void (FullConsole::*)(std::string const&)>(
                          &FullConsole::write))
        .def("write",
             static_cast<void (FullConsole::*)(char32_t)>(&FullConsole::write));
}
