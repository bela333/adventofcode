hasRepeating :: Eq a => [a] -> Bool
hasRepeating (x:xs) = elem x xs || hasRepeating xs
hasRepeating [] = False

findSeq :: Eq a => [a] -> Integer
findSeq l@(x:xs)
    | hasRepeating $ take 4 l = 1+(findSeq xs)
    | otherwise = 4


main :: IO ()
main = readFile "input.txt" >>= print . findSeq