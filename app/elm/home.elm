module Counter exposing (..)

import Html exposing (Html, a, div, text)
import Html.Events exposing (onClick)
import Html.Attributes exposing (class)

main =
  Html.beginnerProgram { model = 0, view = view, update = update }

type Msg = Increment | Decrement

update msg model =
  case msg of
    Increment ->
      model + 1

    Decrement ->
      model - 1

view model =
  div [class "columns"]
    [ div [class "column"]
        [ div [class "block"]
          [ a [ class "button", onClick Decrement ] [ text "-" ]
          , a [ class "button", onClick Increment ] [ text "+" ]
          ]
        ]
      , div [class "column"]
        [ div [] [ text (toString model) ] ]
    ]
