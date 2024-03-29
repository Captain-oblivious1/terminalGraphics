#include <iostream>

// Using default format which is: \${diagram(?::(.+))?}

/*
 * ⦃ 
 *   ┏╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍╍┓
 *   ╏                        ╏
 *   ╏   Thick dashed         ╏
 *   ╏   line (left           ╏
 *   ╏   justified            ╏
 *   ╏   text)           ┏╍╍╍╍┛
 *   ╏                   ╏   ∧
 *   ╏                   ╏   ╎
 *   ╏                   ╏   ╎
 *   ╏                   ┠───┼─────┐
 *   ╏  ┌────┐           ╏   ╎     │
 *   ┗╍╍┥    ┝╍╍╍╍╍╍╍╍╍╍╍┛   ╎     │
 *      │    │               ╎     │
 *      │    │   ╭─────────╮ ╎     │
 *      │    │   │         │ ╰╌╌╌╌╌┼╌╌╌╮
 *      │ ╭──┴───╯         │       │   ╎         ┌────┐      ┌───┐                        ┌───┐
 *      │ │   Thin solid   │◁──────┘   ╎         │User│      │Foo│                        │Bar│
 *      │ │ line (centered │           ╎         └──┬─┘      └─┬─┘                        └─┬─┘
 *      │ │      text)     │◁╌╌╌╌╌╌╌╌╌╌╯            │          │                            │
 *      │ ╰──┬─────────────╯                        │          │<────────────Bar────────────┤
 *      └────┘                                      ├Some text>│                            │
 *                                                  │          │                            │
 *                                                  │<─────────┼───────Foo──────────────────┤
 *                                                  │          │                            │
 *                                                  │          │            Other           │
 * ┌──────────────────────────────────┐             │          │<───────────Text────────────┤
 * │            <interface>           │
 * │            MyInterface           │
 * ├──────────────────────────────────┤
 * │+func1(val:int):float             │
 * │+func2(val1:float,val2:float):void│
 * └──────────────────────────────────┘
 * ⦄
 */

// ⦃ Blah
// ╭─────────╮
// │         │
// │         │
// ╰─────────╯
// ⦄

int main() { std::cout << "Hello world" << std::endl; }
