import Data.List

getOperation :: String -> ([Int] -> Int)
getOperation "+" = sum
getOperation "*" = product

main = do
  content <- map words . lines <$> readFile "input.txt"
  let operations = map getOperation $ last content
  let (numbers :: [[Int]]) = transpose $ map (map read) $ init content
  let problems = zip operations numbers
  let solutions = map (uncurry ($)) problems
  print $ sum solutions
