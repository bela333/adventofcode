{-# LANGUAGE OverloadedStrings #-}

import Data.Bifunctor (Bifunctor (second))
import Data.List (find, nub, sort, sortBy, sortOn)
import Data.Map (Map, alter, empty, toList)
import Data.Maybe (isJust)
import Data.Ord (Down (Down), comparing)
import Data.Text qualified as T
import Data.Text.IO qualified as TIO
import Data.Text.Read qualified as TR

countDistinct :: (Ord a) => [a] -> Map a Int
countDistinct =
  foldr
    ( alter
        ( \v -> Just $ case v of
            Just v -> v + 1
            Nothing -> 1
        )
    )
    empty

allSame :: (Eq a) => [a] -> Bool
allSame [] = True
allSame (x : xs) = all (== x) xs

main = do
  Right boxes <- mapM (mapM (second fst . TR.decimal) . T.splitOn ",") . T.lines <$> TIO.readFile "input.txt"
  let distances = map fst $ sortOn snd $ do
        ([x1, y1, z1], i :: Int) <- zip boxes [0 ..]
        ([x2, y2, z2], j :: Int) <- drop (i + 1) (zip boxes [0 ..])
        return ((i, j), ((x1 - x2) ^ 2 + (y1 - y2) ^ 2 + (z1 - z2) ^ 2) :: Int)
  let circuits = zipWith (const id) boxes [1 :: Int ..]
  let (Just circuits') =
        find (allSame . snd) $
          scanl
            ( \(_, prevCirc) (node1, node2) ->
                let (id1, id2) = (prevCirc !! node1, prevCirc !! node2)
                 in ((node1, node2), map (\id -> if id == id2 then id1 else id) prevCirc)
            )
            ((0, 0), circuits)
            distances
  let ((node1, node2), _) = circuits'
  print $ head (boxes !! node1) * head (boxes !! node2)
