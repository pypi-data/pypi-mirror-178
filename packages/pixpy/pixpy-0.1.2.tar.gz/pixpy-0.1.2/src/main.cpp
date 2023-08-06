#include "colors.hpp"
#include "image.hpp"
#include "keycodes.h"
#include "pixel_console.hpp"
#include "system.hpp"
#include "utils.h"

#include "full_console.hpp"

void noise(PixConsole& con)
{
    auto [cw, ch] = con.get_size();

    for (int y = 0; y < ch; y++) {
        for (int x = 0; x < cw; x++) {
            con.put_char(x, y, rand() % 92 + '!');
        }
    }
}

int main()
{
#ifdef RASPBERRY_PI
    auto sys = create_pi_system();
#else
    auto sys = create_glfw_system();
#endif
    auto screen = sys->init_screen({
        .display_width = 1280,
        .display_height = 920,
    });
    sys->init_input();
    auto s = screen->get_size();
    auto context = std::make_shared<pix::Context>(s.first, s.second, 0);
    context->vpscale = screen->get_scale();

    auto [w, h] = screen->get_size();

    int n = 200;
    float r = 2.0 * M_PI / 235;
    float x = 0;
    float y = 0;
    float t = 0;
    float u = 0;
    float v = 0;

    auto center = Vec2f{s} / 2;

    while (sys->run_loop()) {
        context->clear(color::black);
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                u = sinf(i + v) + sinf(r * i + x);
                v = cosf(i + v) + cosf(r * i + x);
                x = u + t;
                auto col = color::rgba((float)i / n, (float)j / n, 99.0 / 200.0, 1.0);
                context->plot(Vec2f(u, v) * 250 + center, col);
            }
        }
        t += 0.0025;
        sys->handle_events(Overload{[&](QuitEvent) {},
                                    [&](KeyEvent const& k) {}, //
                                    [&](auto) {}});
        context->flush();
        screen->swap();
    }

    return 0;
}
