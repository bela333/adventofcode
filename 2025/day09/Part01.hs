{-# LANGUAGE OverloadedStrings #-}

import Data.Foldable (maximumBy)
import Data.Text qualified as T
import Data.Text.IO qualified as TIO
import Data.Text.Read qualified as TR

first2 :: [a] -> Either String (a, a)
first2 (x : y : _) = Right (x, y)
first2 _ = Left "Not enough elements for first2"

main = do
  Right content <- mapM (mapM (fmap fst . TR.decimal) . T.splitOn ",") . T.lines <$> TIO.readFile "input.txt"
  let Right content' = mapM first2 content
  let rectangles = do
        (p1, i) <- zip content' [1 ..]
        p2 <- drop i content'
        let area = (fst p1 - fst p2 + 1) * (snd p1 - snd p2 + 1)
        return (p1, p2, area)
  let (_, _, bestArea) = maximumBy (\(_, _, area1) (_, _, area2) -> compare area1 area2) rectangles
  print bestArea
