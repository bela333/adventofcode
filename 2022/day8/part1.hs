import Data.List
import Debug.Trace

(!!!) :: [[Integer]] -> (Integer, Integer) -> Integer
(!!!) f (x, y) = (f `genericIndex` y) `genericIndex` x

extractRegion :: (Integer, Integer) -> (Integer, Integer) -> [[Integer]] -> [[Integer]]
extractRegion (x1, y1) (x2, y2) field = map ((genericDrop x1).(genericTake (x2+1))) rows
    where
        rows =  genericDrop y1 (genericTake (y2+1) field)

visible :: (Integer, Integer) -> [[Integer]] -> Bool
visible (x, y) field = heightTest (x, 0) (x, y-1) || heightTest (0, y) (x-1, y) || heightTest (x, y+1) (x, fieldHeight) || heightTest (x+1, y) (fieldWidth, y)
    where
        fieldHeight = genericLength field
        fieldWidth = genericLength (field !! 0)
        elementsInRange :: (Integer, Integer) -> (Integer, Integer) -> [Integer]
        elementsInRange a b = concat $ extractRegion a b field
        height :: Integer
        height = field !!! (x, y)
        heightTest :: (Integer, Integer) -> (Integer, Integer) -> Bool
        heightTest a b = areShorter height (elementsInRange a b)
        areShorter :: Integer -> [Integer] -> Bool
        areShorter threshold xs = all (< threshold) xs


main :: IO ()
main = do
    l <- (map.map) (read . (:[])) <$> lines <$> readFile "input.txt" :: IO [[Integer]]
    let height = genericLength l
    let width = genericLength (l !! 0)
    let t = [visible (x, y) l | x <- [0..width-1], y <- [0..height-1]]
    print $ foldr (\is acc -> if is then acc+1 else acc) 0 t