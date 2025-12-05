module Part02 where

import Data.List
import Text.Read (readMaybe)

type Range = (Int, Int)

isIntersecting :: Range -> Range -> Bool
isIntersecting (al, au) (bl, bu) = let (il, iu) = (max al bl, min au bu) in il <= iu

-- mergeRange processed remaining
mergeRange :: [Range] -> [Range] -> [Range]
mergeRange a [] = a
mergeRange [] (x : xs) = mergeRange [x] xs
mergeRange processed (x : xs) =
  let (intersecting, notIntersecting) = partition (`isIntersecting` x) processed
   in let newProcessed = (minimum $ map fst $ x : intersecting, maximum $ map snd $ x : intersecting) : notIntersecting
       in mergeRange newProcessed xs

parseHeader :: String -> Maybe Range
parseHeader xs =
  case break (== '-') xs of
    (f, '-' : s) -> (,) <$> readMaybe f <*> readMaybe s
    _ -> Nothing

main :: IO ()
main = do
  content <- lines <$> readFile "input.txt"
  let (header, "" : _) = break (== "") content
  let Just header' = mapM parseHeader header
  let simplifiedRanges = mergeRange [] header'
  print $ sum $ map (\(l, u) -> u - l + 1) simplifiedRanges
  return ()
