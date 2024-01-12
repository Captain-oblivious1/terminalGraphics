#include <iostream>

// Using default format which is: \${diagram(?::(.+))?}

/*
 * ⦃ 
 * ┏╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍┓
 * ╏                        ╏
 * ╏   Thick dashed         ╏
 * ╏   line (left           ╏
 * ╏   justified            ╏
 * ╏   text)           ┏╍╍╍╍┛
 * ╏                   ╏   ∧
 * ╏                   ╏   ╎
 * ╏                   ╏   ╎
 * ╏                   ┠───┼─────┐
 * ╏  ┌────┐           ╏   ╎     │
 * ┗╍╍┥    ┝╍╍╍╍╍╍╍╍╍╍╍┛   ╎     │
 *    │    │               ╎     │
 *    │    │   ╭─────────╮ ╎     │
 *    │    │   │         │ ╰╌╌╌╌╌┼╌╌╌╮
 *    │ ╭──┴───╯         │       │   ╎
 *    │ │   Thin solid   │◁──────┘   ╎
 *    │ │ line (centered │           ╎
 *    │ │     text)      │◁╌╌╌╌╌╌╌╌╌╌╯
 *    │ ╰──┬─────────────╯
 *    └────┘
 * ⦄
 */

// ⦃ Blah
// ╭─────────╮
// │         │
// │         │
// ╰─────────╯
// ⦄

int main() { std::cout << "Hello world" << std::endl; }
