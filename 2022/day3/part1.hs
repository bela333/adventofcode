import Data.Maybe
import Debug.Trace

findSame :: Eq a => [a] -> [a] -> a
findSame (a:as) bs
    | a `elem` bs = a
    | otherwise = findSame as bs

processLine :: String -> Char
processLine xs = findSame s1 s2
    where (s1, s2) = splitAt ((length xs) `div` 2) xs

mapping :: [(Char, Integer)]
mapping = zip (['a'..'z'] ++ ['A'..'Z']) [1..]



main :: IO ()
main = do
    f <- readFile "input.txt"
    let l = lines f
    let chars = map processLine l
    let nums = map (\c -> fromJust $ lookup c mapping) chars
    print $ sum nums