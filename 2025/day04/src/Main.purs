module Main where

import Prelude

import Data.Array (catMaybes, concat, filter, fromFoldable, length, (!!))
import Data.Array.Partial (head)
import Data.Foldable (sum)
import Data.Generic.Rep (class Generic)
import Data.Maybe (Maybe(..))
import Data.Show.Generic (genericShow)
import Data.String (CodePoint, Pattern(..), codePointFromChar, split, toCodePointArray)
import Data.Traversable (for)
import Data.TraversableWithIndex (forWithIndex)
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

codePointToCell :: CodePoint -> Cell
codePointToCell cp = if cp == codePointFromChar '.' then Empty else Roll



createCells  :: String ->Array (Array Cell)
createCells xs = let rows = ( filter (_ /= "") $ fromFoldable $ split (Pattern "\n") xs )
                  in 
                    map (\row -> map codePointToCell (fromFoldable $ toCodePointArray row) ) rows


partialMain :: Partial => Effect Unit
partialMain = do
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


main :: Effect Unit
main = unsafePartial partialMain
