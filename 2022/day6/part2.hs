hasRepeating :: Eq a => [a] -> Bool
hasRepeating (x:xs) = elem x xs || hasRepeating xs
hasRepeating [] = False

findSeq :: Eq a => Int -> [a] -> Int
findSeq n l@(x:xs)
    | hasRepeating $ take n l = 1+(findSeq n xs)
    | otherwise = n


main :: IO ()
main = readFile "input.txt" >>= print . (findSeq 14)