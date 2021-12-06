//Mediocre Rust port of quick.py
use std::{usize, ops::Add};

use num_bigint::{BigUint, BigInt};
#[derive(Debug, Clone)]
struct Vector(Vec<BigUint>);

impl Vector {
    pub fn new(size: usize) -> Self {
        Self::fill(size, 0)
    }
    pub fn fill(size: usize, fill: u32) -> Self {
        let inner: Vec<_> = (0..size).map(|_| BigUint::from(fill)).collect();
        Self(inner)
    }
    pub fn ints<const N: usize>(inner: [u32; N]) -> Self{
        let inner: Vec<_> = inner.iter().map(|v|BigUint::from(*v)).collect();
        Self(inner)
    }
    pub fn scalar_mul(&self, n: &BigUint) -> Self {
        let o: Vec<BigUint> = self.0.iter().map(|a| a * n).collect();
        Self(o)
    }
    pub fn add(&self, rhs: &Self) -> Self {
        let inner: Vec<_> = self
            .0
            .iter()
            .zip(rhs.0.iter())
            .map(|(a, b)| a + b)
            .collect();
        Self(inner)
    }
    pub fn sum(&self) -> BigUint{
        let mut acc = BigUint::from(0u8);
        for v in &self.0 {
            acc += v;
        }
        acc
    }
}

#[derive(Debug, Clone)]
struct Matrix(Vec<Vector>);

impl Matrix {
    fn new(colums: usize, rows: usize) -> Matrix{
        Self::fill(colums, rows, 0)
    }
    fn fill(colums: usize, rows: usize, fill: u32) -> Matrix{
        let inner: Vec<_> = (0..colums).map(|_|Vector::fill(rows, fill)).collect();
        Self(inner)
    }
    fn identity(size: usize) -> Matrix{
        let inner: Vec<_> = (0..size).map(|i|{
            let mut o = Vector::new(size);
            o.0[i] = BigUint::from(1u8);
            o
        }).collect();
        Self(inner)
    }
    fn mul_vec(&self, rhs: &Vector) -> Vector {
        rhs.0
            .iter()
            .zip(self.0.iter())
            .map(|(a, b)| b.scalar_mul(a))
            .fold(Vector::new(self.0[0].0.len()), |acc, x| acc.add(&x))
    }
    fn add(&self, rhs: &Self) -> Self{
        let inner: Vec<_> = self.0.iter().zip(rhs.0.iter()).map(|(a, b)|a.add(b)).collect();
        Self(inner)
    }
    fn mul(&self, rhs: &Self) -> Self {
        let inner: Vec<_> = rhs.0.iter().map(|v|self.mul_vec(v)).collect();
        Self(inner)
    }
    fn power(&self, power: usize) -> Self{
        let mut power = power;
        let mut acc = Self::identity(self.0.len());
        let mut v = self.clone();
        let mut i = 1;
        while power > 0{
            if power & 1 == 1 {
                acc = acc.mul(&v);
            }
            v = v.mul(&v);
            power = power >> 1;
            println!("{}", i);
            i += 1;
        }
        acc
    }
}

fn main() {
    let args: Vec<_> = std::env::args().collect();
    let days: usize = if args.len() > 1{
        args[1].parse().unwrap()
    }else{
        80
    };
    let numbers: Vec<usize> = std::fs::read_to_string("../input.txt")
        .unwrap()
        .split(",")
        .map(str::parse::<usize>)
        .map(Result::unwrap)
        .collect();
    let mut freq: Vec<BigUint> = Vec::with_capacity(7);
    for _ in 0..7 {
        freq.push(BigUint::from(0u8));
    }
    for n in numbers {
        freq[n] += BigUint::from(1u8);
    }
    let matrix = Matrix(vec![
        Vector::ints([0, 0, 0, 0, 0, 0, 1, 0, 1]),
        Vector::ints([1, 0, 0, 0, 0, 0, 0, 0, 0]),
        Vector::ints([0, 1, 0, 0, 0, 0, 0, 0, 0]),
        Vector::ints([0, 0, 1, 0, 0, 0, 0, 0, 0]),
        Vector::ints([0, 0, 0, 1, 0, 0, 0, 0, 0]),
        Vector::ints([0, 0, 0, 0, 1, 0, 0, 0, 0]),
        Vector::ints([0, 0, 0, 0, 0, 1, 0, 0, 0]),
        Vector::ints([0, 0, 0, 0, 0, 0, 1, 0, 0]),
        Vector::ints([0, 0, 0, 0, 0, 0, 0, 1, 0]),
    ]);
    let freq = Vector(freq);
    let matrix = matrix.power(days);
    let answer = matrix.mul_vec(&freq);
    println!("{:?}", answer.sum());
    
}
