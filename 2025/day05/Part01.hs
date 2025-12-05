module Part01 where

import Text.Read (readMaybe)

parseHeader :: String -> Maybe (Int, Int)
parseHeader xs =
  case break (== '-') xs of
    (f, '-' : s) -> (,) <$> readMaybe f <*> readMaybe s
    _ -> Nothing

isFresh :: [(Int, Int)] -> Int -> Bool
isFresh xs n = any (\(l, u) -> l <= n && n <= u) xs

main :: IO ()
main = do
  content <- lines <$> readFile "input.txt"
  let (header, "" : footer) = break (== "") content
  let Just header' = mapM parseHeader header
  let Just (footer' :: [Int]) = mapM readMaybe footer
  let isFresh' = isFresh header'
  print $ length $ filter id $ map isFresh' footer'
  return ()
