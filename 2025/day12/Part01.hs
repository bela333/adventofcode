{-# LANGUAGE OverloadedStrings #-}
{-# LANGUAGE PartialTypeSignatures #-}

{- HLINT ignore "Use lambda-case" -}

import Control.Monad (forM, forM_, guard, replicateM, void)
import Data.List
import Data.Maybe (fromJust, listToMaybe)
import Data.Text qualified as T
import Data.Text.IO qualified as TIO
import Data.Text.Read qualified as TR
import Data.Traversable (for)
import Debug.Trace (traceShow, traceShowId)
import Logic
import System.Environment (getArgs)

data Shape = Shape (Int, Int) [[Bool]] deriving (Eq)

width :: Shape -> Int
width (Shape (w, h) _) = w

height :: Shape -> Int
height (Shape (w, h) _) = h

newShape :: [[Bool]] -> Maybe Shape
newShape xs = do
  let height = length xs
  guard $ height > 0
  let width = length $ head xs
  guard $ width > 0
  guard $ all ((== width) . length) xs
  return $ Shape (width, height) xs

instance Show Shape where
  show (Shape _ xs) = intercalate "\n" (map (map $ \v -> if v then '#' else '.') xs) ++ "\n"

data Row = Row (Int, Int) [Int] deriving (Show)

getCounts :: Row -> [Int]
getCounts (Row _ c) = c

---- Standard library wishlist

-- unfoldr, but returns the remaining state
unfoldr' :: (a -> Maybe (e, a)) -> a -> ([e], a)
unfoldr' f a = case f a of
  Just (e, a) -> let (es, a') = unfoldr' f a in (e : es, a')
  Nothing -> ([], a)

rightToMaybe :: Either a b -> Maybe b
rightToMaybe (Right b) = Just b
rightToMaybe _ = Nothing

listToTuple :: [a] -> Maybe (a, a)
listToTuple [a, b] = Just (a, b)
listToTuple _ = Nothing

maybeToRight :: l -> Maybe r -> Either l r
maybeToRight l (Just r) = Right r
maybeToRight l Nothing = Left l

applyAt :: Int -> (a -> a) -> [a] -> [a]
applyAt _ _ [] = []
applyAt 0 f (x : xs) = f x : xs
applyAt n f (x : xs) = x : applyAt (n - 1) f xs

setAt :: Int -> a -> [a] -> [a]
setAt n x' = applyAt n (const x')

setAt2 :: (Int, Int) -> a -> [[a]] -> [[a]]
setAt2 (x, y) e = applyAt y (setAt x e)

---- End of standard library wishlist

parseShapeRow :: T.Text -> Maybe [Bool]
parseShapeRow xs = mapM (\x -> case x of '.' -> Just False; '#' -> Just True; _ -> Nothing) $ T.unpack xs

parseShape :: [T.Text] -> Maybe (Shape, [T.Text])
parseShape xs = let (current, rest) = span (/= "") xs in ((,tail rest) <$> (newShape =<< mapM parseShapeRow (tail current)))

parseRow :: T.Text -> Either String Row
parseRow xs = let (size, counts) = T.span (/= ':') xs in Row <$> ((maybeToRight "Not enough argument to size" . listToTuple) =<< mapM (fmap fst . TR.decimal) (T.splitOn "x" size)) <*> mapM (fmap fst . TR.decimal) (T.words $ T.tail counts)

transposeShape :: Shape -> Shape
transposeShape (Shape _ xs) = fromJust $ newShape $ transpose xs

rotate90 :: Shape -> Shape
rotate90 (Shape _ xs) = fromJust $ newShape $ reverse $ transpose xs

transforms :: [Shape -> Shape]
transforms =
  [ id,
    rotate90,
    rotate90 . rotate90,
    rotate90 . rotate90 . rotate90,
    transposeShape,
    transposeShape . rotate90,
    transposeShape . rotate90 . rotate90,
    transposeShape . rotate90 . rotate90 . rotate90
  ]

isRowFeasible :: [Shape] -> Row -> _
isRowFeasible shapes (Row (w, h) counts) = sum (map (\(Shape _ shape) -> length $ concatMap (filter id) shape) $ concatMap (uncurry replicate) $ zip counts shapes) < w * h

main = do
  (shapes, rows) <- unfoldr' parseShape . T.lines <$> TIO.readFile "input.txt"
  let Right rows' = mapM parseRow rows
  print $ length $ filter (isRowFeasible shapes) rows'
