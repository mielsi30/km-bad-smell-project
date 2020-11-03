LONG_METHOD = "class A { int f(int x) { x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;}}"

LONG_CONSTRUCTOR = "class A { A() { x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;x++;}}"

DATA_CLASS = "class A { public int x; public void setX(int x) { this.x = x; } public int getX() { return this.x; }}"

LARGE_CLASS = "class A { public void a(){} public void b(){} public void c(){} public void d(){} public void e(){}" \
              " public void f(){} public void g(){} public void h(){} public void i(){} public void j(){} }"

METHOD_WITH_SWITCH = "class A { " \
                     "public void f(int x) { " \
                     "switch(x) {" \
                     "case 0: System.out.println(0);" \
                     "}" \
                     "}" \
                     "}"

CONSTRUCTOR_WITH_SWITCH = "class A { " \
                     "A() { " \
                     "int x = 0; " \
                     "switch(x) {" \
                     "case 0: System.out.println(0);" \
                     "}" \
                     "}" \
                     "}"

METHOD_LONG_PARAMETER_LIST = "class A { " \
                     "public void f(int x, int y, int z, int a, int b, int c) { } " \
                     "}"

CONSTRUCTOR_LONG_PARAMETER_LIST = "class A { " \
                     "A(int x, int y, int z, int a, int b, int c) { } " \
                     "}"