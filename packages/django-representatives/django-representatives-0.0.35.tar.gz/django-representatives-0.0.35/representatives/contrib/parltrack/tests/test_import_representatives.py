import pytest
import os
import copy

from django.core.serializers.json import Deserializer
from representatives.models import Representative
from representatives.contrib.parltrack import import_representatives


@pytest.mark.django_db
def test_parltrack_import_representatives():
    fixture = os.path.join(os.path.dirname(__file__),
            'representatives_fixture.json')
    expected = os.path.join(os.path.dirname(__file__),
            'representatives_expected.json')

    # Disable django auto fields
    exclude = ('id', '_state', 'created', 'updated', 'fingerprint')

    with open(fixture, 'r') as f:
        import_representatives.main(f)

    missing = []
    with open(expected, 'r') as f:
        for obj in Deserializer(f.read()):
            compare = copy.copy(obj.object.__dict__)

            for field in exclude:
                if field in compare:
                    compare.pop(field)

            try:
                type(obj.object).objects.get(**compare)
            except:
                missing.append(compare)

    assert len(missing) is 0
    assert Representative.objects.count() == 2
