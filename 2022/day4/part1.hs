splitOn :: Eq a => a -> [a] -> [[a]]
splitOn c [] = [[]]
splitOn c (x:xs)
    | x == c    = []: splitOn c xs
    | otherwise = (x:h):t where (h:t) = splitOn c xs

type Range = (Integer, Integer)
type Pair = (Range, Range)

parseRange :: String -> Range
parseRange xs = (read a, read b)
    where [a, b] = splitOn '-' xs

parsePair :: String -> Pair
parsePair xs = (parseRange a, parseRange b)
    where [a, b] = splitOn ',' xs

rangeContainedIn :: Range -> Range -> Bool
rangeContainedIn (afrom, ato) (bfrom, bto)
    | afrom <= bfrom && ato >= bto = True
    | bfrom <= afrom && bto >= ato = True
    | otherwise                    = False

pairOverlaps :: Pair -> Bool
pairOverlaps (a, b) = rangeContainedIn a b

main :: IO ()
main = do
    l <- lines <$> (readFile "input.txt")
    let pairs = map (pairOverlaps . parsePair) l
    print $ foldr (\b acc -> if b then acc+1 else acc) 0 pairs