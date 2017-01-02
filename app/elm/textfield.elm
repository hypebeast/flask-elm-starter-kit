module Textfield exposing (..)

import Html exposing (Html, Attribute, div, input, text)
import Html.Attributes exposing (..)
import Html.Events exposing (onInput)
import String


main =
  Html.beginnerProgram { model = model, view = view, update = update }


-- MODEL

type alias Model =
  { content : String
  }

model : Model
model =
  { content = "" }


-- UPDATE

type Msg
  = Change String

update : Msg -> Model -> Model
update msg model =
  case msg of
    Change newContent ->
      { model | content = newContent }


-- VIEW

view model =
  div [class "columns"]
    [ div [class "column"]
        [ div [class "block"]
          [ input [ class "input is-success", placeholder "Text to reverse", onInput Change] [] ]
        ]
      , div [class "column"]
        [ div [class "text-big"] [ text (String.reverse model.content) ] ]
    ]
