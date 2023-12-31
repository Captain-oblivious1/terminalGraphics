#include <iostream>

// --diagramFormat \${diagram:(.*)}

// from:
/*
${diagram:One}
*/

// to:
/*
⦃ One:
boxes
and
shit
⦄
*/

// from:
// ${diagram:Two}

// to:
// ⦃ One:
// boxes
// and
// shit
// ⦄

int main() { std::cout << "Hello world" << std::endl; }
