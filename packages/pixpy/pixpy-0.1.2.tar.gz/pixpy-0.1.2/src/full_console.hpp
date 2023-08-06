#pragma once

#include "colors.hpp"
#include "context.hpp"
#include "keycodes.h"
#include "pixel_console.hpp"
#include "system.hpp"

class FullConsole
{
    uint32_t fg = color::light_green;
    uint32_t bg = color::black;

    int cols{};
    int rows{};

    Vec2i cursor{0, 0};

    std::shared_ptr<PixConsole> console;
    std::shared_ptr<System> system;

    Vec2i edit_start{0, 0};
    int xpos = 0;
    std::u32string line;
    bool reading_line = false;
    void refresh();
    int listener = -1;

    System::Propagate put_event(KeyEvent const& event);
    System::Propagate put_event(TextEvent const& te);


public:
    FullConsole(std::shared_ptr<PixConsole> const& con,
                std::shared_ptr<System> const& sys);

    ~FullConsole();

    Vec2i get_cursor() const { return cursor; }
    void set_cursor(int x, int y) { cursor = {x,y}; }
    void set_cursor(Vec2i xy) { cursor = xy; }


    gl_wrap::TexRef get_font_texture();

    Vec2i get_pixel_size() const;

    std::vector<uint32_t> get_tiles() { return console->get_tiles(); }
    void set_tiles(std::vector<uint32_t> const& data)
    {
        console->set_tiles(data);
    }

    void read_line();

    void stop_line()
    {
        cursor_on = false;
        reading_line = false;
    }

    void set_line(std::string const& text);

    Vec2f get_size() const { return Vec2i{console->get_size()}; }
    Vec2f get_tile_size() const { return Vec2i{console->get_char_size()}; }

    void put(int x, int y, char32_t c) { console->put(x, y, fg, bg, c); }
    void text(int x, int y, std::string const& txt)
    {
        console->text(x, y, txt, fg, bg);
    }

    char32_t get(int x, int y) const { return console->get_char(x, y); }

    void write(char32_t ch);

    void write(std::string const& text);

    void set_color(uint32_t fg_, uint32_t bg_);

    void clear()
    {
        console->fill(fg, bg);
    }

    gl_wrap::TexRef get_texture_for_char(char32_t c)
    {
        return console->get_texture_for_char(c);
    }

    void render(pix::Context* context, Vec2f xy, Vec2f sz);

    bool cursor_on = false;
};
