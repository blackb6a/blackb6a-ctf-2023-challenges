#include <algorithm>
#include <bitset>
#include <stdio.h>
#include <vector>
using namespace std;

const int EQS = 20000;
const int LEN = 312 * 64;

typedef bitset<LEN> State;

const State EMPTY = 0;
const uint64_t CONST = 0xb5026f5aa96619e9;

vector<State> state[312];
vector<State> coef_mat;

vector<State> add(vector<State> v1, vector<State> v2) {
  for (int i = 0; i < 64; i++) {
    v1[i] ^= v2[i];
  }
  return v1;
}

vector<State> _lshift_vec(vector<State> vec, int k) {
  vector<State> res;
  for (int i = 0; i < k; i++) {
    res.push_back(EMPTY);
  }
  for (int i = 0; i < vec.size() - k; i++) {
    res.push_back(vec[i]);
  }
  return res;
}

vector<State> _rshift_vec(vector<State> vec, int k) {
  vector<State> res;
  for (int i = k; i < vec.size(); i++) {
    res.push_back(vec[i]);
  }
  for (int i = 0; i < k; i++) {
    res.push_back(EMPTY);
  }
  return res;
}

vector<State> _mask_mask(vector<State> vec, uint64_t mask) {
  vector<State> res;
  for (int i = 0; i < 64; i++) {
    if ((mask >> i) & 1) {
      res.push_back(vec[i]);
    } else {
      res.push_back(EMPTY);
    }
  }
  return res;
}

vector<State> _mask_const(State term, uint64_t mask) {
  vector<State> res;
  for (int i = 0; i < 64; i++) {
    if ((mask >> i) & 1) {
      res.push_back(term);
    } else {
      res.push_back(EMPTY);
    }
  }
  return res;
}

vector<State> _process_vec(vector<State> y) {
  y = add(y, _mask_mask(_rshift_vec(y, 29), 0x5555555555555555));
  y = add(y, _mask_mask(_lshift_vec(y, 17), 0x71d67fffeda60000));
  y = add(y, _mask_mask(_lshift_vec(y, 37), 0xfff7eee000000000));
  y = add(y, _rshift_vec(y, 43));
  return y;
}

void twist() {
  for (int i = 0; i < 312; i++) {
    vector<State> tmp;
    for (int j = 1; j < 31; j++) {
      tmp.push_back(state[(i + 1) % 312][j]);
    }
    for (int j = 31; j < 64; j++) {
      tmp.push_back(state[i][j]);
    }
    tmp.push_back(EMPTY);

    state[i] = tmp;
    state[i] = add(state[i], state[(i + 156) % 312]);
    state[i] = add(state[i], _mask_const(state[(i + 1) % 312][0], CONST));
  }
}

void rref() {
  int eqs = coef_mat.size();
  int row = 0;
  int pivot = 0;
  while (row < eqs && pivot < LEN) {
    if (pivot % 1000 == 0) {
      printf("pivot = %d\n", pivot);
    }
    int cur = row;
    while (cur < eqs && !coef_mat[cur][pivot]) {
      cur++;
    }
    if (cur == eqs) {
      pivot++;
      continue;
    }
    if (cur > row) {
      swap(coef_mat[row], coef_mat[cur]);
    }
    for (cur = row + 1; cur < eqs; cur++) {
      if (coef_mat[cur][pivot]) {
        coef_mat[cur] ^= coef_mat[row];
      }
    }
    row++;
    pivot++;
  }
}

void init_state() {
  for (int i = 0; i < 312; i++) {
    for (int j = 0; j < 64; j++) {
      state[i].push_back(EMPTY);
      state[i][j].flip(i * 64 + j);
    }
  }
}

void init_coef() {
  int idx = 0, cnt = 0;
  for (int i = 0; i < EQS; i++) {
    if (idx == 0) {
      twist();
    }

    if (i % 1000 == 0) {
      printf("i = %d\n", i);
    }

    vector<State> y = state[idx];
    y = _process_vec(y);
    if (i >= 64) {
      coef_mat.push_back(y[63]);
    }

    idx = (idx + 1) % 312;
  }
}

int main() {
  init_state();
  init_coef();
  printf("Started rref\n");
  rref();
  for (int i = 0; i < EQS; i++) {
    for (int j = 0; j < 200; j++) {
      printf("%d", coef_mat[i][j] == 1);
    }
    printf("\n");
  }
}