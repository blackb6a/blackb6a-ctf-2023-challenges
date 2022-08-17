#include <cstdint>
#include <iostream>
#include <random>
#include <vector>

std::mt19937_64 rng;
std::vector<int> res;

#define LEN 20000

int main() {
  rng.seed(69);
  for (int i = 0; i < LEN; i++) {
    uint64_t r = rng();
    res.push_back(r >> 63);
  }

  for (int i = 64; i < 100; i++) {
    std::cout << res[i];
  }

  // for (int i = -1; i >= -64; i--) {
  //   std::cout << res[(i + LEN) % LEN];
  // }

  std::cout << std::endl;
}