import Data.Char (isSpace)
import Data.List

chunksOf :: Int -> [a] -> [[a]]
chunksOf n [] = []
chunksOf n xs = take n xs : chunksOf n (drop n xs)

getOperation :: Char -> ([Int] -> Int)
getOperation '+' = sum
getOperation '*' = product

splitProblem :: [String] -> (Char, [String], [String])
splitProblem (x : xs) = (last x, init x : f, s)
  where
    (f, s) = span (\s -> last s == ' ') xs

solve :: [[Char]] -> Int
solve [] = 0
solve content = opf (map read $ concatMap words current) + solve next
  where
    (op, current, next) = splitProblem content
    opf = getOperation op

main = do
  content <- transpose . lines <$> readFile "input.txt"
  print $ solve content
