work-stuff
==========


#include <stdio.h>
#include <stdlib.h>

#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>

int wakeup(const char *addr) {
    int sock;
    int optv = 1;

    if ((sock = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP)) < 0) {
        perror("socket");
        return -1;
    }
    if (setsockopt(sock, SOL_SOCKET, SO_BROADCAST, (char *)&optv, sizeof(optv))
            < 0) {
        perror("setsockopt");
        return -1;
    }
    struct sockaddr_in sinaddr;
    sinaddr.sin_family = AF_INET;
    sinaddr.sin_port = htons(9);
    unsigned char packet[100];
    if (sendto(sock, packet, sizeof(packet), 0, (struct sockaddr *)&sinaddr,
                sizeof(sinaddr)) < 0) {
        perror("sendto");
        return -1;
    }
    return 0;
}

int main(int argc, char *argv[]) {
    printf("%s\n", wakeup("00:00:00:00:00:00") == 0 ? "SUCCESS" : "FAILED");
    return 0;
}
"wol.c"
