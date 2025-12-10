{-# LANGUAGE OverloadedStrings #-}

import Control.Monad (guard)
import Data.Foldable (maximumBy)
import Data.Maybe (isJust)
import Data.Text qualified as T
import Data.Text.IO qualified as TIO
import Data.Text.Read qualified as TR

type Range = (Int, Int)

type Rect = (Range, Range)

first2 :: [a] -> Either String (a, a)
first2 (x : y : _) = Right (x, y)
first2 _ = Left "Not enough elements for first2"

window :: [a] -> [(a, a)]
window [] = []
window [x] = []
window (x : y : xs) = (x, y) : window (y : xs)

pointsToRange :: Int -> Int -> Range
pointsToRange a b = (min a b, max a b)

pointsToRect :: (Int, Int) -> (Int, Int) -> Rect
pointsToRect (xa, ya) (xb, yb) = (pointsToRange xa xb, pointsToRange ya yb)

intersectRange :: Range -> Range -> Maybe Range
intersectRange (amin, amax) (bmin, bmax) = let r = (max amin bmin, min amax bmax) in if fst r > snd r then Nothing else Just r

intersectRect :: Rect -> Rect -> Maybe Rect
intersectRect (xa, ya) (xb, yb) = (,) <$> intersectRange xa xb <*> intersectRange ya yb

validRange :: Range -> Bool
validRange (a, b) = a <= b

validRect :: Rect -> Bool
validRect (a, b) = validRange a && validRange b

rangeLength :: Range -> Int
rangeLength (a, b) = b - a + 1

main = do
  Right content <- mapM (mapM (fmap fst . TR.decimal) . T.splitOn ",") . T.lines <$> TIO.readFile "input.txt"
  let Right content' = mapM first2 content
  let rectangles = do
        (p1, i) <- zip content' [1 ..]
        p2 <- drop i content'
        let rect = pointsToRect p1 p2
        let rect' = ((fst (fst rect) + 1, snd (fst rect) - 1), (fst (snd rect) + 1, snd (snd rect) - 1))
        guard $ not $ any (\line -> isJust $ intersectRect (uncurry pointsToRect line) rect') $ window content'
        let area = rangeLength (fst rect) * rangeLength (snd rect)
        return (rect, area)
  let res = maximumBy (\(_, area1) (_, area2) -> compare area1 area2) rectangles
  print $ res

