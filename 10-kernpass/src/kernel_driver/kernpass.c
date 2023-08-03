#include <linux/cdev.h>
#include <linux/fs.h>
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/random.h>
#include <linux/slab.h>
#include <linux/uaccess.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("botton");
MODULE_DESCRIPTION("kernpass");

#define DEVICE_NAME "kernpass"
#define ADD_PW 0x13370001 
#define CHK_PW 0x13370002
#define EDIT_PW 0x13370003
#define DEL_PW 0x13370004

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

password_list* main_list;

static int add_password(request_t* req)
{
  unsigned int index;
  unsigned int size;
  char *password;
  password_entity *tmp_entity;

  index = req->index;
  size = req->size;
  password = req->password;

  if (index >= 0 && index < 0x20 && size <= 512) { 

    tmp_entity = (password_entity*)kmalloc(sizeof(password_entity), GFP_KERNEL_ACCOUNT);
    tmp_entity->size = size;
    tmp_entity->password = (char *)kmalloc(size, GFP_KERNEL_ACCOUNT);

    if (unlikely(copy_from_user(tmp_entity->password, password, size))){
      kfree(tmp_entity);
      return -1;
    }

    main_list->passwords[index] = tmp_entity;
  } else {
    return -1;
  }
 
  return 0;
}

static int check_password(request_t* req)
{
  unsigned int index; 
  unsigned int size;
  char *password;
  password_entity *tmp_entity;

  index = req->index;
  password = req->password;

  if (index >= 0 && index < 0x20) { 
    if (main_list->passwords[index]){
      tmp_entity = main_list->passwords[index];
      size = tmp_entity->size;

      if (unlikely(copy_to_user(password, tmp_entity->password, size))){
        return -1;
      }
    } else {
      return -1;
    }
  } else {
    return -1;;
  }

  return 0;
}

static int edit_password(request_t* req)
{
  unsigned int index;
  unsigned int size;
  char *password;
  password_entity *tmp_entity;

  index = req->index;
  password = req->password;

  if (index >= 0 && index < 0x20) { 
    if (main_list->passwords[index]){

      tmp_entity = main_list->passwords[index];
      
      size = tmp_entity->size;
  
      if (unlikely(copy_from_user(tmp_entity->password, password, size))){
        return -1;
      }

    } else {
      return -1;
    }

  } else {
    return -1;
  }

  return 0;
}

static int delete_password(request_t* req)
{
  unsigned int index;

  index = req->index;
  if (index >= 0 && index < 0x20) { 
    kfree(main_list->passwords[index]->password);
    kfree(main_list->passwords[index]);
    main_list->passwords[index] = 0;
  } else{
    return -1;
  }
  return 0;
}

static int module_open(struct inode *inode, struct file *filp) {
  main_list = (password_list*)kmalloc(sizeof(password_list), GFP_KERNEL_ACCOUNT);
  return 0;
}

static int module_close(struct inode *inode, struct file *filp) {

  /* Remove everything */
  ///kfree(b_list);
  return 0;
}

static long module_ioctl(struct file *filp,
                         unsigned int cmd,
                         unsigned long arg) {
  request_t req;
  if (unlikely(copy_from_user(&req, (void*)arg, sizeof(req))))
    return -1;

  switch (cmd) {
    case ADD_PW: return add_password(&req);
    case CHK_PW: return check_password(&req);
    case EDIT_PW: return edit_password(&req);
    case DEL_PW: return delete_password(&req);
    default: return -1;
  }
}

static struct file_operations module_fops = {
  .owner   = THIS_MODULE,
  .open    = module_open,
  .release = module_close,
  .unlocked_ioctl = module_ioctl
};

static dev_t dev_id;
static struct cdev c_dev;

static int __init module_initialize(void)
{
  if (alloc_chrdev_region(&dev_id, 0, 1, DEVICE_NAME))
    return -EBUSY;

  cdev_init(&c_dev, &module_fops);
  c_dev.owner = THIS_MODULE;

  if (cdev_add(&c_dev, dev_id, 1)) {
    unregister_chrdev_region(dev_id, 1);
    return -EBUSY;
  }

  main_list = (password_list*)kmalloc(sizeof(password_list), GFP_KERNEL_ACCOUNT);
  return 0;
}

static void __exit module_cleanup(void)
{
  cdev_del(&c_dev);
  unregister_chrdev_region(dev_id, 1);
}

module_init(module_initialize);
module_exit(module_cleanup);
