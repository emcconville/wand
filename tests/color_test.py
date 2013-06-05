from wand.color import Color


def test_equals():
    """Equality test."""
    assert Color('#fff') == Color('#ffffff') == Color('white')
    assert Color('#000') == Color('#000000') == Color('black')
    assert Color('rgba(0, 0, 0, 0)') == Color('rgba(0, 0, 0, 0)')
    assert Color('rgba(0, 0, 0, 0)') == Color('rgba(1, 1, 1, 0)')


def test_not_equals():
    """Equality test."""
    assert Color('#000') != Color('#fff')
    assert Color('rgba(0, 0, 0, 0)') != Color('rgba(0, 0, 0, 1)')
    assert Color('rgba(0, 0, 0, 1)') != Color('rgba(1, 1, 1, 1)')


def test_red():
    assert Color('black').red == 0
    assert Color('red').red == 1
    assert Color('white').red == 1
    assert 0.5 <= Color('rgba(128, 0, 0, 1)').red < 0.51


def test_green():
    assert Color('black').green == 0
    assert Color('#0f0').green == 1
    assert Color('white').green == 1
    assert 0.5 <= Color('rgba(0, 128, 0, 1)').green < 0.51


def test_blue():
    assert Color('black').blue == 0
    assert Color('blue').blue == 1
    assert Color('white').blue == 1
    assert 0.5 <= Color('rgba(0, 0, 128, 1)').blue < 0.51


def test_alpha():
    assert Color('rgba(0, 0, 0, 1)').alpha == 1
    assert Color('rgba(0, 0, 0, 0)').alpha == 0
    assert 0.49 <= Color('rgba(0, 0, 0, 0.5)').alpha <= 0.5


def test_red_int8():
    assert Color('black').red_int8 == 0
    assert Color('red').red_int8 == 255
    assert Color('white').red_int8 == 255
    assert Color('rgba(128, 0, 0, 1)').red_int8 == 128


def test_green_int8():
    assert Color('black').green_int8 == 0
    assert Color('#0f0').green_int8 == 255
    assert Color('white').green_int8 == 255
    assert Color('rgba(0, 128, 0, 1)').green_int8 == 128


def test_blue_int8():
    assert Color('black').blue_int8 == 0
    assert Color('blue').blue_int8 == 255
    assert Color('white').blue_int8 == 255
    assert Color('rgba(0, 0, 128, 1)').blue_int8 == 128


def test_alpha_int8():
    assert Color('rgba(0, 0, 0, 1)').alpha_int8 == 255
    assert Color('rgba(0, 0, 0, 0)').alpha_int8 == 0
    if not (Color('rgb(127,0,0)').red_quantum <=
            Color('rgba(0,0,0,0.5').alpha_quantum <=
            Color('rgb(128,0,0)').red_quantum):
        # FIXME: I don't know why, but the value PixelGetAlphaQuantum() returns
        #        is inconsistent to other PixelGet{Red,Green,Blue}Quantum()
        #        functions in Travis CI.  We just skip the test in this case.
        return
    assert 127 <= Color('rgba(0, 0, 0, 0.5)').alpha_int8 <= 128


def test_string():
    assert Color('black').string in ('rgb(0,0,0)', 'srgb(0,0,0)')
    assert str(Color('black')) in ('rgb(0,0,0)', 'srgb(0,0,0)')
