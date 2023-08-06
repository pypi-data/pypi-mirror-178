# kiwi menu
'kiwi menu' is a python library that you can use to create simple menus in the terminal screen.

## Install
`pip install kiwi_menu`

## Example
```py
from kiwi_menu import Menu

fruits = ["apple", "banana", "kiwi"]
menu = Menu(
    "Choose a fruit",
    fruits
)
selected = menu.show_menu()
print("You choosed", fruits[selected])
```
Result:

```
> apple
  banana
  kiwi

You choosed apple
```

Observation: You optionaly can define the `color`, `symbol`, and the `pre-selected number`. And you can put some 'texts' for center, like a description with the argument `centered_texts`, with the texts inside a list.