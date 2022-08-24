#include <cstdint>
#include <iostream>
#include <random>

std::mt19937_64 rng;
const uint64_t MAX = 0xFFFFFFFFFFFFFFFF;
const uint64_t THRESHOLD = MAX * 1 / 5;

const int n = 100;
bool out_bit = false;
int bit_equations = 0;

int main() {
  rng.seed(69);
  for (int i = 0; i < n; i++) {
    uint64_t r = rng();
    if (!out_bit) {
      out_bit = r > THRESHOLD;
      if (!out_bit) {
        assert((r >> 62) == 0b00);
        bit_equations += 2;
      }
    } else {
      out_bit = r > MAX - THRESHOLD;
      if (out_bit) {
        assert((r >> 62) == 0b11);
        bit_equations += 2;
      }
    }
    // std::cout << out_bit;
  }
  // std::cout << std::endl;
  std::cout << "From n = " << n << " bits of output, we get " << bit_equations
            << " equations!\n";
}
