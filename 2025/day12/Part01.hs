{-# LANGUAGE OverloadedStrings #-}
{-# LANGUAGE PartialTypeSignatures #-}

{- HLINT ignore "Use lambda-case" -}

import Control.Monad (forM, forM_, guard)
import Data.List
import Data.Maybe (fromJust, listToMaybe)
import Data.Text qualified as T
import Data.Text.IO qualified as TIO
import Data.Text.Read qualified as TR

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
  show (Shape _ xs) = intercalate "\n" (map (map $ \v -> if v then '#' else '.') xs)

data Row = Row (Int, Int) [Int] deriving (Show)

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

-- findPositions (width, height) board shape
findPositions :: Shape -> Shape -> _
findPositions board shape = do
  x <- [0 .. width board - width shape]
  y <- [0 .. height board - height shape]
  let Shape _ boardList = board
  let Shape _ shapeList = shape
  let common = map (drop x) $ drop y boardList
  let common' = all (all (\(a, b) -> not $ a && b)) (zipWith zip common shapeList)
  return (x, y)

-- fitAll :: Shape -> [[Shape]] -> [[(Int, Int)]]
fitAll :: Shape -> [[Shape]] -> _
fitAll board _ = []
fitAll board (shape : shapes) = do
  shapeVariant <- shape
  positions <- findPositions board shapeVariant
  let board' = _
  return positions

main = do
  (shapes, rows) <- unfoldr' parseShape . T.lines <$> TIO.readFile "input.txt"
  let Right rows' = mapM parseRow rows
  let exampleShape = head shapes
  let Row size _ = head rows'
  print (exampleShape, size)
  let exampleVariants = nub $ map ($ exampleShape) transforms
  print $ fitAll (fromJust $ newShape $ replicate (snd size) $ replicate (fst size) False) (replicate 3 exampleVariants)

-- forM_ (nub $ map ($ exampleShape) transforms) $ \v -> do
--   print v
--   putStrLn ""
