import Data.Maybe
import Debug.Trace

-- https://stackoverflow.com/a/12882583
chunks :: Int -> [a] -> [[a]]
chunks _ [] = []
chunks n xs =
    let (ys, zs) = splitAt n xs
    in  ys : chunks n zs

findSame :: Eq a => [a] -> [a] -> [a] -> a
findSame (a:as) bs cs
    | a `elem` bs && a `elem` cs = a
    | otherwise = findSame as bs cs

mapping :: [(Char, Integer)]
mapping = zip (['a'..'z'] ++ ['A'..'Z']) [1..]

getPriorities :: String -> [Integer]
getPriorities = map (\c -> fromJust $ lookup c mapping)

main :: IO ()
main = do
    f <- readFile "input.txt"
    let l = chunks 3 $ lines f
    let badges = map (\[a, b, c] -> findSame a b c) l
    let priorities = getPriorities badges
    print $ sum priorities