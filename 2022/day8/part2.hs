import Data.List
import Debug.Trace


(!!!) :: [[Integer]] -> (Integer, Integer) -> Integer
(!!!) f (x, y) = (f `genericIndex` y) `genericIndex` x

extractRegion :: (Integer, Integer) -> (Integer, Integer) -> [[Integer]] -> [[Integer]]
extractRegion (x1, y1) (x2, y2) field = map ((genericDrop x1).(genericTake (x2+1))) rows
    where
        rows =  genericDrop y1 (genericTake (y2+1) field)

handleFoldr :: Integer -> (Integer, Bool, Integer) -> (Integer, Bool, Integer)
handleFoldr v (c, run, h) | not run = (c, run, h)
handleFoldr v (c, run, h)
    | v < h = (c+1, run, h)
    | otherwise = (c+1, False, h)

getCount :: Integer -> [Integer] -> Integer
getCount height fs = case (foldr handleFoldr (0, True, height) fs) of (c, _, _) -> c

score :: (Integer, Integer) -> [[Integer]] -> Integer
score (x, y) field = c1*c2*c3*c4
    where
        c1 = getCount height (elementsInRange (x, 0) (x, y-1))
        c2 = getCount height (elementsInRange (0, y) (x-1, y))
        c3 = getCount height (reverse $ elementsInRange (x, y+1) (x, fieldHeight))
        c4 = getCount height (reverse $ elementsInRange (x+1, y) (fieldWidth, y))

        fieldHeight = genericLength field
        fieldWidth = genericLength (field !! 0)
        elementsInRange :: (Integer, Integer) -> (Integer, Integer) -> [Integer]
        elementsInRange a b = concat $ extractRegion a b field
        height :: Integer
        height = field !!! (x, y)


main :: IO ()
main = do
    l <- (map.map) (read . (:[])) <$> lines <$> readFile "input.txt" :: IO [[Integer]]
    let height = genericLength l
    let width = genericLength (l !! 0)
    let t = [score (x, y) l | x <- [0..width-1], y <- [0..height-1]]
    --print $ t
    print $ maximum t