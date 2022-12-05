import Debug.Trace
import Data.Char
import Data.List

-- https://stackoverflow.com/a/12882583
chunks :: Int -> [a] -> [[a]]
chunks _ [] = []
chunks n xs =
    let (ys, zs) = splitAt n xs
    in  ys : chunks n zs

splitOn :: Eq a => a -> [a] -> [[a]]
splitOn c [] = [[]]
splitOn c (x:xs)
    | x == c    = []: splitOn c xs
    | otherwise = (x:h):t where (h:t) = splitOn c xs

data Stack = Stack [Char] deriving Show

stackPop :: Stack -> (Char, Stack)
stackPop (Stack (x:xs)) = (x, Stack xs)

stackPush :: Char -> Stack -> Stack
stackPush c (Stack xs) = Stack (c:xs)

data StackState = StackState [Stack] deriving Show

replaceIndex :: Int -> a -> [a] -> [a]
replaceIndex index elem xs = begin ++ [elem] ++ tail end
    where (begin, end) = splitAt index xs

stackStateMove1 :: Int -> Int -> StackState -> StackState
stackStateMove1 from to (StackState stacks) = StackState $ replaceIndex to newTo (replaceIndex from newFrom stacks)
    where
        (x, newFrom) = stackPop (stacks !! from)
        newTo = stackPush x (stacks !! to)

stackStateMove :: Int -> Int -> Int -> StackState -> StackState
stackStateMove 0 _ _ state = state
stackStateMove n from to state = stackStateMove (n-1) from to (stackStateMove1 from to state)

--This goes against EVERYTHING, that's Haskell
trim :: String -> String
trim xs = reverse (dropWhile isSpace (reverse (dropWhile isSpace xs)))

parseHeader :: [String] -> StackState
parseHeader xs = stackFromParts parts
    where
        parts :: [[Char]]
        parts = map (map (!! 1) . filter (not . null)) $ transpose $ map ((map trim) . (chunks 4)) (init xs)
        stackFromParts :: [[Char]] -> StackState
        stackFromParts xs = StackState $ map (Stack) xs



parseStep :: String -> (Int, Int, Int)
parseStep xs = (read $ parts !! 1, (read $ parts !! 3) - 1, (read $ parts !! 5) - 1)
    where parts = splitOn ' ' xs

stackTops :: StackState -> String
stackTops (StackState stacks) = map (\(Stack xs) -> head xs) stacks

main = do
    f <- readFile "input.txt"
    let l = lines f
    let header = takeWhile (/= "") l
    let rest = tail $ dropWhile (/= "") l
    let steps = map parseStep rest
    let state = parseHeader header
    let state' = foldl (\st (n, from, to) -> stackStateMove n from to st) state steps
    print $ stackTops state'