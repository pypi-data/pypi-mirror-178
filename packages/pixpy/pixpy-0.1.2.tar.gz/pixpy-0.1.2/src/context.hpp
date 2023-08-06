#pragma once

#include "colors.hpp"
#include "gl/buffer.hpp"
#include "gl/color.hpp"
#include "gl/functions.hpp"
#include "gl/program.hpp"
#include "gl/program_cache.hpp"
#include "gl/texture.hpp"

#include "vec2.hpp"

namespace pix {

class Context
{
    GLuint target = 0;
    Vec2f offset{0, 0};
    Vec2f target_size;

public:
    float vpscale = 1.0F;

    float line_width = 1;
    gl_wrap::Color fg;

private:
    float last_x = 0;
    float last_y = 0;

    gl_wrap::Program& colored;
    gl_wrap::Program& textured;
    gl_wrap::Program& filled;

    template <typename T> constexpr float to_screen_x(T x) const
    {
        return (static_cast<float>(x) + offset.x) * 2.0F / target_size.x - 1.0F;
    }

    template <typename T> constexpr float to_screen_y(T y) const
    {
        return (static_cast<float>(y) + offset.y) * -2.0F / target_size.y +
               1.0F;
    }

    template <typename CO>
    void draw_filled(CO const& container, gl_wrap::Primitive primitive);

    template <typename CO>
    void draw_textured(CO const& container, gl_wrap::Primitive primitive);

    std::vector<float> generate_circle(Vec2f const& center, float radius,
                                       bool include_center = true) const;
    std::array<float, 4> generate_line(double x0, double y0, double x1,
                                       double y1);
    std::vector<float> generate_lines(float const* screen_cords, int count) const;
    std::array<float, 8> generate_quad(float x, float y, float w,
                                       float h) const;
    std::array<float, 8> rotated_quad(Vec2f center, Vec2f sz, float rot) const;
    std::array<float, 16> generate_quad_with_uvs(Vec2f pos, Vec2f size) const;

    std::array<float, 16> rotated_quad_with_uvs(Vec2f center, Vec2f sz,
                                                float rot) const;

    void draw_points();

public:
    constexpr Vec2<float> to_screen(Vec2f const& v) const
    {
        auto res = (v + offset) * Vec2f{2, -2} / target_size + Vec2f{-1, 1};
        return {static_cast<float>(res.x), static_cast<float>(res.y)};
    }

    constexpr Vec2<float> to_screen(float x, float y) const
    {
        return to_screen(Vec2f{x, y});
    }

    Context(float w, float h, GLuint fb = 0);
    Context(Vec2f const& offset, Vec2f const& size, GLuint fb = 0);

    Vec2f const& screen_size() { return target_size; }

    void set_target() const;

    void set_color(gl_wrap::Color const& col);

    void circle(Vec2f const& v, float r);
    void filled_circle(Vec2f const& v, float r);
    void line(float x0, float y0, float x1, float y1);
    void line(float x1, float y1);
    void filled_rect(float x, float y, float w, float h);
    void rect(float x, float y, float w, float h);
    void blit(gl_wrap::TexRef const& tex, Vec2f pos, Vec2f size);
    void draw(gl_wrap::TexRef const& tex, Vec2f center, Vec2f size, float rot);

    void plot(Vec2f point, gl_wrap::Color col);
    void flush();


    void clear(gl_wrap::Color const& col) const;
};
} // namespace pix
