extern "C"
{
#include "glk/glk.h"
}

#include <filesystem>
namespace fs = std::filesystem;

#include "full_console.hpp"

// #include "colors.hpp"
// #include "gl/functions.hpp"
// #include "gl/program_cache.hpp"
// #include "keycodes.h"
// #include "pix.hpp"
// #include "pixel_console.hpp"
#include "system.hpp"

#include <memory>

class GlkGame
{
    std::shared_ptr<FullConsole> con;
    std::shared_ptr<Screen> screen;
    std::shared_ptr<pix::Context> context;
    std::shared_ptr<System> sys;
    bool quit = false;

public:
    explicit GlkGame(Screen::Settings const& settings) { init(settings); }

    void init(Screen::Settings const& settings)
    {
#ifdef RASPBERRY_PI
        sys = create_pi_system();
#else
        sys = create_glfw_system();
#endif
        screen = sys->init_screen(settings);
        sys->init_input();
        bool quit = false;
        context = std::make_shared<pix::Context>(settings.display_width, settings.display_height);

        auto font = std::make_shared<ConsoleFont>(FreetypeFont::unscii);
        con = std::make_shared<FullConsole>(
           std::make_shared<PixConsole>(80, 50, font), sys);

        auto [pw, ph] = con->get_pixel_size();

        auto [w, h] = screen->get_size();
        auto cw = w / 8 / 2;
        auto ch = h / 16 / 2;
        //printf("%dx%d %dx%d\n", w, h, cw, ch);
    }

    char* _linebuf = nullptr;
    int _maxlen = 0;
    bool got_line = false;

    int update(event_t* event)
    {
        sys->handle_events(
            Overload{[&](QuitEvent) { exit(0); },
                     [&](TextEvent const& te) {
                         got_line = true;
                         auto t = te.text.substr(0,te.text.length()-1);
                         strcpy(_linebuf, t.c_str());
                     },
                     [&](auto) {}});

        con->render(context.get(), {0,0}, {-1,-1});
        screen->swap();
        event->type = evtype_None;
        if (got_line) {
            // printf("%s %d\n", line->c_str(), line->length());
            event->type = evtype_LineInput;
            event->val1 = strlen(_linebuf);
            got_line = false;
            con->stop_line();
            con->write(10);
        }
        return 0;
    }

    void request_line(char* buf, int maxlen, int initlen)
    {
        _linebuf = buf;
        _maxlen = maxlen;
        con->read_line();
        //[&](auto const& s) {
        //    got_line = true;
        //    strcpy(_linebuf, utf8::utf8_encode(s).c_str());
        //});
    }

    void write(char32_t c) { con->write(c); }
    void write(std::string const& text) { con->write(text); }
};

static std::unique_ptr<GlkGame> game;

int main()
{
    Screen::Settings settings;
    settings.display_width = 1600;
    settings.display_height = 800;
    // settings.console_font = "data/Hack.ttf";
    // settings.font_size = 64;
    // settings.display_width = 2560/2;
    // settings.display_height = 1440/2;
    game = std::make_unique<GlkGame>(settings);
    glk_main();
    return 0;
}

extern "C" void glk_exit()
{
    exit(0);
}

extern "C" struct glk_stream_struct
{
    FILE* fp;
    glui32 rock;
};

extern "C" struct glk_window_struct
{
    int x;
};

extern "C" struct glk_fileref_struct
{
    fs::path name;
    glui32 rock;
    glui32 usage;
};

std::unordered_map<glui32, std::string> names = {
    {fileusage_Data, "dat"},
    {fileusage_SavedGame, "sav"},
    {fileusage_Transcript, "trans"},
    {fileusage_InputRecord, "rec"},
    //{fileusage_TypeMask, "tm"},
    //{fileusage_TextMode, "tm"},
    //{fileusage_BinaryMode, "bin"},
};

frefid_t glk_fileref_create_by_name(glui32 usage, char* name, glui32 rock)
{
    printf("Open %s\n", name);
    auto* fr = new glk_fileref_struct;
    fr->name = name;
    fr->usage = usage;
    fr->rock = rock;
    return fr;
}

frefid_t glk_fileref_create_by_prompt(glui32 usage, glui32 mode, glui32 rock)
{
    printf("Prompt\n");
    auto* fr = new glk_fileref_struct;
    fr->name = "temp";
    fr->usage = usage;
    fr->rock = rock;
    return fr;
}

void glk_fileref_destroy(frefid_t fref)
{
    delete fref;
}

winid_t glk_window_open(winid_t split, glui32 method, glui32 size,
                        glui32 wintype, glui32 rock)
{
    if (split != nullptr) { return nullptr; }
    return new glk_window_struct;
}

void glk_window_get_size(winid_t win, glui32* widthptr, glui32* heightptr)
{
    if (widthptr != nullptr) *widthptr = 80;
    if (heightptr != nullptr) *heightptr = 50;
}
void glk_window_clear(winid_t win) {}
void glk_window_move_cursor(winid_t win, glui32 xpos, glui32 ypos) {}
void glk_set_window(winid_t win) {}

strid_t glk_stream_open_file(frefid_t fileref, glui32 fmode, glui32 rock)
{
    auto* s = new glk_stream_struct;
    s->fp = fopen(fileref->name.string().c_str(), "rb");
    s->rock = rock;
    return s;
}
strid_t glk_stream_open_memory(char* buf, glui32 buflen, glui32 fmode,
                               glui32 rock)
{
    return nullptr;
}
void glk_stream_set_position(strid_t str, glsi32 pos, glui32 seekmode)
{
    static const std::unordered_map<glui32, int> modes = {
        {seekmode_Start, SEEK_SET},
        {seekmode_Current, SEEK_CUR},
        {seekmode_End, SEEK_END},
    };
    fseek(str->fp, pos, modes.at(seekmode));
}

void glk_stream_close(strid_t str, stream_result_t* result)
{
    fclose(str->fp);
    delete str;
}

void glk_put_char(unsigned char ch)
{
    game->write(ch);
}
void glk_put_char_stream(strid_t str, unsigned char ch) {}
void glk_put_string(char* s)
{
    game->write(s);
}
void glk_put_string_stream(strid_t str, char* s) {}
void glk_put_buffer(char* buf, glui32 len)
{
    game->write(std::string(buf, len));
}
void glk_put_buffer_stream(strid_t str, char* buf, glui32 len) {}
void glk_set_style(glui32 styl) {}
void glk_set_style_stream(strid_t str, glui32 styl) {}

glsi32 glk_get_char_stream(strid_t str)
{
    return fgetc(str->fp);
}
glui32 glk_get_line_stream(strid_t str, char* buf, glui32 len) {
    return 0;
}
glui32 glk_get_buffer_stream(strid_t str, char* buf, glui32 len) {
    return 0;
}
void glk_select(event_t* event)
{
    game->update(event);
}
void glk_select_poll(event_t* event)
{
    game->update(event);
}

void glk_request_timer_events(glui32 millisecs) {}

void glk_request_line_event(winid_t win, char* buf, glui32 maxlen,
                            glui32 initlen)
{
    game->request_line(buf, maxlen, initlen);
    printf("Line\n");
}
void glk_request_char_event(winid_t win)
{

    printf("Char\n");
}
void glk_request_mouse_event(winid_t win) {}

void glk_cancel_line_event(winid_t win, event_t* event) {}
void glk_cancel_char_event(winid_t win) {}
void glk_cancel_mouse_event(winid_t win) {}
