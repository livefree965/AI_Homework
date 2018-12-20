#include <iostream>
using namespace std;
extern "C"{
    void add(int* pos);
}
void add(int* pos){
    pos[2]=pos[0]+pos[1];
}