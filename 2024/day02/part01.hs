monotone [a,b] | b-a > 0 = 1
               | b-a < 0 = -1
monotone (a:b:rest) | b-a > 0 && 1 == monotone (b:rest) = 1
                    | b-a < 0 && -1 == monotone (b:rest) = -1
                    | otherwise = 0

gradiant (a:b:xs) = let diff = abs (a-b) in 1 <= diff && diff <= 3 && gradiant (b:xs)
gradiant (_:_) = True

p :: [Integer] -> Bool
p xs | monotone xs /= 0 && gradiant xs = True
     | otherwise = False

main :: IO ()
main = do
    content :: [[Integer]] <- map (map read.words) . lines<$>readFile "input.txt"
    print $ length $ filter p content