{-# LANGUAGE OverloadedStrings #-}

import Data.Map qualified as M
import Data.Maybe (fromJust)
import Data.Set (Set, empty, fromList, member, toList, union, (\\))
import Data.Set qualified as S
import Data.Text qualified as T
import Data.Text.IO qualified as TIO

data Graph = Graph {vertices :: Set T.Text, edges :: Set (T.Text, T.Text)} deriving (Show)

instance Semigroup Graph where
  a <> b = Graph {vertices = vertices a `union` vertices b, edges = edges a `union` edges b}

instance Monoid Graph where
  mempty = Graph {vertices = empty, edges = empty}

parseLine :: T.Text -> Either String Graph
parseLine xs =
  if T.last (head parts) /= ':'
    then Left "Invalid line format"
    else
      Right $ Graph {vertices = fromList $ from : to, edges = fromList $ map (from,) to}
  where
    parts = T.words xs
    from = T.init $ head parts
    to = tail parts

topo :: Graph -> Maybe [T.Text]
topo g = (\l -> l ++ toList (vertices g \\ fromList l)) <$> go g
  where
    go (Graph {vertices = vertices, edges = edges})
      | null edges = Just []
      | otherwise = if null sources then Nothing else (toList sources ++) <$> go Graph {vertices = vertices, edges = S.filter (not . flip member sources . fst) edges}
      where
        froms = S.map fst edges
        tos = S.map snd edges
        sources = froms \\ tos

countPaths :: Graph -> [T.Text] -> T.Text -> M.Map T.Text Int
countPaths _ [] goal = M.empty
countPaths g (v : vs) goal = M.insert v (if v == goal then 1 else sum $ map (\e -> fromJust $ M.lookup (snd e) prev) $ filter (\e -> fst e == v) $ toList $ edges g) prev
  where
    prev = countPaths g vs goal

findPaths :: Graph -> [T.Text] -> T.Text -> M.Map T.Text [[T.Text]]
findPaths _ [] goal = M.empty
findPaths g (v : vs) goal = M.insert v (if v == goal then [[goal]] else map (v :) $ concatMap (\e -> fromJust $ M.lookup (snd e) prev) (filter (\e -> fst e == v) $ toList $ edges g)) prev
  where
    prev = findPaths g vs goal

window :: [a] -> [(a, a)]
window (x : y : xs) = (x, y) : window (y : xs)
window _ = []

main = do
  Right content <- fmap mconcat . mapM parseLine . T.lines <$> TIO.readFile "input.txt"
  let Just order = topo content
  let routesFromTo from to = M.lookup from $ countPaths content order to
  let p1 = product <$> mapM (uncurry routesFromTo) (window ["svr", "fft", "dac", "out"])
  let p2 = product <$> mapM (uncurry routesFromTo) (window ["svr", "dac", "fft", "out"])
  print $ (+) <$> p1 <*> p2
