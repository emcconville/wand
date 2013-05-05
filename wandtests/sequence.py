from attest import assert_hook

from attest import Tests, raises

from wand.image import ClosedImageError, Image
from .image import asset


tests = Tests()


@tests.test
def length():
    with Image(filename=asset('apple.ico')) as img:
        assert len(img.sequence) == 4


@tests.test
def getitem():
    with Image(filename=asset('apple.ico')) as img:
        size = img.size
        assert size == img.sequence[img.sequence.current_index].size
        assert img.sequence[0].size == (32, 32)
        assert img.sequence[1].size == (16, 16)
        assert img.sequence[2].size == (32, 32)
        assert img.sequence[3].size == (16, 16)
        with raises(IndexError):
            img.sequence[4]
        assert img.sequence[-1].size == (16, 16)
        assert img.sequence[-2].size == (32, 32)
        assert img.sequence[-3].size == (16, 16)
        assert img.sequence[-4].size == (32, 32)
        with raises(IndexError):
            img.sequence[-5]
        assert img.size == size


@tests.test
def setitem():
    with Image(filename=asset('apple.ico')) as imga:
        with Image(filename=asset('google.ico')) as imgg:
            imga.sequence[2] = imgg
        assert len(imga.sequence) == 4
        assert imga.sequence[2].size == (16, 16)


@tests.test
def delitem():
    with Image(filename=asset('apple.ico')) as img:
        detached = img.sequence[0]
        del img.sequence[0]
        assert len(img.sequence) == 3
        assert img.sequence[0] is not detached
        assert img.sequence[0].size == (16, 16)


@tests.test
def iterator():
    with Image(filename=asset('apple.ico')) as img:
        container_size = img.sequence[img.sequence.current_index].size
        actual = []
        expected = [(32, 32), (16, 16), (32, 32), (16, 16)]
        for i in img.sequence:
            actual.append(i.size)
            assert img.size == container_size
        assert actual == expected


@tests.test
def append():
    with Image(filename=asset('apple.ico')) as imga:
        with Image(filename=asset('google.ico')) as imgg:
            imga.sequence.append(imgg)
            assert imga.sequence[4] == imgg.sequence[0]
        assert len(imga.sequence) == 5
    with Image(filename=asset('apple.ico')) as imga:
        with Image(filename=asset('github.ico')) as imgg:
            imga.sequence.append(imgg)
            assert imga.sequence[4] == imgg.sequence[0]
        assert len(imga.sequence) == 5


@tests.test
def insert():
    with Image(filename=asset('apple.ico')) as imga:
        instances = [imga.sequence[i] for i in xrange(2, 4)]
        with Image(filename=asset('google.ico')) as imgg:
            imga.sequence.insert(2, imgg)
            assert imga.sequence[2] == imgg.sequence[0]
        assert len(imga.sequence) == 5
        for i, instance in enumerate(instances):
            assert instance == imga.sequence[3 + i]


@tests.test
def insert_first():
    with Image(filename=asset('apple.ico')) as imga:
        with Image(filename=asset('google.ico')) as imgg:
            imga.sequence.insert(0, imgg)
            assert len(imga.sequence) == 5
            assert imga.sequence[0] == imgg.sequence[0], \
                   ('imga.sequence = ' + repr(list(imga.sequence)) +
                    ', imgg.sequence = ' + repr(list(imgg.sequence)))
        assert len(imga.sequence) == 5


@tests.test
def extend():
    with Image(filename=asset('apple.ico')) as a:
        with Image(filename=asset('apple.ico')) as b:
            a.sequence.extend(list(b.sequence))
            for i in xrange(4):
                assert a.sequence[4 + i] == b.sequence[i]
        assert len(a.sequence) == 8


@tests.test
def extend_sequence():
    with Image(filename=asset('apple.ico')) as a:
        with Image(filename=asset('apple.ico')) as b:
            a.sequence.extend(b.sequence)
            for i in xrange(4):
                assert a.sequence[4 + i] == b.sequence[i]
        assert len(a.sequence) == 8


cmp_funcs = {
    'equals': lambda i: i,  # identity
    'hash_equals': hash,
    'signature_equals': lambda i: i.signature
}

for cmp_name in cmp_funcs:
    def _equals_test(f=cmp_funcs[cmp_name]):
        with Image(filename=asset('apple.ico')) as a:
            with Image(filename=asset('apple.ico')) as b:
                    assert f(a) == f(b)
                    assert f(a.sequence[0]) == f(b.sequence[0])
                    assert f(a) != f(b.sequence[1])
                    assert f(a.sequence[0]) != f(b.sequence[1])
                    assert f(a.sequence[1]) == f(b.sequence[1])
    _equals_test.__name__ = cmp_name
    globals()[cmp_name] = tests.test(_equals_test)


@tests.test
def clone():
    with Image(filename=asset('apple.ico')) as img:
        with img.sequence[2].clone() as single:
            assert single.wand != img.wand
            assert len(single.sequence) == 1
            assert len(list(single.sequence)) == 1
            assert single.size == img.sequence[2].size
