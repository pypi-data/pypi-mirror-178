#include "colors.hpp"
#include "gl/functions.hpp"
#include "gl/program_cache.hpp"
#include "image.hpp"
#include "keycodes.h"
#include "pixel_console.hpp"
#include "system.hpp"

// Helper template to join multiple lambdas into one overload set
template <typename... Ts> struct Overload : Ts... // NOLINT
{
    using Ts::operator()...;
};
template <class... Ts> Overload(Ts...) -> Overload<Ts...>;

void noise(PixConsole& con)
{
    auto [cw, ch] = con.get_size();

    for (int y = 0; y < ch; y++) {
        for (int x = 0; x < cw; x++) {
            // con.put_color(x, y, color::white, 0xff000000);
            con.put_char(x, y, rand() % 92 + '!');
        }
    }
    con.render(0, 0, 1, 1);
}

class LineEditor
{
    std::shared_ptr<PixConsole> _console;
    std::pair<int, int> pos;
public:
    explicit LineEditor(std::shared_ptr<PixConsole> const& console)
        : _console{console}
    {
        pos.first = pos.second = 5;
    }

    void put_event(KeyEvent event)
    {
        auto key = static_cast<Key>(event.key);

        if (key == Key::RIGHT) {
            pos.first++;
        }
    }

    void put_event(TextEvent const& te)
    {
        for(auto&& c : te.text) {
            _console->put_char(pos.first, pos.second, c);
            pos.first++;
        }
    }


};

int main()
{
    Settings settings;
    // settings.console_font = "data/Hack.ttf";
    // settings.font_size = 64;
    // settings.display_width = 2560/2;
    // settings.display_height = 1440/2;
#ifdef RASPBERRY_PI
    auto sys = create_pi_system();
#else
    auto sys = create_sdl_system();
#endif
    auto screen = sys->init_screen(settings);
    bool quit = false;

    auto [w, h] = screen->get_size();
    gl_wrap::setViewport({w, h});

    glEnable(GL_BLEND);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    glBindFramebuffer(GL_FRAMEBUFFER, 0);

    auto cw = w / 8;
    auto ch = h / 16;
    auto con = std::make_shared<PixConsole>(
        cw, ch, settings.console_font.string(), settings.font_size);

    // con->set_tile_size(30, 31);

    auto [w2, h2] = con->get_size();
    printf("%d %d console\n", w2, h2);

    pix::set_transform();
    auto image = pix::load_png("data/enemy.png");

    auto tex = std::make_shared<gl_wrap::Texture>(
        image.width, image.height, image.ptr, GL_RGBA, image.format);
    gl_wrap::TexRef texr{tex};
    auto htex = con->get_texture_for_char('A');
    pix::set_transform();
    glBlendFunc(GL_ONE, GL_ZERO);
    // glDisable(GL_BLEND);
    // htex.copy_from(texr);
    // glEnable(GL_BLEND);
    glBindFramebuffer(GL_FRAMEBUFFER, 0);
    gl_wrap::setViewport({w, h});
    //    htex.set_target();
    //    gl_wrap::ProgramCache::get_instance().textured.use();
    //    htex.bind();
    //    htex.yflip();
    //    glBlendFunc(GL_ONE, GL_ZERO);
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
    // con->set_tile_image('H', gl_wrap::TexRef{tex});
    // con->set_tile_image('e', gl_wrap::TexRef{tex});

    con->text(1, 1, "POO");
    con->text(2, 2, "Allo");
    con->text(5, 5, "COWABUNGA!");
    int y = 0;
    int x = 0;
    LineEditor editor(con);
    while (!quit) {

        // clang-format off
        sys->handle_events(Overload{
            [&](QuitEvent) { quit = true; },
            [&](TextEvent const& te) { editor.put_event(te); },
            [&](KeyEvent const& k) {
                editor.put_event(k);
                switch(static_cast<Key>(k.key)) {
                case Key::UP: y--; break;
                case Key::DOWN: y++; break;
                case Key::LEFT: x--; break;
                case Key::RIGHT: x++; break;
                default: break;
                }

            },
            [&](auto) {}
        });
        // clang-format on

        // con->put_char(x, y, 'x');
        // con->put_color(x, y, color::grey, color::orange);
        //noise(*con);
        con->render(0,0,1,1);

        pix::set_transform();
        pix::set_colors(0xffffffff, 0x80808080);
        htex.bind();
        auto& program = gl_wrap::ProgramCache::get_instance().textured;
        program.use();
        // pix::draw_quad_impl(10, 10, 1000, 1000);
        // w = 1280;
        // h = 720;
        pix::draw_quad_uvs(10, 10, 30, 31, texr.uvs);
        pix::draw_quad_uvs(w - 40, 10, 30, 31, texr.uvs);
        pix::draw_quad_uvs(w - 40, h - 40, 30, 31, texr.uvs);
        pix::draw_quad_uvs(10, h - 40, 30, 31, texr.uvs);

        // pix::draw_quad_filled(200,200,100,100);
        screen->swap();
    }

    return 0;
}
