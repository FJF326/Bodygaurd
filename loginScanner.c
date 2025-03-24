#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <string.h>


typedef struct loginAttempt{
    char type[15];
    char username[50];
    char ip[50];
    char time[15];
}loginAttempt;
loginAttempt theList[1000];
int isSuspicious = 3;
char buffer[1000];
void main () {
    //find failed logins
    char *findFailedLogins = "sudo grep 'authentication failure' /var/log/auth.log | grep -i ' user='";
    FILE *failedLogins = popen(findFailedLogins,"r");
    if(failedLogins==NULL){
        printf("Failed to run grep\n");
        return;
    }
    
    while(fgets(buffer, sizeof(buffer),failedLogins)){
        loginAttempt newAttempt;
        
        //type starts at char 55
        char typeBuffer[15];
        strncpy(typeBuffer,buffer + 55, 15);
        
        for(int count = 0; count < 15; count++){
            char c = typeBuffer[count];
            if(c==':'){
                strncpy(newAttempt.type,typeBuffer,count);
                break;
            }
        }
        printf("%s\n\n",newAttempt.type);
    }
    

    return;

}