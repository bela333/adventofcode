module Main where

import Prelude

import Data.Array (catMaybes, concat, filter, fromFoldable, length, mapWithIndex, zip, (!!))
import Data.Array.Partial (head)
import Data.Enum (fromEnum)
import Data.Eq.Generic (genericEq)
import Data.Foldable (sum)
import Data.Generic.Rep (class Generic)
import Data.Maybe (Maybe(..))
import Data.Show.Generic (genericShow)
import Data.String (CodePoint, Pattern(..), codePointFromChar, split, toCodePointArray)
import Data.Traversable (for)
import Data.TraversableWithIndex (forWithIndex)
import Data.Tuple (uncurry)
import Effect (Effect)
import Effect.Console (log)
import Node.Encoding (Encoding(..))
import Node.FS.Sync (readTextFile)
import Partial.Unsafe (unsafePartial)

data Cell = Empty | Roll 

isEmpty :: Cell -> Boolean
isEmpty Empty = true
isEmpty _ = false

isRoll :: Cell -> Boolean
isRoll Roll = true
isRoll _ = false

derive instance genericCell :: Generic Cell _

instance showCell :: Show Cell where
  show = genericShow


instance eqCell :: Eq Cell where
  eq = genericEq

codePointToCell :: CodePoint -> Cell
codePointToCell cp = if cp == codePointFromChar '.' then Empty else Roll



createCells  :: String ->Array (Array Cell)
createCells xs = let rows = ( filter (_ /= "") $ fromFoldable $ split (Pattern "\n") xs )
                  in 
                    map (\row -> map codePointToCell (fromFoldable $ toCodePointArray row) ) rows


part01 :: Partial => Effect Unit
part01 = do
  content <- readTextFile UTF8 "input.txt"
  let cells = createCells content
  let width = length cells
  let height = length $ head cells
  log $ show $ {width: width, height: height}
  v :: Array (Array (Maybe Int)) <- forWithIndex cells $ \i row -> do
     forWithIndex row $ \j cell -> do
        case cell of
          Roll → pure $ Just $ length $ filter isRoll $ catMaybes $ [
              ( _ !! ( j-1 ) ) =<< cells !! ( i-1 ),
              ( _ !! ( j-1 ) ) =<< cells !! ( i+1 ),
              ( _ !! ( j+1 ) ) =<< cells !! ( i-1 ),
              ( _ !! ( j+1 ) ) =<< cells !! ( i+1 ),
              ( _ !! ( j-1 ) ) =<< cells !! ( i ),
              ( _ !! ( j+1 ) ) =<< cells !! ( i ),
              ( _ !! ( j ) ) =<< cells !! ( i-1 ),
              ( _ !! ( j ) ) =<< cells !! ( i+1 )
          ]
          Empty → pure Nothing
  let v' = concat $ map catMaybes v
  log $ show $ length $ filter (_<4) v'
  pure unit



limit :: forall a. Eq a => (a -> a) -> a -> a
limit step prev = let next = step prev in 
  if next == prev then prev else limit step next


clean :: Array (Array Cell) -> Array (Array Cell) 
clean cells = let v = ( ( flip mapWithIndex ) cells $ \i row -> 
              ( flip mapWithIndex ) row $ \j cell -> 
                  case cell of
                    Roll → Just $ length $ filter isRoll $ catMaybes $ [
                        ( _ !! ( j-1 ) ) =<< cells !! ( i-1 ),
                        ( _ !! ( j-1 ) ) =<< cells !! ( i+1 ),
                        ( _ !! ( j+1 ) ) =<< cells !! ( i-1 ),
                        ( _ !! ( j+1 ) ) =<< cells !! ( i+1 ),
                        ( _ !! ( j-1 ) ) =<< cells !! ( i ),
                        ( _ !! ( j+1 ) ) =<< cells !! ( i ),
                        ( _ !! ( j ) ) =<< cells !! ( i-1 ),
                        ( _ !! ( j ) ) =<< cells !! ( i+1 )
                      ]
                    Empty → Nothing
                  )
   in
      map (map $ case _ of
            Nothing -> Empty
            Just b -> if b < 4 then Empty else Roll
            ) v



part02 :: Partial => Effect Unit
part02 = do
  content <- readTextFile UTF8 "input.txt"
  let cells = createCells content
  let width = length cells
  let height = length $ head cells
  log $ show $ {width: width, height: height}
  let cells' = limit clean cells
  let row = sum $ map (uncurry (/=) >>> fromEnum) $ concat $ map (uncurry zip) ( zip cells cells')
  log $ show $ row
  pure unit


main :: Effect Unit
main = do
  unsafePartial part01
  unsafePartial part02
