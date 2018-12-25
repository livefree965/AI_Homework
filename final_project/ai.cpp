#include <iostream>
using namespace std;
int gl=8;
extern "C"{
    void add(int* pos);
}
void add(int* pos){
    pos[2]=pos[0]+pos[1]+gl;
    gl=5;
}