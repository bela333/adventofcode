{-# LANGUAGE OverloadedStrings #-}

module Logic where

import Control.Monad (ap, forM, forM_, liftM, replicateM)
import Data.Text qualified as T
import Text.Printf (printf)

newtype Var = Var Int deriving (Eq, Ord, Show)

data Lit = Pos Var | Neg Var deriving (Eq, Ord, Show)

type Clause = [Lit]

type CNF = [Clause]

newtype CNFM a = CNFM {runCNFM :: Int -> (Int, CNF, a)}

instance Monad CNFM where
  (CNFM a) >>= bf = CNFM $ \varcounter ->
    let (varcounter', cnf1, aret) = a varcounter
     in case runCNFM (bf aret) varcounter' of
          (varcounter'', cnf2, bret) -> (varcounter'', cnf1 ++ cnf2, bret)

instance Applicative CNFM where
  pure x = CNFM {runCNFM = (,[],x)}
  (<*>) = ap

instance Functor CNFM where
  fmap = liftM

newVar :: CNFM Var
newVar = CNFM $ \varcounter -> (varcounter + 1, [], Var varcounter)

constrain :: Clause -> CNFM ()
constrain clause = CNFM (,[clause],())

implies :: Lit -> Lit -> Clause
implies a b = [negateLit a, b]

negateLit :: Lit -> Lit
negateLit (Pos x) = Neg x
negateLit (Neg x) = Pos x

andLit :: [Lit] -> CNFM Lit
andLit lits = do
  x <- newVar
  forM_ lits $ \lit -> do
    constrain [Neg x, lit]
  constrain $ Pos x : map negateLit lits
  return $ Pos x

andLit2 :: Lit -> Lit -> CNFM Lit
andLit2 a b = andLit [a, b]

orLit :: [Lit] -> CNFM Lit
orLit lits = negateLit <$> andLit (map negateLit lits)

pairs :: [a] -> [(a, a)]
pairs [] = []
pairs (x : xs) = map (x,) xs ++ pairs xs

atmostOne :: [Lit] -> CNFM ()
atmostOne lits = forM_ (pairs lits) (\(a, b) -> constrain [negateLit a, negateLit b])

exactlyOne :: [Lit] -> CNFM ()
exactlyOne lits = do
  atmostOne lits
  constrain lits

literalToDimacs :: Lit -> T.Text
literalToDimacs (Pos (Var n)) = T.pack $ show (n + 1) -- our variables are 0 indexed, while dimacs is 1 indexed
literalToDimacs (Neg (Var n)) = T.pack $ show (-(n + 1))

clauseToDimacs :: Clause -> T.Text
clauseToDimacs clause = T.intercalate " " $ map literalToDimacs clause ++ ["0"]

cnfmToDimacs :: CNFM () -> [T.Text]
cnfmToDimacs cnfm = map clauseToDimacs clauses
  where
    (varcounter, clauses, ()) = runCNFM cnfm 0
    clausecounter = length clauses

toggleLit :: Bool -> Lit -> Lit
toggleLit False = id
toggleLit True = negateLit

evalCNFM :: CNFM a -> a
evalCNFM cnfm = let (_, _, ret) = runCNFM cnfm 0 in ret
