#include <new>
#include <malloc.h>
 
void* operator new(std::size_t size) {
	    return malloc(size);
}
 
void* operator new[](std::size_t size) {
	    return malloc(size);
}
 
void operator delete(void* ptr) {
	    free(ptr);
}
 
void operator delete[](void* ptr) {
	    free(ptr);
}

extern "C" void __cxa_pure_virtual() { while(1); }
