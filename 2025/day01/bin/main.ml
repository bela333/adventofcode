let currentNumber = ref 50
let count_part1 = ref 0

exception Invalid_format

let ic = In_channel.with_open_text "input.txt" In_channel.input_lines
let goodMod a m = ((a mod m) + m) mod m;;

let bod = function
  | s when String.starts_with ~prefix:"L" s ->
      let n = int_of_string (String.sub s 1 (String.length s - 1)) in
      currentNumber := goodMod (!currentNumber - n) 100;
      print_int !currentNumber;
      print_newline ();
      if !currentNumber == 0 then count_part1 := !count_part1 + 1 else ()
  | s when String.starts_with ~prefix:"R" s ->
      let n = int_of_string (String.sub s 1 (String.length s - 1)) in
      currentNumber := goodMod (!currentNumber + n) 100;
      print_int !currentNumber;
      print_newline ();
      if !currentNumber == 0 then count_part1 := !count_part1 + 1 else ()
  | _ -> raise Invalid_format
in
List.iter bod ic
;;

print_int !count_part1
