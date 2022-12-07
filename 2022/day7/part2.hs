import Data.Maybe
import Data.Char
import Debug.Trace

splitOn :: Eq a => a -> [a] -> [[a]]
splitOn c [] = [[]]
splitOn c (x:xs)
    | x == c    = []: splitOn c xs
    | otherwise = (x:h):t where (h:t) = splitOn c xs

data Tree = Directory String [Tree] | File String Integer deriving Show

type Path = [String]

data State = State Tree Path deriving Show

getTree :: State -> Tree
getTree (State tree _) = tree

getName :: Tree -> String
getName (Directory name _) = name
getName (File name _) = name

getByName :: String -> Tree -> Tree
getByName folder (Directory _ contents) = fromJust $ lookup folder $ map (\f -> (getName f, f)) contents

setFolder :: String -> Tree -> Tree -> Tree
setFolder folder new (Directory n (x:xs))
    | getName x == folder = Directory n (new:xs)
    | otherwise = Directory n' (x:xs') where (Directory n' xs') = setFolder folder new (Directory n xs)

mkdir :: String -> State -> State
mkdir folder (State (Directory current rest) []) = State (Directory current (Directory folder []:rest)) []
mkdir folder (State tree (p:ps)) = State (setFolder p tree' tree) (p:ps')
    where (State tree' ps') = mkdir folder (State (getByName p tree) ps)

mkfile :: String -> Integer -> State -> State
mkfile file size (State (Directory current rest) []) = State (Directory current (File file size:rest)) []
mkfile file size (State tree (p:ps)) = State (setFolder p tree' tree) (p:ps)
    where (State tree' _) = mkfile file size (State (getByName p tree) ps)

cd :: String -> State -> State
cd ".." (State tree path) = State tree (init path)
cd folder (State tree path) = State tree (path ++ [folder])

handleLine :: State -> String -> State
handleLine state ('$':' ':'c':'d':' ':folder) = cd folder state
handleLine state ('d':'i':'r':' ':folder) = mkdir folder state
handleLine state line | isDigit $ head line = mkfile name (read size) state
    where [size, name] = splitOn ' ' line
handleLine state _ = state

totalSize :: Tree -> Integer
totalSize (File _ s) = s
totalSize (Directory _ contents) = sum $ map totalSize contents

allFolderSizes :: Tree -> [Integer]
allFolderSizes d@(Directory _ contents) = totalSize d :(concat $ map allFolderSizes contents)
allFolderSizes _ = []

solution :: Tree -> Integer
solution d = minimum $ filter (> required) $ allFolderSizes d
    where
        free = 70000000 - totalSize d
        needed = 30000000
        used = totalSize d
        required = needed - free

main :: IO ()
main = do
    l <- tail <$> lines <$> readFile "input.txt"
    let defaultState = State (Directory "/" []) []
    let state = foldl handleLine defaultState l
    let tree = getTree state
    print $ solution tree