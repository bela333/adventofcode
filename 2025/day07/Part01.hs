{-# LANGUAGE LambdaCase #-}

import Data.Maybe (catMaybes)

data Cell = Spawner | Empty | Tachyon | Splitter

instance Show Cell where
  show Spawner = "S"
  show Empty = "."
  show Tachyon = "|"
  show Splitter = "^"

charToCell :: Char -> Cell
charToCell 'S' = Spawner
charToCell '.' = Empty
charToCell '|' = Tachyon
charToCell '^' = Splitter

data Event = Split | SpawnTachyon Int deriving (Show)

-- createEvents previousRow currentRow
createEvents :: [Cell] -> [Cell] -> [Event]
createEvents previousRow currentRow =
  concatMap
    ( \(prev, curr, i) -> case (prev, curr) of
        (Tachyon, Splitter) -> [Split, SpawnTachyon $ i - 1, SpawnTachyon $ i + 1]
        (_, Spawner) -> [SpawnTachyon i]
        (Tachyon, _) -> [SpawnTachyon i]
        _ -> []
    )
    (zip3 previousRow currentRow [0 ..])

update :: Int -> a -> [a] -> [a]
update 0 v (x : xs) = v : xs
update i v (x : xs) = x : update (i - 1) v xs

applyEvents :: [Cell] -> [Event] -> [Cell]
applyEvents row [] = row
applyEvents row (SpawnTachyon i : xs) = applyEvents (update i Tachyon row) xs
applyEvents row (_ : xs) = applyEvents row xs

main :: IO ()
main = do
  content <- map (map charToCell) . lines <$> readFile "input.txt"
  let rowLength = length $ head content
  let baseRow = replicate rowLength Empty
  let h = scanl (\(a, evs) b -> let newEvs = createEvents a b in (applyEvents b newEvs, evs ++ newEvs)) (baseRow, []) content
  print $ map fst h
  print $
    ( \(_, evs) ->
        length $
          filter
            ( \case
                Split -> True
                _ -> False
            )
            evs
    )
      (last h)
