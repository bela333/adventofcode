{-# LANGUAGE DataKinds #-}
{-# LANGUAGE GADTs #-}
{-# LANGUAGE OverloadedStrings #-}
{-# LANGUAGE PartialTypeSignatures #-}

import Data.Kind
import Data.Text qualified as T
import Data.Text.IO qualified as TIO
import Data.Text.Read qualified as TR
import GHC.TypeLits

rightToMaybe :: Either a b -> Maybe b
rightToMaybe (Right b) = Just b
rightToMaybe _ = Nothing

data Light = On | Off deriving (Show)

newtype Button = Button [Int] deriving (Show)

data Row = Row {lights :: [Light], buttons :: [Button], joltage :: [Int]} deriving (Show)

parseLight :: Char -> Maybe Light
parseLight '.' = Just Off
parseLight '#' = Just On
parseLight _ = Nothing

parseLights :: T.Text -> Maybe [Light]
parseLights xs | T.head xs == '[' && T.last xs == ']' = mapM parseLight (T.unpack (T.init $ T.tail xs))
parseLights _ = Nothing

parseButton :: T.Text -> Maybe Button
parseButton xs | T.head xs == '(' && T.last xs == ')' = fmap Button $ mapM (fmap fst . rightToMaybe . TR.decimal) $ T.splitOn "," $ T.init $ T.tail xs

parseJoltage :: T.Text -> Maybe [Int]
parseJoltage xs | T.head xs == '{' && T.last xs == '}' = mapM (fmap fst . rightToMaybe . TR.decimal) $ T.splitOn "," $ T.init $ T.tail xs

parseRow :: T.Text -> Maybe Row
parseRow xs = Row <$> lights <*> buttons <*> joltage
  where
    w = T.words xs
    lights = parseLights $ head w
    buttons = mapM parseButton $ init $ tail w
    joltage = parseJoltage $ last w

main = do
  content <- map parseRow . T.lines <$> TIO.readFile "input.txt"
  print content
