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
          [ a [ class "button is-outlined is-medium is-primary", onClick Decrement ] [ text "-" ]
          , a [ class "button is-outlined is-medium is-primary margin-left-10", onClick Increment ] [ text "+" ]
          ]
        ]
      , div [class "column"]
        [ div [class "text-big"] [ text (toString model) ] ]
    ]
