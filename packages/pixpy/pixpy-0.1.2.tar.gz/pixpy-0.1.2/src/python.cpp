#include "python/class_console.hpp"
#include "python/class_context.hpp"
#include "python/class_font.hpp"
#include "python/class_image.hpp"
#include "python/class_screen.hpp"
#include "python/class_vec2.hpp"
#include "python/mod_color.hpp"
#include "python/mod_event.hpp"
#include "python/mod_key.hpp"

#include "gl/texture.hpp"

#include "context.hpp"
#include "font.hpp"
#include "image.hpp"
#include "machine.hpp"
#include "settings.hpp"
#include "system.hpp"
#include "vec2.hpp"

#include <pybind11/detail/common.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/stl/filesystem.h>

#include <cctype>
#include <chrono>
#include <filesystem>
#include <thread>

namespace fs = std::filesystem;
namespace gl = gl_wrap;
namespace py = pybind11;

static Machine m;

Machine& Machine::get_instance()
{
    return m;
}

void init()
{
    if (m.sys == nullptr) {
#ifdef RASPBERRY_PI
        m.sys = create_pi_system();
#else
        m.sys = create_glfw_system();
#endif
    }
    auto atexit = py::module_::import("atexit");
    atexit.attr("register")(py::cpp_function([] {
        if (m.frame_counter == 0 && m.screen != nullptr) {
            log("Running at exit\n");
            m.screen->swap();
            while (m.sys->run_loop()) {
                std::this_thread::sleep_for(std::chrono::milliseconds(10));
            }
        }
        log("Done");
    }));
}

std::shared_ptr<Screen> open_display(int width, int height, bool full_screen)
{
    init();
    Screen::Settings settings{.screen = full_screen ? ScreenType::Full
                                                    : ScreenType::Window,
                              .display_width = width,
                              .display_height = height};

    m.screen = m.sys->init_screen(settings);

    auto [realw, realh] = m.screen->get_size();

    m.context = std::make_shared<pix::Context>(realw, realh, 0);
    m.context->vpscale = m.screen->get_scale();

    m.sys->init_input();
    return m.screen;
}

std::shared_ptr<Screen> open_display2(Vec2f const& size, bool full_screen)
{
    return open_display(static_cast<int>(size.x), static_cast<int>(size.y),
                        full_screen);
}

void save_png(gl::TexRef const& tex, fs::path const& file_name)
{
    auto pixels = tex.read_pixels();
    pix::Image img{static_cast<int>(tex.width()),
                   static_cast<int>(tex.height()), pixels.data()};
    img.flip();
    pix::save_png(img, file_name.string());
}

// gl_wrap::TexRef load_png(fs::path const& file_name)
//{
//     auto image = pix::load_png(file_name);
//     image.flip();
//
//     auto tex = std::make_shared<gl_wrap::Texture>(
//         image.width, image.height, image.ptr, GL_RGBA, image.format);
//     return gl_wrap::TexRef{tex};
// }

std::shared_ptr<FreetypeFont> load_font(fs::path const& name, int size)
{
    return std::make_shared<FreetypeFont>(name.string().c_str(), size);
}

void demo(int dw, int dh, bool fs)
{
    if (dw < 0) dw = 1280;
    if (dh < 0) dh = 720;
    open_display(dw, dh, fs);
    auto [w, h] = m.screen->get_size();

    int n = 200;
    float r = 2.0 * M_PI / 235;
    float x = 0;
    float y = 0;
    float t = 0;
    float u = 0;
    float v = 0;

    auto center = Vec2f{(double)w, (double)h} / 2;

    while (m.sys->run_loop()) {
        m.context->clear(color::black);
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                u = sinf(i + v) + sinf(r * i + x);
                v = cosf(i + v) + cosf(r * i + x);
                x = u + t;
                auto col =
                    color::rgba((float)i / n, (float)j / n, 99.0 / 200.0, 1.0);
                m.context->plot(Vec2f(u, v) * 250 + center, col);
            }
        }
        t += 0.0025;
        m.sys->handle_events(Overload{[&](QuitEvent) {},
                                      [&](KeyEvent const& k) {}, //
                                      [&](auto) {}});
        m.context->flush();
        m.screen->swap();
    }
    exit(0);
}

PYBIND11_MODULE(pixpy, mod)
{
    mod.doc() = "pixpy";

    add_key_module(mod.def_submodule("key"));
    add_color_module(mod.def_submodule("color"));
    add_vec2_class<double>(mod, "Vec2");
    add_event_mod(mod.def_submodule("event"));
    add_font_class(mod);
    add_console_class(mod);

    auto screen = add_screen_class(mod);
    add_draw_functions(screen);

    // MODULE
    mod.def("demo", &demo, py::arg("width") = -1,
            py::arg("height") = -1, py::arg("full_screen") = false);
    mod.def("open_display", &open_display, py::arg("width") = -1,
            py::arg("height") = -1, py::arg("full_screen") = false);
    mod.def("open_display", &open_display2, py::arg("size"),
            py::arg("full_screen") = false);
    mod.def("get_display", [] { return m.screen; });
    mod.def("poll_events", [] { m.sys->run_loop(); });
    mod.def("get_event", [] { return m.sys->next_event(); });
    mod.def("all_events", [] { return m.sys->all_events(); });
    mod.def("is_pressed", [](int key) { return m.sys->is_pressed(key); });
    mod.def("is_pressed", [](char32_t key) { return m.sys->is_pressed(key); });
    mod.def("was_pressed", [](int key) { return m.sys->was_pressed(key); });
    mod.def("was_pressed",
            [](char32_t key) { return m.sys->was_pressed(key); });
    mod.def("get_pointer", [] { return Vec2f{m.sys->get_pointer()}; });
    mod.def("run_loop", [] { return m.sys->run_loop(); });
    mod.def("load_png", &pix::load_png);
    mod.def("save_png", &save_png);
    mod.def("rgba", &color::rgba);
    mod.def("load_font", &load_font, py::arg("name"), py::arg("size") = 0);

    auto ctx = add_context_class(mod);
    add_draw_functions(ctx);

    auto tc = add_image_class(mod);
    add_draw_functions(tc);
}
