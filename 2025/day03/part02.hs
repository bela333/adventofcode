module Part02 where

import Data.Char (digitToInt)
import Data.Maybe (catMaybes)
import Debug.Trace (trace, traceShow)

-- INVARIANT: length _result <= size
naive :: Int -> [Int] -> [Int]
naive size [] = []
naive 0 _ = []
naive size (x : xs) =
  let prev = naive size xs
   in if length prev < size
        then
          x : xs
        else
          if x >= head prev
            then
              x : naive (size - 1) prev
            else
              prev

arrayToNum :: [Int] -> Int
arrayToNum [] = 0
arrayToNum (x : xs) = (10 ^ length xs) * x + arrayToNum xs

main = do
  content <- map (map digitToInt) . lines <$> readFile "input.txt"
  print content
  let results = map (arrayToNum . naive 12) content
  print results
  print $ sum results
