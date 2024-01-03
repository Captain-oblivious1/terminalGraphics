#include <iostream>

// --diagramFormat \${diagram:(.*)}

/*
 * ⦃ One
 * ╭─────────────────────╮
 * │                     │
 * │    New text         ├─╮
 * ╰──────────────────┬──╯ │
 *                    │    │
 * New text           ╰────╯
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
