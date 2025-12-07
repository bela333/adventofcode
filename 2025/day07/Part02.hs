{-# LANGUAGE LambdaCase #-}

import Data.Maybe (catMaybes)

data Cell = Spawner | Empty | Tachyon Int | Splitter

instance Show Cell where
  show Spawner = "S"
  show Empty = "."
  show (Tachyon n) = show n
  show Splitter = "^"

charToCell :: Char -> Cell
charToCell 'S' = Spawner
charToCell '.' = Empty
-- charToCell '|' = Tachyon
charToCell '^' = Splitter

data Event = Split | SpawnTachyon Int Int deriving (Show)

-- createEvents previousRow currentRow
createEvents :: [Cell] -> [Cell] -> [Event]
createEvents previousRow currentRow =
  concatMap
    ( \(prev, curr, i) -> case (prev, curr) of
        (Tachyon u, Splitter) -> [Split, SpawnTachyon (i - 1) u, SpawnTachyon (i + 1) u]
        (_, Spawner) -> [SpawnTachyon i 1]
        (Tachyon u, _) -> [SpawnTachyon i u]
        _ -> []
    )
    (zip3 previousRow currentRow [0 ..])

update :: Int -> (a -> a) -> [a] -> [a]
update 0 f (x : xs) = f x : xs
update i v (x : xs) = x : update (i - 1) v xs

applyEvent :: [Cell] -> Event -> [Cell]
applyEvent row (SpawnTachyon i u) = update i (\case Tachyon u' -> Tachyon (u + u'); _ -> Tachyon u) row
applyEvent row _ = row

applyEvents :: [Cell] -> [Event] -> [Cell]
applyEvents = foldl applyEvent

main :: IO ()
main = do
  content <- map (map charToCell) . lines <$> readFile "input.txt"
  let rowLength = length $ head content
  let baseRow = replicate rowLength Empty
  let h = scanl (\(a, evs) b -> let newEvs = createEvents a b in (applyEvents b newEvs, evs ++ newEvs)) (baseRow, []) content
  print $ map fst h
