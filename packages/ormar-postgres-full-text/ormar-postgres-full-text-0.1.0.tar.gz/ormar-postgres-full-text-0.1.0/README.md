# ormar-postgres-full-text
Extension to use full text search from postgresql in ormar ORM.

## Install

```shell
pip install ormar-postgres-full-text
```

## Usage

For usage example refer to `examples/basic_example/main.py`

## Caveat

TSVector is not a textual data type.
Although you pass a string as the value, postgres would transform it internally and represent it as bag of words, so when retrieving a model containing TSVector, the value will be different than the one you provided initially.
```
>>> await FulltextModel.objects.create(text="hello world")
>>> (await FulltextModel.objects.filter(text__match="hello").first()).text
"'hello' 'world'"
```
