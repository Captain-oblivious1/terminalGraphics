#include <iostream>

// --diagramFormat \${diagram:(.*)}

/*
 * ⦃ One
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

/*
⦃ Two
boxes
and
shit
⦄
*/

// ${diagram:Three}

// to:
// ⦃ Four
// boxes
// and
// shit
// ⦄

int main() { std::cout << "Hello world" << std::endl; }
