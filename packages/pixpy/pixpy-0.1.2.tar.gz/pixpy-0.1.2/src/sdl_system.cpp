#include "gl/gl.hpp"
#ifdef USE_ASOUND
#    include "player_linux.h"
#endif
#include "system.hpp"
#include "utf8.h"
#include <SDL2/SDL.h>
#include <SDL2/SDL_audio.h>
#include <SDL2/SDL_joystick.h>
#include <SDL2/SDL_video.h>

#include <array>
#include <memory>
#include <unordered_map>
#include <vector>

class SDLWindow : public Screen
{
    SDL_Window* window = nullptr;

public:
    explicit SDLWindow(SDL_Window* win) : window(win) {}
    void swap() override { SDL_GL_SwapWindow(window); }
    std::pair<int, int> get_size() override
    {
        int w = -1;
        int h = -1;
        SDL_GL_GetDrawableSize(window, &w, &h);
        printf("%d %d\n", w, h);
        return {w, h};
    }
};

class SDLSystem : public System
{
    uint32_t audio_device = 0;
    std::unordered_map<uint32_t, uint32_t> pressed;

    std::vector<SDL_Joystick*> joysticks;
    std::array<uint32_t, 16> lastAxis{};

#ifdef USE_ASOUND
    std::unique_ptr<LinuxPlayer> player;
#endif

    static inline std::unordered_map<uint32_t, Key> sdl_map = {
        {SDLK_LEFT, Key::LEFT},     {SDLK_RIGHT, Key::RIGHT},
        {SDLK_PAGEUP, Key::PAGEUP}, {SDLK_PAGEDOWN, Key::PAGEDOWN},
        {SDLK_UP, Key::UP},         {SDLK_DOWN, Key::DOWN},
        {SDLK_END, Key::END},       {SDLK_HOME, Key::HOME},
        {SDLK_ESCAPE, Key::ESCAPE}, {SDLK_RETURN, Key::ENTER},
        {SDLK_INSERT, Key::INSERT}, {SDLK_DELETE, Key::DELETE},
        {SDLK_F1, Key::F1},         {SDLK_F2, Key::F2},
        {SDLK_F3, Key::F3},         {SDLK_F4, Key::F4},
        {SDLK_F5, Key::F5},         {SDLK_F6, Key::F6},
        {SDLK_F7, Key::F7},         {SDLK_F8, Key::F8},
        {SDLK_F9, Key::F9},         {SDLK_F10, Key::F10},
        {SDLK_F11, Key::F11},       {SDLK_F12, Key::F12},
    };

    static constexpr bool in_unicode_range(uint32_t c)
    {
        return c >= 0x20 && c <= 0x0f'ffff;
    }

    static uint32_t sdl2key(uint32_t code)
    {
        auto it = sdl_map.find(code);
        if (it != sdl_map.end()) { return static_cast<int>(it->second); }
        return code;
    }

public:
    SDLSystem()
    {
        SDL_Init(SDL_INIT_VIDEO | SDL_INIT_AUDIO | SDL_INIT_JOYSTICK |
                 SDL_INIT_EVENTS);
    };

    std::shared_ptr<Screen> init_screen(Settings const& settings) override
    {

        SDL_JoystickEventState(SDL_ENABLE);
        for (int i = 0; i < SDL_NumJoysticks(); i++) {
            joysticks.push_back(SDL_JoystickOpen(i));
        }

        auto* window = SDL_CreateWindow(
            settings.title.c_str(), SDL_WINDOWPOS_UNDEFINED,
            SDL_WINDOWPOS_UNDEFINED, settings.display_width,
            settings.display_height,
            (settings.screen == ScreenType::None ? SDL_WINDOW_HIDDEN : 0) |
                SDL_WINDOW_OPENGL | SDL_WINDOW_ALLOW_HIGHDPI |
                (settings.screen == ScreenType::Full
                     ? SDL_WINDOW_FULLSCREEN_DESKTOP
                     : 0));
        // SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, 3);
        // SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, 3);
        SDL_GL_CreateContext(window);
#ifndef USE_GLES
        GLenum err = glewInit();
#endif
        glEnable(GL_BLEND);
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
        glBindFramebuffer(GL_FRAMEBUFFER, 0);
        int w = 0;
        int h = 0;
        SDL_GetWindowSize(window, &w, &h);
        // printf("%d x %d\n", w, h);
        // SDL_GL_GetDrawableSize(window, &w, &h);
        // printf("%d x %d\n", w, h);
        // auto* renderer = SDL_GetRenderer(window);
        // SDL_GetRendererOutputSize(renderer, &w, &h);
        // printf("%d x %d\n", w, h);
        glViewport(0, 0, w, h);
        return std::make_shared<SDLWindow>(window);
    }

    void init_input(Settings const& settings) override {}

    bool is_pressed(uint32_t code, int device) override
    {
        if (device == -1) { return pressed[code] != 0; }
        return (pressed[code] & (1 << device)) != 0;
    }

    AnyEvent poll_events() override
    {
        static constexpr std::array jbuttons{Key::FIRE,   Key::B,    Key::X,
                                             Key::Y,      Key::L1,   Key::L2,
                                             Key::SELECT, Key::START};
        SDL_Event e;
        while (SDL_PollEvent(&e) != 0) {
            int device = 0;
            if (e.type == SDL_MOUSEMOTION) {
                auto& me = e.motion;
                if (me.state != 0) { return MoveEvent{me.x, me.y, 1}; }
            } else if (e.type == SDL_MOUSEBUTTONDOWN) {
                return ClickEvent{e.button.x, e.button.y, 1};
            } else if (e.type == SDL_TEXTINPUT) {
                return TextEvent{e.text.text, 0};
            } else if (e.type == SDL_KEYDOWN) {
                auto code = sdl2key(e.key.keysym.sym);
                printf("DOWN %x\n", code);

                auto& ke = e.key;
                pressed[code] |= (1 << device);
                auto mod = ke.keysym.mod;
                if (!in_unicode_range(code) || (mod & 0xc0) != 0) {
                    return KeyEvent{code, mod, device};
                }
            } else if (e.type == SDL_KEYUP) {
                auto& ke = e.key;
                auto code = sdl2key(ke.keysym.sym);
                pressed[code] &= ~(1 << device);
            } else if (e.type == SDL_JOYBUTTONDOWN) {
                device = (e.jbutton.which + 1);
                if (e.jbutton.button <= 7) {
                    auto code =
                        static_cast<uint32_t>(jbuttons[e.jbutton.button]);
                    pressed[code] |= (1 << device);
                    return KeyEvent{code, 0, device};
                }
            } else if (e.type == SDL_JOYBUTTONUP) {
                device = (e.jbutton.which + 1);
                if (e.jbutton.button <= 7) {
                    auto code = jbuttons[e.jbutton.button];
                    pressed[static_cast<int>(code)] &= ~(1 << device);
                }
            } else if (e.type == SDL_JOYAXISMOTION) {
                device = (e.jbutton.which + 1);
                uint32_t mask = (1 << device);
                uint32_t neg_key = 0;
                uint32_t pos_key = 0;
                if (e.jaxis.axis == 0) {
                    neg_key = static_cast<uint32_t>(Key::LEFT);
                    pos_key = static_cast<uint32_t>(Key::RIGHT);
                } else if (e.jaxis.axis == 1) {
                    neg_key = static_cast<uint32_t>(Key::UP);
                    pos_key = static_cast<uint32_t>(Key::DOWN);
                }
                if (pos_key != 0) {
                    if (e.jaxis.value > 10000) {
                        if ((pressed[pos_key] & mask) == 0) {
                            pressed[pos_key] |= mask;
                            return KeyEvent{pos_key, 0, device};
                        }
                    } else if (e.jaxis.value < -10000) {
                        if ((pressed[neg_key] & mask) == 0) {
                            pressed[neg_key] |= mask;
                            return KeyEvent{neg_key, 0, device};
                        }
                    } else {
                        pressed[pos_key] &= ~mask;
                        pressed[neg_key] &= ~mask;
                    }
                }
            } else if (e.type == SDL_JOYHATMOTION) {
                static constexpr std::array directions{Key::UP, Key::RIGHT,
                                                       Key::DOWN, Key::LEFT};
                auto a = e.jhat.value;
                device = (e.jbutton.which + 1);
                auto delta = lastAxis[device] ^ a;
                uint32_t button = 0;
                bool down = false;
                for (int i = 0; i < 4; i++) {
                    uint32_t mask = 1 << i;
                    if ((delta & mask) == mask) {
                        button = static_cast<uint32_t>(directions[i]);
                        down = (a & mask) != 0;
                    }
                }
                lastAxis[device] = a;
                if (down) {
                    pressed[button] |= (1 << device);
                    return KeyEvent{button, 0, device};
                }
                pressed[button] &= ~(1 << device);
            } else if (e.type == SDL_QUIT) {
                return QuitEvent{};
            } else if (e.type == SDL_WINDOWEVENT) {
                if (e.window.event == SDL_WINDOWEVENT_RESIZED) {
                    SDL_Log("Window %d resized to %dx%d", e.window.windowID,
                            e.window.data1, e.window.data2);
                }
            }
        }
        return NoEvent{};
    }

#ifdef USE_ASOUND
    void init_audio(Settings const&) override
    {
        player = std::make_unique<LinuxPlayer>(44100);
    }

    void
    set_audio_callback(std::function<void(float*, size_t)> const& fcb) override
    {

        player->play([fcb](int16_t* data, size_t sz) {
            std::array<float, 32768> fa; // NOLINT
            fcb(fa.data(), sz);
            for (int i = 0; i < sz; i++) {
                auto f = std::clamp(fa[i], -1.0F, 1.0F);
                data[i] = static_cast<int16_t>(f * 32767.0);
            }
        });
    }
#else
    std::function<void(float*, size_t)> audio_callback;

    void
    set_audio_callback(std::function<void(float*, size_t)> const& cb) override
    {
        audio_callback = cb;
    }

    void init_audio(Settings const& /*settings*/) override
    {
        SDL_AudioSpec want;
        SDL_AudioSpec have;

        SDL_memset(&want, 0, sizeof(want));
        want.freq = 44100;
        want.format = AUDIO_F32;
        want.channels = 2;
        want.samples = 4096;
        want.userdata = this;
        want.callback = [](void* userdata, Uint8* stream, int len) {
            auto* sys = static_cast<SDLSystem*>(userdata);
            if (sys->audio_callback) {
                sys->audio_callback(reinterpret_cast<float*>(stream), len / 4);
            }
        };
        audio_device = SDL_OpenAudioDevice(
            nullptr, 0, &want, &have,
            SDL_AUDIO_ALLOW_ANY_CHANGE); // & (~SDL_AUDIO_ALLOW_FORMAT_CHANGE));

        SDL_PauseAudioDevice(audio_device, 0);
    }
#endif
};

std::unique_ptr<System> create_sdl_system()
{
    return std::make_unique<SDLSystem>();
}
