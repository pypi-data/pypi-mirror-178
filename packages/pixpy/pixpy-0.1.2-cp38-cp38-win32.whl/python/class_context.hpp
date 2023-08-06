#pragma once

#include "../colors.hpp"
#include "../gl/texture.hpp"
#include "../machine.hpp"
#include "../vec2.hpp"
#include "full_console.hpp"

#include <optional>
#include <pybind11/detail/common.h>
#include <pybind11/pybind11.h>

#include <string>
#include <tuple>

namespace py = pybind11;
namespace gl = gl_wrap;

inline std::shared_ptr<pix::Context> make_context(Vec2f size)
{
    if (size.x == 0 && size.y == 0) {
        size = Vec2f{Machine::get_instance().screen->get_size()};
    }
    return std::make_shared<pix::Context>(size.x, size.y);
}

inline pix::Context* context_from(gl::TexRef& tr)
{
    if (tr.data != nullptr) {
        return static_cast<pix::Context*>(tr.data.get());
    }

    auto* context = new pix::Context(
        {static_cast<float>(tr.x()), static_cast<float>(tr.y())},
        {static_cast<float>(tr.tex->width), static_cast<float>(tr.tex->height)},
        tr.get_target());
    tr.data = std::shared_ptr<void>(static_cast<void*>(context), [](void* ptr) {
        delete static_cast<pix::Context*>(ptr);
    });
    return context;
}

inline pix::Context* context_from(Screen& screen)
{
    return Machine::get_instance().context.get();
}

inline pix::Context* context_from(pix::Context& context)
{
    return &context;
}

template <typename T, typename... O>
inline void add_draw_functions(pybind11::class_<T, O...>& cls)
{
    // clang-format off
    cls.def("circle", [](T& thiz, Vec2f const& center, float r) {
      context_from(thiz)->circle(center, r);
    }, py::arg("center"), py::arg("radius"));

    cls.def("filled_circle", [](T& thiz, Vec2f const& center, float r) {
      context_from(thiz)->filled_circle(center, r);
    }, py::arg("center"), py::arg("radius"));

    cls.def("line", [](T& thiz, Vec2f const& from, Vec2f const& to) {
      context_from(thiz)->line(from.x, from.y, to.x, to.y);
    }, py::arg("start"), py::arg("end"));

    cls.def("line", [](T& thiz, Vec2f const& to) {
      context_from(thiz)->line(to.x, to.y);
    }, py::arg("end"));

    cls.def("plot", [](T& thiz, Vec2f const& to, uint32_t color) {
      context_from(thiz)->plot(to, gl_wrap::Color(color));
    }, py::arg("center"), py::arg("color"));

    cls.def("rect", [](T& thiz, Vec2f const& xy, Vec2f const& size) {
      context_from(thiz)->rect(xy.x, xy.y, size.x, size.y);
    }, py::arg("top_left"), py::arg("size"));

    cls.def("filled_rect", [](T& thiz, Vec2f const& xy, Vec2f const& size) {
      context_from(thiz)->filled_rect(xy.x, xy.y, size.x, size.y);
    }, py::arg("top_left"), py::arg("size"));

    cls.def("draw", [](T& thiz, gl_wrap::TexRef const& tr,
                       std::optional<Vec2f> xy, std::optional<Vec2f> center,
                       Vec2f size, float rot) {
            pix::Context* ctx = context_from(thiz);
            if (center) {
                ctx->draw(tr, *center, size, rot);
            } else if (xy) {
               ctx->blit(tr, *xy, size); 
            } else {
               ctx->blit(tr, {0,0}, size); 
            }
            }, py::arg("image"), py::arg("top_left") = std::nullopt,
            py::arg("center") = std::nullopt,
            py::arg("size") = Vec2f{-1, -1}, py::arg("rot") = 0);
    cls.def("draw", [](T& thiz, FullConsole& con,
                       Vec2f const& xy, Vec2f const& size) {
                con.render(context_from(thiz), xy, size);
            }, py::arg("drawable"), py::arg("top_left") = Vec2f{0, 0},
            py::arg("size") = Vec2f{-1, -1});
    cls.def("blit", [](T& thiz, gl_wrap::TexRef const& tr,
                       Vec2f const& xy, Vec2f const& size) {
              context_from(thiz)->blit(tr, xy, size);
            }, py::arg("image"), py::arg("top_left") = Vec2f{0, 0},
            py::arg("size") = Vec2f{-1, -1});
    cls.def( "clear", [](T& thiz, uint32_t color) {
      context_from(thiz)->clear(color);
    }, py::arg("color") = color::black);
    cls.def_property("draw_color", [](T& thiz) {
      return context_from(thiz)->fg;
    }, [](T& thiz, uint32_t color) {
      context_from(thiz)->set_color(color);
    });
    cls.def_property("line_width", [](T& thiz) {
      return context_from(thiz)->line_width;
    }, [](T& thiz, float lw) {
      context_from(thiz)->line_width = lw;
    });
    cls.def_property_readonly(
        "context", [](T& tr) { return context_from(tr); });
    // clang-format on
}
inline auto add_context_class(py::module_ const& mod)
{
    return py::class_<pix::Context, std::shared_ptr<pix::Context>>(mod,
                                                                   "Context")
        .def(py::init<>(&make_context), py::arg("size") = Vec2f{0, 0});
}
