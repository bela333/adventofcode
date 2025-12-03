module Part01 where

import Data.Char (digitToInt)
import Data.Maybe (catMaybes)

data ResNum
  = ResNumEmpty
  | ResNumOne Int
  | ResNumTwo Int Int
  deriving (Show)

resNumToInt :: ResNum -> Int
resNumToInt (ResNumOne a) = a
resNumToInt (ResNumTwo a b) = 10 * a + b

instance Semigroup ResNum where
  ResNumEmpty <> b = b
  a <> ResNumEmpty = a
  ResNumOne a <> ResNumOne b = ResNumTwo a b
  ResNumOne a <> b@(ResNumTwo bu bl) =
    if a >= bu
      then
        ResNumTwo a (max bu bl)
      else
        b
  ResNumTwo au al <> ResNumOne b =
    if au >= al
      then
        ResNumTwo au (max al b)
      else
        ResNumTwo al b
  ResNumTwo au al <> b@(ResNumTwo bu bl) =
    if au >= al && au >= bu
      then
        ResNumTwo au (max al (max bu bl))
      else
        ResNumOne al <> b

instance Monoid ResNum where
  mempty = ResNumEmpty

optimizeBank :: [Int] -> ResNum
optimizeBank = mconcat . map ResNumOne

main = do
  content <- map (map digitToInt) . lines <$> readFile "input.txt"
  print content
  let results = map optimizeBank content
  print results
  print $ sum $ map resNumToInt results
