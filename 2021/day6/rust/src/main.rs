use std::{usize};

use num_bigint::BigUint;

fn main() {
    let numbers: Vec<usize> = std::fs::read_to_string("../input.txt")
        .unwrap()
        .split(",")
        .map(str::parse::<usize>)
        .map(Result::unwrap)
        .collect();
    let mut freq: Vec<BigUint> = Vec::with_capacity(7);
    let mut next: Vec<BigUint> = Vec::with_capacity(7);
    for _ in 0..7 {
        freq.push(BigUint::from(0u8));
        next.push(BigUint::from(0u8));
    }
    for n in numbers {
        freq[n] += BigUint::from(1u8);
    }
    for i in 0..9999999 {
        next[(i+2)%7] += &freq[i%7];
        let j = if i == 0{
            6
        }else{
            (i-1)%7
        };
        freq[j] += &next[j];
        next[j] = BigUint::from(0u8);
        if i%100000 == 0{
            println!("{}", (i as f32)/9999999.0*100.0);
        }
    }
    let freq_sum = freq.iter().fold(BigUint::from(0u8), |acc, x|acc+x);
    let next_sum = next.iter().fold(BigUint::from(0u8), |acc, x|acc+x);
    println!("{}", freq_sum+next_sum)
}
