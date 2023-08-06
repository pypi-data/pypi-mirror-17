.. -*- coding: utf-8 -*-

deasciiify
==========

*Translate ASCII text into readable non-ASCII text*

-----

Use ``deasciiify`` to translate ASCII text into readable non-ASCII text. It was
created for the purpose of test data generation to detect unicode bugs and to
use as a fake language on a webpage to simulate how foreign languages can break
webpage layouts and whatnot. The output is deterministic to make automated
testing easier.

Installation
------------

.. code::

    $ pip install deasciiify

Usage
-----

.. code:: python

    >>> from deasciiify import deasciiify
    >>> print(deasciiify('The quick brown fox jumps over the lazy dog.'))
    Ṱḥẹ ʠǚîĉʞ ɓṙōẇṇ ᶂø× ǰúṁᶈș óʋᶒṝ ᵵĥĕ ȴạᵶý ḍọḡ.

    >>> # elongate by 50%
    >>> print(deasciiify('The quick brown fox jumps over the lazy dog.',
    ...                  elongate=0.5))
    𝕋ȟẹ ʠůḭċḱ ᵬṙồẁñ ḟḟᶂᵮợẋᶍ ǰưḿṁᵱṣᵴṣ ǫṽếṛᵳ ṭħȇ ɫäǎąẩžɀẓẑẕᶎᶎẓẓỹÿŷӮ ḋöᵷ.

    >>> # elongate by 100 characters
    >>> print(deasciiify('The quick brown fox jumps over the lazy dog.',
    ...                  elongate=100))
    Ʈɦẻ ʠűȋḉƙḱᶄḵḳķʞǩƙḱᶄḵḳ ƀᶉŏẁἦ ƒḟḟᶂḟƒởᶍ×ẍẋᶍ ĵứȗửǔǚṷȕǜûủũṳṹữụṻưṃɱḿṁḿɱḿṁᶈşᵴșŝș
    ȫṽḙɽᵳɾŕŕŗȓṙɼᵳȑᵳɽȓȑᶉᵳᶉ ƭẖė ℓἂậẳẩầạẳἇầǡᶏạᶏƶžźƶȥᶎẑᵶżȥᶎẑᶎγƴẏӲӰýỳŷẏγẏỳ ᶑốǥ.

    >>> # preserve HTML, entities, and gettext params
    >>> print(deasciiify(
    ...     'The <em>quick</em> <strong style="color:brown;">brown</strong> '
    ...     'fox %(verb)s over the &ldquo;lazy&rdquo; %s.'))
    Ṯȟè <em>ʠúᶖćḵ</em> <strong style="color:brown;">ḃᵲóẅἢ</strong> ḟọẍ %(verb)s
    ȏʋềŕ ṱȟḝ &ldquo;ḽӓżӮ&rdquo; %s.
