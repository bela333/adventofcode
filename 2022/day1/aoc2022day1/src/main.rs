fn main() {
    let f = std::fs::read_to_string("input.txt").unwrap();
    let lines = f.split("\n");
    let elves = lines.collect::<Vec<_>>();
    let elves: Vec<&[&str]> = elves.split(|n|(*n)=="").collect();
    let elves: Vec<Vec<i32>> = elves.into_iter().map(|elf|elf.iter().map(|val|val.parse().unwrap()).collect()).collect();

    let elves: Vec<i32> = elves.into_iter().map(|a|a.into_iter().sum()).collect();
    //Part 1
    println!("Part 1: {}", elves.iter().max().unwrap());
    
    //Part 1
    let mut elves = elves;
    let l = elves.len();
    //Use quickselect to find the top 3 items
    elves.select_nth_unstable(l-3);
    println!("Part 2: {}", elves[l-3..].iter().sum::<i32>());
}
