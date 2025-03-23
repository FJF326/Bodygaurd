#include <stdio.h>
#include <stdlib.h>
#include <time.h>


struct loginAttempt{
    char username[50];
    char ip[50];
    time_t time;
};

int isSuspicious = 0;


void main () {

}