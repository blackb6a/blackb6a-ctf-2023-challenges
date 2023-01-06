# Rusty

DISCLAIMER: WORK IN PROGRESS (06.01.2023)

Short explanation:

- `Box` just dumps whatever is inside onto the heap
- This means that `s1`, `s2`, `s3` are all allocated on the heap
- `SmallVec` is a type that is stored on the stack when it is "small" (in the code, <= 0x10 elements)
- Otherwise, the code copies all data onto the heap
- However, the issue that I linked to in the comment shows that there is an accidental `free` call
- And since `v` is "passed by value" in the function, at the end the deallocator is called, causing double-free
  - Try commenting out `v[9] = 0x41`, you should get "free(): double free detected in tcache 2"
- This means that after calling `grow(&mut v, 0x20)` (where `0x20` is just 2 * N, the new capacity), there will be a free call
- By following [how2heap](https://github.com/shellphish/how2heap/blob/master/glibc_2.35/fastbin_dup_into_stack.c), I made the program return a stack pointer for a heap allocation, as shown by `s3`
