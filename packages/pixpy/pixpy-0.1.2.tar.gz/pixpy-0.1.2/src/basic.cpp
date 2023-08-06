#include "utils.h"
#include "parser.h"

#include <fmt/format.h>

extern char const * const basic_grammar;

int main(int argc, char** argv)
{
    using SV = const SemanticValues;

    auto prg = utils::read_as_string(argv[1]);

    auto parser = std::make_unique<Parser>(basic_grammar);
    parser->packrat();

    parser->after("Integer", [&](SV& sv) -> std::any {
      fmt::print("I:{}\n", sv.token_view());
        return sv.token_view();
    });

    parser->after("Statement", [&](SV& sv) -> std::any {
        fmt::print("S:{}\n", sv.token_view());
        return {};
        });

    fmt::print("{}", prg);

    auto node = parser->parse(prg, argv[1]);
    parser->evaluate(node);
    return 0;
}
