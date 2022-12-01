import Data.List

splitOn :: Eq a => a -> [a] -> [[a]]
splitOn c [] = [[]]
splitOn c (x:xs)
    | x == c    = []: splitOn c xs
    | otherwise = (x:h):t where (h:t) = splitOn c xs

splitLines :: String -> [String]
splitLines = splitOn '\n'

main :: IO ()
main = do 
    file <- readFile "input.txt"
    let lines = splitLines file
    let elves = splitOn "" lines
    let elves' = (map.map) read elves :: [[Integer]]
    let sums = map sum elves'
    print $ foldr max (head sums) (tail sums)