#include <iostream>

// --diagramFormat \${diagram:(.*)}

/*
 * ⦃ One
 * ╭────────────────────────╮
 * │                        │
 * │                        │
 * │                        │
 * │                        │
 * │      Test text.   ╭───┬╯
 * │                   │   │
 * │                   │   │
 * │                   │   │
 * │                   ├───┼─────╮
 * │  ╭────╮           │   │     │
 * ╰──┤    ├───────────╯   │     │
 *    │    │               └─────┼───┐
 *    │    │                     │   │
 *    │    │                     │   │
 *    │ ╭──┴────────────╮        │   │
 *    │ │               │◁───────╯   │
 *    │ │   Foo Bar.    │◁───────────┘
 *    │ │               │
 *    │ ╰──┬────────────╯
 *    ╰────╯
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
