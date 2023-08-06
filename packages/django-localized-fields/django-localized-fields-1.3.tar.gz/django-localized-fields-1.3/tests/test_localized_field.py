from django.conf import settings
from django.db.utils import IntegrityError
from django.test import TestCase
from django.utils import translation

from localized_fields.fields import LocalizedField, LocalizedValue
from localized_fields.forms import LocalizedFieldForm


def get_init_values() -> dict:
    """Gets a test dictionary containing a key
    for every language."""

    keys = {}

    for lang_code, lang_name in settings.LANGUAGES:
        keys[lang_code] = 'value in %s' % lang_name

    return keys


class LocalizedValueTestCase(TestCase):
    """Tests the :see:LocalizedValue class."""

    @staticmethod
    def tearDown():
        """Assures that the current language
        is set back to the default."""

        translation.activate(settings.LANGUAGE_CODE)

    @staticmethod
    def test_init():
        """Tests whether the __init__ function
        of the :see:LocalizedValue class works
        as expected."""

        keys = get_init_values()
        value = LocalizedValue(keys)

        for lang_code, _ in settings.LANGUAGES:
            assert getattr(value, lang_code, None) == keys[lang_code]

    @staticmethod
    def test_init_default_values():
        """Tests wehther the __init__ function
        of the :see:LocalizedValue accepts the
        default value or an empty dict properly."""

        value = LocalizedValue()

        for lang_code, _ in settings.LANGUAGES:
            assert getattr(value, lang_code) is None

    @staticmethod
    def test_get_explicit():
        """Tests whether the the :see:LocalizedValue
        class's :see:get function works properly
        when specifying an explicit value."""

        keys = get_init_values()
        localized_value = LocalizedValue(keys)

        for language, value in keys.items():
            assert localized_value.get(language) == value

    @staticmethod
    def test_get_current_language():
        """Tests whether the :see:LocalizedValue
        class's see:get function properly
        gets the value in the current language."""

        keys = get_init_values()
        localized_value = LocalizedValue(keys)

        for language, value in keys.items():
            translation.activate(language)
            assert localized_value.get() == value

    @staticmethod
    def test_set():
        """Tests whether the :see:LocalizedValue
        class's see:set function works properly."""

        localized_value = LocalizedValue()

        for language, value in get_init_values():
            localized_value.set(language, value)
            assert localized_value.get(language) == value
            assert getattr(localized_value, language) == value

    @staticmethod
    def test_str():
        """Tests whether the :see:LocalizedValue
        class's __str__ works properly."""

        keys = get_init_values()
        localized_value = LocalizedValue(keys)

        for language, value in keys.items():
            translation.activate(language)
            assert str(localized_value) == value

    @staticmethod
    def test_str_fallback():
        """Tests whether the :see:LocalizedValue
        class's __str__'s fallback functionality
        works properly."""

        test_value = 'myvalue'

        localized_value = LocalizedValue({
            settings.LANGUAGE_CODE: test_value
        })

        other_language = settings.LANGUAGES[-1][0]

        # make sure that, by default it returns
        # the value in the default language
        assert str(localized_value) == test_value

        # make sure that it falls back to the
        # primary language when there's no value
        # available in the current language
        translation.activate(other_language)
        assert str(localized_value) == test_value

        # make sure that it's just __str__ falling
        # back and that for the other language
        # there's no actual value
        assert localized_value.get(other_language) != test_value


class LocalizedFieldTestCase(TestCase):
    """Tests the :see:LocalizedField class."""

    @staticmethod
    def test_from_db_value():
        """Tests whether the :see:from_db_value function
        produces the expected :see:LocalizedValue."""

        input_data = get_init_values()
        localized_value = LocalizedField.from_db_value(input_data)

        for lang_code, _ in settings.LANGUAGES:
            assert getattr(localized_value, lang_code) == input_data[lang_code]

    @staticmethod
    def test_from_db_value_none():
        """Tests whether the :see:from_db_valuei function
        correctly handles None values."""

        localized_value = LocalizedField.from_db_value(None)

        for lang_code, _ in settings.LANGUAGES:
            assert localized_value.get(lang_code) is None

    @staticmethod
    def test_to_python():
        """Tests whether the :see:to_python function
        produces the expected :see:LocalizedValue."""

        input_data = get_init_values()
        localized_value = LocalizedField().to_python(input_data)

        for language, value in input_data.items():
            assert localized_value.get(language) == value

    @staticmethod
    def test_to_python_none():
        """Tests whether the :see:to_python function
        produces the expected :see:LocalizedValue
        instance when it is passes None."""

        localized_value = LocalizedField().to_python(None)
        assert localized_value

        for lang_code, _ in settings.LANGUAGES:
            assert localized_value.get(lang_code) is None

    @staticmethod
    def test_to_python_non_dict():
        """Tests whether the :see:to_python function produces
        the expected :see:LocalizedValue when it is
        passed a non-dictionary value."""

        localized_value = LocalizedField().to_python(list())
        assert localized_value

        for lang_code, _ in settings.LANGUAGES:
            assert localized_value.get(lang_code) is None

    @staticmethod
    def test_get_prep_value():
        """"Tests whether the :see:get_prep_value function
        produces the expected dictionary."""

        input_data = get_init_values()
        localized_value = LocalizedValue(input_data)

        output_data = LocalizedField().get_prep_value(localized_value)

        for language, value in input_data.items():
            assert language in output_data
            assert output_data.get(language) == value

    @staticmethod
    def test_get_prep_value_none():
        """Tests whether the :see:get_prep_value function
        produces the expected output when it is passed None."""

        output_data = LocalizedField().get_prep_value(None)
        assert not output_data

    @staticmethod
    def test_get_prep_value_no_localized_value():
        """Tests whether the :see:get_prep_value function
        produces the expected output when it is passed a
        non-LocalizedValue value."""

        output_data = LocalizedField().get_prep_value(['huh'])
        assert not output_data

    def test_get_prep_value_clean(self):
        """Tests whether the :see:get_prep_value produces
        None as the output when it is passed an empty, but
        valid LocalizedValue value but, only when null=True."""

        localized_value = LocalizedValue()

        with self.assertRaises(IntegrityError):
            LocalizedField(null=False).get_prep_value(localized_value)

        assert not LocalizedField(null=True).get_prep_value(localized_value)
        assert not LocalizedField().clean(None)
        assert not LocalizedField().clean(['huh'])

    @staticmethod
    def test_default_value():
        """Tests whether the default value is a :see:LocalizedValue
        instance."""

        field = LocalizedField()

        assert field.default
        assert isinstance(field.default, LocalizedValue)

        for lang_code, _ in settings.LANGUAGES:
            assert not field.default.get(lang_code)

    @staticmethod
    def test_default_value_override():
        """Tests whether the default value of a field
        can correctly be overriden."""

        default_value = LocalizedValue(get_init_values())
        field = LocalizedField(default=default_value)

        assert field.default
        assert isinstance(field.default, LocalizedValue)

        for lang_code, _ in settings.LANGUAGES:
            assert default_value.get(lang_code) == field.default.get(lang_code)

    @staticmethod
    def test_formfield():
        """Tests whether the :see:formfield function
        correctly returns a valid form."""

        assert isinstance(
            LocalizedField().formfield(),
            LocalizedFieldForm
        )
