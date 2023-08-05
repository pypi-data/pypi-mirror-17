Parler Tools
extracts applicable methods from aldryn-translation-tools to be used without django-cms


models.TranslatedAutoSlugMixin
------------------------------

This is a TranslatableModel mixin that automatically generates a suitable
slug for the object on ``save()``.

If ``slug_globally_unique`` is ``True``, then slugs will be required to be
unique across all languages.

If ``slug_globally_unique`` is ``False`` (default), then the strategy used here
is that it is OK for two objects to use the same slug if the slugs are for
different languages. So if this were used on a translated Article model, these
URLs would be valid:

``/en/pain`` - An article in EN about physical discomfort

``/fr/pain`` - An article in FR about bread

Of course, this means that when resolving an object from its URL, care must
be taken to factor in the language segment of the URL too.

When using this mixin, it is important to also set the
``slug_source_field_name`` property on the implementing model to the name of
the translated field which the slug is to be derived from. If you require more
slugs to be derived from multiple fields (translated or otherwise), simply
override the method ``get_slug_source`` to provide the source string for the
slug.

Configuration properties
************************

slug_default
~~~~~~~~~~~~
Provide a lazy translated string to use for the default slug should an object
not have a source string to derive a slug from.

slug_field_name
~~~~~~~~~~~~~~~
Provide the name of the translated field in which generated slug shall
be stored.

slug_globally_unique
~~~~~~~~~~~~~~~~~~~~
A boolean flag controlling whether slugs are globally unique, or only unique
with each language. Default value is False.

slug_max_length
~~~~~~~~~~~~~~~
Declares the max_length of slugs. This defaults to the ``max_length`` of the
slug_field and is determined via introspection.

slug_separator
~~~~~~~~~~~~~~
This determines the separator used before any index added to the slug. It does
**not** determine the separator used in the slug itself, which is always ``-``.
This is only provided for compatibility with the slugify()`` method in
aldryn_common, but it is not recommended to be used. Defaults to ``-``.

slug_source_field_name
~~~~~~~~~~~~~~~~~~~~~~
Provide the name of the translated field to be used for deriving the slug.
If more than one field, or other complex sources are required, override the
method ``get_slug_source()`` instead. Note that if ``get_slug_source()`` is
overriden, it is recommended to also override ``get_slug_default()``.


Public methods
**************

get_slug_default
~~~~~~~~~~~~~~~~

Naively constructs a translated default slug from the object. For better
results, just set the `slug_default` property on the class to a lazy
translated string. Alternatively, override this method if you need to more
programmtically determine the default slug.

Example: If your model is "news article" and your source field is "title" this
will return "news-article-without-title".


get_slug_max_length
~~~~~~~~~~~~~~~~~~~
Accepts an optional parameter ``idx_len``.

Introspects the slug field to determine the maximum length, taking into account
a possible separator and up to a [idx_len]-digit number.


get_slug_source
~~~~~~~~~~~~~~~
Simply returns the value of the slug source field. Override for more complex
situations such as using multiple fields (translated or not) as the source.

