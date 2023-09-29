# How to: Navigate through the document using XPath

## Introduction
XPath is the query language to navigate through *any* XML document (not just TEI) -- it allows you to find *exactly* what you are looking for. More powerfully, it also allows you to find the *type* of things you are looking for, creating a list that you can work through. So, for example, while using a normal search function to find all notes would work, using XPath you can also specify that you only need the notes in chapter 4, or only the notes of a specific subtype, or only the notes that do not contain a specific attribute, etc.

## How to use XPath in Oxygen
Oxygen makes searching with XPath very easy: there is a text field on the top left of the screen with a label saying `XPath 2.0`. Simply put your expression on that input box and press enter to search using XPath. The search results will appear at the bottom of the screen. You can click on each result to be taken to its place in the TEI document.

## XPath syntax
XPath has, like the name implies, a *path-like* syntax: so everything is inside something else, and that is indicated by the presence of a forward slash `/`.

### Basic path search
So if you where to search for `/` you would get the entire document back. This allows for very specific searches, so if you were to search for:

```
/TEI/text/front/pb
```

you would get a list of all `pb` elements that are inside the `front` element, which is inside the `text` element, which is inside the root `TEI` element.

### Advanced path search
Finding an element where you already know exactly its location is, however, not very useful in the majority of cases. Normally, you are more likely to require a list of all elements of a specific type. To do this, you use a double-forward slash `//` which means that the element can be anywhere from the point where the forward slash is. So searching something like:

```
//pb
```

would give you a list of all the `pb` elements anywhere in the document.

You can get a bit more restrictive by using a combination of specific and general paths. Let's say you want to find all `pb` elements inside the body of the text. If you use something like:

```
/TEI/text/body/pb
```

will actually only return six results: that's because you are ignoring all the `pb` elements that show up inside the chapter `div`. So you need to add something like:

```
/TEI/text/body//pb
```

This means that it will find any `pb` elements at whatever level (i.e., inside however many `div` or other elements), as long as they are inside the `body`, meaning it will ignore whatever `pb` elements exist in the `front` or `back` of the text.

### Searching elements with attributes
XPath really comes into its own once you start needing to find elements with specific attributes, or even with specific attribute values. The syntax to search for attributes is as follows:

```
elementName[@attributeName="attributeValue"]
```

Remember, however, that the rules for the path still apply, so if you search for:

```
note[@type="authorial"]
```

you will get no results: there are no `note` elements at the root of the file. To correct this search, you need to use the general path, so:

```
//note[@type="authorial"]
```

which will return all notes anywhere on the document. You can, of course, be more specific than this. Let's say you want all authorial gloss notes in chapter 1. You'd use

```
//div[@n=1]//note[@type="authorial" and @subtype="gloss"]
```

This would give you a list of all notes that have a `@type` of "authorial" and a `@subtype` of "gloss" that appear anywhere inside a `@div` that contains an `@n` attribute of "1" (i.e., chapter one), which itself can appear anywhere on the document. (Technically it can only appear in one place, but writing it like this is easier than having the entire path, which would be something like: `/TEI/text/body/div[@n="1"]` which would also ignore any notes that appear inside paragraphs or other elements.)

## More on XPath
There is a lot more to using XPath than this (it is its own language), however this should give you a good footing to start some of the most useful and common searches. If you want a more detailed guide, or how to search for something really specific, [have a look at this cheatsheet.](https://devhints.io/xpath) (this is geared towards HTML, but you can replace the element names with TEI ones).